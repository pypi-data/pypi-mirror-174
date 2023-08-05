import argparse
import json
from collections import deque
from pathlib import Path
import cv2
import numpy as np
import torch
from torchvision.transforms.functional import to_tensor
from lipreading.model import Lipreading
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

STD_SIZE = (256, 256)
STABLE_PNTS_IDS = [33, 36, 39, 42, 45]
START_IDX = 48
STOP_IDX = 68
CROP_WIDTH = CROP_HEIGHT = 96
MAX = 0
READ_FLAG = False
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
mouthchange = 0.001
prelen = 5

class TestForReal:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--config-path', type=Path,
                            default=Path(r'D:\python\TCN-csdntest\configs\lrw_resnet18_mstcn.json'))
        parser.add_argument('--model-path', type=Path, default=Path(
            r'D:\python\TCN-csdntest\train_logs\tcn\2022-10-27T19-35-16\ckpt.best.pth.tar'))
        parser.add_argument('--device', type=str, default='cuda')
        parser.add_argument('--queue-length', type=int, default=29)
        parser.add_argument('--allow-size-mismatch', default=True, action='store_true',
                            help='If True, allows to init from model with mismatching weight tensors. Useful to init from model with diff. number of classes')
        args = parser.parse_args()

        model = TestForReal.load_model(args.config_path)
        model.load_state_dict(torch.load(Path(args.model_path), map_location=args.device)['model_state_dict'])
        model = model.to(args.device)

        global max, READ_FLAG

        with Path(r'D:\python\TCN-csdntest\labels\5WordsSortedList.txt').open() as fp:
            vocab = fp.readlines()
        assert len(vocab) == 5

        queue = deque(maxlen=50)  # 用于装载最终数据

        changes = []
        frames = []
        len_of_frames = 0
        preframes = []
        houframes = []

        cap = cv2.VideoCapture(0)
        predicted = False
        text = []

        while cap.isOpened():
            ret, image_np = cap.read()
            if not ret:
                break

            # cv2.imshow('img',image_np)

            changes = TestForReal.get_changes(image_np, changes)

            # if(mouthOpen(changes)):
            #     cv2.imshow('open image ',image_np)
            # cv2.waitKey(30000)
            if TestForReal.mouthOpen(changes) and not READ_FLAG and len(changes) == prelen:
                READ_FLAG = True
                frames = []

            if READ_FLAG and len(frames) == 0:
                frames = preframes + frames

            if READ_FLAG:
                frames.append(image_np)
                if len(houframes) == prelen:
                    del houframes[0]
                houframes.append(image_np)
            else:
                if len(preframes) == 5:
                    del preframes[0]
                preframes.append(image_np)

            if READ_FLAG and TestForReal.mouthClose(changes):
                # frames=preframes+frames
                # frames=frames+houframes
                # print(len(frames))
                len_of_frames = len(frames)
                print('length of frames is ', len(frames))
                # frames=reframe(frames)

                for img in frames:
                    cropped_img = TestForReal.crop(img)
                    # cv2.imshow('First cropped_img is ', cropped_img)
                    # cv2.waitKey(0)

                    patch_torch = to_tensor(cv2.cvtColor(cropped_img, cv2.COLOR_RGB2GRAY)).to(args.device)
                    queue.append(patch_torch)
                    READ_FLAG = False
                preframes = []
                houframes = []

            if len(queue) >= args.queue_length:
                with torch.no_grad():
                    model_input = torch.stack(list(queue), dim=1).unsqueeze(0)
                    logits = model(model_input, lengths=[len_of_frames])
                    print('logits is ', logits)
                    probs = torch.nn.functional.softmax(logits, dim=-1)

                    probs = probs[0].detach().cpu().numpy()

                top = np.argmax(probs)
                print('prediction  is  ', vocab[top])
                predicted = True
                text = 'prediction is ' + vocab[top]
                len_of_frames = 0
                queue.clear()
            if predicted:
                cv2.putText(image_np, text, (40, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 1, 4)

                cv2.namedWindow('img')
                cv2.imshow('img', image_np)

            cv2.namedWindow('img')
            cv2.imshow('img', image_np)
            key = cv2.waitKey(1)
            if key in {27, ord('q')}:  # 27 is Esc
                break
            elif key == ord(' '):
                cv2.waitKey(0)

        cv2.destroyAllWindows()

    def crop(image):
        with mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
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

    def mouthOpen(changes):
        var = np.var(changes)
        if var >= mouthchange and len(changes) >= prelen:
            for change in changes:
                if change > 0.1:
                    return True
        return False


    def get_changes(image, changes):
        with mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as face_mesh:

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(image)
            image.flags.writeable = True

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    landmark = face_landmarks.landmark
                    if len(changes) == prelen:
                        del changes[0]
                    a = (landmark[13].x - landmark[14].x)
                    b = (landmark[13].y - landmark[14].y)
                    c = (landmark[62].x - landmark[292].x)
                    d = (landmark[62].y - landmark[292].y)
                    ##### 这个计算嘴部变换的指标是否效果好？
                    change = ((a ** 2 + b ** 2) / (c ** 2 + d ** 2)) ** (0.5)

                    changes.append(change)
            return changes

    def VideoCapture(*args, **kwargs):
        cap = cv2.VideoCapture(*args, **kwargs)
        try:
            yield cap
        finally:
            cap.release()

    def load_model(config_path: Path):
        with config_path.open() as fp:
            config = json.load(fp)
        tcn_options = {
            'num_layers': config['tcn_num_layers'],
            'kernel_size': config['tcn_kernel_size'],
            'dropout': config['tcn_dropout'],
            'dwpw': config['tcn_dwpw'],
            'width_mult': config['tcn_width_mult'],
        }
        return Lipreading(
            num_classes=5,
            tcn_options=tcn_options,
            backbone_type=config['backbone_type'],
            relu_type=config['relu_type'],
            width_mult=config['width_mult'],
            extract_feats=False,
        )

    def mouthClose(changes):
        var = np.var(changes)
        close_flag = True
        if len(changes) < prelen:
            close_flag = False
            print("prelen is not enough")
        elif var >= mouthchange:  # 方差过大认为并没有闭嘴
            close_flag = False
        else:
            for change in changes:
                if change > 0.1:
                    close_flag = False
        return close_flag

    def judge_out_of_range(proportion, deque):
        length = len(deque)
        Flag = True
        for i in range(0, length):
            if (proportion > deque[i] - 0.1):
                Flag = False
        return Flag

    def reframe(deque):
        total_frame = len(deque)
        delta = total_frame / 35
        deque1 = []
        for i in range(0, 35):
            deque1.append(deque[int(i * delta)])
        return deque1


if __name__ == '__main__':
    test = TestForReal()  # 实时检测