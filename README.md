# JapanScholarScraper / 日本の研究者の研究業績取得ツール
日本の研究者の研究業績を Web リソースから取得する Python スクリプト群です。現在、以下の Web リソースに対応しています。
* [Researchmap](https://researchmap.jp/)
* [科学研究費助成事業データベース](https://kaken.nii.ac.jp/ja/) (※要 API キー)

## 実行例
各 Web リソース用の情報取得スクリプトと、統合版のスクリプトを用意しています。基本的な使い方はいずれも、研究者名が一行ずつ書かれたテキストファイル (UTF-8) を引数に与えて実行するのみです。Windows 11 上でのみ動作確認しています。ここでは、サンプル用の研究者リスト [sample_scholars.txt](https://github.com/yshhrknmr/JapanScholarScraper/blob/main/sample_scholars.txt) を使って説明します。出力ファイルは [sample_output](https://github.com/yshhrknmr/JapanScholarScraper/tree/main/sample_output) ディレクトリにあります。

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
以下の作業は 

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
user_agent に、ご自身が普段使っている Web ブラウザのエージェント情報を記入してください。不明の場合は、例えば [こちらのURL](https://testpage.jp/tool/ip_user_agent.php) にある `HTTP_USER_AGENT` という文字列をコピペしてください。
#### 科研費
```
kakenhi:
(中略)
  # 科研費データベースの API キー. 即時発行可能. 詳細: https://support.nii.ac.jp/ja/cinii/api/developer 
  appid:  'PUT_YOUR_OWN_API_KEY'
```
`appid` は科研費データベースにアクセスするための API キーです。設定ファイル内の `PUT_YOUR_OWN_API_KEY` という文字列を置き換えてください。スクリプトの実行時引数で指定することもできます。API キーの発行は、[こちらのURL](https://support.nii.ac.jp/ja/cinii/api/developer) の「デベロッパー登録」で即座に発行できます。
