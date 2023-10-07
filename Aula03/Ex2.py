#!/usr/bin/env python3
import cv2
import copy
import numpy as np
import time



def main():

    frame_number = 0
    average = 134
    prev_average = 0
    threshold = 10.0
    n_cars = 0
    tic = 0

    #Define multiple roi's
    roi0 = {'point_start': (404, 276), 'point_end': (460, 422), 'average':130,
        'average_previous':130, 'tic':time.time(), 'n_cars': 0}
    roi1 = {'point_start': (536, 285), 'point_end': (639, 414), 'average':130,
        'average_previous':130, 'tic':time.time(), 'n_cars': 0}
    roi2 = {'point_start': (687, 362), 'point_end': (847, 515), 'average':130,
        'average_previous':130, 'tic':time.time(), 'n_cars': 0}
    roi3 = {'point_start': (799, 219), 'point_end': (934, 318), 'average':130,
        'average_previous':130, 'tic':time.time(), 'n_cars': 0}

    rois = [roi0,roi1,roi2,roi3]

    #Load images
    cap = cv2.VideoCapture('../../savi_23-24/Parte03/docs/traffic.mp4')

    while cap.isOpened():
        ret, image_rgb = cap.read()

        # End when video ends
        if ret is False:
            break

        # End video
        if cv2.waitKey(35) & 0xFF == ord('q') :
            break

        # Copy original video
        image_gui = copy.deepcopy(image_rgb)

        #Convert frame to gray
        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)

        for roi in rois:

            point_start = roi['point_start']
            point_end = roi['point_end']

            #Create ROI
            image_roi = image_gray[point_start[1]:point_end[1], point_start[0]:point_end[0]]
            
            #Calculate average pixel density
            roi['prev_average']  = roi['average']
            roi['average'] = np.mean(image_roi)

            blackout_thrsh = 1.0
            time_since_tic = time.time() - roi['tic']

            if (abs(roi['average'] - roi['prev_average']) > threshold) and (time_since_tic > blackout_thrsh):
                roi['tic'] = time.time()
                roi['n_cars'] = roi['n_cars'] + 1




        # Visualization
        image_gui = cv2.putText(image_gui, 'Frame ' + str(frame_number), (500, 20), cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, (255,255,0), 2, cv2.LINE_AA)
        
        for roi in rois:
            
            point_start = roi['point_start']
            point_end = roi['point_end']

            cv2.rectangle(image_gui, (point_start[0], point_start[1]), (point_end[0], point_end[1]), (0,255,0), 4)
            
            image_gui = cv2.putText(image_gui, 'Avg: ' + str(round(roi['average'])), (point_start[0],point_start[1]-5) , cv2.FONT_HERSHEY_SIMPLEX, 
                            0.7, (255,255,0), 2, cv2.LINE_AA)      
            image_gui = cv2.putText(image_gui, 'N_cars: ' + str(roi['n_cars']), (point_start[0],point_end[1]+20) , cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, (255,255,0), 2, cv2.LINE_AA)   
        
        
        cv2.imshow('Video',image_gui)


        frame_number = frame_number + 1


if __name__ == '__main__':
    main()



    