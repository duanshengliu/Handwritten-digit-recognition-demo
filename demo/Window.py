# -*- coding:utf-8 -*-
from tkinter import *
from PIL import Image,ImageDraw
import numpy as np
from tensorflow import keras

class Window:

    def __init__(self,win,ww,wh):
        self.win=win
        self.ww=ww
        self.wh=wh
        self.win.geometry("%dx%d+%d+%d" %(ww,wh,500,100))
        self.win.title("手写数字识别软件---by DuanshengLiu")
        self.can=Canvas(self.win,width=ww-130,height=wh-32,bg='white')
        self.can.place(x=0,y=0)
        self.can.bind("<B1-Motion>",self.paint)

        self.label1=Label(self.win,text="识别结果:",font=('微软雅黑',20))
        self.label1.place(x=405,y=0)
        self.label2=Label(self.win,width=6,height=2,text='',font=('微软雅黑',20),
                          background="white",relief="ridge",borderwidth=10)
        self.label2.place(x=405,y=50)

        self.button1=Button(self.win,text="Predict",width=10,height=1,bg='gray',command=self.predict)
        self.button1.place(x=ww/6,y=wh-30)
        self.button2=Button(self.win,text="Clear",width=10,height=1,bg='white',command=self.clear)
        self.button2.place(x=ww/2,y=wh-30)

        self.image=Image.new("RGB",(ww-130,wh-30),color=(0,0,0))#(0,0,0)表示黑色背景
        self.draw=ImageDraw.Draw(self.image)
        self.model=keras.models.load_model("cnn.h5")#加载训练好的cnn模型

    def paint(self,event):
        self.x1,self.y1=event.x,event.y
        self.x2,self.y2=(self.x1+25),(self.y1+25)
        self.can.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="black")
        self.draw.rectangle(((self.x1,self.y1),(self.x2,self.y2)),(255,255,255))#(255,255,255)表示白色字

    def predict(self):
        #实际预测的是黑底白字和训练集一致
        #self.image.resize
        if np.array(self.image).sum()==0:#检测到还没进行手写就预测,显示预测结果为空
            self.display('空')
        else:
            self.image=self.image.resize((28,28),Image.ANTIALIAS).convert('L')
            self.image=np.array(self.image).reshape(1,28,28,1)#训练时shape为(-1,28,28,1)
            self.rec=self.model.predict_classes(self.image)[0]
            self.display(self.rec)#显示预测结果

            #预测完成就将self.image还原为黑底,但是画布上的保留,
            #这样在画布继续绘制所形成的组合也能进行预测
            self.image=Image.new("RGB",(self.ww-130,self.wh-30),(0,0,0))
            self.draw=ImageDraw.Draw(self.image)

    def clear(self):
        self.can.delete("all")
        self.image=Image.new("RGB",(self.ww-130,self.wh-30),(0,0,0))#(0,0,0)表示黑色背景
        self.draw=ImageDraw.Draw(self.image)
        self.display('')

    def display(self,string):
        self.label2=Label(self.win,width=6,height=2,text=string,font=('微软雅黑',20),
                          background="white",relief="ridge",borderwidth=10)
        self.label2.place(x=405,y=50)

    def closeEvent():#关闭前清除session(),防止'NoneType' object is not callable
        keras.backend.clear_session()
        sys.exit()