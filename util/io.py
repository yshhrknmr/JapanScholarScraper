import yaml
import time
import pandas as pd
import openpyxl

def load_yaml_config(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return config
    except Exception as e:
        print(f"  Exception: {e}")
        return None


def dump_yaml_config(yaml_config):
    print('dump yaml config:')
    print(yaml.safe_dump(yaml_config))


def read_names_from_file(filename):
    names = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                names.append(line)
    return names


def excel_writer(filename, data_dict):
    try:
        df = pd.DataFrame(data_dict)
        df.to_excel(filename, index=False)

        time.sleep(0.5)

        wb = openpyxl.load_workbook(filename)
        for sheet in wb.sheetnames:
            ws = wb[sheet]
            ws.auto_filter.ref = ws.dimensions
            ws.freeze_panes = 'B2'
        wb.save(filename)
    except Exception as e:
        print(f"  Exception: {e}")
        return None
