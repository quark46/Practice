import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QComboBox, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2
import numpy as np

class ImageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image = None

    #Создание виджетов, настройка лэйаутов, подключение сигналов
    def initUI(self):
        self.setWindowTitle('Image Viewer')
        self.setGeometry(100, 100, 800, 600)
        self.label = QLabel(self)
        self.load_button = QPushButton('Загрузить изображение', self)
        self.camera_button = QPushButton('Сделать снимок с веб-камеры', self)
        self.channel_combo = QComboBox(self)
        self.channel_combo.addItems(['Оригинал', 'Красный канал', 'Зеленый канал', 'Синий канал'])
        self.channel_combo.setStyleSheet("QComboBox { text-align: center; }")
        self.load_button.setStyleSheet("QPushButton { text-align: center; }")
        self.camera_button.setStyleSheet("QPushButton { text-align: center; }")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.load_button)
        layout.addWidget(self.camera_button)
        layout.addWidget(self.channel_combo)
        layout.setAlignment(Qt.AlignCenter)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.load_button.clicked.connect(self.load_image)
        self.camera_button.clicked.connect(self.capture_from_camera)
        self.channel_combo.currentIndexChanged.connect(self.display_channel)

    def load_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg)", options=options)
        if file_name:
            self.image = cv2.imread(file_name)
            if self.image is None:
                print("Ошибка загрузки изображения")
                return
            self.display_image(self.image)

    def capture_from_camera(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Не удалось открыть камеру")
            return
        ret, frame = cap.read()
        if ret:
            self.image = frame
            self.display_image(self.image)
        else:
            print("Не удалось сделать снимок")
        cap.release()

    def display_image(self, img):
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(q_img))

    def display_channel(self, index):
        if self.image is None:
            return
        if index == 0:  # Оригинал
            self.display_image(self.image)
        else:
            channel_img = self.image.copy()
            if index == 1:  # Красный канал
                channel_img[:, :, 0] = 0
                channel_img[:, :, 1] = 0
            elif index == 2:  # Зеленый канал
                channel_img[:, :, 0] = 0
                channel_img[:, :, 2] = 0
            elif index == 3:  # Синий канал
                channel_img[:, :, 1] = 0
                channel_img[:, :, 2] = 0
            self.display_image(channel_img)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageApp()
    ex.show()
    sys.exit(app.exec_())