import argparse
import cv2
import numpy as np 
import datetime
def str2bool(v):
    """
    Converts string to bool type; enables command line 
    arguments in the format of '--arg1 true --arg2 false'
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def get_time():
    now = datetime.datetime.now()
    second, minute, hour=now.second, now.minute, now.hour
    day, month, year = now.day, now.month, now.year
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return ( second, minute, hour, day, month, year, dt_string)

def draw_box(image, boxs) :
    colors = [(np.random.randint(255),
                     np.random.randint(255),
                     np.random.randint(255)) for _ in range(10)]
    for i, (left, top, right, bottom, score) in enumerate(boxs) :
        cv2.rectangle(image, (left, top), ( right, bottom), color= colors[i], thickness= 2)
        cv2.putText(image, "{:.2f}".format(score), (left, top- 16), cv2.FONT_HERSHEY_SIMPLEX, fontScale= 0.8, color= colors[i], thickness= 1, lineType= cv2.LINE_AA)
        second, minute, hour, day, month, year, dt_string = get_time()
        cv2.putText(image, "{}".format(dt_string), (left, top- 4), cv2.FONT_HERSHEY_SIMPLEX, fontScale= 0.5, color= colors[i], thickness= 1, lineType= cv2.LINE_AA)

    return image

            