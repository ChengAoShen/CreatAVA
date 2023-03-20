import os
import shutil

from setting import video_time, stride, frame_rate

def fragment_videos(in_data_dir, out_data_dir, stride=10, video_time=3):
    '''
    将指定目录中的视频按固定时间间隔切割为多个片段

    Args:
    in_data_dir (str): 输入视频所在目录路径
    out_data_dir (str): 输出视频所在目录路径
    strid (int): 切割时间间隔，默认为10秒
    video_time (int): 每个视频片段时长，默认为3秒
    '''
    # 创建输出目录
    if not os.path.exists(out_data_dir):
        print(out_data_dir + " doesn't exist. Creating it.")
        os.makedirs(out_data_dir)

    index_fragment = 1
    for video_name in os.listdir(in_data_dir):
        if video_name.startswith('.'):
            continue
        video_duration = int(float(os.popen(f'ffprobe -v error -show_entries format=duration \
                -of default=noprint_wrappers=1:nokey=1 "{in_data_dir}/{video_name}"').read()[:-1]))
        for t in range(0, video_duration, stride):
            os.system(f'ffmpeg -ss {t} -t {video_time} -y -i "{in_data_dir}/{video_name}" \
                "{out_data_dir}/{index_fragment}.mp4"')
            index_fragment += 1


def extract_frames(in_data_dir, out_data_dir, frame_rate=30):
    """
    从给定的视频文件夹in_data_dir中提取视频帧，存储为JPG格式图片到out_data_dir中。

    Args:
    in_data_dir:str，输入视频文件夹路径。
    out_data_dir:str，输出帧文件夹路径。
    frame_rate:int，帧率，默认为30。
    """
    if not os.path.exists(out_data_dir):
        print(out_data_dir + " doesn't exist. Creating it.")
        os.makedirs(out_data_dir)

    for video in os.listdir(in_data_dir):
        if not video.startswith('.'):
            video_name = os.path.splitext(os.path.basename(video))[0]
            print(video_name)
            out_video_dir = os.path.join(out_data_dir, video_name)
            os.makedirs(out_video_dir, exist_ok=True)
            out_name = os.path.join(out_video_dir, f"{video_name}_%06d.jpg")
            os.system(
                f"ffmpeg -i '{os.path.join(in_data_dir, video)}' -r {frame_rate} -q:v 1 '{out_name}'")


def save_key_frames(frames_dir,seconds,start=0,all=False):
    """从frames文件夹中选择指定的图片,按照每秒一帧的频率

    Args:
        frames_dir (_type_): frames文件夹的路径
        seconds (_type_): 视频的时长
        start (_type_): 视频的起始时间
        all (bool, optional): 判断是否将所有图片整合. Defaults to False.
    """
    frames = range(start, seconds+1)

    # num_frames 存放对应图片的编号
    num_frames = []

    for i in frames:
        num_frames.append(i*30+1)

    #遍历./frames
    for filepath,dirnames,filenames in os.walk(frames_dir):
        if all:
            #在key_frames_all下创建对应的目录文件夹
            if len(filenames)!=0:
                temp_name = filepath.split('/')[-1]
                path_temp_name = './data/key_frames_all/'+temp_name
            if not os.path.exists('./data/key_frames_all'):
                os.makedirs('./data/key_frames_all')
        else:
            #在key_frames下创建对应的目录文件夹
            if len(filenames)!=0:
                temp_name = filepath.split('/')[-1]
                path_temp_name = './data/key_frames/'+temp_name
                if not os.path.exists(path_temp_name):
                    os.makedirs(path_temp_name)

        filenames=sorted(filenames)
        #找到指定的图片，然后移动到key_frames中对应的文件夹下
        for filename in filenames:
            if "checkpoint" in filename:
                continue
            if "Store" in filename:
                continue
            temp_num = filename.split('_')[1]
            temp_num = temp_num.split('.')[0]
            temp_num = int(temp_num)
            if temp_num in num_frames:
                temp_num = str(temp_num)
                temp_num = temp_num.zfill(6)
                temp_num = temp_name + "_" + temp_num + ".jpg"

                srcfile = filepath + '/' + temp_num
                if all:
                    dstpath = './data/key_frames_all/' + temp_num
                else:
                    dstpath = path_temp_name + '/' + temp_num
                # 复制文件
                shutil.copy(srcfile, dstpath)

def build_YOLO_data(in_data_dir, out_data_dir, interval):
    if not os.path.exists(out_data_dir):
        print(out_data_dir + " doesn't exist. Creating it.")
        os.makedirs(out_data_dir)

    index=0
    for video in os.listdir(in_data_dir):
        if not video.startswith('.'):
            video_name = os.path.basename(video)
        # print(video_name)
        video_duration = int(float(os.popen(f'ffprobe -v error -show_entries format=duration \
                -of default=noprint_wrappers=1:nokey=1 "{in_data_dir}/{video_name}"').read()[:-1]))
        # print(video_duration)

        for t in range(0, video_duration, interval):
            out_name = os.path.join(out_data_dir, f"{index}.jpg")
            print(out_name)
            os.system(
                f"ffmpeg -ss {t} -i '{os.path.join(in_data_dir, video)}' -y -vframes 1 '{out_name}'")
            index+=1


if __name__ == "__main__":
    fragment_videos('./data/original_videos', './data/fragment_videos', stride=stride, video_time=video_time)
    extract_frames('./data/fragment_videos', './data/frames', frame_rate=frame_rate)
    save_key_frames('./data/frames',video_time)
    save_key_frames('./data/frames',video_time,all=True)

    # build_YOLO_data("./data/original_videos","./data/yolo_train_data",10)
