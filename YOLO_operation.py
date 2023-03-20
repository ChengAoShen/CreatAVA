from ultralytics import YOLO
from setting import key_frames_dir_all

from setting import yolo_data_dir,weight_path

def YOLO_train(data_yaml, epochs):
    model = YOLO("yolov8s.pt")
    model.train(data=data_yaml, 
                project = yolo_data_dir,
                epochs=epochs)

def YOLO_track(source, weight, show=False, save=False, save_txt=False, save_conf=False):
    model = YOLO(weight) 
    model.track(source=source,
                project = yolo_data_dir,
                show=show, save=save, save_txt=save_txt, save_conf=save_conf) 

if __name__ == '__main__':
    YOLO_track(key_frames_dir_all, weight_path,show=False, save=False,save_txt=True, save_conf=True)
