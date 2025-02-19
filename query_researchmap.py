import os
import util.io
import argparse
import researchmap.util
from researchmap.personal_data import ResearchmapPersonalData
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    config = util.io.load_yaml_config('config.yaml')
    if config is None:
        exit()

    parser = argparse.ArgumentParser(description='漢字氏名からresearchmapのURLを検索し、Excelファイルに出力')
    parser.add_argument('-i', '--input_list', required=True, help='漢字氏名が1行ずつ記載された入力テキストファイル(UTF-8)')
    parser.add_argument('-o', '--output_excel', default='', help='出力するExcelファイル名')
    args = parser.parse_args()

    if args.output_excel == '':
        args.output_excel = config['researchmap']['default_output']
        print(f'Note: args.output_excel set as: {args.output_excel}')

    options = Options()
    options.add_argument('--disable-usb-discovery')
    if config['researchmap']['user_agent'] != '':
        options.add_argument(f"--user-agent={config['researchmap']['user_agent']}")
    if config['researchmap']['headless']:
        options.add_argument("--headless")
   
    chrome_driver = webdriver.Chrome(options=options)

    names = util.io.read_names_from_file(args.input_list)
    n_names = len(names)
    print('{} names loaded'.format(n_names))

    base_dirname = os.path.basename(args.input_list).split('.')[0]
    if not os.path.exists(base_dirname):
        os.makedirs(base_dirname, exist_ok=True)
        print(f'Note: directory "{base_dirname}" created')

    data = []
    for idx, name in enumerate(names, 1):
        print('[{}/{}] querying {}'.format(idx, n_names, name))

        url = researchmap.util.find_researchmap_url_ddgs(chrome_driver, name)

        entry = {'氏名': name,
                 '所属': None,
                 '職位': None,
                 '研究分野': None,
                 'キーワード': None,
                 '国際雑誌': 0,
                 '主著国際雑誌': 0,
                 '和文雑誌': 0,
                 '主著和文雑誌': 0,
                 '国際会議': 0,
                 '主著国際会議': 0,
                 '受賞': 0,
                 '主著受賞': 0,
                 'ResearchmapURL': url
                 }

        if url is None or type(url) is not str:
            print('  URL not found')
            data.append(entry)
            continue

        if not url.startswith('https://researchmap.jp/'):
            print('  Wrong URL: {}'.format(url))
            data.append(entry)
            continue

        query_url = url.replace('researchmap', 'api.researchmap') if url else None

        if url and len(url) > len('https://researchmap.jp/'):
            researchmap_data = ResearchmapPersonalData()

            json_data = researchmap.util.get_researchmap_json(query_url)
            researchmap_data.parse_json(json_data)

            json_data = researchmap.util.get_researchmap_json(query_url+'/published_papers?start=1&limit=10000')
            researchmap_data.parse_published_papers(json_data)

            researchmap_data.summarize_achievement_stats()
            # print('  {}'.format(researchmap_data.achievement_stats))

            entry['所属'] = ';'.join([d['所属'] for d in researchmap_data.affiliations])
            entry['職位'] = ';'.join([d['職位'] for d in researchmap_data.affiliations])
            entry['研究分野'] = researchmap_data.research_field
            entry['キーワード'] = researchmap_data.research_keyword
            entry['国際雑誌'] = researchmap_data.achievement_stats['国際雑誌']
            entry['主著国際雑誌'] = researchmap_data.achievement_stats['主著国際雑誌']
            entry['和文雑誌'] = researchmap_data.achievement_stats['和文雑誌']
            entry['主著和文雑誌'] = researchmap_data.achievement_stats['主著和文雑誌']
            entry['国際会議'] = researchmap_data.achievement_stats['国際会議']
            entry['主著国際会議'] = researchmap_data.achievement_stats['主著国際会議']
            entry['受賞'] = researchmap_data.achievement_stats['受賞']
            entry['主著受賞'] = researchmap_data.achievement_stats['主著受賞']

            save_path = f'{base_dirname}/researchmap_{name}.xlsx'
            researchmap_data.save_to_excel(save_path)

        print('  {}'.format(entry))
        data.append(entry)

    util.io.excel_writer(args.output_excel, data)

    chrome_driver.quit()

if __name__ == '__main__':
    main()
