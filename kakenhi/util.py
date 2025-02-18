import requests
import urllib.parse
import json

def query_json(appid, name):
    url = f"https://nrid.nii.ac.jp/opensearch/?appid={appid}&qg={urllib.parse.quote(name)}&format=json"
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    try:
        return response.json()
    except Exception as e:
        print(f'Error: {e}')
        return None


def save_json(filename, json_data):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)


def extract_pi_projects(json_data, name=None):
    entry = {'氏名': name, '所属': None, '部署': None, '職位': None, '研究者番号': None, '科研費URL': None, '科研代表': None}

    if json_data is None:
        entry['所属'] = 'Error: empty json'
        return entry

    if 'researchers' not in json_data or len(json_data['researchers']) == 0:
        entry['所属'] = 'Error: no "researchers"'
        return entry
    
    if 'affiliations:current' not in json_data['researchers'][0] or len(json_data['researchers'][0]['affiliations:current']) == 0:
        entry['所属'] = 'Error: no "affiliations"'
        return entry

    if name is None and len(json_data['researchers']) > 0 and len(json_data['researchers'][0]['name']['humanReadableValue']) > 0:
        entry['氏名'] = json_data['researchers'][0]['name']['humanReadableValue'][0]['text']

    current_affilication = json_data['researchers'][0]['affiliations:current'][0]

    if len(current_affilication['affiliation:institution']['humanReadableValue']) > 0:
        entry['所属'] = current_affilication['affiliation:institution']['humanReadableValue'][0]['text']
    if len(current_affilication['affiliation:department']['humanReadableValue']) > 0:
        entry['部署'] = current_affilication['affiliation:department']['humanReadableValue'][0]['text']
    if len(current_affilication['affiliation:jobTitle']['humanReadableValue']) > 0:
        entry['職位'] = current_affilication['affiliation:jobTitle']['humanReadableValue'][0]['text']

    if len(json_data['researchers'][0]['id:person:erad']) > 0:
        entry['研究者番号'] = json_data['researchers'][0]['id:person:erad'][0]
        entry['科研費URL'] = f"https://nrid.nii.ac.jp/ja/nrid/10000{entry['研究者番号']}/"

    project_dict = {}

    for project in json_data['researchers'][0]['work:project']:
        if project['role'][0]['code:roleInProject:kakenhi'] == 'principal_investigator':
            project_category = project['category'][0]['humanReadableValue'][0]['text']
            if project_category == '特別研究員奨励費':
                continue
            project_category = project_category.replace('研究', '')
            project_since = project['since']['fiscal:year']['commonEra:year']
            project_until = project['until']['fiscal:year']['commonEra:year']

            if project_category in project_dict:
                project_dict[project_category].append(f"{project_since}-{project_until}")
            else:
                project_dict[project_category] = [f"{project_since}-{project_until}"]

    if len(project_dict) > 0:
        project_list = []

        for key in project_dict.keys():
            project_str = f"{key}[{', '.join(sorted(project_dict[key]))}]"
            project_list.append(project_str)

        entry['科研代表'] = ', '.join(project_list)

    return entry
