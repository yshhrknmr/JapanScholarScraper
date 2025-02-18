import kakenhi.util
import util.io
import argparse

def main():
    config = util.io.load_yaml_config('config.yaml')
    if config is None:
        exit()

    parser = argparse.ArgumentParser(description='漢字氏名から科研費データベースを検索し、Excelファイルに出力します。')
    parser.add_argument('-i', '--input_list', required=True, help='漢字氏名が1行ずつ記載された入力テキストファイル(UTF-8)')
    parser.add_argument('-o', '--output_excel', default='', help='出力するExcelファイル名')
    parser.add_argument('-a', '--appid', default='', help='NIIデベロッパーのAPIキー, 詳細: https://support.nii.ac.jp/ja/cinii/api/developer')
    args = parser.parse_args()

    if args.output_excel == '':
        args.output_excel = config['kakenhi']['default_output']
        print(f'Note: args.output_excel set as: {args.output_excel}')
    
    if args.appid == '':
        args.appid = config['kakenhi']['appid']
        print(f'Note: args.appid set as: {args.appid}')

    names = util.io.read_names_from_file(args.input_list)
    n_names = len(names)
    print('{} names loaded'.format(n_names))

    data = []
    for idx, name in enumerate(names, 1):
        print('[{}/{}] querying {}'.format(idx, n_names, name))

        json_data = kakenhi.util.query_json(args.appid, name)
        entry = kakenhi.util.extract_pi_projects(json_data, name)

        print('  {}'.format(entry))
        data.append(entry)

    util.io.excel_writer(args.output_excel, data)

if __name__ == '__main__':
    main()
