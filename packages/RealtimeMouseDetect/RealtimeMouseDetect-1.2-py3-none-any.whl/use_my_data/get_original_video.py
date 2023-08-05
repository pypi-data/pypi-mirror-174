import cv2
import time
Start = False


root_filename = "E:\\datasets\\raw_video\\"

class GetOriginalVideo():

    def get_raw_video(word, patition):
        global Start
        cap = cv2.VideoCapture(0)
        while (cap.isOpened):
            ret, frame = cap.read()
            if ret:
                key = cv2.waitKey(1)
                if key == ord(' '):
                    if not Start:
                        fourcc = cv2.VideoWriter_fourcc(*'XVID')
                        filename = root_filename + word + '\\' + patition + '\\' + word + '.mp4'
                        out = cv2.VideoWriter(filename, fourcc, 30.0, (640, 480))
                        Start = True
                        print('录制开始' + word + "'s" + " " + patition)
                    else:
                        out.release()
                        print("录制结束")
                        Start = False

                if key == 27:
                    break
                if Start:
                    out.write(frame)
                cv2.imshow('frame', frame)
            else:
                break

        cap.release()
        cv2.destroyAllWindows()

    get_raw_video('hello', 'val')

# sorry，morning，thank，fine, hello
# train 50 test 10 val 10