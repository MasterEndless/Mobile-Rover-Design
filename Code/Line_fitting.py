#coding: utf-8 #
import cv2
import numpy as np
import math
import skimage as sk
import random

#Line fitting Function
def Least_squares(x,y):
    x=np.array(x)
    y=np.array(y)
    x_ = x.mean()
    y_ = y.mean()
    m = np.zeros(1)
    n = np.zeros(1)
    k = np.zeros(1)
    p = np.zeros(1)
    for i in np.arange(50):
        k = (x[i]-x_)* (y[i]-y_)
        m += k
        p = np.square( x[i]-x_ )
        n = n + p
    k = m/n
    b = y_ - k* x_
    return k,b



'''
def linefit(x,y):
     N = float(len(x))
     sx, sy, sxx, syy, sxy = 0, 0, 0, 0, 0
     for i in range(0, int(N)):
          sx += x[i]
          sy += y[i]
          sxx += x[i] * x[i]
          syy += y[i] * y[i]
          sxy += x[i] * y[i]
          a = (0.00000001+(sy * sx / N - sxy)) / ((sx * sx / N - sxx)+0.000001)
          b = (sy - a * sx) / N
          r = abs(sy * sx / N - sxy) / math.sqrt((sxx - sx * sx / N) * (syy - sy * sy / N))
     return a,b,r
'''
#Determine the line equation
def RANSAC(x,y):
     n=2
     len_array=range(len(x))
     k=50  #iteration times
     t=25  #threshold of distance
     d=300 #number of points
     fit_kbr=[]
     for i in range(k):
          points_list_x = []
          points_list_y = []
          index1=random.choice(len_array)
          index2=random.choice(len_array)
          x_coor1 = x[index1]
          y_coor1 = y[index1]
          x_coor2 = x[index2]
          y_coor2 = y[index2]
          for index in len_array:
               if x_coor2-x_coor1!=0:
                    y_test=(y_coor2-y_coor1)/(x_coor2-x_coor1)*(x[index]-x_coor1)+y_coor1
                    if abs(y_test-y[index])<25:
                         points_list_x.append(x[index])
                         points_list_y.append(y[index])
          if len(points_list_x)> 300:
               k,b=Least_squares(points_list_x,points_list_y)
               sum=0
               for i in range(len(points_list_x)):
                    sum=sum+(k*points_list_x[i]+b-points_list_y[i])**2
               fit_kbr.append([k,b,sum])
     sum = np.array([a[2] for a in fit_kbr])
     k_=np.array([a[0] for a in fit_kbr])
     b_=np.array([a[1] for a in fit_kbr])
     i=np.argmax(sum,axis=0)[0]
     k_final=k_[i][0]
     b_final=b_[i][0]

     return k_final,b_final

# -----Main Function Start----------

#RGB to HSV
img=cv2.imread('C:\\Users\\15871\Documents\\TDPS\\Sunny_pic\\99.png')
cv2.imshow('original',img)
cv2.waitKey(0)
imgG = cv2.GaussianBlur(img, (3,3), 0 )
hsv = cv2.cvtColor(imgG, cv2.COLOR_BGR2HSV)
H,S,V=cv2.split(hsv)
lower_hsv=np.array([4,11,60])#下阙值
upper_hsv=np.array([20,40,130])#上阕值
mask=cv2.inRange(hsv,lowerb=lower_hsv,upperb=upper_hsv)#
#cv2.imshow('mask',mask)
#cv2.waitKey(0)
kernal=np.ones((17,17),np.uint8)
dilate=cv2.dilate(mask,kernal)
ret,thresh1=cv2.threshold(dilate,70,255,cv2.THRESH_BINARY_INV)
img_tre = cv2.GaussianBlur(thresh1, (3,3), 0 )


#cv2.imshow('dilate',dilate)
cv2.imshow('img_tre',img_tre)
cv2.imshow('final',final)
#cv2.line(dst, (39, 181), (275, 423), (255, 0, 0), 1)
cv2.waitKey(0)


#Get Line equation

#height=np.size(dst,0)
#width=np.size(dst,1)
y_coordinate=[]
x_coordinate=[]
#for i in range(height):
#     for j in range(width):
#          if dst[i][j]!=0:
 #              x_coordinate.append(j)
  #             y_coordinate.append(-i)
#k,b=RANSAC(x_coordinate,y_coordinate)
#print(k,b)




#imgG = cv2.GaussianBlur(dst, (3,3), 0 )

#cv2.imshow('aa',imgG)
#minLineLength = 50
#maxLineGap = 10
#lines = cv2.HoughLinesP(dst, 1.0, np.pi / 180, minLineLength,maxLineGap )

#print(lines)
#for x1, y1, x2, y2 in lines[0]:
#     cv2.line(dst, (x1, y1), (x2, y2), (255, 0, 0), 5)

#cv2.imshow("houghline", dst)


