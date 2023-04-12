import numpy as np
import cv2
import torch
import argparse
import os
import time

from src import str2bool, draw_box


def predict(model, image) :
    res = []
    results = model(image)
    if len(results.xyxy[0]) > 0 :
        for i in range(len(results.xyxy[0])) :
            left, top, right, bottom, score =int(results.xyxy[0][i][0]),int(results.xyxy[0][i][1]),int(results.xyxy[0][i][2]),int(results.xyxy[0][i][3]), float(results.xyxy[0][i][4])
            res.append((left, top, right, bottom, score))
    return res




def main(opt) :
    
    PATH_VIDEO = opt.video
    IMAGE = opt.image
    SOURCE = opt.source
    SAVE_RESULTS = opt.save_results
    LOAD_HEIGHT = opt.load_height
    LOAD_WIDTH = opt.load_width
    PATH_SAVE = opt.path_save
    SHOW = opt.show
    CHECKPOINT_DIR = opt.checkpoint_dir

    os.makedirs(PATH_SAVE, exist_ok= True)
    os.makedirs(os.path.join(PATH_SAVE, SOURCE), exist_ok= True)

    model = torch.hub.load('./', 'custom', path=CHECKPOINT_DIR, source='local')
    image = None
    if SOURCE =='video' :
        name_video = PATH_VIDEO.split('/')[-1]
        cap = cv2.VideoCapture(PATH_VIDEO)
        fps = cap.get(cv2.CAP_PROP_FPS)
        video = cv2.VideoWriter(os.path.join(PATH_SAVE, SOURCE, name_video.split('.')[0]+'.avi'), 
                         cv2.VideoWriter_fourcc(*'XVID'),
                         10, (LOAD_WIDTH, LOAD_HEIGHT))

        while cap.isOpened():
            start_time = time.time()
            # Doc anh tu video
            _, frame = cap.read()
            if frame is None:
                break

            frame = cv2.resize(frame, (LOAD_WIDTH, LOAD_HEIGHT))
            results = predict(model, frame)
            if results is not None :
                print(results)
                frame = draw_box(frame, results)

            end_time = time.time()
            elapsed_time = end_time - start_time
            fps = 1 / elapsed_time
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            video.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('s'):
                break
            if SHOW :
                cv2.imshow('video', frame)
        cap.release()
        video.release()
        print('Done, save video: {}'.format(os.path.join(PATH_SAVE, SOURCE, name_video.split('.')[0]+'.avi')))
    else :
        image = cv2.imread(IMAGE)
        result = predict(model, image)
        image = draw_box(image, result)
        name_image = IMAGE.split('/')[-1]
        if SAVE_RESULTS:
            cv2.imwrite(os.path.join(PATH_SAVE, SOURCE, name_image), image)
            print('Done, save image : {}'.format(os.path.join(PATH_SAVE, SOURCE, name_image)))
        if SHOW :
            cv2.imshow('image', image)
        print(result)

def get_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', type= str, default= 'data/video_test/test.mov')
    parser.add_argument('--image', type= str, default= 'data/test/trung-bien-so-dep-nhieu-xe-o-to-doi-gia-vai-ty-dong-gay-sot.jpg')
    parser.add_argument('--source', type= str, default= 'video', choices= ['video', 'image'])
    parser.add_argument('--checkpoint_dir', type= str, default= 'checkpoints/best.pt')
    parser.add_argument('--save_results', type=str2bool, default= True)
    parser.add_argument('--load_height', type= int, default= 360)
    parser.add_argument('--load_width', type= int, default= 480)
    parser.add_argument('--path_save', type= str, default= 'save')
    parser.add_argument('--show', action='store_true', default= False)
    args = parser.parse_args()
    return args
if __name__ == '__main__' :
    opt = get_args_parser()
    main(opt= opt)
