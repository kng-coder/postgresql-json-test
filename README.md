# postgresql-json-test

## 概要

PostgreSQLのjsonb型カラムの動作を検証するためのコード・実行環境です。
実行環境はvscodeのdevcontainerを用いてdocker上に構築しています。

## 使い方

本リポジトリをローカルにチェックアウト後、チェックアウトしたディレクトリをvscodeで開き、
コマンドパレットで「コンテナーでリビルドして再度開く」を選択すればdocker上に実行環境が構築されます。

PostgreSQLに接続したい場合は、vscodeのターミナルで以下を入力してください。
```sh
psql -h postgresql user user
```

憲章に使用したソースは、ターミナルから以下のコマンドで実行できます。
```sh
python test.py
```
