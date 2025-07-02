import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QComboBox, QVBoxLayout, QWidget, QDialog, QLineEdit, QFormLayout, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2
import numpy as np

class CropDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Введите координаты обрезки')
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        self.width_input = QLineEdit()
        self.height_input = QLineEdit()
        layout = QFormLayout()
        layout.addRow('X:', self.x_input)
        layout.addRow('Y:', self.y_input)
        layout.addRow('Ширина:', self.width_input)
        layout.addRow('Высота:', self.height_input)
        ok_button = QPushButton('ОК')
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        self.setLayout(layout)


    def get_values(self):
        try:
            x = int(self.x_input.text())
            y = int(self.y_input.text())
            width = int(self.width_input.text())
            height = int(self.height_input.text())
            return x, y, width, height
        except ValueError:
            return None


class BlurDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Введите размер ядра для усреднения')
        self.kernel_width = QLineEdit()
        self.kernel_height = QLineEdit()
        layout = QFormLayout()
        layout.addRow('Ширина ядра:', self.kernel_width)
        layout.addRow('Высота ядра:', self.kernel_height)
        ok_button = QPushButton('ОК')
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        self.setLayout(layout)


    def get_values(self):
        try:
            width = int(self.kernel_width.text())
            height = int(self.kernel_height.text())
            return width, height
        except ValueError:
            return None


class CircleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Введите параметры круга')
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        self.radius_input = QLineEdit()
        layout = QFormLayout()
        layout.addRow('X центра:', self.x_input)
        layout.addRow('Y центра:', self.y_input)
        layout.addRow('Радиус:', self.radius_input)
        ok_button = QPushButton('ОК')
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        self.setLayout(layout)


    def get_values(self):
        try:
            x = int(self.x_input.text())
            y = int(self.y_input.text())
            radius = int(self.radius_input.text())
            return x, y, radius
        except ValueError:
            return None


class ImageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image = None


    def initUI(self):
        self.setWindowTitle('Image Viewer')
        self.setGeometry(100, 100, 800, 600)
        self.label = QLabel(self)
        self.load_button = QPushButton('Загрузить изображение', self)
        self.camera_button = QPushButton('Сделать снимок с веб-камеры', self)
        self.crop_button = QPushButton('Обрезать изображение', self)
        self.blur_button = QPushButton('Усреднить изображение', self)
        self.circle_button = QPushButton('Нарисовать круг', self)
        self.channel_combo = QComboBox(self)
        self.channel_combo.addItems(['Оригинал', 'Красный канал', 'Зеленый канал', 'Синий канал'])
        self.channel_combo.setStyleSheet("QComboBox { text-align: center; }")
        self.load_button.setStyleSheet("QPushButton { text-align: center; }")
        self.camera_button.setStyleSheet("QPushButton { text-align: center; }")
        self.crop_button.setStyleSheet("QPushButton { text-align: center; }")
        self.blur_button.setStyleSheet("QPushButton { text-align: center; }")
        self.circle_button.setStyleSheet("QPushButton { text-align: center; }")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.load_button)
        layout.addWidget(self.camera_button)
        layout.addWidget(self.crop_button)
        layout.addWidget(self.blur_button)
        layout.addWidget(self.circle_button)
        layout.addWidget(self.channel_combo)
        layout.setAlignment(Qt.AlignCenter)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.load_button.clicked.connect(self.load_image)
        self.camera_button.clicked.connect(self.capture_from_camera)
        self.crop_button.clicked.connect(self.crop_image)
        self.blur_button.clicked.connect(self.blur_image)
        self.circle_button.clicked.connect(self.draw_circle)
        self.channel_combo.currentIndexChanged.connect(self.display_channel)


    def load_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg)", options=options)

        if file_name:
            self.image = cv2.imread(file_name)

            if self.image is None:
                print("Ошибка загрузки изображения")
                QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение")
                return
            
            self.display_image(self.image)


    def capture_from_camera(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Не удалось открыть камеру")
            QMessageBox.warning(self, "Ошибка", "Не удалось открыть веб-камеру")
            return
        
        ret, frame = cap.read()

        if ret:
            self.image = frame
            self.display_image(self.image)
        else:
            print("Не удалось сделать снимок")
            QMessageBox.warning(self, "Ошибка", "Не удалось сделать снимок")

        cap.release()


    def crop_image(self):
        if self.image is None:
            QMessageBox.warning(self, "Ошибка", "Сначала загрузите изображение")
            return
        
        dialog = CropDialog(self)
        if dialog.exec_():
            values = dialog.get_values()

            if values is None:
                QMessageBox.warning(self, "Ошибка", "Введите корректные числовые значения")
                return
            
            x, y, width, height = values

            if x < 0 or y < 0 or width <= 0 or height <= 0:
                QMessageBox.warning(self, "Ошибка", "Координаты и размеры должны быть положительными")
                return
            
            if x + width > self.image.shape[1] or y + height > self.image.shape[0]:
                QMessageBox.warning(self, "Ошибка", "Координаты или размеры выходят за границы изображения")
                return
            
            cropped_image = self.image[y:y+height, x:x+width]

            if cropped_image.size == 0 or cropped_image.shape[0] == 0 or cropped_image.shape[1] == 0:
                QMessageBox.warning(self, "Ошибка", "Обрезанное изображение пустое. Проверьте координаты и размеры")
                return
            
            self.image = cropped_image
            current_channel = self.channel_combo.currentIndex()
            self.display_channel(current_channel)


    def blur_image(self):
        if self.image is None:
            QMessageBox.warning(self, "Ошибка", "Сначала загрузите изображение")
            return
        
        dialog = BlurDialog(self)

        if dialog.exec_():
            values = dialog.get_values()

            if values is None:
                QMessageBox.warning(self, "Ошибка", "Введите корректные числовые значения")
                return
            
            width, height = values

            if width <= 0 or height <= 0:
                QMessageBox.warning(self, "Ошибка", "Размеры ядра должны быть положительными")
                return
            
            if width % 2 == 0 or height % 2 == 0:
                QMessageBox.warning(self, "Ошибка", "Размеры ядра должны быть нечётными")
                return
            
            if width > self.image.shape[1] or height > self.image.shape[0]:
                QMessageBox.warning(self, "Ошибка", "Размеры ядра превышают размеры изображения")
                return
            blurred_image = cv2.blur(self.image, (width, height))

            if blurred_image is None or blurred_image.size == 0:
                QMessageBox.warning(self, "Ошибка", "Не удалось применить усреднение")
                return
            
            self.image = blurred_image
            current_channel = self.channel_combo.currentIndex()
            self.display_channel(current_channel)


    def draw_circle(self):
        if self.image is None:
            QMessageBox.warning(self, "Ошибка", "Сначала загрузите изображение")
            return
        dialog = CircleDialog(self)

        if dialog.exec_():
            values = dialog.get_values()

            if values is None:
                QMessageBox.warning(self, "Ошибка", "Введите корректные числовые значения")
                return
            x, y, radius = values

            if x < 0 or y < 0 or radius <= 0:
                QMessageBox.warning(self, "Ошибка", "Координаты и радиус должны быть положительными")
                return
            
            if x - radius < 0 or x + radius > self.image.shape[1] or y - radius < 0 or y + radius > self.image.shape[0]:
                QMessageBox.warning(self, "Ошибка", "Круг выходит за границы изображения")
                return
            
            circle_image = self.image.copy()
            cv2.circle(circle_image, (x, y), radius, (0, 0, 255), 2)
            self.image = circle_image
            current_channel = self.channel_combo.currentIndex()
            self.display_channel(current_channel)


    def display_image(self, img):
        if img is None or img.size == 0:
            QMessageBox.warning(self, "Ошибка", "Невозможно отобразить изображение")
            return
        
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data.tobytes(), width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(q_img))

    def display_channel(self, index):
        if self.image is None:
            return
        
        if index == 0:
            self.display_image(self.image)
        else:
            channel_img = self.image.copy()
            if index == 1:
                channel_img[:, :, 0] = 0
                channel_img[:, :, 1] = 0
            elif index == 2:
                channel_img[:, :, 0] = 0
                channel_img[:, :, 2] = 0
            elif index == 3:
                channel_img[:, :, 1] = 0
                channel_img[:, :, 2] = 0
            self.display_image(channel_img)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageApp()
    ex.show()
    sys.exit(app.exec_())
