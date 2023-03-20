video_time=3 # 视频时长
stride=10 # 切片视频间隔
frame_rate=30 # 抽帧频率

attributes = {'1':dict(aname='head', type=2, options={'0':'talk',
                   '1':'bow'},default_option_id="", anchor_id = 'FILE1_Z0_XY1'),

                   '2': dict(aname='body', type=2, options={'0':'stand',
                   '1':'sit', '2':'walk'}, default_option_id="", anchor_id='FILE1_Z0_XY1'),
                   
                  '3':dict(aname='limbs', type=2, options={'0':'hand up',
                   '1':'catch'},default_option_id="", anchor_id = 'FILE1_Z0_XY1')
                  }