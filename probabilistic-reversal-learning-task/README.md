# 確率的逆転学習課題 ドキュメント/プログラム


## python 刺激提示 ProbabilisticReversalLearning ver 1.0.0 （[Maual-Probabilistic_Reversal_learning20230711aRev01.pdf](/probabilistic-reversal-learning-task/Maual-Probabilistic_Reversal_learning20230711aRev01.pdf)
- 動作推奨環境
- 関連ファイル
- 動作システムの補足
- 『ProbabilisticReversalLearning』
- Psychopy-Builderの起動と『ProbabilisticReversalLearning』の実行
- 『ProbabilisticReversalLearning』のシーケンス
- 環境設定について
- 出力ファイル

## 画面刺激プログラム（[P_Reversal_Learning](/probabilistic-reversal-learning-task/P_Reversal_Learning)）

- プログラム本体/pythonスクリプト
 - [BuilderProbabilisticReservalLearning-pp20220205.psyexp](https://github.com/ken-nakae/marmoset-task-example-programs/blob/main/probabilistic-reversal-learning-task/P_Reversal_Learning/BuilderProbabilisticReservalLearning-pp20220205.psyexp) : psychopy builder刺激提示プログラム本体
- python刺激提示プログラム(P_Reversal_Learningフォルダ内)
 - [LibFeeder/Feeder.py](/probabilistic-reversal-learning-task/P_Reversal_Learning/LibFeeder/Feeder.py) : 給餌装置 制御ライブラリプログラム
 - [LibWin/MouseExit.py](/probabilistic-reversal-learning-task/P_Reversal_Learning/LibWin/MouseExit.py) : 画面終了ライブラリプログラム
 - [BuilderSession.py](/probabilistic-reversal-learning-task/P_Reversal_Learning/BuilderSession.py) : psychopy環境 制御プログラム
 - [TaskProbabilisticReversalLearning.py](/probabilistic-reversal-learning-task/P_Reversal_Learning/TaskProbabilisticReversalLearning.py) : ProbabilisticReversalLearning 制御プログラム
 - [PRL_block_loop.csv](/probabilistic-reversal-learning-task/P_Reversal_Learning/PRL_block_loop.csv) : 『ProbabilisticReversalLearning』を構成するcvsファイル（[環境設定](https://marmoset-task-example.netlify.app/docs/probabilistic-reversal-learning-task/python-program-setting)参照）
 - [PRL_trial_loop.csv](/probabilistic-reversal-learning-task/P_Reversal_Learning/PRL_trial_loop.csv) :   正解/不正解時の画像を指定するcvs設定ファイル（[環境設定](https://marmoset-task-example.netlify.app/docs/probabilistic-reversal-learning-task/python-program-setting)参照）
 - [Resource/image](/probabilistic-reversal-learning-task/P_Reversal_Learning/resource/image) : 刺激提示で使用する画像ファイルを格納（[環境設定](https://marmoset-task-example.netlify.app/docs/probabilistic-reversal-learning-task/python-program-setting)参照）
 - [Resource/sound](/probabilistic-reversal-learning-task/P_Reversal_Learning/resource/sound) : 刺激提示で使用する音ファイルを格納（[環境設定](https://marmoset-task-example.netlify.app/docs/probabilistic-reversal-learning-task/python-program-setting)参照）

# 備考
プログラムの実行には、下記サードパーティプログラムが必要となります。
あわせてインストールしてください。

## PsychoPy3
https://www.psychopy.org/

PsychoPy®は、行動科学（神経科学、心理学、心理物理学、言語学...）の幅広い実験を実行できる、Pythonベースの無料のクロスプラットフォームパッケージです。


その他詳細は下記下記ウェブサイトをご確認ください。

https://marmoset-task-example.netlify.app/docs/probabilistic-reversal-learning-task


----

Copyright © 2023 Ken Nakae

https://twitter.com/ken_nakae754
