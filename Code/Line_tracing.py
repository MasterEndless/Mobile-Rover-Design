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
print '....WIFIROBOTS START!!!...'
global Path_Dect_px
Path_Dect_px = 320
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
def PathDect(func):
	global Path_Dect_px	#巡线中心点坐标值
	while True:
		print 'Path_Dect_px %d '%Path_Dect_px	 #打印巡线中心点坐标值
		if (Path_Dect_px < 260)&(Path_Dect_px > 0):	#如果巡线中心点偏左，就需要左转来校正。
			print("turn left")
			Motor_TurnLeft()
		elif Path_Dect_px > 420:#如果巡线中心点偏右，就需要右转来校正。
			print("turn right")
			Motor_TurnRight()
		else :		#如果巡线中心点居中，就可以直行。
			print("go stright")
			Motor_Forward()
		time.sleep(0.007)
		Motor_Stop()
		time.sleep(0.007)
cap = cv2.VideoCapture(0)	#实例化摄像头
Path_Dect_px_sum  = 0	#坐标值求和
threads = []
t1 = threading.Thread(target=PathDect,args=(u'监听',))
threads.append(t1)
for t in threads:
		t.setDaemon(True)
		t.start()
while True:
	ret,frame = cap.read()	#capture frame_by_frame
	imgG = cv2.GaussianBlur(frame, (3, 3), 0)
	hsv = cv2.cvtColor(imgG, cv2.COLOR_BGR2HSV)
	H, S, V = cv2.split(hsv)
	lower_hsv = np.array([15, 30, 120])  # 下阙值
	upper_hsv = np.array([25, 45, 200])  # 上阕值
	mask = cv2.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)  #
	kernal = np.ones((5, 5), np.uint8)
	dilate = cv2.dilate(mask, kernal)
	ret, thresh1 = cv2.threshold(dilate, 70, 255, cv2.THRESH_BINARY_INV)
	Path_Dect_fre_count = 1
	for j in range(0,640,5):		#采样像素点，5为步进，一共128个点
		if thresh1[240,j] == 0:		
			Path_Dect_px_sum = Path_Dect_px_sum + j		#黑色像素点坐标值求和
			Path_Dect_fre_count = Path_Dect_fre_count + 1	#黑色像素点个数求和
	Path_Dect_px = (Path_Dect_px_sum )/(Path_Dect_fre_count)	#黑色像素中心点为坐标和除以个数
	Path_Dect_px_sum = 0
	cv2.imshow('BINARY',thresh1)		#树莓派桌面显示二值化图像，比较占资源默认注释掉调试时可以打开
	if cv2.waitKey(1)&0XFF ==ord('q'):#检测到按键q退出
		Motor_Stop()
		break	
cap.release()
cv2.destroyAllWindows()