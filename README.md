# ipocc_collector

## 説明
* ipoの株情報を取得するプログラム
* 実行は毎日行う想定（cronで設定）。おすすめは市場が閉まった後の時間
* 情報はyahooとipokabu.netから収集

## 準備
* 保存する場合はmongoDB atlasに登録が必要。

（保存不要でもDBに登録しているところをコメントアウトする必要あり）

* メールもgmailのアカウントが必要

（またはコメントアウト）

1.準備ができたらconfig.jsonを作成

（config_sample.jsonを参考）

2.requirements.txt（未作成）から必要なモジュールをインストール

3.プロジェクトディレクトリに移動しboss.pyを実行

