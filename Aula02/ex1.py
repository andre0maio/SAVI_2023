import cv2
import copy

def main():
    #Load image
    image_ori = cv2.imread('../savi_23-24/Parte02/images/lake.jpg')
    #teste 2
    #Print Image type
    print(type(image_ori))
    print(image_ori.shape)

    # Nightfall
    h, w, nc = image_ori.shape
    image = copy.deepcopy(image_ori)

    reduction = 50
    for row in range(0,h):
        for col in range(0,w):
            image[row,col,0] = max(image[row,col,0] - reduction,0)
            image[row,col,1] = max(image[row,col,1] - reduction,0)
            image[row,col,2] = max(image[row,col,1] - reduction,0)

    #------------------------------------------------------#
    # Show Image
    #------------------------------------------------------#
    cv2.imshow('Original',image_ori)
    cv2.imshow('Nightfall',image)

    # Pause Program
    cv2.waitKey(0)

if __name__ == '__main__':
    main()