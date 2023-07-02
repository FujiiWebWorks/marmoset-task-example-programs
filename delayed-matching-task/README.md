# 遅延見本合わせ課題 ドキュメント/プログラム

## 給餌/給水装置取扱説明書（[FeedingAndWaterSupplySystemManual.pdf](/delayed-matching-task/FeedingAndWaterSupplySystemManual.pdf)）
- 注意事項
- 給餌装置各部説明
- 蓋の取り付け、取り外し方法
- 各部分解と組み立て方法
- 給餌装置用PCの設定
- 給餌器の動作チェック方法
- キャリブレーション方法
- 給水装置各部説明
- 給餌器の動作チェック方法
- 給水装置用PCの設定
- 給水措置の動作チェック
- 付録1) 給水装置のコントロールコマンドについて
- 付録2) 給水装置ポンプ仕様
- 付録3) 給水装置用パイプホルダー



## python 刺激提示 DelayedMatch ver 1.0.2（[Manual-DelayedMatch20221029a-oneR.pdf](/delayed-matching-task/Manual-DelayedMatch20221029a-oneR.pdf)）
- 動作環境
- 動作確認ハードウェア
- 関連ファイル
- タッチパネル関係の Windows 上での設定について
- 実行の流れ
- 環境設定ファイル
- ネットワーク通信
- サンプルプログラム『DelayedMatch』
- 出力ファイル
- 付録

## 給水装置 パイプホルダー組立手順書（[PipeHolderAssemblyInstructions.pdf](/delayed-matching-task/PipeHolderAssemblyInstructions.pdf)）
- 手順1〜5


## 給餌器用プログラム（[Feeder_Test](/delayed-matching-task/Feeder_Test)）
- feeder_test.exe
- hspext.dll

## 給水器用プログラム（[Drink_Test](/delayed-matching-task/Drink_Test)）
- drink_test.exe
- hspext.dll

## 画面刺激プログラム（[PyBTTs](/delayed-matching-task/PyBTTs)）
- [PyBTTs/bin/](/delayed-matching-task/PyBTTs/bin/)PyBTTsRunOne.exe（ランチャープログラム）
- [PyBTTs/Env/envPyBTTs.txt](/delayed-matching-task/PyBTTs/Env/envPyBTTs.txt)（ハードウェア関連の設定ファイル）
- [PyBTTs/Run](/delayed-matching-task/PyBTTs/Run)（『python 刺激提示プログラム』を格納）
 - [『PyBTTsDelayedMatchV16』フォルダ](/delayed-matching-task/PyBTTs/Run/PyBTTsDelayedMatchV16)
   - [BTTs16DMExtraStateDelayTTLLoop.py](/delayed-matching-task/PyBTTs/Run/PyBTTsDelayedMatchV16/BTTs16DMExtraStateDelayTTLLoop.py) : python 刺激提示プログラム本体
   - [CommonV010011](/delayed-matching-task/PyBTTs/Run/PyBTTsDelayedMatchV16/CommonV010011) : python 各種ライブラリが格納されています
   - [bttsTrialDM.py](/delayed-matching-task/PyBTTs/Run/PyBTTsDelayedMatchV16/bttsTrialDM.py) : トライアルプログラム本体
 - [『PyBTTsParamList』フォルダ](/delayed-matching-task/PyBTTs/Run/PyBTTsParamList): 実験毎の課題パラメータを設定
   - [BTTsParamDMV16-20220928a.py](/delayed-matching-task/PyBTTs/Run/PyBTTsParamList/BTTsParamDMV16-20220928a.py) : 良く使う変数はこのファイルを編集することでデフォルト値を変更できます。パラメータの詳細は次ページに記載します。

# 備考
プログラムの実行には、下記サードパーティプログラムが必要となります。
あわせてインストールしてください。

## Virtual COM Port Drivers
https://ftdichip.com/drivers/vcp-drivers/

FTDI社製デバイスのVCP（Virtual COM Port）ドライバ

## PsychoPy3
https://www.psychopy.org/

PsychoPy®は、行動科学（神経科学、心理学、心理物理学、言語学...）の幅広い実験を実行できる、Pythonベースの無料のクロスプラットフォームパッケージです。


その他詳細は下記下記ウェブサイトをご確認ください。

https://marmoset-task-example.netlify.app/docs/delayed-matching-task/python-program-download

----

Copyright © 2023 Ken Nakae

https://twitter.com/ken_nakae754
