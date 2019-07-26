#coding:utf-8

#Python中声明文件编码的注释，编码格式指定为utf-8
from socket import *
from time import ctime
import binascii
import RPi.GPIO as GPIO
import time
import threading
import cv2
import numpy as np
from collections import  deque
import colorList

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
########LED口定义#################
LED0 = 10
LED1 = 9
LED2 = 25
########电机驱动接口定义#################
ENA = 13	#//L298使能A
ENB = 20	#//L298使能B
IN1 = 19	#//电机接口1
IN2 = 16	#//电机接口2
IN3 = 21	#//电机接口3
IN4 = 26	#//电机接口4
#########led初始化为000##########
GPIO.setup(LED0,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED1,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED2,GPIO.OUT,initial=GPIO.HIGH)
#########电机初始化为LOW##########
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
ENA_pwm=GPIO.PWM(ENA,1000)
ENA_pwm.start(0)
ENA_pwm.ChangeDutyCycle(80)  
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)

GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
ENB_pwm=GPIO.PWM(ENB,1000)
ENB_pwm.start(0)
ENB_pwm.ChangeDutyCycle(80)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
##########机器人方向控制###########################
def Motor_Forward():
	print 'motor forward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
	GPIO.output(LED1,False)#LED1亮
	GPIO.output(LED2,False)#LED1亮
def Motor_Backward():
	print 'motor_backward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
	GPIO.output(LED1,True)#LED1灭
	GPIO.output(LED2,False)#LED2亮
def Motor_TurnLeft():
	print 'motor_turnleft'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
	GPIO.output(LED1,False)#LED1亮
	GPIO.output(LED2,True) #LED2灭
def Motor_TurnRight():
	print 'motor_turnright'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
	GPIO.output(LED1,False)#LED1亮
	GPIO.output(LED2,True) #LED2灭
def Motor_Stop():
	print 'motor_stop'
	GPIO.output(ENA,False)
	GPIO.output(ENB,False)
	GPIO.output(IN1,False)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,False)
	GPIO.output(LED1,True)#LED1灭
	GPIO.output(LED2,True)#LED2亮
##########机器人速度控制###########################
def ENA_Speed(EA_num):
	speed=hex(eval('0x'+EA_num))
	speed=int(speed,16)
	print 'EA_A改变啦 %d '%speed
	ENA_pwm.ChangeDutyCycle(speed)
def ENB_Speed(EB_num):
	speed=hex(eval('0x'+EB_num))
	speed=int(speed,16)
	print 'EB_B改变啦 %d '%speed
	ENB_pwm.ChangeDutyCycle(speed)

def Change_Direc(Path_Dect_px):
	if (Path_Dect_px < 245)&(Path_Dect_px > 0):	#如果巡线中心点偏左，就需要左转来校正。
		print("turn left")
		Motor_TurnLeft()
		time.sleep(0.03)
	elif Path_Dect_px > 435:#如果巡线中心点偏右，就需要右转来校正。
		print("turn right")
		Motor_TurnRight()
		time.sleep(0.03)
	else :		#如果巡线中心点居中，就可以直行。
		print("go stright")
		Motor_Forward()
	        time.sleep(0.07)
	Motor_Stop()
	time.sleep(0.02)


#处理图片
def get_color(frame):           #找到最大颜色
######    print('get color')
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    maxsum = -100
    color = None
    color_dict = colorList.getColorList()
    for d in color_dict:
        mask = cv2.inRange(hsv,color_dict[d][0],color_dict[d][1])
        ##cv2.imshow('11.jpg',mask)

        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        binary = cv2.dilate(binary,None,iterations=2)
        cnts, hiera = cv2.findContours(binary.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        sum = 0
        for c in cnts:
            sum+=cv2.contourArea(c)
        if sum > maxsum :
            maxsum = sum
            color = d
    
    return color
 
def find_the_maximum_color(frame):
    color_dict = colorList.getColorList()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, color_dict[get_color(frame)][0], color_dict[get_color(frame)][1])  # find the maximum color
    a = color_dict[get_color(frame)][0]
    b = color_dict[get_color(frame)][1]
    cap.release()
    print('find it !')
    return a,b
def matching_color(a,b,frame):
    mybuffer = 16
    pts = deque(maxlen=mybuffer)
    counter = 0
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, a, b)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    # 初始化瓶盖圆形轮廓质心
    center = None
    # 如果存在轮廓
    if len(cnts) > 0:
        # 找到面积最大的轮廓
        c = max(cnts, key=cv2.contourArea)
        # 确定面积最大的轮廓的外接圆
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        # 计算轮廓的矩
        M = cv2.moments(c)
        # 计算质心
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # 只有当半径大于10时，才执行画图
    if radius > 10:
        frame_new = cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        # 把质心添加到pts中，并且是添加到列表左侧
        pts.appendleft(center)

    else:  # 如果图像中没有检测到瓶盖，则清空pts，图像上不显示轨迹。
        pts.clear()
    Area=3.14*radius*radius
    return frame_new,center[0],Area

time.sleep(3)
cap=cv2.VideoCapture(0)


if __name__ == '__main__':
    ret1, frame = cap.read()  # capture frame_by_frame
print(get_color(frame))
up_thre, down_thre = find_the_maximum_color(frame)
time.sleep(7)
cap = cv2.VideoCapture(0)
while True:
    ret2, frame_2 = cap.read()  # capture another frame
    frame_new,Path_Dect_px,area=matching_color(up_thre,down_thre,frame_2)
    if area > 380000:
        Motor_Stop()
        break
    Change_Direc(Path_Dect_px)

cap.release()
cv2.destroyAllWindows()