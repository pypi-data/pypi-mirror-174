import os
import mediapipe as mp
from collections import deque
import cv2
import numpy as np


def convert_bgr2gray(data):
    return np.stack([cv2.cvtColor(_, cv2.COLOR_BGR2GRAY) for _ in data], axis=0)


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

mouthchange = 0.001  # 嘴巴变化幅度
prelen = 6
raw_video_path='E:\\datasets\\raw_video'
new_save_filepath2='E:\\datasets\\processed_npz'
#new_save_filepath1=r"C:\Users\lhy\Desktop\file_for_lipreading1\dataset_for_3"
#new_save_filepath2=r"C:\Users\lhy\Desktop\file_for_lipreading1\npz_file_difference_3_crop2"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps=30
piexl=(640,480)

words=['fine','hello','morning','sorry','thank']
partitions= ['train','test','val']

def crop(image):
    with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        for face_landmarks in results.multi_face_landmarks:
            lid, lod = list(enumerate(face_landmarks.landmark))[61]
            rid, rod = list(enumerate(face_landmarks.landmark))[291]
            nose_id, nose = list(enumerate(face_landmarks.landmark))[6]

            center_x, center_y = (lod.x + rod.x) / 2, (lod.y + rod.y) / 2
            nose_x, nose_y = nose.x, nose.y

            h, w, c = image.shape
            squre = h * abs(nose_y - center_y)
            y0 = int(center_y * h - 0.9 * squre)
            y1 = int(center_y * h + 0.9 * squre)
            x0 = int(center_x * w - 0.9 * squre)
            x1 = int(center_x * w + 0.9 * squre)
            image = image[y0:y1, x0:x1]  # 裁剪坐标为[y0:y1, x0:x1]
            image = cv2.resize(image, (96, 96), interpolation=cv2.INTER_CUBIC)
            return image


def convert_bgr2gray(data):
    return np.stack([cv2.cvtColor(_, cv2.COLOR_BGR2GRAY) for _ in data], axis=0)

def save2npz(filename, data=None):
    assert data is not None, "data is {}".format(data)
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    np.savez_compressed(filename, data=data)

def get_changes(image,changes):
    with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = cv2.flip(image, 0)
        results = face_mesh.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmark = face_landmarks.landmark
                if len(changes) == prelen:
                    del changes[0]
                a = (landmark[13].x - landmark[14].x)
                b = (landmark[13].y - landmark[14].y)
                c = (landmark[62].x - landmark[292].x)
                d = (landmark[62].y - landmark[292].y)
                change = ((a ** 2 + b ** 2) / (c ** 2 + d ** 2)) ** (0.5)
                changes.append(change)
        return changes


def mouthOpen(changes):
    if(len(changes)<prelen):return False
    var = np.var(changes)
    if var >= mouthchange and len(changes) >= prelen:
        for change in changes:
            if change > 0.1:
                return True
    return False


def mouthClose(changes):
    var=np.var(changes)
    close_flag=True
    if len(changes)<prelen:
        close_flag= False
        print("prelen is not enough")
    elif var >=mouthchange  :#方差过大认为并没有闭嘴
        close_flag=False
    else:
        for consisten in changes:
            if consisten > 0.1:
                close_flag=False
    return close_flag

#本函数目的在于将视频或者从摄像头读取的文件，分割成说话的片段，并分割出嘴部，而后填充
#参数介绍，init_num指从指定的编号开始，word选择录入的词汇，paritition为选择录入的数据部分，
def preprocess_video_to_mouth(init_num,word,partition,src):

    changes = []
    frames = []
    preframes = []
    houframes = []
    if src==0:
        cap=cv2.VideoCapture(0)
    else:

        video_src = raw_video_path+'\\'+word+'\\'+ partition+'\\'+word+'.mp4'
        cap=cv2.VideoCapture(video_src)
        print(video_src)
    READ_FLAG=False
    save_num=init_num
    complete_one_sequence=False
    while cap.isOpened():

        ret, image_np = cap.read()
        if not ret:
            break
        changes = get_changes(image_np, changes)

        if mouthOpen(changes) and not READ_FLAG and len(changes)==prelen:
            READ_FLAG=True
            frames=[]
            print('mouth is open ')

        if READ_FLAG:
            frames.append(image_np)
            if len(houframes)==prelen:
                del houframes[0]
            houframes.append(image_np)
        else:
            if len(preframes)==5:
                del preframes[0]
            preframes.append(image_np)

        if READ_FLAG and mouthClose(changes):
                frames = preframes + frames
                if(len(frames)<20):#读取到的帧太少，认为并没有成功读取
                    frames=[]
                    houframes=[]
                else:
                    complete_one_sequence=True
                print('length of frames is ', len(frames))
        #至此应当已经完成对一个说话片段的截取


        if(complete_one_sequence):
            frames1 = deque(maxlen=60)

            if (save_num >= 10):
                str_save_num1 = '000' + str(save_num)
            else:
                str_save_num1 = '0000' + str(save_num)

            # file_path = new_save_filepath1 + '\\' + word + "\\" +partition+'\\'+word +'_'+str_save_num1+'.mp4'
            npz_path = new_save_filepath2 + '\\' + word + "\\" +partition+'\\'+word +'_'+str_save_num1+'.npz'
            # print('file_path is ',file_path)
            # out = cv2.VideoWriter(file_path, fourcc, fps, (96,96))
            for img in frames:
                cropped_img = crop(img)
                frames1.append(cropped_img)
                # cropped_img=img
                # out.write(cropped_img)
            print(len(frames1))
            np_array=np.array(frames1)
            data = convert_bgr2gray(np_array)
            save2npz(npz_path,data)
            READ_FLAG = False
            complete_one_sequence=False
            preframes = []
            houframes = []
            save_num=save_num+1

for i in range(0,5):
    for j in range(0,3):
        preprocess_video_to_mouth(1,words[i],partitions[j],1)
