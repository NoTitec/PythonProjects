import sys
import matplotlib.pyplot as plt  # draw grape
from PyQt5.QtCore import QUrl  # gui packge
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # figure apperence
from win32api import GetSystemMetrics
import numpy as np  # math library
import scipy.io as sio  # wav read library
import scipy.io.wavfile


class Myapp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = QLabel('no music', self)
        self.fig = plt.figure(figsize=(500, 100))
        self.canvas = FigureCanvas(self.fig)
        self.init_ui()
        self.player = QMediaPlayer()

    def open_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', './')[0]  # get cd
        print(file_name)
        self.set_title(file_name)
        self.set_music(file_name)
        self.draw_wave(file_name)

    def set_title(self, file_name):
        title = file_name.split('/')[-1].split('.')[0]  # or [:-4]
        self.title.setText(title)
        self.title.repaint()  # 상위객체에 바뀐값으로 다시 출력해달라고 요청

    def draw_wave(self, file_name):
        rate, data = sio.wavfile.read(file_name)  # rate: sampling, data=realdata
        size = len(data)
        time = np.arange(size) / float(rate)  # get sec
        plt.plot(time, data)
        plt.xlim(time[0], time[-1])  # first to last
        plt.xlabel('time (s)')
        plt.ylabel('samplitude')
        self.canvas.draw()

    def set_music(self, file_name):
        url = QUrl.fromLocalFile(file_name)
        content = QMediaContent(url)
        self.player.setMedia(content)

    def play(self):
        self.player.play()

    def stop(self):
        self.player.stop()

    def init_ui(self):
        open_button = QPushButton('open')  # 버튼추가
        open_button.clicked.connect(self.open_file)

        play_button = QPushButton('play')
        play_button.clicked.connect(self.play)  # play함수를 연결

        stop_button = QPushButton('stop')
        stop_button.clicked.connect(self.stop)  # stop함수를 연결

        hbox = QHBoxLayout()
        hbox.addStretch(1)  # 간격
        hbox.addWidget(open_button)  # 버튼위젯추가
        hbox.addWidget(play_button)
        hbox.addWidget(stop_button)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.title)
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.setWindowTitle('musicplayer')
        self.setGeometry(0, 40, GetSystemMetrics(0), 900)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Myapp()
    sys.exit(app.exec_())
