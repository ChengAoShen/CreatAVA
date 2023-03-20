video_time=3 # 视频时长
stride=100 # 切片视频间隔
frame_rate=30 # 抽帧频率

attributes = {'1':dict(aname='head', type=2, options={'0':'talk',
                   '1':'bow'},default_option_id="", anchor_id = 'FILE1_Z0_XY1'),

                   '2': dict(aname='body', type=2, options={'0':'stand',
                   '1':'sit', '2':'walk'}, default_option_id="", anchor_id='FILE1_Z0_XY1'),
                   
                  '3':dict(aname='limbs', type=2, options={'0':'hand up',
                   '1':'catch'},default_option_id="", anchor_id = 'FILE1_Z0_XY1')
                  }

# path setting
original_video_dir = "./data/original_videos" # raw video path
fragment_video_dir = "./data/fragment_videos" # cutted video path
frames_dir = "./data/frames" # all frames path
key_frames_dir = "./data/key_frames" # the path to key frames, this path will have two folder
key_frames_dir_all = key_frames_dir+"_all"
yolo_without_label_dir = "./data/yolo_without_label" # the path to save yolo label dataset

yolo_labeled_dir=""
yolo_data_dir = "./runs" # 运行YOLOv8保存的数据集路径
weight_path = "./yolov8s.pt" # 进入最后需要修改

AVA_dic_path = "./data/AVA.pkl"
ID_path = "./data/id.pkl"

train_withoutID_csv='./train_without_personID.csv'


save_dir="./dataset" # 数据集最终保存路径
train_csv_path=save_dir+"train_with_personID.csv"
