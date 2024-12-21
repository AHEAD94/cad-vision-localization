import os
import cv2


def load(video_file):
    print("[Video load]")
    if os.path.isfile(video_file):
        cap = cv2.VideoCapture(video_file)
        print("-file: " + video_file)
    else:
        print("-There is no file")

    return cap


def play(capture):
    if capture.isOpened():
        fps = capture.get(cv2.CAP_PROP_FPS)
        f_count = capture.get(cv2.CAP_PROP_FRAME_COUNT)
        f_width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        f_height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

        print('Frames per second: ', fps, 'FPS')
        print('Frames count: ', f_count)
        print('Frames width: ', f_width)
        print('Frames height: ', f_height)

    while capture.isOpened():
        ret, frame = capture.read()
        if ret:
            denominator = 4
            re_frame = cv2.resize(frame, (round(f_width / denominator), round(f_height / denominator)))
            cv2.imshow('result', re_frame)
            key = cv2.waitKey(10)

            if key == ord('q'):
                break
        else:
            break

    capture.release()
    cv2.destroyAllWindows()
