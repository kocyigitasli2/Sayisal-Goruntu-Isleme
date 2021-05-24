import sys
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import numpy as np
from PIL import Image 
from matplotlib import pyplot as plt

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        widget = QtWidgets.QWidget()

        vertical_box = QtWidgets.QVBoxLayout()
        horizontal_box1 = QtWidgets.QHBoxLayout()
        horizontal_box2 = QtWidgets.QHBoxLayout()
        verticall_box2 = QtWidgets.QVBoxLayout()
        horizontal_box3 = QtWidgets.QHBoxLayout()
        horizontal_box4 = QtWidgets.QHBoxLayout()
        
        self.label1 = QtWidgets.QLabel("                        Ön İşleme                      ",self)
        self.comboBox1 = QtWidgets.QComboBox(self)
        self.comboBox1.addItem(" ",self)
        self.comboBox1.addItem("Gri Seviyeye Dönüşüm",self)
        self.comboBox1.addItem("İstenilen Bölgenin Kesilip Alınması",self)
        self.comboBox1.addItem("Histogram",self)
        
        
        self.label2 = QtWidgets.QLabel("       Filtreleme         ",self)
        self.comboBox2 = QtWidgets.QComboBox(self)
        self.comboBox2.addItem(" ",self)
        self.comboBox2.addItem("Bulanıklaştırma",self)
        self.comboBox2.addItem("Keskinleştirme",self)
        self.comboBox2.addItem("Kenar Bulma",self)      
        
        self.label3 = QtWidgets.QLabel("Morfolojik İşlem  ",self)
        self.comboBox3 = QtWidgets.QComboBox(self)
        self.comboBox3.addItem(" ",self)
        self.comboBox3.addItem("Genişletme",self)
        self.comboBox3.addItem("Erozyon",self)

        self.label4 = QtWidgets.QLabel("                     Segmentasyon               ",self)
        self.comboBox4 = QtWidgets.QComboBox(self)
        self.comboBox4.addItem(" ",self)
        self.comboBox4.addItem("4'lü Komşuluk ile Nesne Bulma",self)
        self.comboBox4.addItem("Gri Seviye Görselde Nesne Bulma",self)
        self.comboBox4.addItem("Renkli Görselde Nesne Bulma",self)
        
        self.label5 = QtWidgets.QLabel("Dosya Tipi   ",self)
        self.comboBox5 = QtWidgets.QComboBox(self)
        self.comboBox5.addItem("       " ,self)
        self.comboBox5.addItem(".jpg",self)
        self.comboBox5.addItem(".bmp",self)
        self.comboBox5.addItem(".png",self) 
        


        
        self.imageUploadButton = QtWidgets.QPushButton("Resim Yükle")
        horizontal_box1.addWidget(self.imageUploadButton)
        horizontal_box2.addWidget(self.label1)
        horizontal_box3.addWidget(self.comboBox1)
        horizontal_box2.addWidget(self.label2)
        horizontal_box3.addWidget(self.comboBox2)
        horizontal_box2.addWidget(self.label3)
        horizontal_box3.addWidget(self.comboBox3)
        horizontal_box2.addWidget(self.label4)
        horizontal_box3.addWidget(self.comboBox4)
        horizontal_box2.addWidget(self.label5)
        horizontal_box3.addWidget(self.comboBox5)

        
        horizontal_box2.addStretch()
        horizontal_box3.addStretch()

        self.label = QtWidgets.QLabel()
        verticall_box2.addWidget(self.label)
        self.label.setAlignment(Qt.AlignCenter)

        self.imageDownloadButton = QtWidgets.QPushButton("KAYDET")
        horizontal_box4.addStretch()
        horizontal_box4.addWidget(self.imageDownloadButton)
        
        vertical_box.addLayout(horizontal_box1)
        vertical_box.addLayout(horizontal_box2)
        vertical_box.addLayout(horizontal_box3)
        vertical_box.addStretch()
        vertical_box.addLayout(verticall_box2)
        vertical_box.addStretch()
        vertical_box.addLayout(horizontal_box4)

        self.imageUploadButton.clicked.connect(self.dosyaSec)
        self.comboBox1.currentTextChanged.connect(self.combo1_bagla)
        self.comboBox2.currentTextChanged.connect(self.combo2_bagla)
        self.comboBox3.currentTextChanged.connect(self.combo3_bagla)
        self.comboBox5.currentTextChanged.connect(self.kaydet)
        
        widget.setLayout(vertical_box)
        self.setCentralWidget(widget)
        self.setGeometry(100,100,200,200)
        self.setWindowTitle('Görüntü İşleme Proje Ödevi')
        self.show()
        
        self.flag=0

        
    def dosyaSec(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
            'd:\\',"Image files (*.jpg *.gif *.png)")
        self.image = fname[0]
        self.img_deneme = fname[0]
        if len(fname[0]) > 0:
            self.label.setPixmap(QPixmap(fname[0]))


    def combo1_bagla(self):
        if self.comboBox1.currentText() == "Gri Seviyeye Dönüşüm":
            img =cv2.imread(self.img_deneme)
            h,w = img.shape[:2]
            img2 = np.zeros((h,w,1), np.uint8)
            
            for i in range(h):
                for j in range(w):
                    img2[i,j]= int(((img[i,j][0]*0.2989)+(img[i,j][1]*0.5870)+(img[i,j][2]*0.1140)))
                    
            cv2.imwrite('a.png',img2)
            self.image=img2
            self.label.setPixmap(QPixmap('a.png'))
            self.flag=1

        
        if self.comboBox1.currentText() == "İstenilen Bölgenin Kesilip Alınması":
            img = cv2.imread('a.png')
            roi = cv2.selectROI("Alan secip ESC'ye basiniz.",img,False)
            imCrop = img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
            cv2.imshow("Goruntu", imCrop)
            cv2.imwrite("a.png",imCrop)
            img_kirpik = cv2.imread("a.png")
            self.image=img_kirpik
            self.label.setPixmap(QPixmap('a.png'))
            self.flag=2

        
        if self.comboBox1.currentText() == "Histogram":
            if self.flag == 0:
                img2 = cv2.imread(self.img_deneme)
            if self.flag == 1:
                img2 = cv2.imread('a.png')
            if self.flag == 2:
                img2 = cv2.imread('a.png')    
            h,w = img2.shape[:2] # img is a grayscale image
            y = np.zeros((256), np.uint8)
            for i in range(0,h):
               for j in range(0,w):
                  y[img2[i,j]] += 1
            x = np.arange(0,256)
            plt.bar(x,y,align="center")
            plt.savefig('histogram.png')
            img2 = cv2.imread("histogram.png")
            self.image=img2
            self.label.setPixmap(QPixmap('histogram.png'))
    
    
    def combo2_bagla(self):
        def average(img,x,y,blurfactor):
            rtotal = gtotal = btotal = 0
            for x2 in range(x-blurfactor,x+blurfactor+1):
                for y2 in range(y-blurfactor,y+blurfactor+1):
                    r,g,b = img.getpixel((x2,y2))
                    rtotal = rtotal + r
                    gtotal = gtotal + g
                    btotal = btotal + b
            rtotal = rtotal // ((blurfactor * 2 +1)**2)
            gtotal = gtotal // ((blurfactor * 2 +1)**2)
            btotal = btotal // ((blurfactor * 2 +1)**2)
            return (rtotal, gtotal, btotal)
    
        if self.comboBox2.currentText() == "Bulanıklaştırma":
            img = Image.open("a.png")
            w = img.size[0]
            h = img.size[1]
            img2 = Image.new("RGB",(w,h),(0,0,0))
            
            for x in range(5,w-5):
                for y in range(5,h-5):
                    r,g,b = img.getpixel((x,y))
                    r2,g2,b2 = average(img,x,y,5)
                    img2.putpixel((x,y),(r2,g2,b2))
                    
            img2 = img2.save("a.png")
            img2 = cv2.imread("a.png")
            self.image = img2
            self.label.setPixmap(QPixmap('a.png'))
            
    def combo3_bagla(self):
        if self.comboBox3.currentText() == "Genişletme":
            img1= cv2.imread('a.png',0)
            m,n= img1.shape
            k=5
            SE= np.ones((k,k), dtype=np.uint8)
            constant= (k-1)//2
            imgErode= np.zeros((m,n), dtype=np.uint8)
            for i in range(constant, m-constant):
              for j in range(constant,n-constant):
                temp= img1[i-constant:i+constant+1, j-constant:j+constant+1]
                product= temp*SE
                imgErode[i,j]= np.min(product)
            cv2.imwrite("a.png", imgErode)
            img2 = cv2.imread("a.png")
            self.image = img2
            self.label.setPixmap(QPixmap('a.png'))
        
        if self.comboBox3.currentText() == "Erozyon":
            img2= cv2.imread('a.png',0)
            p,q= img2.shape
            imgDilate= np.zeros((p,q), dtype=np.uint8)
            SED= np.array([[0,1,0], [1,1,1],[0,1,0]])
            constant1=1
            for i in range(constant1, p-constant1):
              for j in range(constant1,q-constant1):
                temp= img2[i-constant1:i+constant1+1, j-constant1:j+constant1+1]
                product= temp*SED
                imgDilate[i,j]= np.max(product)
            cv2.imwrite("a.png", imgDilate)
            img2 = cv2.imread("a.png")
            self.image = img2
            self.label.setPixmap(QPixmap('a.png'))

            
    def kaydet(self):
        if self.comboBox5.currentText() == ".jpg":
            img = cv2.imread('a.png',0)
            dosyaAdi = "cikti.jpg"
            cv2.imwrite(dosyaAdi,img)
        
        if self.comboBox5.currentText() == ".bmp":
            img = cv2.imread('a.png',0)
            dosyaAdi = "cikti.bmp"
            cv2.imwrite(dosyaAdi,img)
        
        if self.comboBox5.currentText() == ".png":
            img = cv2.imread('a.png',0)
            dosyaAdi = "a.png"
            cv2.imwrite(dosyaAdi,img)            

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()