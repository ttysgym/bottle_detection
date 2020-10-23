# yoloのannotationファイルを固定座標で作成するディレクトリ
- [Trainng項目のexampleのフォーマット](https://github.com/qqwweee/keras-yolo3)

## Attention
  - **annotationファイルは絶対パスでjpgファイルを取得しているのでyoloを実行する環境でannotationファイルを取得すること!!**

## how to use
  - カレントディレクトリは /dive_groupwork
  - 以下を実行すると、annotation_for_yolo.txtが生成される
  ```
  python annotaition_text_for_yolo/make_annotation.py
  ```
  - default_argument
    - 座標情報（500mlのボトルを前提）
      x_min=95, y_min=140, x_max=170,y_max=360
    - 画像データのディレクトリ
      shutter2imageのそれぞれのbottle_nameフォルダ
  ```
  引数を指定する場合の例
  python annotaition_text_for_yolo/make_annotation.py --x_min=80 --y_min=150 --x_max=180 --y_max=400 --image_path='photo'
  ```
