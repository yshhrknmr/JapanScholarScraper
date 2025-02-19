# JapanScholarScraper / 日本の研究者の研究業績取得ツール
日本の研究者の研究業績を Web リソースから取得する Python スクリプト群です。現在、以下の Web リソースに対応しています。
* [Researchmap](https://researchmap.jp/)
* [科学研究費助成事業データベース](https://kaken.nii.ac.jp/ja/) (※要 API キー)

## 実行例
各 Web リソース用の情報取得スクリプトと、統合版のスクリプトを用意しています。基本的な使い方はいずれも、研究者名が一行ずつ書かれたテキストファイル (UTF-8) を引数に与えて実行するのみです。Windows 11 上の Python 3.11.9 でのみ動作確認しています。ここでは、サンプル用の研究者リスト [sample_scholars.txt](https://github.com/yshhrknmr/JapanScholarScraper/blob/main/sample_scholars.txt) を使って説明します。出力ファイルのサンプルは [sample_output](https://github.com/yshhrknmr/JapanScholarScraper/tree/main/sample_output) ディレクトリにあります。

> [!CAUTION]
> 研究者名を記録したテキストファイルは必ず UTF-8 エンコーディングで記録してください。

### Researchmap
```
> python query_researchmap.py -i sample_scholars.txt
```
出力ファイルは次の 2 種類です。
* サマリ情報が記録された Excel ファイル (デフォルトファイル名: [summary_researchmap.xlsx](https://github.com/yshhrknmr/JapanScholarScraper/blob/main/sample_output/summary_researchmap.xlsx))
* [研究者リスト名で作成されるディレクトリ](https://github.com/yshhrknmr/JapanScholarScraper/tree/main/sample_output/sample_scholars)直下の、研究者ごとの詳細情報が記録された Excel ファイル

### 科研費
```
> python query_kakenhi.py -i sample_scholars.txt
```
出力ファイルは、サマリ情報が記録された Excel ファイル (デフォルトファイル名: [summary_kakenhi.xlsx](https://github.com/yshhrknmr/JapanScholarScraper/blob/main/sample_output/summary_kakenhi.xlsx)) のみです。

### 統合版
```
> python query_all.py -i sample_scholars.txt
```
出力ファイルは次の 2 種類です。
* サマリ情報が記録された Excel ファイル (デフォルトファイル名: [summary_all.xlsx](https://github.com/yshhrknmr/JapanScholarScraper/blob/main/sample_output/summary_all.xlsx))
* [研究者リスト名で作成されるディレクトリ](https://github.com/yshhrknmr/JapanScholarScraper/tree/main/sample_output/sample_scholars)直下の、研究者ごとの詳細情報が記録された Excel ファイル

## 実行の準備
### リポジトリの clone
まずこのリポジトリを clone してください。以下は https 経由の場合です。
```
> git clone https://github.com/yshhrknmr/JapanScholarScraper.git
```
以下の作業は `JapanScholarScraper` リポジトリ内で行います。

### Python ライブラリのインストール
以下の Python ライブラリを手動でインストール
```
> python -m pip install pyyaml selenium pandas openpyxl
```
するか、requirements.txt を使って一気にインストールしてください。
```
> python -m pip install -r requirements.txt
```

### Google Chrome のインストール
Researchmap の問い合わせのために Google Chrome を呼び出している関係で、Google Chrome をインストールしてください。

### 設定ファイルの編集
設定ファイル [config.yaml](https://github.com/yshhrknmr/JapanScholarScraper/blob/main/config.yaml) を編集してください。特に重要な項目は以下です。

#### Researchmap
```
researchmap:
(中略)
  # selenium の webdriver が偽装する Web ブラウザのエージェント文字列
  user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
```
`user_agent` に、ご自身が普段使っている Web ブラウザのエージェント情報を記入してください。不明の場合は、例えば [こちらのURL](https://testpage.jp/tool/ip_user_agent.php) にある `HTTP_USER_AGENT` の直下に表示される文字列をコピペしてください。
#### 科研費
```
kakenhi:
(中略)
  # 科研費データベースの API キー. 即時発行可能. 詳細: https://support.nii.ac.jp/ja/cinii/api/developer 
  appid:  'PUT_YOUR_OWN_API_KEY'
```
`appid` は科研費データベースにアクセスするための API キーです。[こちらのURL](https://support.nii.ac.jp/ja/cinii/api/developer) の「デベロッパー登録」から取得し (必要事項の入力後に即座に発行されます)、設定ファイル内の `PUT_YOUR_OWN_API_KEY` という文字列を置き換えてください。スクリプトの実行時引数で指定することもできます。

## 各スクリプトの詳細
### Researchmap
#### 使い方の詳細
```
> python query_researchmap.py --help
usage: query_researchmap.py [-h] -i INPUT_LIST [-o OUTPUT_EXCEL]

漢字氏名からresearchmapのURLを検索し、Excelファイルに出力

options:
  -h, --help            show this help message and exit
  -i INPUT_LIST, --input_list INPUT_LIST
                        漢字氏名が1行ずつ記載された入力テキストファイル(UTF-8)
  -o OUTPUT_EXCEL, --output_excel OUTPUT_EXCEL
                        出力するExcelファイル名
```
#### 仕様
Researchmap から各研究者の情報を得るには、研究者ごとに設定された ID を取得する必要があります。研究者氏名とその ID を紐づける API は存在するのですが、研究機関の担当者しか利用できません。そこで、一般の検索エンジン (DuckDuckGo) を利用し、研究者氏名をクエリとして ID を取得しています。検索エンジンから BAN されるのを避けるために、1 人問い合わせるたびにランダムに 1～4 秒の待ち時間を入れています。しかしこれでも BAN される場合があります。設定ファイルの `user_agent` に普段使っている Web ブラウザのエージェント情報を記入してもらえば回避できるはずです。

Researchmap の研究者ごとの ID を取得したら、それを用いて研究者情報が記録された JSON ファイルを取得します。しかし Researchmap の記載内容は研究者ごとにバラバラで、論文の学会・雑誌名なども表記がバラバラです。スクリプト内で論文の種別を、国際雑誌、和文雑誌、国際会議、その他に分類していますが、ヒューリスティックな判定方法なので、誤りを含んでいる可能性が高いです。

### 科研費
#### 使い方の詳細
```
> python query_kakenhi.py --help
usage: query_kakenhi.py [-h] -i INPUT_LIST [-o OUTPUT_EXCEL] [-a APPID]

漢字氏名から科研費データベースを検索し、Excelファイルに出力します。

options:
  -h, --help            show this help message and exit
  -i INPUT_LIST, --input_list INPUT_LIST
                        漢字氏名が1行ずつ記載された入力テキストファイル(UTF-8)
  -o OUTPUT_EXCEL, --output_excel OUTPUT_EXCEL
                        出力するExcelファイル名
  -a APPID, --appid APPID
                        NIIデベロッパーのAPIキー, 詳細: https://support.nii.ac.jp/ja/cinii/api/developer
```
#### 仕様
NII の API を利用して情報を取得します (そのため API キーが必要です)。問い合わせ件数がそれほど多くないという前提で、問い合わせの待ち時間を入れていないので、高速に問い合わせ可能です。

研究者ごとの情報を記録した JSON ファイルを取得し、研究代表者となっている研究課題の種別 (基盤(A)(B)(C)など) とその実施期間をまとめて出力します。同じ種別で複数回採択されている場合は、種別ごとに集約します。簡略化のため種別名に含まれる「研究」という文字列を削除しているので、種別名によっては不自然になっている可能性があります。なお「特別研究員奨励費」は、教員が指導している留学生などの研究予算だと見なして除外しています。

### 統合版
#### 使い方の詳細
```
> python query_all.py --help
usage: query_all.py [-h] -i INPUT_LIST [-o OUTPUT_EXCEL] [-a KAKENHI_APPID]

漢字氏名からresearchmapのURLを検索し、Excelファイルに出力

options:
  -h, --help            show this help message and exit
  -i INPUT_LIST, --input_list INPUT_LIST
                        漢字氏名が1行ずつ記載された入力テキストファイル(UTF-8)
  -o OUTPUT_EXCEL, --output_excel OUTPUT_EXCEL
                        出力するExcelファイル名
  -a KAKENHI_APPID, --kakenhi_appid KAKENHI_APPID
                        NIIデベロッパーのAPIキー, 詳細: https://support.nii.ac.jp/ja/cinii/api/developer
```
#### 仕様
各 Web リソース用のスクリプトを統合しただけなので、詳細は各スクリプトの説明を参照してください。

## 制限事項
* 各 Web リソースには、必ずしも最新かつ正確な情報が記載されているとは限りません。最新かつ正確な情報は必ずご自身で確認してください。
* 現在は同姓同名の研究者に対応していません。近日対応予定です。
