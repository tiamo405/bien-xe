# 1. Data
```
data __train __img1.jpg
    |        |__img1.txt
    |__val   __img1.jpg
    |        |__img1.txt
    |__coco.yaml
```
* coco.yaml
```
train: data/train  # train images (relative to 'path') 128 images
val: data/val  # val images (relative to 'path') 128 images
test:  # test images (optional)

# Classes
names:
  0: bienxe
```
* Dowload data

[GDrive - chua update](https://drive.google.com/drive/folders/1-2sdlLjvX52bU_tQb-lOvHP3cWblVdsB?usp=share_link)
# 2. Train
```
bash train.sh
```
or
```
python train.py --data coco.yaml --epochs 100 ----weights '' --cfg yolov5n.yaml  --batch-size 16
```
# 3.Test
```
python demo.py --source video --video data/video_test/test.mov
                --source image --image data/test/trung-bien-so-dep-nhieu-xe-o-to-doi-gia-vai-ty-dong-gay-sot.jpg
```
# 4. Colab

