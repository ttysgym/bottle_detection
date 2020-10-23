# -*- coding: utf-8 -*-
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']="3"
import warnings
warnings.simplefilter("ignore")
from tensorflow.python.util import deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False

import logging
import datetime as dt

import pygame.mixer
import numpy as np
# ラズパイ時に復活
# import picamera
from PIL import Image
import time

import main_yolo_ikeda

from translate_2 import *
from bottle_master import bottle_master
# ラズパイ時に復活
from shutter2image import shutter2image
import os
import datetime
import pandas as pd

from keras.preprocessing import image
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import efficientnet.keras

# modelを初期値をNoneに
# time_debugモードを追加


def date_initialize():
    today_dt = dt.date.today()
    today_str = today_dt.strftime("%Y_%m_%d")
    return today_str

today = date_initialize()


def setup_logger(name, logfile='LOGFILE'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even DEBUG messages
    fh = logging.FileHandler(logfile + today + ".txt")
    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s')
    fh.setFormatter(fh_formatter)

    # create console handler with a INFO log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter('%(message)s - %(asctime)s - %(levelname)s', '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(ch_formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

# 各モジュールの最初のほうで、グローバルに宣言しておく
logger = setup_logger(__name__)

class MAIN:
    """
    マスタークラス

    """
    def __init__(self, model, lang, time_debug=True, log_mode="INFO"):
        self.model_dict = {'y':"YOLO", 'e':"EFF", 'r':"Random"}
        self.language_dict = {'k':'Kinyarwanda', 'e':'English', 'f':'French', 'j':'Japanese'}
        self.model = model
        self.lang = lang
        self.check_list = ["y", "n"]
        self.time_debug = time_debug
        self.log_mode = log_mode


    def mode_select(self):
      """
      初期起動モードを選択させる関数
      標準入力から引数を取って分岐する
      """
      mode_list = ["1", "2", "3"]
      logger.info(translate_language(self.lang, "current"))
      logger.info(translate_language(self.lang, "status").format(self.model, self.language_dict[self.lang]))
      
      logger.info(translate_language(self.lang, "choice"))
      logger.info(translate_language(self.lang, "mode"))
      print("--------------------")
      mode = input(translate_language(self.lang, "mode_select"))
      logger.debug("choice mode : {}".format(mode))

      while mode not in mode_list:
          logger.warning(translate_language(self.lang, "input_error"))
          mode = input(translate_language(self.lang, "select4"))
          logger.debug("rechoice mode : {}".format(mode))

      if mode == "1":
        register = Register(self.model, self.lang, self.time_debug)
        register.main()
      elif mode == "2":
        setup = setup_mode(self.model, self.lang)
        setup.setup_mode_select()
      elif mode == "3":
        shutter2image.main()
        
        


# モデルのクラスを記載

class Random_model():
    def __init__(self):
        self.loaded_model = 100
    def Preprocess(self, pil_image=None):
        #　モデルに応じてリサイズ処理をしてインスタンス変数
        self.image_array = np.random.randn(100, 100)
    def predict(self):
        # インスタンス変数のarrayから予測、予測されたラベルを返す
        random_index = np.random.choice(10, np.random.randint(1, 4))
        return list(random_index)


class EFF_function(MAIN):
    def __init__(self):
        self.hold = np.load("/home/pi/dive_groupwork/efficient_env/group_work/models/pro_hold_vector_size_down.npy")
        self.clf = load_model('/home/pi/dive_groupwork/efficient_env/group_work/models/pro_eff3_model_size_down.h5')
        
    def Preprocess(self, im_array):
        tmp_array = im_array.resize((150, 150))
        tmp_array = img_to_array(tmp_array)
        tmp_array = tmp_array.astype('float32')/255.0
        self.im_array = tmp_array.reshape((1,150,150,3))
    
    def cosine_similarity(self, x1, x2):
        """
        test_dataと学習済み商品のコサイン類似度を算出
        n_dimはベクトルの次元　1000~1500程度
        x1: 対象の商品のベクトル   shape(1, n_dim)
        x2: 学習済みの商品のベクトル(hold_vector) shape(5, n_dim)
        return: 5つの商品に対するコサイン類似度 shape(1,5)
        """
        
        if x1.ndim == 1:
            x1 = x1[np.newaxis]
        if x2.ndim == 1:
            x2 = x2[np.newaxis]
        x1_norm = np.linalg.norm(x1, axis=1)
        x2_norm = np.linalg.norm(x2, axis=1)
        cosine_sim = np.dot(x1, x2.T)/(x1_norm*x2_norm+1e-10)
        return cosine_sim     
            
            
    def judgment(self, predict_vector, hold_vector, thresh):
        """
        predict_vector : shape(1, n_dim)
        hold_vector : shape(5, n_dim)
        """
        cos_similarity = self.cosine_similarity(predict_vector, hold_vector) # shape(1, 5)
        print(cos_similarity[0])
        # 最も値が高いindexを取得
        high_index = np.argmax(cos_similarity[0]) # int
        # cos類似度が閾値を超えるか
        if cos_similarity[0][high_index] > thresh:
            return high_index
        
        else:
            return 5  

    def predict(self):
        # predict
        img_pred = self.clf.predict(self.im_array)
        jd = self.judgment(predict_vector=img_pred, hold_vector=self.hold, thresh=0.992)
        # return jd
        return [jd]

class YOLO_function(MAIN):
    def __init__(self):
        args = parser.parse_args()
        #self.clf = load_model('/yolo/model_data/trained_weights_final.h5', compile=False)
        #print(os.getcwd())
        clf = load_model(args.model_path, compile=False)
        # yolo.pyのYOLOクラスをインスタンス化
        self.yolo = yolo.YOLO()
        # yoloの初回起動
        sample_img = Image.open('/home/pi/dive_groupwork/yolo/init/sample.jpg')
        _, _, _ = self.yolo.detect_image(sample_img)
        
    def Preprocess(self, im_array):
        self.img = img

    def predict(self):
        # predict
        jd, _, _ = self.yolo.detect_image(self.img)
        # return jd
        return jd
    
# Registerクラス
class Register(MAIN):
    def __init__(self, model, lang, time_debug):
        # 親クラスのインスタンス変数を読み込み
        super().__init__(model, lang, time_debug)
        # bottle_master_dfを呼び込む
        self.bottle_master_df = bottle_master.bottle_master_df(self.model)
            
    def main(self):
        #　モデルのオブジェクトを呼び込む、モデルクラス後に追加
        print(self.model + " loading now")
        
        if self.model == "Random":
            self.model_object = Random_model()
        elif self.model == "EFF":
            self.model_object = EFF_function()
        elif self.model == "YOLO":
            main_yolo_ikeda.main(self.model, self.lang)
        else:
            pass
        
        
        print('bottle_master')
        print(self.bottle_master_df)
        while True:
            # 空のdfを作成
            total_df = pd.DataFrame(columns=['name', 'price'])
            while True:
                # 「商品を置いてenterを押してください」
                scene = "scan_start"
                input(translate_language(self.lang, scene))
                logger.debug("hit the enter to read product")

                # 時間を図る self.time_debugに応じて対応
                if self.time_debug:
                    time_start = time.perf_counter()
                    logger.debug("time count start")
                # 写真撮影をしてnumpy_arrayで受け取る
                image_array = shutter2image.shutter_array()
                logger.debug("shutter to image")

                # numpy_arrayをPILへ変換してモデルの入力用に加工
                img = Image.fromarray(image_array)
                logger.debug("image to PIL")

                # 画像表示
                img.show()
                
                # modelオブジェクトのPreprocessでPILをresize, numpy_arrayに変換
                self.model_object.Preprocess(img)
                logger.debug("PIL to numpy_array")
                
                # 予測されたindexのリストを読み込む
                predict_index_list = self.model_object.predict()
                logger.debug('予測されたラベルインデックスのリスト {}'.format(predict_index_list))

                # 予測されたindexのリストからdfを作成
                predict_df = self.bottle_master_df.iloc[predict_index_list, [2, 3]].reset_index(drop=True)
                logger.debug("index_list to predict_dataframe")

                # 小計をdiplay
                scene = "read_message"
                logger.info(translate_language(self.lang, "read_message"))
                #print('読み取られた商品の一覧は以下になります')
                print(predict_df)

                # 時間計測
                if self.time_debug:
                    time_end = time.perf_counter()
                    # 商品を読み取るまで {}[s] 経過しました
                    scene = "time"
                    logger.info(translate_language(self.lang, scene).format(time_end-time_start))

                while True:
                # 読み取られた商品が正しい場合は「y」、誤っていた場合は「n」を押してください
                    scene = "correct?"
                    key = input(translate_language(self.lang, scene))
                    logger.debug("correct? {}".format(key))

                    if key != 'y' and key != 'n':
                        # 正しく入力されていません
                        scene = "input_error"
                        logger.warning(translate_language(self.lang, scene))
                    else:
                        break
                
                if key == 'y':
                    total_df = pd.concat([total_df, predict_df], axis=0).reset_index(drop=True)
                    print(total_df)
                    # 小計
                    scene = "subtotal"
                    logger.info(translate_language(self.lang, scene).format(total_df["price"].sum()))

                    while True:
                        # 続けて商品をスキャンする場合は「y」、会計する場合は「f」、\n キャンセルする商品がある場合は「ｘ」を押して下さい。
                        scene = "continue?"
                        key = input(translate_language(self.lang, scene))
                        if key != 'y' and key != 'f' and key != 'x':
                            # 正しく入力されていません
                            scene = "input_error"
                            logger.warning(translate_language(self.lang, scene))
                        # 商品をdeleteする処理
                        elif key == 'x':
                            while True:
                                logger.debug("delete mode start")
                                print(total_df)
                                # scene設定
                                key = input(translate_language(self.lang, "delete"))
                                logger.debug("selected delete number : {}".format(key))
                                key_list = [str(i) for i in range(len(total_df))] + ['n']
                                if key not in key_list:
                                    # 正しく入力されていません
                                    scene = "input_error"
                                    logger.warning(translate_language(self.lang, scene))
                                elif key == 'n':
                                    break
                                else:
                                    logger.info(translate_language(self.lang, "delete_complete"))
                                    print(total_df[int(key):int(key)+1])
                                    #　total_dfから消去
                                    total_df = total_df.drop(index=int(key))
                                    #　indexをreset
                                    total_df = total_df.reset_index(drop=True)
                        else:
                            break

                    if key == 'f':
                        # 合計
                        print(total_df)
                        scene = "total"
                        logger.info(translate_language(self.lang, scene).format(total_df['price'].sum()))

                        # ありがとうございました
                        scene = "thanks"
                        logger.info(translate_language(self.lang, scene))
                        move = input("next step to enter :")
                        if move == "quit":
                            self.mode_select()
                        else:
                            break
                    elif key == 'y':
                        # 次の商品を指定の位置に置いてください。
                        scene = "next"
                        logger.info(translate_language(self.lang, scene))
                    


class setup_mode(MAIN):
    """
    サブクラス
    設定変更モード

    変更できる設定
    ・分析モデル設定
    ・使用言語設定
    """
    def __init__(self, model, lang):
        # 親クラスのインスタンス変数を読み込み
        super().__init__(model, lang)

    def setup_mode_select(self):
        logger.info(translate_language(self.lang, "setup_mode"))
        stdin = input(translate_language(self.lang, "setup_choice"))
        logger.debug("choice setup mode : {}".format(stdin))

        if stdin == "1":
          self.model_select()
        elif stdin == "2":
          self.language_select()
        if stdin == "3":
          self.mode_select()


    def model_select(self):
        logger.info(translate_language(self.lang, "m_select0"))
        print("YOLO : 'y'\nEfficientNet : 'e'")
        stdin = input(translate_language(self.lang, "m_select1"))
        logger.debug("choice model : {}".format(stdin))
        while stdin not in self.model_dict.keys():
            stdin = input(translate_language(self.lang, "select4"))
            logger.debug("re choice model : {}".format(stdin))
        
        self.model = self.model_dict[stdin]
        logger.info(translate_language(self.lang, "m_select2").format(self.model))
        exit_flg = input(translate_language(self.lang, "m_select3"))
        logger.debug("mode end? : {}".format(exit_flg))

        while exit_flg not in self.check_list:
            exit_flg = input(translate_language(tmp_lang, "select4"))
        
        if exit_flg == "y":
            self.setup_mode_select()
        else:
            print("")
            self.model_select()
    
    def language_select(self):
        tmp_lang = self.lang

        logger.info(translate_language(self.lang, "l_select0"))
        print("Kinyarwanda : 'k'\nEnglish : 'e'\nFrench : 'f'\nJapanese : 'j'")
        self.lang = input(translate_language(self.lang, "l_select1"))
        logger.debug("choice lang : {}".format(self.lang))
        
        if self.lang in self.language_dict.keys():
            tmp_lang = self.lang
        while self.lang not in self.language_dict.keys():
            self.lang = input(translate_language(tmp_lang, "select4"))


        logger.info(translate_language(self.lang, "l_select2").format(self.language_dict[self.lang]))
        exit_flg = input(translate_language(self.lang, "l_select3"))
        logger.debug("mode end? : {}".format(exit_flg))

        while exit_flg not in self.check_list:
            exit_flg = input(translate_language(tmp_lang, "select4"))
        
        if exit_flg == "y":
            self.setup_mode_select()
        else:
            print("")
            self.language_select()

if __name__ == '__main__':
    main = MAIN(model='YOLO', lang="j", time_debug=True, log_mode="INFO")
    main.mode_select()

