import numpy as np
import json

from .AutoDriveDataset import AutoDriveDataset
from .convert import convert, id_dict, id_dict_single,id_dict_traffic
from tqdm import tqdm

###wwjo ktraffic load
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

single_cls = False       # just detect vehicle
traffic_cls = False

class BddDataset(AutoDriveDataset):
    def __init__(self, cfg, is_train, inputsize, transform=None):
        super().__init__(cfg, is_train, inputsize, transform)
        self.db = self._get_db()
        self.is_train = is_train
        self.cfg = cfg

    def _get_db(self):
        """
        get database from the annotation file

        Inputs:

        Returns:
        gt_db: (list)database   [a,b,c,...]
                a: (dictionary){'image':, 'information':, ......}
        image: image path
        mask: path of the segmetation label
        label: [cls_id, center_x//256, center_y//256, w//256, h//256] 256=IMAGE_SIZE
        """
        print('building database...')
        gt_db = []
        #root_dir = '/media/jo/26BC515EBC512997/ktraffic_full/label'
        root_dir = '/media/jo/26BC515EBC512997/ktraffic_full/label'

        val_dir = '/media/jo/26BC515EBC512997/ktraffic_sample/label'

        seg_dummy_path = '/home/jo/Desktop/data/ktraffic/seg_dummy.png'
        possible_file_extension = ['.json']
        if self.is_train==True:
            for (root, dirs, files) in os.walk(root_dir):
                if len(files) > 0:
                    for file_name in tqdm(files):
                        ###if there is selected extension file
                        if os.path.splitext(file_name)[1] in possible_file_extension:
                            ### for each .json file
                            label_path = root + '/' + file_name
                            
                            # 경로에서 \를 모두 /로 바꿔줘야함
                            label_path = label_path.replace('\\', '/') # \는 \\로 나타내야함  
                            ###load json file to python code
                            with open(label_path, 'r') as f:
                                label = json.load(f)
                            ###build image path
                            label_path1, file_path1 = os.path.split(label_path)
                            label_path2, file_path2 = os.path.split(label_path1)
                            label_path2 = label_path2.replace('/label', '')

                            image_path = label_path2 + '/' + file_path1.replace('.json', '.jpg')

                            ###data example:: {'annotation': [{'light_count': '3', 'box': [407, 288, 449, 306], 
                            # 'attribute': [{'red': 'on', 'green': 'off', 'x_light': 'off', 
                            # 'others_arrow': 'off', 'yellow': 'off', 'left_arrow': 'off'}], 
                            # 'type': 'car', 'class': 'traffic_light', 'direction': 'horizontal'}], 
                            # 'image': {'filename': 's01000560.jpg', 'imsize': [1280, 720]}}
                            anno = label['annotation']
                            size = label['image']['imsize']

                            ###make room for cls&box list per image
                            anno = self.filter_data(anno)

                            gt = np.zeros((len(anno), 5))
                            obj_cnt=0
                            cls_id = 0
                            rec = []

                            ###for each objects
                            for obj in anno:
                                category = obj['class']
                                if category == "traffic_light" and obj['attribute'][0]['others_arrow'] == "off":
                                    if obj['attribute'][0]['green'] == "on":
                                        cls_id=0
                                    elif obj['attribute'][0]['yellow'] == "on":
                                        cls_id=1
                                    elif obj['attribute'][0]['red'] == "on":
                                        cls_id=2
                                    elif obj['attribute'][0]['x_light'] == "on":
                                        cls_id=3
                                    elif obj['attribute'][0]['left_arrow'] == "on":
                                        cls_id=0
                                    else: cls_id=0
                                    x1 = float(obj['box'][0])
                                    y1 = float(obj['box'][1])
                                    x2 = float(obj['box'][2])
                                    y2 = float(obj['box'][3])
                                    box = convert((size[0], size[1]), (x1, x2, y1, y2))
                                    gt[obj_cnt][0] = cls_id
                                    gt[obj_cnt][1:] = list(box)
                                obj_cnt=obj_cnt+1

                                if category == "traffic_light":
                                        ###make rec class
                                    rec = [{
                                        'image': image_path,
                                        'label': gt,
                                        'mask': seg_dummy_path,
                                        'lane': seg_dummy_path
                                    }]
                                    gt_db += rec    

            print('total data length: ',len(gt_db))
            print('Train build finish')
            return gt_db
        if self.is_train!=True:
            for (root, dirs, files) in os.walk(val_dir):
                if len(files) > 0:
                    for file_name in tqdm(files):
                        ###if there is selected extension file
                        if os.path.splitext(file_name)[1] in possible_file_extension:
                            ### for each .json file
                            label_path = root + '/' + file_name
                            
                            # 경로에서 \를 모두 /로 바꿔줘야함
                            label_path = label_path.replace('\\', '/') # \는 \\로 나타내야함  
                            ###load json file to python code
                            with open(label_path, 'r') as f:
                                label = json.load(f)
                            ###build image path
                            label_path1, file_path1 = os.path.split(label_path)
                            label_path2, file_path2 = os.path.split(label_path1)
                            label_path2 = label_path2.replace('/label', '')

                            image_path = label_path2 + '/' + file_path1.replace('.json', '.jpg')

                            ###data example:: {'annotation': [{'light_count': '3', 'box': [407, 288, 449, 306], 
                            # 'attribute': [{'red': 'on', 'green': 'off', 'x_light': 'off', 
                            # 'others_arrow': 'off', 'yellow': 'off', 'left_arrow': 'off'}], 
                            # 'type': 'car', 'class': 'traffic_light', 'direction': 'horizontal'}], 
                            # 'image': {'filename': 's01000560.jpg', 'imsize': [1280, 720]}}
                            anno = label['annotation']
                            size = label['image']['imsize']

                            ###make room for cls&box list per image
                            anno = self.filter_data(anno)

                            gt = np.zeros((len(anno), 5))
                            obj_cnt=0
                            cls_id = 0
                            rec = []

                            ###for each objects
                            for obj in anno:
                                category = obj['class']
                                if category == "traffic_light" and obj['attribute'][0]['others_arrow'] == "off":
                                    if obj['attribute'][0]['green'] == "on":
                                        cls_id=0
                                    elif obj['attribute'][0]['yellow'] == "on":
                                        cls_id=1
                                    elif obj['attribute'][0]['red'] == "on":
                                        cls_id=2
                                    elif obj['attribute'][0]['x_light'] == "on":
                                        cls_id=3
                                    elif obj['attribute'][0]['left_arrow'] == "on":
                                        cls_id=0
                                    else: cls_id=0
                                    x1 = float(obj['box'][0])
                                    y1 = float(obj['box'][1])
                                    x2 = float(obj['box'][2])
                                    y2 = float(obj['box'][3])
                                    box = convert((size[0], size[1]), (x1, x2, y1, y2))
                                    gt[obj_cnt][0] = cls_id
                                    gt[obj_cnt][1:] = list(box)
                                obj_cnt=obj_cnt+1

                                if category == "traffic_light":
                                        ###make rec class
                                    rec = [{
                                        'image': image_path,
                                        'label': gt,
                                        'mask': seg_dummy_path,
                                        'lane': seg_dummy_path
                                    }]
                                    gt_db += rec    

            print('total data length: ',len(gt_db))
            print('eval build finish')
            return gt_db



    def filter_data(self, data):
        remain = []
        ###for each objects
        for obj in data:
            x1 = float(obj['box'][0])
            y1 = float(obj['box'][1])
            x2 = float(obj['box'][2])
            y2 = float(obj['box'][3])
            category = obj['class']
            ###only traffic_light class and bigger than n-pixel
            if category == "traffic_light" and (x2-x1) > 10 and (y2-y1) > 10:
                remain.append(obj)
        return remain

    def evaluate(self, cfg, preds, output_dir, *args, **kwargs):
        """  
        """
        pass
