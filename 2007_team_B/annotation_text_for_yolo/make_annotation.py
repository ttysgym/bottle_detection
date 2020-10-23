#!/usr/bin/env python
#! -*- coding: utf-8 -*-
import os
import csv
import argparse
import glob
import pandas as pd

parser = argparse.ArgumentParser(description='this program is to read image.jpg and make annotation.txt for yolo')
parser.add_argument('--x_min', default=95, help="coordinate x_min")
parser.add_argument('--y_min', default=140, help="coordinate y_min")
parser.add_argument('--x_max', default=170, help="coordinate x_max")
parser.add_argument('--y_max', default=360, help="coordinate y_max")
parser.add_argument('--image_path', default='shutter2image', help="dive_groupwork配下のディレクトリでファイルが保存せているディレクトリ名")

def main():
    # 引数を読み込み
    args = parser.parse_args()
    x_min = args.x_min
    y_min = args.y_min
    x_max = args.x_max
    y_max = args.y_max
    image_path = args.image_path

    cwd_path = os.getcwd()

    # bottle_masterをリストで読み込み
    bottle_list = []
    with open(os.path.join(cwd_path, 'bottle_master/bottle_master.csv'), 'r') as f:
        reader = csv.reader(f)
        for bottle_name, _ in reader:
             bottle_list.append(bottle_name)

    annotation_df = pd.DataFrame(columns=['file_path', 'coordinate_classid'])
    file_path = []
    coordinate_classid=[]
    # jpgファイルが保存されているファイルを開き、jpgファイルのリストを取得
    for class_id, bottle_dir in enumerate(bottle_list):
        jpg_path = str(cwd_path) + '/' + image_path + '/' + bottle_dir + '/*.jpg'
        file_name_list = glob.glob(jpg_path)
        ccid = '{},{},{},{},{}'.format(x_min, y_min, x_max, y_max, class_id)
        for file_name in file_name_list:
            file_path.append(file_name)
            coordinate_classid.append(ccid)
    annotation_df['file_path'] = file_path
    annotation_df['coordinate_classid'] = coordinate_classid
    annotation_df.to_csv(os.path.join(cwd_path, 'annotation_text_for_yolo/annotation_for_yolo.txt'), sep='\t', header=None, index=False)
    print('annotation_for_yolo.txt is created!!')

if __name__ == '__main__':
    main()
