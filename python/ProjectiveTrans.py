## Import library
import numpy as np
import cv2
from PIL import Image
import tkinter
from tkinter import filedialog

## Function to get contour of the picture
def getContour(event, x, y, flg, params):
    raw_img = params["img"]
    wname = params["wname"]
    cor_list = params["cor_list"]
    cor_num=params["cor_num"]

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(cor_list) < cor_num:
            cor_list.append([x, y])

    img = raw_img.copy()
    ## Show lines of the cousor
    h, w = img.shape[0], img.shape[1]
    cv2.line(img, (x, 0), (x, h), (255, 0, 0), 1)
    cv2.line(img, (0, y), (w, y), (255, 0, 0), 1)

    ## Show points and lines of selected contours
    for i in range(len(cor_list)):
        cv2.circle(img, (cor_list[i][0], cor_list[i][1]), 3, (0, 0, 255), 3)
        if 0 < i:
            cv2.line(img, (cor_list[i][0], cor_list[i][1]),
                    (cor_list[i-1][0], cor_list[i-1][1]), (0, 255, 0), 2)
        if i == cor_num -1:
            cv2.line(img, (cor_list[i][0], cor_list[i][1]),
                    (cor_list[0][0], cor_list[0][1]), (0, 255, 0), 2)
    if 0 < len(cor_list) < cor_num:
        cv2.line(img, (x, y), (cor_list[len(cor_list)-1][0], cor_list[len(cor_list)-1][1]), (0, 255, 0), 2)

    cv2.imshow(wname, img)

## main function
def main():
    ## Get path of target picture
    img_path = tkinter.filedialog.askopenfilename()
    src_img = Image.open(img_path)
    src_img = np.array(src_img)

    ## reshape picture
    h, w = src_img.shape[0], src_img.shape[1]
    ratio = 800 / w
    img = cv2.resize(src_img, None, None, ratio, ratio)

    ## set parameters
    wname = "ProjectiveTrans"
    cor_num = 4
    cor_list = []
    params = {
        "img": img,
        "wname": wname,  
        "cor_list": cor_list,
        "cor_num": cor_num,
    }

    ## show image and get contours
    cv2.namedWindow(wname)
    cv2.setMouseCallback(wname, getContour, params)
    cv2.imshow(wname, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    ## perspective transform
    src = np.float32(cor_list) / ratio
    o_width = int(np.linalg.norm(src[1] - src[0]))
    o_height = int(np.linalg.norm(src[3] - src[0]))
    dst = np.float32([[0, 0], [o_width, 0], [o_width, o_height], [0, o_height]])

    M = cv2.getPerspectiveTransform(src, dst)
    out_img = cv2.warpPerspective(src_img, M, (o_width, o_height))

    ## output image
    out_name = tkinter.filedialog.asksaveasfilename()
    cv2.imwrite(out_name, out_img)


if __name__ == "__main__":
    main()

