import numpy as np
import cv2
import time
import pyautogui
from directkeys import PressKey, ReleaseKey, W, A, S, D
from draw_lanes import draw_lanes
from grabscreen import grab_screen


def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    #cv2.imshow('window2', mask)
    return masked


def process_img(image):
    original_image = image
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=150, threshold2=295)
    processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)
    vertices = np.array([[10, 500], [10, 300],  [800, 300], [800, 500],
                         ], np.int32)
    processed_img = roi(processed_img, [vertices])
    lines = cv2.HoughLinesP(processed_img, 1, np.pi / 180, 180, 15, 10)
    m1 = 0
    m2 = 0
    try:
        l1, l2, m1, m2 = draw_lanes(original_image, lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0, 255, 0], 30)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0, 255, 0], 30)
    except Exception as e:
        print(str(e))
        pass
    try:
        for coords in lines:
            coords = coords[0]
            try:
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 0, 0], 3)


            except Exception as e:
                print(str(e))
    except Exception as e:
        pass

    return processed_img, original_image, m1, m2


def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)


def left():
    PressKey(A)
    ReleaseKey(W)
    ReleaseKey(D)
    ReleaseKey(A)


def right():
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)


def slow_ya_roll():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)


for i in list(range(4))[::-1]:
    print(i + 1)
    time.sleep(1)

last_time = time.time()
while True:
    screen = grab_screen(region=(0, 40, 800, 640))
    print('Frame took {} seconds'.format(time.time() - last_time))
    last_time = time.time()
    new_screen, original_image, m1, m2 = process_img(screen)
    cv2.imshow('window2', cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    #cv2.imshow('window1', new_screen)
    # if m1 < 0 and m2 < 0:
    #     right()
    # elif m1 > 0 and m2 > 0:
    #     left()
    # else:
    #     straight()
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break