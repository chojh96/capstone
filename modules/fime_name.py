
  
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
import cv2
import numpy as np
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from visualize_cv2 import model, display_instances, class_names
scaler=0.4


class Form(QWidget):



    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.setWindowTitle("Mosaic _ capstone")
        box = QBoxLayout(QBoxLayout.TopToBottom)
        
        self.lb_2 = QLabel("파일 가져온 후 start 클릭")
        self.lb = QLabel()
        self.lb_3 = QLabel()
        self.lb_4 = QLabel()
        self.pb = QPushButton("파일가져오기")
        self.qb = QPushButton("시작하기")
        self.qb_2 = QPushButton("실시간 작업 시작하기")
        box.addWidget(self.lb_2)
        box.addWidget(self.lb)
        box.addWidget(self.lb_3)
        box.addWidget(self.lb_4)
        box.addWidget(self.pb)
        box.addWidget(self.qb)
        box.addWidget(self.qb_2)
        self.setLayout(box)
        self.pb.clicked.connect(self.get_file_name)
        self.qb.clicked.connect(self.button1Function)
        self.qb_2.clicked.connect(self.button2Function)
        
        

    def get_file_name(self):
        filename = QFileDialog.getOpenFileName()
        self.lb.setText(filename[0])
        

        


    def button1Function(self) :
        capture = cv2.VideoCapture("kmm.mov")
        size = (
            int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
        codec = cv2.VideoWriter_fourcc(*'DIVX')
        output = cv2.VideoWriter('1.mp4', codec, 60.0, size)

        print("btn_1 Clicked!!!!!!!!!!222")
        self.lb_3.setText("*****진행중*****")
        self.lb_3.repaint()
        print("btn_1 Clicked!!!!!!!!!!333")


        while(capture.isOpened()):
            print("btn_1 Clicked!!!!!!!!!!444444")
            ret, frame = capture.read()

            if ret:
                print("btn_1 Clicked!!!!!!!!55555555")
                        # add mask to frame
                results = model.detect([frame], verbose=1)
                
                r = results[0]
                                
                masks = r['masks'][:, :, r['class_ids']==44]
                mask = np.sum(masks, axis=2).astype(np.bool)
                mask_3d = np.repeat(np.expand_dims(mask, axis=2), 3, axis=2).astype(np.uint8)
                
                blurred_img = cv2.blur(frame, (101, 101))   #블러
                mask_3d_blurred = cv2.medianBlur(mask_3d,9)
                
                
                person_mask = mask_3d_blurred * blurred_img.astype(np.float32)  #배경 그대로, 사람 블러
                bg_mask = (1 - mask_3d_blurred) * frame.astype(np.float32)
                out = (person_mask + bg_mask).astype(np.uint8)


                output.write(out)
                out=cv2.resize(out,(int(out.shape[1] * scaler),int(out.shape[0] * scaler)))
                
                cv2.imshow('out', out)
                

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("btn_1 Clicked!!!!!!!!!!666666")
                    break
            else:
                break
            
        capture.release()
        output.release()
        cv2.destroyAllWindows()
        self.lb_4.setText("완료")
        self.lb_4.repaint()



    def button2Function(self) :
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
       


        self.lb_3.setText("*****진행중*****")
        self.lb_3.repaint()
        while True:
            ret, frame = capture.read()
            results = model.detect([frame], verbose=0)
            r = results[0]
       # frame = display_instances(frame, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])
            cv2.imshow('frame', frame)
            k = cv2.waitKey(0)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif k==ord('s'):
                cv2.VideoWriter('mycam.avi', codec, fc, (int(cap.get(3)), int(cap.get(4))))
                capture.release()
                cv2.destroyAllWindows()
                self.lb_4.setText("완료")
                self.lb_4.repaint() 

        capture.release()
        cv2.destroyAllWindows()
        self.lb_4.setText("완료")
        self.lb_4.repaint()
        
    


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())

