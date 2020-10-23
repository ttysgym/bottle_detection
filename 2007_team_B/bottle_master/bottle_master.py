import os
os.environ['TF_CPP_MIN_LOG_LEVEL']="3"
import warnings
warnings.simplefilter("ignore")
from tensorflow.python.util import deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False

import csv
import pandas as pd
import time
import datetime
from pandasql import sqldf



# bottle_masterを読み込みをDataFrame型で取得する
def bottle_master_df(model):
    # csvファイルを読み込む
    cwd_path = os.getcwd()
    
    # modelに応じて読むファイル変える
    if model == "YOLO":
        file_path = os.path.join(cwd_path, 'bottle_master/bottle_master.csv')
    elif model == "EFF":
        file_path = os.path.join(cwd_path, 'bottle_master/bottle_master_eff2.csv')
        
    bottle_master_df = pd.read_csv(file_path)
    
    #日付型に変換
    bottle_master_df["revisiondate"] = pd.to_datetime(bottle_master_df["revisiondate"])

    #Sqlクエリを定義
    q = """
        SELECT  main.id
            ,main.revisiondate
            ,main.name
            ,main.price
        FROM bottle_master_df as main
        INNER JOIN
            (
                SELECT  id
                        ,MAX(revisiondate) as revisiondate
                FROM bottle_master_df
                WHERE revisiondate <= "{}"
                GROUP BY id
            ) as sub
        ON  main.id = sub.id
        AND main.revisiondate = sub.revisiondate
        """
    
    #サーバー日付を取得
    today = pd.to_datetime(datetime.date.today())

    bottle_master_df = sqldf(q.format(today), locals())
    return bottle_master_df

# bottle_masterを読み込みを辞書型を取得する
def bottle_master_dict():
    bottle_master_dict = {}
    # csvファイルを読み込む
    cwd_path = os.getcwd()
    file_path = os.path.join(cwd_path, 'bottle_master/bottle_master.csv')
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for idx, bottle_name, price in reader:
            bottle_master_dict[idx] = [bottle_name, int(price)]

    return bottle_master_dict

# 学習データが格納されているディレクトリのパスとラベルの辞書を取得する
def bottle_label_dirpath():
    data_dir_path = []
    label_dict = {}
    label = 0
    # csvファイルを読み込む
    cwd_path = os.getcwd()
    file_path = os.path.join(cwd_path, 'bottle_master/bottle_master.csv')
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for bottle_name, _ in reader:
            # pathの取得、リストへ
            path = os.path.join(cwd_path, 'shutter2image', bottle_name)
            data_dir_path.append(path)
            # ラベルを辞書へ記録
            label_dict[bottle_name] = label
            label += 1
    return data_dir_path, label_dict
