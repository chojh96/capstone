
  
#!/usr/bin/env python
# coding: utf-8

# 예제 내용p
# * QTreeWidget을 사용하여 아이템을 표시

__author__ = "Deokyu Lim <hong18s@gmail.com>"

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import cv2
import numpy as np
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from visualize_cv2 import model, display_instances, class_names
# 프로그램에 필요한 라이브러리 추가 

scaler=0.4 #동영상의 크기를 조절하기 위함
filename=[] #자신이 원하는 동영상을 사용하기 위해 변수 배열선언


class Form(QWidget):



    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.setWindowTitle("2019_Capstone") #window title을 "2019_Capstone"으로 선언
        box = QBoxLayout(QBoxLayout.TopToBottom)
        
        self.lb_2 = QLabel("파일 가져온 후 시작하기 버튼 누르기")
        self.lb = QLabel()
        self.lb_3 = QLabel()
        self.lb_4 = QLabel()
        self.pb = QPushButton("파일가져오기")
        self.qb = QPushButton("시작하기")
        #self.qb_2 = QPushButton("실시간 작업 시작하기")
        box.addWidget(self.lb_2)
        box.addWidget(self.lb)
        box.addWidget(self.lb_3)
        box.addWidget(self.lb_4)
        box.addWidget(self.pb)
        box.addWidget(self.qb)
        #box.addWidget(self.qb_2)
        self.setLayout(box)
        self.pb.clicked.connect(self.get_file_name) # "파일가져오기"버튼을 누르면  get_file_name 함수 실행
        self.qb.clicked.connect(self.button1Function) # 시작하기 버튼을 누르면 button1Function 함수 실
        #self.qb_2.clicked.connect(self.button2Function)

        #main화면의 구성
        

    def get_file_name(self):
        global filename
        
        filename = QFileDialog.getOpenFileName() #파일목록에서 원하는 동영상파일을 불러와 그 파일의 주소는 filename이라는 변수에 넣어준다.
        self.lb.setText(filename[0])

        print(filename[0])

        


        


    def button1Function(self) :
        
        capture = cv2.VideoCapture(filename[0]) #파일의 주소를 불러와 capture한다. 
        size = (
            int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
        codec = cv2.VideoWriter_fourcc(*'DIVX')
        output = cv2.VideoWriter('1.mp4', codec, 60.0, size) 
        
        self.lb_3.setText("*****진행중*****")
        self.lb_3.repaint()
        
        while(capture.isOpened()):
            ret, frame = capture.read()

            if ret:
                        # add mask to frame
                results = model.detect([frame], verbose=1) 
                
                r = results[0] 
                                
                masks = r['masks'][:, :, r['class_ids']==44] #knife's class_ids is 44
                mask = np.sum(masks, axis=2).astype(np.bool)
                mask_3d = np.repeat(np.expand_dims(mask, axis=2), 3, axis=2).astype(np.uint8)
                
                blurred_img = cv2.blur(frame, (101, 101))   #블러
                mask_3d_blurred = cv2.medianBlur(mask_3d,9)
                    
                person_mask = mask_3d_blurred * blurred_img.astype(np.float32)  #배경 그대로, 칼 블러 
                bg_mask = (1 - mask_3d_blurred) * frame.astype(np.float32)
                out = (person_mask + bg_mask).astype(np.uint8
                                                     
                output.write(out) 
                out=cv2.resize(out,(int(out.shape[1] * scaler),int(out.shape[0] * scaler)))
                
                cv2.imshow('out', out)
                

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
            
        capture.release()
        output.release()
        cv2.destroyAllWindows()
        self.lb_3.setText("완료")
        self.lb_3.repaint()



    #def button2Function(self) :
        #capture = cv2.VideoCapture(0)
        #capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        #capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        #self.lb_3.setText("*****진행중*****")
        #self.lb_3.repaint()
        
        #while True:
            #ret, frame = capture.read()
            #results = model.detect([frame], verbose=0)
            #r = results[0]
          
       # frame = display_instances(frame, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])
            #cv2.imshow('frame', frame)
            #if cv2.waitKey(1) & 0xFF == ord('q'):

                 #break

        #capture.release()
        #cv2.destroyAllWindows()
        #self.lb_4.setText("완료")
        #self.lb_4.repaint()
        
    


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())

