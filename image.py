import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextBrowser, QFileDialog, QComboBox, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import Qt, QSize
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

# Установите путь к исполняемому файлу Tesseract OCR (если он не в PATH)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class FirstForm(QWidget):
    def __init__(self, background_image_path, second_form):
        super().__init__()

        self.second_form = second_form

        self.background_image_path = background_image_path

        self.setWindowTitle('Справка')
        self.setGeometry(100, 100, 600, 400)
        self.setFixedSize(1080, 675)

        layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Устанавливаем задний фон
        self.set_background_image()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(320, 180)  # Фиксированный размер для отображения изображения

        self.browse_button = QPushButton('Выбрать изображение', self)
        self.browse_button.clicked.connect(self.browse_image)

        # Add label for browse button
        browse_label = QLabel("Эта кнопка отвечает за выбор вашего изображения и отображение его в приложении.", self)
        browse_label.setWordWrap(True)

        left_layout.addWidget(self.image_label)
        left_layout.addWidget(browse_label)
        left_layout.addWidget(self.browse_button)
        left_layout.addStretch(1)  # Добавляем пространство для равномерного размещения

        self.text_browser = QTextBrowser(self)
        self.text_browser.setReadOnly(True)

        self.extract_text_button = QPushButton('Извлечь текст', self)
        self.extract_text_button.clicked.connect(self.extract_text)

        # Add label for extract text button
        extract_label = QLabel("Это самая главная кнопка на форме, которая отвечает за основной функционал приложения.", self)
        extract_label.setWordWrap(True)

        language_layout = QVBoxLayout()
        self.language_combo = QComboBox(self)
        self.language_combo.addItem('Русский', 'rus')
        self.language_combo.addItem('English', 'eng')
        self.language_combo.setCurrentIndex(0)  # Выбран русский по умолчанию
        self.language_combo.currentIndexChanged.connect(self.language_changed)

        # Add label for language combo box
        language_label = QLabel("Этот выпадающий список отвечает за считывание текста с изображения на выбранном языке.", self)
        language_label.setWordWrap(True)

        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)

        right_layout.addLayout(language_layout)
        right_layout.addWidget(self.text_browser)
        right_layout.addWidget(extract_label)
        right_layout.addWidget(self.extract_text_button)

        self.copy_button = QPushButton('Скопировать', self)
        self.copy_button.clicked.connect(self.copy_text)

        # Add label for copy button
        copy_label = QLabel("Вы можете скопировать текст, который выводит приложение.", self)
        copy_label.setWordWrap(True)

        self.save_button = QPushButton('Сохранить текст', self)
        self.save_button.clicked.connect(self.save_text)

        # Add label for save button
        save_label = QLabel("Возможность сохранить текст, поможет вам легче работать с приложением.", self)
        save_label.setWordWrap(True)

        right_layout.addWidget(copy_label)
        right_layout.addWidget(self.copy_button)
        right_layout.addWidget(save_label)
        right_layout.addWidget(self.save_button)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        # Add a stretch to push the transition button to the right
        layout.addStretch()

        self.load_second_form_button = QPushButton('Перейти к приложению', self)
        self.load_second_form_button.clicked.connect(self.load_second_form)
        layout.addWidget(self.load_second_form_button, alignment=Qt.AlignBottom | Qt.AlignRight)

        self.setLayout(layout)

        self.image_path = None
        self.language = 'rus'  # По умолчанию установим русский язык



    def set_background_image(self):
        # Устанавливаем задний фон
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap(self.background_image_path)))
        self.setPalette(palette)

    def browse_image(self):
        options = QFileDialog.Options()
        image_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp);;All Files (*)", options=options)
        if image_path:
            self.image_path = image_path
            self.load_image(image_path)

    def load_image(self, image_path):
        max_width = 320
        max_height = 180

        img = QImage(image_path)
        if img.width() > max_width or img.height() > max_height:
            img = img.scaled(QSize(max_width, max_height), Qt.KeepAspectRatio)

        pixmap = QPixmap.fromImage(img)
        self.image_label.setPixmap(pixmap)

    def extract_text(self):
        if self.image_path:
            extracted_text = self.extract_text_from_image(self.image_path)
            self.text_browser.setPlainText(extracted_text)

    def extract_text_from_image(self, image_path):
        try:
            image = Image.open(image_path).convert("L")
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2)
            image = image.filter(ImageFilter.SMOOTH)
            image = image.filter(ImageFilter.SHARPEN)
            text = pytesseract.image_to_string(image, lang=self.language)

            return text
        except Exception as e:
            return str(e)

    def language_changed(self, index):
        lang_code = self.language_combo.currentData()
        self.language = lang_code

    def copy_text(self):
        extracted_text = self.text_browser.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(extracted_text)

    def save_text(self):
        extracted_text = self.text_browser.toPlainText()
        if extracted_text:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить текст", "", "Text Files (*.txt);;All Files (*)", options=options)
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(extracted_text)
        else:
            QMessageBox.warning(self, "Предупреждение", "Вы еще не извлекли никакого текста", QMessageBox.Ok)

    def load_second_form(self):
        self.second_form.show()
        self.hide()


class ImageUploader(QWidget):
    def __init__(self, background_image_path):
        super().__init__()

        self.background_image_path = background_image_path

        self.setWindowTitle('Приложение')
        self.setGeometry(100, 100, 600, 400)
        self.setFixedSize(1080, 675)

        layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Устанавливаем задний фон
        self.set_background_image()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setAcceptDrops(True)
        self.image_label.setFixedSize(320, 180)  # Фиксированный размер для отображения изображения

        self.browse_button = QPushButton('Выбрать изображение', self)
        self.browse_button.clicked.connect(self.browse_image)
        self.browse_button.setToolTip("Эта кнопка отвечает за выбор вашего изображения и отображение его в приложении.")

        left_layout.addWidget(self.image_label)
        left_layout.addWidget(self.browse_button)
        left_layout.addStretch(1)  # Добавляем пространство для равномерного размещения

        self.text_browser = QTextBrowser(self)
        self.text_browser.setReadOnly(True)

        self.extract_text_button = QPushButton('Извлечь текст', self)
        self.extract_text_button.clicked.connect(self.extract_text)
        self.extract_text_button.setToolTip("Это самая главная кнопка на форме, которая отвечает за основной функционал приложения.")

        language_layout = QVBoxLayout()
        self.language_combo = QComboBox(self)
        self.language_combo.addItem('Русский', 'rus')
        self.language_combo.addItem('English', 'eng')
        self.language_combo.setCurrentIndex(0)  # Выбран русский по умолчанию
        self.language_combo.currentIndexChanged.connect(self.language_changed)
        self.language_combo.setToolTip("Этот выпадающий список отвечает за считывание текста с изображения на выбранном языке.")
        language_layout.addWidget(self.language_combo)

        right_layout.addLayout(language_layout)
        right_layout.addWidget(self.text_browser)
        right_layout.addWidget(self.extract_text_button)

        self.copy_button = QPushButton('Скопировать', self)
        self.copy_button.clicked.connect(self.copy_text)
        self.copy_button.setToolTip("Вы можете скопировать текст, который выводит приложение.")

        self.save_button = QPushButton('Сохранить текст', self)
        self.save_button.clicked.connect(self.save_text)
        self.save_button.setToolTip("Возможность сохранить текст, поможет вам легче работать с приложением.")

        right_layout.addWidget(self.copy_button)
        right_layout.addWidget(self.save_button)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.setLayout(layout)

        self.image_path = None
        self.language = 'rus'  # По умолчанию установим русский язык

    def set_background_image(self):
        # Устанавливаем задний фон
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap(self.background_image_path)))
        self.setPalette(palette)

    def drop_image(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            image_path = mime_data.urls()[0].toLocalFile()
            if image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                self.load_image(image_path)
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def browse_image(self):
        options = QFileDialog.Options()
        image_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp);;All Files (*)", options=options)
        if image_path:
            self.image_path = image_path
            self.load_image(image_path)

    def load_image(self, image_path):
        max_width = 320
        max_height = 180

        img = QImage(image_path)
        if img.width() > max_width or img.height() > max_height:
            img = img.scaled(QSize(max_width, max_height), Qt.KeepAspectRatio)

        pixmap = QPixmap.fromImage(img)
        self.image_label.setPixmap(pixmap)

    def extract_text(self):
        if self.image_path:
            extracted_text = self.extract_text_from_image(self.image_path)
            self.text_browser.setPlainText(extracted_text)

    def extract_text_from_image(self, image_path):
        try:
            image = Image.open(image_path).convert("L")
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2)
            image = image.filter(ImageFilter.SMOOTH)
            image = image.filter(ImageFilter.SHARPEN)
            text = pytesseract.image_to_string(image, lang=self.language)

            return text
        except Exception as e:
            return str(e)

    def language_changed(self, index):
        lang_code = self.language_combo.currentData()
        self.language = lang_code

    def copy_text(self):
        extracted_text = self.text_browser.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(extracted_text)

    def save_text(self):
        extracted_text = self.text_browser.toPlainText()
        if extracted_text:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить текст", "", "Text Files (*.txt);;All Files (*)", options=options)
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(extracted_text)
        else:
            QMessageBox.warning(self, "Предупреждение", "Вы еще не извлекли никакого текста", QMessageBox.Ok)


def main():
    app = QApplication(sys.argv)
    second_form = ImageUploader('grad.jpg')
    first_form = FirstForm('grad.jpg', second_form)  # Pass the second form instance to the first form
    first_form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
