#!/usr/bin/env python
#! -*- coding: utf-8 -*-
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']="3"
import warnings
warnings.simplefilter("ignore")
from tensorflow.python.util import deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False

from keras.preprocessing import image
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import pygame.mixer
import numpy as np

# ラズパイ時に復活
import picamera
from PIL import Image
from time import sleep, perf_counter
from translate import *
from bottle_master import bottle_master
# ラズパイ時に復活
from shutter2image import shutter2image

import datetime
import argparse
import pandas as pd

from yolo import YOLO
from timeit import default_timer as timer

from main_1019 import MAIN


def init_yolo(yolo):
    """
    yoloモデルを起動する処理
    """
    sample_img = Image.open('init/sample.jpg')
    _, _, _ = yolo.detect_image(sample_img)

parser = argparse.ArgumentParser(description='model_data/trained_weights_final.h5')
# modelが保存されているpathを引数で指定してください
# parser.add_argument('--model_path', default=None, help="path to saved_mode")
parser.add_argument('--model_path', default='/home/pi/dive_groupwork/yolo_test/model_data/trained_weights_final.h5', help="path to saved_mode")

# デバッグの処理
parser.add_argument('--time_debug', default=False, help="debug_mode True or False")

#if __name__ == 'main_yolo_ikeda':
def main(model, lang):
    parser = argparse.ArgumentParser(description='model_data/trained_weights_final.h5')
    # modelが保存されているpathを引数で指定してください
    # parser.add_argument('--model_path', default=None, help="path to saved_mode")
    parser.add_argument('--model_path', default='/home/pi/dive_groupwork/yolo_test/model_data/trained_weights_final.h5', help="path to saved_mode")

    # デバッグの処理
    parser.add_argument('--time_debug', default=False, help="debug_mode True or False")
    
    # 引数を読み込み
    args = parser.parse_args()

    # モデル+重みを読込み
    
    # self_model = load_model(args.model_path, compile=False)

    #商品価格等の情報をbottle_masterから読み込み
    # name_price_dict = bottle_master.bottle_master_dict()
    # _, label_dict = bottle_master.bottle_label_dirpath()
    # bottle_label = {}
    # for key, value in label_dict.items():
    #     bottle_label[value] = key
    bottle_master_df = bottle_master.bottle_master_df(model="YOLO")
    
    """
    # 言語モードを選択
    while True:
        print("Please select a language!!")
        print()
        lang = input('Kinyarwanda :「k」,English :「e」,French :「f」,Japanese :「j」')
        print()
        if lang not in ['k', 'e', 'f', 'j']:
            print('Please input correctly')
            print()
        else:
            break
    """

    # yolo.pyのYOLOクラスをインスタンス化
    yolo = YOLO()
    # yoloの初回起動
    init_yolo(yolo)

    while True:
        # 空のdfを作成
        total_df = pd.DataFrame(columns=['name', 'price'])
        while True:
            # 「商品を置いてenterを押してください」
            while True:
                scene = "scan_start"
                input(translate_language(lang, scene))
                print()

                # 時間を図る self.time_debugに応じて対応
                if args.time_debug is True:
                    time_start = perf_counter()

                # 写真撮影をしてnumpy_arrayで受け取る
                image_array = shutter2image.shutter_array()

                # numpy_arrayをPILへ変換してモデルの入力用に加工
                img = Image.fromarray(image_array)

                # 読み込んだmodelでpridictを実行

                # predicted_classes = yolo_video.main(img)
                # start = timer()
                # _, _, predicted_classes = yolo.detect_image(img)
            
                predict_index_list, _, _ = yolo.detect_image(img)
                if predict_index_list.any():
                    break
                else:
                    scene = 'not_registered'
                    print(translate_language(lang, scene))
                    print()
            # end = timer()
            # print(end - start)
            

            # 時間計測
            if args.time_debug is True:
                time_end = perf_counter()
                print('デバッグ用、本番環境ではいらない、予測されたラベルインデックスのリスト {}'.format(predict_index_list))
                scene = "time"
                print(translate_language(lang, scene).format(time_end-time_start))



            # 予測されたindexのリストからdfを作成
            predict_df = bottle_master_df.iloc[predict_index_list, [2, 3]].reset_index(drop=True)

            # 小計をdiplay
            scene = "read_message"
            # 10/18 translate.pyの上記sceneの文言変更
            # print(translate_language(self.lang, scene).format('test_bottle', random_price))
            print(translate_language(lang, scene))
            print()
            print(predict_df)
            print()

            # print('商品 : {} 値段 : {} が読み取られました'.format(name, name_price_dict[name]))

            while True:
                scene = "correct?"
                key = input(translate_language(lang, scene))
                print()

                if key != 'y' and key != 'n':
                     # 正しく入力されていません
                    scene = "input_error"
                    print(translate_language(lang, scene))
                    print()
                else:
                    break
                
            if key == 'y':
                total_df = pd.concat([total_df, predict_df], axis=0).reset_index(drop=True)
                print(total_df)
                print()
                # 小計
                scene = "subtotal"
                print(translate_language(lang, scene).format(total_df["price"].sum()))
                print()

                while True:
                    # 続けて商品をスキャンする場合は「y」、会計する場合は「f」、\n キャンセルする商品がある場合は「ｘ」を押して下さい。
                    scene = "continue?"
                    key = input(translate_language(lang, scene))
                    print()
                    if key != 'y' and key != 'f' and key != 'x':
                        # 正しく入力されていません
                        scene = "input_error"
                        print(translate_language(lang, scene))
                        print()
                    # 商品をdeleteする処理
                    elif key == 'x':
                        while True:
                            print(total_df)
                            print()
                            # scene設定, translate.pyへ追加
                            scene = 'delete'
                            key = input(translate_language(lang, scene).format(len(total_df)-1))
                            print()
                            key_list = [str(i) for i in range(len(total_df))] + ['n']
                            if key not in key_list:
                                # 正しく入力されていません
                                scene = "input_error"
                                print(translate_language(lang, scene))
                                print()
                            elif key == 'n':
                                break
                            else:
                                scene = 'delete_complete'
                                print(translate_language(lang, scene))
                                print()
                                print(total_df[int(key):int(key)+1])
                                print()
                                #　total_dfから消去
                                total_df = total_df.drop(index=int(key))
                                #　indexをreset
                                total_df = total_df.reset_index(drop=True)
                    else:
                        break

                if key == 'f':
                    # 合計
                    print(total_df)
                    print()
                    scene = "total"
                    print(translate_language(lang, scene).format(total_df['price'].sum()))
                    print()

                    # ありがとうございました
                    scene = "thanks"
                    print(translate_language(lang, scene))
                    move = input("next step to enter :")
                    if move == "quit":
                        test = MAIN(model, lang)
                        test.mode_select()
                    else:
                        break
                elif key == 'y':
                    # 次の商品を指定の位置に置いてください。
                    scene = "next"
                    print(translate_language(lang, scene))
                    print()
