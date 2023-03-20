import os

from setting import attributes,save_dir

def build_action_list(save_dir):
    id=1
    for l in attributes.items():
        for _,action in l[1]["options"].items():
            with open(os.path.join(save_dir,"action_list.pbtxt"),"a") as f:
                f.write(f'item{{\n  name: {action}\n  id: {id}\n}}\n')
            id+=1

def build_included_timestamps(save_dir):
    ...

def build_train_excluded_timestamps(save_dir):
    with open(os.path.join(save_dir,"./train_excluded_timestamps.csv"),"w") as f:
        ...# TODO: write excluded timestamps


if __name__=="__main__":
    build_action_list(save_dir)
    build_train_excluded_timestamps(save_dir)
