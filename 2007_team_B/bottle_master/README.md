# bottle_masterを管理するディレクトリ
## 1. bottle_masterをcsvファイルで作成
  - make_bottle_master.ipynb　を実行し、csvファイルを作成

## 2. bottle_nameとpriceの辞書を取得
  - pwdは/dive_groupworkで機能
  - how to use
    ```
    from bottle_master import bottle_master
    name_price_dict = bottle_master.bottle_master_dict()

    # name_price_dictの例
    # name_price_dict = {'cola': 100, 'namacha': 200, 'calpis': 150, 'gogotea': 130, 'pocari': 140}
    ```


## 3. 学習時に使用するbottle_image.jpgが保存されているディレクトリのパスリストとラベルを取得
  - pwdは/dive_groupworkで機能
  - how to use
    ```
    from bottle_master import bottle_master
    data_dir_path, label_dict = bottle_master.bottle_label_dirpath()

    # data_dir_pathの例
    # data_dir_path = ['/dive_groupwork/shutter2image/cola', '/dive_groupwork/shutter2image/namacha',,]
    # label_dictの例
    # label_dict = {'cola': 0, 'namacha': 1, 'calpis': 2, 'gogotea': 3, 'pocari': 4}
    ```
