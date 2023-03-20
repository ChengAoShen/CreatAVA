from ultralytics import YOLO

def YOLO_train(data_yaml, epochs):
    model = YOLO('yolov8s.yaml')
    model = YOLO('yolov8s.pt')
    model.train(data=data_yaml, epochs=epochs)

def YOLO_predict(img_dir,weight, save=False, save_txt=True, save_conf=True):
    model = YOLO(weight)
    model(img_dir, save=save, save_txt=save_txt, save_conf=save_conf)

def YOLO_track(source, weight, show=False, save=False, save_txt=False, save_conf=False):
    model = YOLO(weight) 
    model.track(source=source, show=show, save=save, save_txt=save_txt, save_conf=save_conf) 


if __name__ == '__main__':
    #! 似乎可以直接使用YOLO_track同时得到bbox和编号
    YOLO_track("./data/key_frames_all", 'yolov8s.pt',show=True, save=True,save_txt=True, save_conf=True)
