import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PIL import Image
from math import *

# 가로레이아웃 3개 세로 1개  가로는 hbox 세로는 vbox

class myapp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = QLabel('')
        self.img = Image.init()
        self.slider_v = QSlider(Qt.Horizontal)
        self.slider_v.setRange(0,200)
        self.slider_v.setValue(140)
        self.slider_u = QSlider(Qt.Horizontal)
        self.slider_u.setRange(0, 200)
        self.slider_u.setValue(130)
        self.slider_bright = QSlider(Qt.Horizontal)
        self.slider_bright.setRange(0, 200)
        self.slider_bright.setValue(120)
        self.init_vi()

    def rgbtoCmyk(self,r, g, b):
        black = min(min(255 - r, 255 - g), 255 - b)
        if (black!=255):
            cyan = (255 - r - black) / (255 - black)

            magenta = (255 - g - black) / (255 - black)

            yellow = (255 - b - black) / (255 - black)

            return cyan,magenta,yellow,black
        else:
            cyan = 255 - r

            magenta = 255 - g

            yellow = 255 - b

            return cyan,magenta,yellow,black

    def Cmyktorgb(self,cyan,magenta,yellow,black):
        if (black != 255):
            r = ((255 - cyan) * (255 - black)) / 255

            g = ((255 - magenta) * (255 - black)) / 255

            b = ((255 - yellow) * (255 - black)) / 255

            return r,g,b
        else:
            r = 255 - cyan

            g = 255 - magenta

            b = 255 - yellow

            return r,g,b

    def init_vi(self):
        button_open = QPushButton('open')
        button_open.clicked.connect(self.openfile)
        hbox = QHBoxLayout()
        hbox.addWidget(button_open)
        hbox.addWidget(QLabel("파일명:"))
        hbox.addWidget(self.title)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        button_r = QPushButton('R')
        button_r.clicked.connect(self.show_red)
        button_g = QPushButton('G')
        button_g.clicked.connect(self.show_green)
        button_b = QPushButton('B')
        button_b.clicked.connect(self.show_blue)
        button_o = QPushButton('원본')
        button_o.clicked.connect(self.showorginal)
        hbox2.addWidget(button_r)
        hbox2.addWidget(button_g)
        hbox2.addWidget(button_b)
        hbox2.addWidget(button_o)
        hbox2.addStretch(1)

        hbox21=QHBoxLayout()
        hbox21.addStretch(1)
        button_c = QPushButton('C')
        button_c.clicked.connect(self.show_C)
        button_m = QPushButton('M')
        button_m.clicked.connect(self.show_m)
        button_y = QPushButton('Y')
        button_y.clicked.connect(self.show_y)
        button_k = QPushButton('K')
        button_k.clicked.connect(self.show_k)
        hbox21.addWidget(button_c)
        hbox21.addWidget(button_m)
        hbox21.addWidget(button_y)
        hbox21.addWidget(button_k)
        hbox21.addStretch(1)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(QLabel("Y"))
        hbox3.addWidget(self.slider_bright)
        hbox3.addWidget(QLabel("U"))
        hbox3.addWidget(self.slider_u)
        hbox3.addWidget(QLabel("V"))
        hbox3.addWidget(self.slider_v)
        button_g=QPushButton("show")
        button_g.clicked.connect(self.show_slide)
        hbox3.addWidget(button_g)
        hbox3.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox21)
        vbox.addLayout(hbox3)
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.setWindowTitle("imageviewer")
        self.setGeometry(500, 500, 500, 500)
        self.show()

    def openfile(self):
        filename = QFileDialog.getOpenFileName(self, 'open file', './')[0]
        title = filename.split("/")[-1].split(".")[0]
        self.title.setText(title)
        self.img = Image.open(filename)
        self.title.repaint()

    def showorginal(self):
        self.img.show()

    def show_red(self):
        imgr = self.img.copy()
        for i in range(0, imgr.size[0]):
            for j in range(0, imgr.size[1]):
                rgb= imgr.getpixel((i, j))
                imgr.putpixel((i, j), (rgb[0], 0, 0))
        imgr.show()

    def show_green(self):
        imgr = self.img.copy()
        for i in range(0, imgr.size[0]):
            for j in range(0, imgr.size[1]):
                rgb= imgr.getpixel((i, j))
                imgr.putpixel((i, j), (0, rgb[1], 0))
        imgr.show()

    def show_blue(self):
        imgr = self.img.copy()
        for i in range(0, imgr.size[0]):
            for j in range(0, imgr.size[1]):
                rgb= imgr.getpixel((i, j))
                imgr.putpixel((i, j), (0, 0, rgb[2]))
        imgr.show()

    def show_gray(self):
        imgr = self.img.copy()
        for i in range(0, imgr.size[0]):
            for j in range(0, imgr.size[1]):
                rgb= imgr.getpixel((i, j))
                gray= int(rgb[0]*0.299 +rgb[1] *0.587+rgb[2] *0.114)
                imgr.putpixel((i, j), (gray,gray,gray))
        imgr.show()

    def show_C(self):
        imgr = self.img.copy()
        for i in range(0, imgr.size[0]):
            for j in range(0, imgr.size[1]):
                rgb = imgr.getpixel((i, j))
                maxv = max(rgb)
                if maxv != 0:
                    c = (maxv - rgb[0]) / maxv
                    # m = (maxv - rgb[1]) / maxv
                    # y=(maxv-rgb[2])/maxv
                    m = 0
                    y = 0
                    k = 1 - maxv / 255
                    r = 61 * (1 - c) * (1 - k)
                    g = 91 * (1 - m) * (1 - k)
                    b = 220 * (1 - y) * (1 - k)
                    imgr.putpixel((i, j), (int(r), int(g), int(b)))
                else:
                    imgr.putpixel((i, j), (61, 91, 220))
        imgr.show()

    def show_m(self):
        imgr = self.img.copy()
        for i in range(0, imgr.size[0]):
            for j in range(0, imgr.size[1]):
                rgb = imgr.getpixel((i, j))
                maxv = max(rgb)
                if maxv != 0:
                    # c = (maxv - rgb[0]) / maxv
                    m=(maxv-rgb[1])/maxv
                    # y=(maxv-rgb[2])/maxv
                    c = 0
                    y = 0
                    k = 1 - maxv / 255
                    r = 61 * (1 - c) * (1 - k)
                    g = 91 * (1 - m) * (1 - k)
                    b = 220 * (1 - y) * (1 - k)
                    imgr.putpixel((i, j), (int(r), int(g), int(b)))
                else:
                    imgr.putpixel((i, j), (61, 91, 220))
        imgr.show()

    def show_y(self):
        imgr = self.img.copy()
        for i in range(0, imgr.size[0]):
            for j in range(0, imgr.size[1]):
                rgb = imgr.getpixel((i, j))
                maxv = max(rgb)
                if maxv != 0:
                    # c = (maxv - rgb[0]) / maxv
                    # m = (maxv - rgb[1]) / maxv
                    y=(maxv-rgb[2])/maxv
                    c = 0
                    m = 0
                    k = 1 - maxv / 255
                    r = 61 * (1 - c) * (1 - k)
                    g = 91 * (1 - m) * (1 - k)
                    b = 220 * (1 - y) * (1 - k)
                    imgr.putpixel((i, j), (int(r), int(g), int(b)))
                else:
                    imgr.putpixel((i, j), (61, 91, 220))
        imgr.show()

    def show_k(self):
        imgr = self.img.copy()
        for i in range(0, imgr.size[0]):
            for j in range(0, imgr.size[1]):
                rgb = imgr.getpixel((i, j))
                maxv = max(rgb)
                if maxv != 0:
                    # c = (maxv - rgb[0]) / maxv
                    # m = (maxv - rgb[1]) / maxv
                    # y = (maxv - rgb[2]) / maxv
                    c = 0
                    m = 0
                    y = 0
                    k = 1 - maxv / 255
                    r = 61 * (1 - c) * (1 - k)
                    g = 91 * (1 - m) * (1 - k)
                    b = 220 * (1 - y) * (1 - k)
                    imgr.putpixel((i, j), (int(r), int(g), int(b)))
                else:
                    imgr.putpixel((i, j), (61, 91, 220))
        imgr.show()

    def show_slide(self):
        imgr = self.img.copy()
        for i in range(0, imgr.size[0]):
            for j in range(0, imgr.size[1]):
                rgb= imgr.getpixel((i, j))
                #rgb->yuv
                y = 0.257*rgb[0]+0.504*rgb[1]+0.098*rgb[2]+16
                u = -0.148 * rgb[0] - 0.291 * rgb[1] + 0.439 * rgb[2] + 128
                v = 0.439 * rgb[0] - 0.368 * rgb[1] - 0.071 * rgb[2] + 128
                y = y*self.slider_bright.value()/100
                u = u*self.slider_u.value()/100
                v = v*self.slider_v.value()/100
                #yuv->rgb
                r = 1.164*(y-16)+1.596*(v-128)
                g = 1.164 * (y - 16) - 0.813 * (v - 128)-0.391*(u-128)
                b = 1.164 * (y - 16) + 2.018 * (u - 128)
                #rgb 변경
                r = int(r)
                g = int(g)
                b = int(b)
                imgr.putpixel((i,j),(r,g,b))
        imgr.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = myapp()
    sys.exit(app.exec_())
