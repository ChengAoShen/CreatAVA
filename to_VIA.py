import os
import pickle
import json
import cv2
from collections import defaultdict

from via3_tool import Via3Json
from setting import attributes,yolo_data_dir,key_frames_dir,AVA_dic_path,ID_path


def YOLO_to_AVA(labelDir, PKL_path,ID_path, show=False):
    """将YOLO的标注转化成AVA的标注

    Args:
        labelDir (_type_): 标签文件的root文件夹
        PKL_path (_type_): 保存的pkl文件的路径
        showPkl (bool, optional): 是否对于转换后的字典进行展示.
    """
    results_dict = {}
    id_frame=[]
    # 因为文件夹中没有子文件夹，因此只需要遍历一次
    for root, dirs, files in os.walk(labelDir):
        if root == labelDir:
            # 排序，防止10排在1的前面
            files.sort(key=lambda arr: (int(arr[:-7]), int(arr[3:-4])))
            for name in files:
                temp_file_name = name.split("_")[0]
                temp_video_ID = name.split("_")[1].split('.')[0]
                temp_video_ID = int(temp_video_ID)
                temp_video_ID = str(int((temp_video_ID-1)/30)) # 计算秒数
                temp_video_ID = temp_video_ID.zfill(4)  # 填充4位
                key = temp_file_name + ',' + temp_video_ID # 拼接得到key

                # 读取yolov中的信息
                with open(os.path.join(root, name), 'r') as temp_txt:
                    temp_data_txt = temp_txt.readlines()

                results = []
                for i in temp_data_txt:
                    j = i.split(' ')
                    if j[0] == '0': # 只保留第一个的标注
                        # 由于yolov5的检测结果是 xywh
                        # 要将xywh转化成xyxy
                        y = j
                        y[1] = float(j[1]) - float(j[3]) / 2  # top left x
                        y[2] = float(j[2]) - float(j[4]) / 2  # top left y
                        y[3] = float(j[1]) + float(j[3])  # bottom right x
                        y[4] = float(j[2]) + float(j[4])  # bottom right y
                        results.append([y[1], y[2], y[3], y[4], y[5]])
                        id_frame.append((temp_file_name, int(temp_video_ID),y[1],y[6][:-1]))
                results_dict[key] = results

    if show:
        for i in results_dict:
            print(i, results_dict[i])
        print(id_frame)

    with open(PKL_path, "wb") as pklfile:
        pickle.dump(results_dict, pklfile)

    with open(ID_path, "wb") as idfile:
        pickle.dump(id_frame, idfile)

def create_via_json(pkl_path, frames_path):
    f = open(pkl_path, 'rb')
    info = pickle.load(f, encoding='iso-8859-1')

    # len_x与循环的作用主要是获取每个视频下视频帧的数量
    dirname = ''
    len_x = {}
    for i in info:
        temp_dirname = i.split(',')[0]
        if dirname == temp_dirname:
            # 正在循环一个视频文件里的东西
            len_x[dirname] = len_x[dirname] + 1
        else:
            # 进入下一个视频文件
            dirname = temp_dirname
            len_x[dirname] = 1

    dirname = ''
    for i in info:
        temp_dirname = i.split(',')[0]
        if dirname == temp_dirname:
            # 正在循环一个视频文件里的东西

            image_id = image_id + 1
            files_img_num = int(i.split(',')[1])

            # 如果当前出现 files_img_num - 1 与 image_id 不相等的情况
            # 那就代表当前 image_id对应的图片中没有人
            # 那么via的标注记为空
            if files_img_num - 1 != image_id:
                files_dict[str(image_id)] = dict(fname=i.split(
                    ',')[0] + '_' + (str((image_id+1)*30+1)).zfill(6) + '.jpg', type=2)
                via3.dumpFiles(files_dict)
                if files_img_num - 1 != image_id:
                    while image_id < files_img_num - 1:
                        image_id = image_id + 1
                        files_dict[str(image_id)] = dict(fname=i.split(
                            ',')[0] + '_' + (str((image_id+1)*30+1)).zfill(6) + '.jpg', type=2)
                        via3.dumpFiles(files_dict)
                        print("middle loss", image_id, "   ", num_images)
                        print("files_img_num-1", files_img_num -
                              1, " image_id", image_id)
                        len_x[dirname] = len_x[dirname] + 1
                        continue

            files_dict[str(image_id)] = dict(fname=i.split(
                ',')[0] + '_' + (str(int(i.split(',')[1])*30+1)).zfill(6) + '.jpg', type=2)

            for vid, result in enumerate(info[i], 1):
                xyxy = result
                xyxy[0] = img_W*xyxy[0]
                xyxy[2] = img_W*xyxy[2]
                xyxy[1] = img_H*xyxy[1]
                xyxy[3] = img_H*xyxy[3]
                temp_w = xyxy[2] - xyxy[0]
                temp_h = xyxy[3] - xyxy[1]

                metadata_dict = dict(vid=str(image_id),
                                     xy=[2, float(xyxy[0]), float(
                                         xyxy[1]), float(temp_w), float(temp_h)],
                                     av={'1': '0'})

                metadatas_dict['image{}_{}'.format(
                    image_id, vid)] = metadata_dict

            via3.dumpFiles(files_dict)
            via3.dumpMetedatas(metadatas_dict)

            print("OK ", image_id, "   ", num_images)
            if image_id == num_images:
                views_dict = {}
                for i, vid in enumerate(vid_list, 1):
                    views_dict[vid] = defaultdict(list)
                    views_dict[vid]['fid_list'].append(str(i))
                via3.dumpViews(views_dict)
                via3.dempJsonSave()
                print("save")

            # 当一个视频的图片的标注信息遍历完后：image_id == len_x[dirname]，
            # 但是视频的标注信息长度仍然小于视频实际图片长度
            # 即视频图片最后几张都是没有人，导致视频标注信息最后几张没有
            # 那么就执行下面的语句，给最后几张图片添加空的标注信息
            print("image_id", image_id,
                  " len_x[dirname]", len_x[dirname], " num_images", num_images)
            if image_id == len_x[dirname] and image_id < num_images:
                while image_id < num_images:
                    image_id = image_id + 1
                    files_dict[str(image_id)] = dict(fname=i.split(
                        ',')[0] + '_' + (str((image_id+1)*30+1)).zfill(6) + '.jpg', type=2)
                    via3.dumpFiles(files_dict)
                print("end loss", image_id, "   ", num_images)
                views_dict = {}
                for i, vid in enumerate(vid_list, 1):
                    views_dict[vid] = defaultdict(list)
                    views_dict[vid]['fid_list'].append(str(i))
                via3.dumpViews(views_dict)
                via3.dempJsonSave()
                print("save")
        else:
            # 进入下一个视频文件
            dirname = temp_dirname
            print("dirname", dirname)

            # 为每一个视频文件创建一个via的json文件
            temp_json_path = frames_path + '/'+dirname + '/' + dirname + '_proposal.json'

            # 获取视频有多少个帧
            for root, dirs, files in os.walk(frames_path + "/" + dirname, topdown=False):
                if "ipynb_checkpoints" in root:
                    continue
                num_images = 0
                for file in files:
                    if '.jpg' in file:
                        num_images = num_images + 1
                        temp_img_path = frames_path + "/"+dirname + '/' + file  # 图片路径
                        img = cv2.imread(temp_img_path)  # 读取图片信息
                        sp = img.shape  # [高|宽|像素值由三种原色构成]
                        img_H = sp[0]
                        img_W = sp[1]

            via3 = Via3Json(temp_json_path, mode='dump')
            vid_list = list(map(str, range(1, num_images+1)))
            via3.dumpPrejects(vid_list)
            via3.dumpConfigs()
            via3.dumpAttributes(attributes)

            files_dict,  metadatas_dict = {}, {}
            # 图片ID从1开始计算
            image_id = 1
            files_dict[str(image_id)] = dict(fname=i.split(
                ',')[0] + '_' + (str(int(i.split(',')[1])*30+1)).zfill(6) + '.jpg', type=2)

            for vid, result in enumerate(info[i], 1):
                xyxy = result
                xyxy[0] = img_W*xyxy[0]
                xyxy[2] = img_W*xyxy[2]
                xyxy[1] = img_H*xyxy[1]
                xyxy[3] = img_H*xyxy[3]
                temp_w = xyxy[2] - xyxy[0]
                temp_h = xyxy[3] - xyxy[1]

                metadata_dict = dict(vid=str(image_id),
                                     xy=[2, float(xyxy[0]), float(
                                         xyxy[1]), float(temp_w), float(temp_h)],
                                     av={'1': '0'})
                print(metadata_dict)
                metadatas_dict['image{}_{}'.format(
                    image_id, vid)] = metadata_dict

            via3.dumpFiles(files_dict)
            via3.dumpMetedatas(metadatas_dict)


def delete_default(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            # via的json标注文件以_proposal.json结尾
            if "_proposal.json" in file:
                jsonPath = root+'/'+file
                # 读取标注文件
                with open(jsonPath, encoding='utf-8') as f:
                    line = f.readline()
                    viaJson = json.loads(line)
                    for metadata in viaJson['metadata']:
                        # 对标注文件中所有av进行修改，av就是当前选中的标注值
                        # 下面的1，2，3代表3种多选，如头部、身体、四肢三个部位的行为
                        # 这里的值应动态获取，时间关系，先固定成这样
                        viaJson['metadata'][metadata]["av"] = {
                            '1': '', '2': '', '3': ''}
                    # 修改后的文件名
                    newName = file.split(".")[0]+'.json'
                    with open(root+'/'+newName, 'w') as f2:
                        f2.write(json.dumps(viaJson))


if __name__ == "__main__":
    YOLO_to_AVA(yolo_data_dir+'/track/labels', AVA_dic_path, ID_path,True)
    create_via_json(AVA_dic_path, key_frames_dir)
    delete_default(key_frames_dir)
