import os
import shutil
import json

from os import listdir

dir_list = os.listdir('/home/ai/disk/data/doppio/ms_coco/val/doppio_labels/object_detection_labels')
print(dir_list)
print(len(dir_list))
dir_list.remove('info.json')
print(len(dir_list))
file_dict = dict()
file_dict['json_files'] = dir_list
dir_list = os.listdir('/home/ai/disk/data/doppio/ms_coco/val/images')
print(len(dir_list))
print(dir_list)