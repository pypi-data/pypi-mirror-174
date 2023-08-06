import json
import cv2
import albumentations as A
from torch.utils.data.dataset import Dataset
import torch
from albumentations.pytorch import ToTensorV2
from glob import glob
import numpy as np
from collections import OrderedDict
import urllib.request
import os
import requests 

class DoppioDataset(Dataset):

    def __init__(self, dataset=None, split_dir=None, task_info=None, augmentation=None, valid_classes=None):
        
        transforms_kwargs_params = {}
        self.transforms_kwargs_input = dict()
       
        url_label_address =  "http://222.231.59.68/{}/{}/doppio_labels/{}_labels/".format(dataset, split_dir, list(task_info.keys())[0])
        self.url_image_address =  "http://222.231.59.68/{}/{}/images/".format(dataset, split_dir)


        url_files = os.path.join(url_label_address, "files.json")

       
        # ms_coco , val, object dtection
        with urllib.request.urlopen(url_files) as url:
            url_files_dict = json.load(url)

        url_temp_label_json = url_files_dict['label_files']
        self.url_image = url_files_dict['image_files']
        #url_mask = url_info['url_mask']

        self.json_files = []

        # info json 정보를 불러오기 ? 이거는 처음에 한번만 호출하면 되니깐 #http://222.231.59.68/ms_coco/train/images/000000000009.jpg
        url_info =  os.path.join(url_label_address, "info.json")
        # ms_coco , val, object dtection
        with urllib.request.urlopen(url_info) as url:
            self.info_json = json.load(url)
        
        # task 는 사용자가 요청하는거 
        self.task = list(task_info.values())[0]

        for item in self.task:
            if item == "bbox":
                transforms_kwargs_params['bbox_params'] = A.BboxParams(format="pascal_voc", label_fields=['class']) # ouput 할때 yolo 나 coco format 처럼 다른 스타일로 내보내게 자유도를 줘야함.
                self.transforms_kwargs_input['bboxes'] = None
            elif item == "segmentation":
                self.transforms_kwargs_input['masks'] = None
            elif item == "keypoint":
                transforms_kwargs_params['keypoint_params'] = A.KeypointParams(format="xy", label_fields=['keypoint_labels'])
                self.transforms_kwargs_input['keypoints'] = None
                self.transforms_kwargs_input['keypoint_visible'] = None
                self.transforms_kwargs_input['keypoint_labels'] = None
                self.keypoint_classes = [ i for i in range(len(self.info_json['keypoint_classes']))]
            elif item == "segmentation_mask":
                self.transforms_kwargs_input['mask'] = None
                self.classes_total = dict(zip( self.info_json['classes'], range(len( self.info_json['classes']))))
                
            elif item == "class":
                self.transforms_kwargs_input['class'] = None

        if valid_classes != None: # 빼고 싶은 코드가 있을 경우
            self.info_json['classes'] =  dict(zip(valid_classes, range(len(valid_classes))))
            self.ori2valid_class_num = {}

            for t, t_valid_class in enumerate(valid_classes):
                self.ori2valid_class_num[self.classes_total[t_valid_class]] = t

        semantic_mask_flag = 0
        if "segmentation_mask" in task_info:
            semantic_mask_flag = 1
            
        # json 파일에서 유저가 넣은 valid class 가 하나도 없을 경우 제거하는 코드

        for url_json in url_temp_label_json:
            url_json_path = os.path.join(url_label_address, url_json)  
            with urllib.request.urlopen(url_json_path) as url:
                label_json_file = json.load(url)

            flag = 0 
            for ann in label_json_file['annotation']:
                classes = ann['class']
                if classes in self.info_json['classes']:
                    flag = 1
                    break
            if flag == 1 or semantic_mask_flag == 1:
                self.json_files.append(label_json_file)
            
        print("augmentation 부분 코드 맞춰줘야 한다. ")
        
        self.transform = A.Compose(
            augmentation,
            **transforms_kwargs_params
            
        )
        # self.trans = trans
        self.transforms_kwargs_input['image'] = None

    def __getitem__(self, index):

        self.doppio_output = OrderedDict()
        self.doppio_output['area'] = []
        self.doppio_output['image'] = None
        
        for item in self.task:
            if item == "bbox":
                self.doppio_output["bbox"] = []
            elif item == "segmentation":
                self.doppio_output["segmentation"] = []
            elif item == "keypoint":
                self.doppio_output["keypoint"] = []
                self.doppio_output["keypoint_visible"] = []
                self.doppio_output["keypoint_labels"] = []
            elif item == "segmentation_mask":
                self.doppio_output["segmentation_path"] = []
            elif item == "class":
                self.doppio_output['class'] = []        

        json_file = self.json_files[index]
        img_name = json_file['image_name']
        im_path = os.path.join(self.url_image_address, img_name)
    
       
        image_nparray = np.asarray(bytearray(requests.get(im_path).content), dtype=np.uint8)
        img = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
        im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)



        annotations = json_file['annotation']

        if "class" in self.doppio_output.keys():
            self.doppio_output.move_to_end('class', False)

        ann_keys = list(self.doppio_output.keys())

        for ann in annotations: # ex) 이미지의 박스 여러개 일때 
            for ann_key in ann_keys:
                if ann_key in ann.keys():
                    temp_ = ann[ann_key] 
                    if ann_key == "class":
                        if temp_ != "" and temp_ in self.info_json['classes']: # defaeul
                            self.doppio_output[ann_key].append(int(self.info_json['classes'][temp_]))
                        else:
                            break
                    elif ann_key == "keypoint":
                        self.doppio_output[ann_key].append(temp_)
                    elif ann_key == "segmentation":
                        h, w, _ = img.shape
                        m = np.zeros([h, w], dtype=np.int32)
                        if len(np.array(temp_).shape) == 2:
                            self.doppio_output[ann_key].append(cv2.fillPoly(m,  [np.array(temp_)], 1 ))
                        else:
                            make_temp_array = [np.array(l) for l in temp_]
                            self.doppio_output[ann_key].append(cv2.fillPoly(m, make_temp_array,1 ))
                    elif ann_key == "segmentation_path":
                        mask = self.mask_file[index]
                        self.doppio_output[ann_key].append(mask)
                    else:
                        self.doppio_output[ann_key].append(temp_)

        for key in self.transforms_kwargs_input:
            if key == "image":
                self.transforms_kwargs_input[key] = im_rgb
            elif key == 'bboxes':
                self.transforms_kwargs_input[key] =  self.doppio_output['bbox']
            elif key == "class":
                self.transforms_kwargs_input[key] = self.doppio_output['class']
            elif key == "mask": 
                mask = self.doppio_output['segmentation_path'][0]
                copy_mask = np.zeros_like(mask)
                for temp_key, value in self.ori2valid_class_num.items():   
                    copy_mask[mask == temp_key] = value
                self.transforms_kwargs_input[key] = copy_mask
            elif key == "masks":
                self.transforms_kwargs_input[key] = self.doppio_output['segmentation']
            elif key == "keypoints":
                self.transforms_kwargs_input[key] = [el for kp in self.doppio_output['keypoint'] for el in kp]
            elif key == "keypoint_labels":
                self.transforms_kwargs_input[key] = self.keypoint_classes * len(self.doppio_output['keypoint'])
            elif key == "keypoint_visible":
                self.transforms_kwargs_input[key] = [el for kp in self.doppio_output['keypoint_visible'] for el in kp]    
        
        img_tensor = self.transform(**self.transforms_kwargs_input)

        return img_tensor

    # 데이터의 전체 길이를 구하는 함수
    def __len__(self):
        return len(self.json_files)


def collate(batch_data):

    keys_ = batch_data[0].keys()
    return_dict ={}

    for k in keys_:
        if k == 'class_labels':
            tmps = [s[k] for s in batch_data]
            return_dict[k] = tmps
        elif k == "keypoints":
            max_value = max(batch_data[0]["keypoint_labels"]) + 1
            tmps = [torch.as_tensor( np.array(s[k]).reshape(-1,max_value,2)) for s in batch_data]
            return_dict[k] = tmps
        elif k == "keypoint_labels":
            max_value = max(batch_data[0]["keypoint_labels"]) + 1
            tmps = [torch.as_tensor( np.array(s[k]).reshape(-1,max_value)) for s in batch_data]
            return_dict[k] = tmps
        elif k == "keypoint_visible":
            max_value = max(batch_data[0]["keypoint_labels"]) + 1
            tmps = [torch.as_tensor( np.array(s[k]).reshape(-1, max_value)) for s in batch_data]
            return_dict[k] = tmps
        elif k == 'image':
            tmp = [s[k] for s in batch_data]
            return_dict[k] = torch.stack(tmp, 0)
        elif k == "masks":
            try:
                h, w = batch_data[0][k][0].shape    
                tmps = [torch.from_numpy(np.vstack(s[k]).astype(np.float).reshape(-1, h, w)) for s in batch_data]
                return_dict[k] = tmps
            except:
                continue
        elif k == "mask":
            tmp = [s[k] for s in batch_data]
            return_dict[k] = torch.stack(tmp, 0)
        elif k == "bboxes":
            tmps = [torch.as_tensor(s[k]) for s in batch_data]
            return_dict[k] = tmps
        else:
            tmps = [torch.as_tensor(s[k]) for s in batch_data]
            return_dict[k] = tmps

    return return_dict

def doppio(dataset=None, split_dir=None, task_info=None):


    custom_dataset = DoppioDataset(dataset=dataset, split_dir=split_dir, task_info=task_info, augmentation=[A.Resize(width=1000, height=1000),ToTensorV2(transpose_mask=True)])# [A.Resize(width=512, height=512),ToTensorV2(transpose_mask=True)])

    my_dataset_loader = torch.utils.data.DataLoader(dataset=custom_dataset,
                                                    batch_size=8,
                                                    shuffle=True,  num_workers=8, collate_fn=collate)

    return my_dataset_loader


    
