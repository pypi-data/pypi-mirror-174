from re import findall
from json import dumps as json_dumps
from gitlab_ps_utils.api import GitLabApi
from gitlab_ps_utils.misc_utils import safe_json_response, is_error_message_present
from gitlab_ps_utils.dict_utils import dig
from gitlab_evaluate.lib import human_bytes as hb
from gitlab_evaluate.lib import utils

gl_api = GitLabApi()

# Project only keyset-based pagination - https://docs.gitlab.com/ee/api/#keyset-based-pagination

def get_last_id(link):
    # Get id_after value. If the Link key is missing it's done, with an empty list response
    return findall(r"id_after=(.+?)&", link)[0] if link else None

'''
Generates the URL to get the full project info with statistics
'''
def proj_info_get(i, source):
    '''Trying to create proper api call with project id.'''
    return f"{source}/api/v4/projects/{str(i)}?statistics=true"

def proj_packages_url(i):
    return f"projects/{str(i)}/packages"

def proj_registries_url(i):
    return f"projects/{str(i)}/registry/repositories"

def proj_registries_tags_url(pid, rid):
    return f"projects/{str(pid)}/registry/repositories/{str(rid)}/tags"

def proj_registries_tag_details_url(pid, rid, tid):
    return f"projects/{str(pid)}/registry/repositories/{str(rid)}/tags/{tid}"

def get_registry_details(i):
    return f"registry/repositories/{str(i)}?size=true"

# def proj_commits_get(i, source):
#     '''Trying to create proper api call with project id to get the number of commits.'''
#     i = str(i)
#     commits_url = "/api/v4/projects/{i}/repository?statistics=yes"
#     gl_commits_pl = source + commits_url
#     return gl_commits_pl       
### Functions - Return API Data
# Gets the X-Total from the statistics page with the -I on a curl
def check_x_total_value_update_dict(check_func, p, host, token, api, headers={}, value_column_name="DEFAULT_VALUE", over_column_name="DEFAULT_COLUMN_NAME", results={}):
    flag = False
    count = get_total_count(host, token, api, p['path_with_namespace'], value_column_name)
    if count:
        num_over = check_func(count)
        if num_over:
            flag = True
        results[value_column_name] = count
        results[over_column_name] = num_over
    else:
        print(f"Could not retrieve {value_column_name} for project: {p.get('id')} - {p.get('path_with_namespace')}")
    return flag

def get_total_count(host, token, api, full_path, entity):
    if count := gl_api.get_count(host, token, api):
        return count
    else:
        formatted_entity = utils.to_camel_case(entity)
        query = {
            "query": """
                query {
                    project(fullPath: "%s") {
                        name,
                        %s {
                            count
                        }
                    }
                }
            """ % (full_path, formatted_entity)
        }

        if gql_resp := safe_json_response(gl_api.generate_post_request(host, token, None, json_dumps(query), graphql_query=True)):
            return dig(gql_resp, 'data', 'project', formatted_entity, 'count')


# gets the full stats of the project and sorts based on the returned items, passing a few through the HumanReadable utility
def check_full_stats(url, project, my_dict, headers={}):
    if result := safe_json_response(gl_api.generate_get_request(host="", api="", token=headers.get("PRIVATE-TOKEN"), url=url)): 
        if kind := result.get("namespace"):
            my_dict.update({"kind": kind.get("kind")})
        if stats := result.get("statistics"):
            # storage_size = result.get('storage_size')
            # commit_count = stats.get('commit_count')
            # repository_size = stats.get('repository_size')
            # wiki_size = stats.get['wiki_size']
            # lfs_objects_size = stats.get['lfs_objects_size']
            # job_artifacts_size = stats.get['job_artifacts_size']
            # snippets_size = stats.get['snippets_size']
            # packages_size = stats.get['packages_size']
            export_total = 0
            for k, v in stats.items():
                updated_dict_entry = { k: hb.HumanBytes.format(v, True) if k != "commit_count" else v, k + "_over": utils.check_size(k, v)}
                my_dict.update(updated_dict_entry)

                # If k an item that would be part of the export, add to running total
                if k in [
                    "repository_size",
                    "wiki_size",
                    "lfs_objects_size",
                    "snippets_size",
                    "uploads_size"
                ]:
                    export_total += int(v)

                # my_dict[k] = {
                #     "value": hb.HumanBytes.format(v, True) if k != 'commit_count' else v,
                #     "over": utils.check_size(k, v)
                # }
            
            # Write running total to my_dict
            my_dict.update({"Estimated Export Size": hb.HumanBytes.format(export_total, True)})
            export_total = 0
            # reset running total? Not loop, so maybe not
        else:
            print(f"Could not extracts stats for project {project.get('path_with_namepsace')}.\n")
    else:
        print(f"Could not retrieve project with stats for project id: {project.get('id')}")

def get_registry_size(pid, path_with_namespace, source, token):
    """
        Iterates over a project's registry data and returns the total size of registry data
    """
    if total_size := get_registry_size_by_graphql(path_with_namespace, source, token):
        print('Retrieved registry size by single GraphQL query')
    else:
        print('Failed to receive registry size by GraphQL queries. Falling back to REST calls')
        registry_hashes = {}
        for registry_repo in gl_api.list_all(source, token, proj_registries_url(pid)):
            error, _ = is_error_message_present(registry_repo)
            if error:
                print(f'Container registry from {path_with_namespace} inaccessible or disabled. Skipping')
                continue
            rid = registry_repo['id']
            for registry_tags in gl_api.list_all(source, token, proj_registries_tags_url(pid, rid)):
                tid = registry_tags['name']
                repo_details = safe_json_response(gl_api.generate_get_request(source, token, proj_registries_tag_details_url(pid, rid, tid)))
                if repo_size := repo_details.get('total_size'):
                    registry_hashes['short_revision'] = repo_size

        total_size = sum(registry_hashes.values())

    return utils.sizeof_fmt(total_size), utils.check_storage_size(total_size)

def get_registry_size_by_graphql(path_with_namespace, source, token):
    """
        Makes a single GraphQL query to get the total registry size
        of a project. This query could return an error stating
        the query result is too large
    """
    query = {
        'query': """
            query {
                project(fullPath: "%s") {
                    statistics {
                        containerRegistrySize
                        }
                    }
                }
                
        """ % path_with_namespace
    }
    if gql_resp := safe_json_response(gl_api.generate_post_request(source, token, None, data=json_dumps(query), graphql_query=True)):
        return dig(gql_resp, 'data', 'project', 'statistics', 'containerRegistrySize')

def getApplicationInfo(host,token,api):
    if resp := gl_api.generate_get_request(host=host, token=token, api=api):
        result = resp.json()
        ## error handling - look for 200 
        return result

def getVersion(host,token,api):
    if resp := gl_api.generate_get_request(host=host,token=token,api=api):
        result = resp.json()
        ## error handling - look for 200 
        return result

def getArchivedProjectCount(host,token):
    if resp := gl_api.generate_get_request(host=host,token=token,api='projects?archived=True'):
        result = resp.headers.get('X-Total')
        return result