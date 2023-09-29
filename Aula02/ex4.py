#!/usr/bin/env python3
import cv2
import numpy as np

def main():
    #Load images
    scene = cv2.imread('../savi_23-24/Parte02/images/scene.jpg')
    scene_gray = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)
    scene_gray_RGB = np.stack((scene_gray,)*3, axis = -1) 

    template  = cv2.imread('../savi_23-24/Parte02/images/wally.png')

    #Find Wally
    result = cv2.matchTemplate(scene,template,cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)
    print('Match location: ' + str(max_loc))

    #Merge images (Option 1)
    h,w,_ = template.shape
    final_1 = scene_gray_RGB
    final_1[max_loc[1]:max_loc[1] + h,max_loc[0]:max_loc[0] + w] = scene[max_loc[1]:max_loc[1] + h,max_loc[0]:max_loc[0] + w]
    #cv2.imshow('Final',final_1)
    
    #Merge images (Option 2)
    mask = np.zeros(scene.shape[:2], dtype="uint8")
    mask[max_loc[1]:max_loc[1] + h,max_loc[0]:max_loc[0] + w] = 255
    mask = cv2.bitwise_and(scene, scene, mask=mask)
    final_2 = cv2.add(scene_gray_RGB,mask)
    cv2.imshow('Final',final_2)

    

    #h,w,_ = template.shape
    #mask[max_loc[1]:max_loc[1] + h,max_loc[0]:max_loc[0] + w] = scene_gray_RGB

    #print(scene_gray_RGB.shape)
    #

    #Create Mask
    #mask = np.zeros(scene.shape[:2], dtype="uint8")
    #masked = cv2.bitwise_and(scene, scene, mask=mask)
    #cv2.imshow('masked',masked)

    #final_image = cv2.bitwise_and(scene, scene_gray_RGB)


    #gray_image = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)
    #gray_image[max_loc[1]:max_loc[1] + h,max_loc[0]:max_loc[0] + w] = template

    #Draw rectangle
    
    # Show Image
    #cv2.imshow('gray_image',gray_image)
    #cv2.imshow('wall',template)


    # Pause Program
    cv2.waitKey(0)



if __name__ == '__main__':
    main()



    