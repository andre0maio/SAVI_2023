#!/usr/bin/env python3
import cv2

start_point = None
end_point = None

def mouse_click(event, x,y, flags, param):
    global start_point,end_point

    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x,y)
        print('Start point:'+ str(start_point))
    elif event == cv2.EVENT_LBUTTONUP:  
        end_point = (x,y)
        print('End point:' + str(end_point))


def main():

    global start_point,end_point

    #Load images
    scene = cv2.imread('../savi_23-24/Parte02/images/scene.jpg')
    
    # Show Image
    cv2.imshow('Scene',scene)

    cv2.setMouseCallback('Scene', mouse_click)

    while True:
        if start_point is not None and end_point is not None:
            break
        cv2.waitKey(15)
    
    template = scene[start_point[1]:end_point[1],start_point[0]:end_point[0]]
    cv2.imshow('Template', template)

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
    
    # Pause Program
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()



    