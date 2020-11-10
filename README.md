# bottle_detection
raspberry piとraspberry pi cameraを用いてペトボトル飲料を自動検出するセルフレジシステム。

検出可能な商品は下記５種：

コカ・コーラ
午後の紅茶レモンティー
生茶
ポカリスエット
ほうじ茶
機能一覧：

商品の検出（複数可）
検出商品の商品名及び金額表示

モデル
Keras適合のtiny-yolov3を実装（github)。YOLO作者が公開している（YOLO website）学習済みモデルを初期重みとし、検出対象商品の画像データセットを転移学習させた。

環境条件
Python 3.5.3
tensorflow 1.14.0
keras 2.2.0

起動方法
main_yolo.pyを実行
