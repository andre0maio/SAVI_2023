#!/usr/bin/env python3
import cv2

point_start = None
point_end = None

def mouseCallback(event,x,y,flags,param):
    global point_start, point_end

    if event == cv2.EVENT_LBUTTONDOWN:
        point_start = (x,y)
    elif event == cv2.EVENT_LBUTTONUP:
        point_end = (x,y)


def main():
    global point_start, point_end

    #Load images
    cap = cv2.VideoCapture('../../savi_23-24/Parte03/docs/traffic.mp4')

    while cap.isOpened():
        ret, frame = cap.read()

        if ret == True:
            break
        

    # Select Square
    cv2.imshow('Scene',frame)
    cv2.setMouseCallback('Scene',mouseCallback)

    while True:
        if point_start is not None and point_end is not None:
            print('point_start = ' + str(point_start))
            print('point_end = ' + str(point_end))
            break
        cv2.waitKey(20)

    cv2.rectangle(frame, (point_start[0], point_start[1]), (point_end[0], point_end[1]), (0,255,0), 4)

    cv2.imshow('Scene',frame)
    
    # Pause Program
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()



    