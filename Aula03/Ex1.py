#!/usr/bin/env python3
import cv2

def main():

    #Load images
    cap = cv2.VideoCapture('../savi_23-24/Parte03/docs/traffic.mp4')
    
    # Pause Program
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()



    