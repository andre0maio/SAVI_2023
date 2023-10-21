#!/usr/bin/env python3
import copy
import csv
import math
import time
from random import randint

import cv2
import numpy as np
from track import Detection,Track, computeIOU
from colorama import Fore, Back, Style



def main():
    #------------------------------
    # Initialization
    #------------------------------

    #Import video
    cap = cv2.VideoCapture('../../savi_23-24/Parte04/docs/OxfordTownCentre/TownCentreXVID.mp4')
    video_frame_number = 0

    # Create person detector
    detector_filename = './fullbody2.xml' 
    detector = cv2.CascadeClassifier(detector_filename)
    
    # Parameters
    tracks = []
    person_count = 0
    video_frame_number = 0

    iou_threshold = 0.3
    deactivate_threshold = 5.0 #segundos
    distance_threshold = 100


    #------------------------------
    # Execution
    #------------------------------
    while cap.isOpened():

        result, image_rgb = cap.read()
        # Stop when video ends
        if result is False:
            break

        # End video if 'q' key is pressed
        if cv2.waitKey(35) & 0xFF == ord('q') :
            break

        frame_stamp = round(float(cap.get(cv2.CAP_PROP_POS_MSEC))/1000,2)
        image_gui = copy.deepcopy(image_rgb)
        height, width, _ = image_gui.shape  

        #------------------------------
        # Detect Person using haar cascade classifier
        #------------------------------
        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
        haar_detections = detector.detectMultiScale(image_gray, scaleFactor=1.2, minNeighbors=4,
                                            minSize=(20, 40), flags=cv2.CASCADE_SCALE_IMAGE)

    
        #------------------------------
        # Create list of detections
        #------------------------------   
        detections = []
        detections_idx = 0
        for x,y,w,h in haar_detections:
            detections_id = str(video_frame_number) + '_' + str(detections_idx)
            detection = Detection(x, x+w, y, y+h, detections_id, frame_stamp)
            detections.append(detection)
            detections_idx += 1
        
        all_detections = copy.deepcopy(detections)

        # ------------------------------------------------------
        # Association Detection with tracks
        # ------------------------------------------------------
        idxs_detections_to_remove = []
        for idx_detection, detection in enumerate(detections):
            for track in tracks:

                # Check if track is active
                if not track.active:
                    continue

                # Calculate IOU
                iou_val = computeIOU(detection, track.detections[-1])
                if iou_val > iou_threshold:
                    track.update(detection)
                    idxs_detections_to_remove.append(idx_detection)                    
                    break
        
        idxs_detections_to_remove.reverse()
        for idx in idxs_detections_to_remove:
            del detections[idx]

        # --------------------------------------
        # Create new trackers
        # --------------------------------------
        for detection in detections:
            color = (randint(0,255), randint(0,255), randint(0,255))
            track = Track('T' + str(person_count),detection, color = color)
            tracks.append(track)
            person_count += 1

        # --------------------------------------
        # Deactivate tracks if last detection has been seen a long time ago
        # --------------------------------------
        for track in tracks:
            time_since_last_detection = frame_stamp - track.detections[-1].stamp
            if time_since_last_detection > deactivate_threshold:
                track.active = False

        #------------------------------
        # Visualization
        #------------------------------
        for detection in all_detections:
            detection.draw(image_gui, (255,0,0))

        # Draw list of tracks
        for track in tracks:
            if not track.active:
                continue
            track.draw(image_gui)

        if video_frame_number == 0:
            cv2.namedWindow('GUI',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('GUI', int(width/2), int(height/2))

        # Add frame number and time to top left corner
        cv2.putText(image_gui, 'Frame ' + str(video_frame_number) + ' Time ' + str(frame_stamp) + ' secs',
                    (10,40), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2, cv2.LINE_AA)

        cv2.imshow('GUI',image_gui)

        video_frame_number += 1
    
if __name__ == '__main__':
    main()