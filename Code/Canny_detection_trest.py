#coding: utf-8 #
import cv2
import numpy as np
import math
import time

def find_center(img):
    count=np.zeros(640)
    for j in range(640):
        for k in range(480):
            if img[k][j]==255:
                count[j]=count[j]+1
    mean=np.sum(count)/640
    Path_Dect_px_sum=0
    Path_Dect_fre_count=0
    for j in range(0, 640, 5):  # 采样像素点，5为步进，一共128个点
        if count[j] > mean:
            Path_Dect_px_sum = Path_Dect_px_sum + j  # 黑色像素点坐标值求和
            Path_Dect_fre_count = Path_Dect_fre_count + 1  # 黑色像素点个数求和
    center=Path_Dect_px_sum/Path_Dect_fre_count
    return center


start=time.time()
img=cv2.imread('C:\\Users\\15871\Documents\\TDPS\\Sunny_pic\\1111.png')
canny=cv2.Canny(img,180,380)
center=find_center(canny)
print(center)








