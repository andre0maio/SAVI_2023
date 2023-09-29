#!/usr/bin/env python3
import cv2
import copy

def main():

    #Load images
    scene = cv2.imread('../savi_23-24/Parte02/images/scene.jpg')
    template  = cv2.imread('../savi_23-24/Parte02/images/wally.png')

    #Find Wally
    result = cv2.matchTemplate(scene,template,cv2.TM_CCOEFF_NORMED)
    
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    print(max_val)
    print(max_loc)

    #Draw rectangle
    h,w,_ = template.shape
    cv2.rectangle(scene,max_loc,(max_loc[0] + w,max_loc[1] + w), (0,255,0), 2)

    # Show Image
    cv2.imshow('Scene',scene)
    #cv2.imshow('wall',template)


    # Pause Program
    cv2.waitKey(0)

if __name__ == '__main__':
    main()