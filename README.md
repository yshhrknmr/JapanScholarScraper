# JapanScholarScraper / 日本の研究者の研究業績取得ツール
日本の研究者の研究業績を Web リソースから取得する Python スクリプト群です。現在、以下の Web リソースに対応しています。
* [Researchmap](https://researchmap.jp/)
* [科学研究費助成事業データベース](https://kaken.nii.ac.jp/ja/) (※要 API キー)

## 実行例
各 Web リソース用の情報取得スクリプトと、統合版のスクリプトを用意しています。基本的な使い方はいずれも、研究者名が一行ずつ書かれたテキストファイル (UTF-8) を引数に与えて実行するのみです。Windows 11 上でのみ動作確認しています。ここでは、サンプル用の研究者リスト [sample_scholars.txt](https://github.com/yshhrknmr/JapanScholarScraper/blob/main/sample_scholars.txt) を使って説明します。出力ファイルは [sample_output](https://github.com/yshhrknmr/JapanScholarScraper/tree/main/sample_output) ディレクトリにあります。

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

#### 科研費
