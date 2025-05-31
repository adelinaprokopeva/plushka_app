from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from database import update_profile, create_connection


class ProfileWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.photo_path = None

        # Инициализация UI
        self.init_ui()
        self.load_profile()

        # Настройка окна
        self.setWindowTitle("Мой профиль")
        self.setFixedSize(600, 500)

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        # Заголовок
        title = QLabel("Мой профиль")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Область с фото
        photo_container = QWidget()
        photo_layout = QVBoxLayout(photo_container)
        photo_layout.setContentsMargins(0, 0, 0, 0)

        self.photo_label = QLabel()
        self.photo_label.setFixedSize(200, 200)
        self.photo_label.setStyleSheet("""
            border: 2px dashed #aaa;
            border-radius: 5px;
            background-color: #f5f5f5;
        """)
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_add_photo = QPushButton("Добавить фото")
        btn_add_photo.setFixedWidth(200)
        btn_add_photo.clicked.connect(self.add_photo)

        photo_layout.addWidget(self.photo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        photo_layout.addWidget(btn_add_photo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Поля ввода
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите ваше имя")

        self.about_input = QTextEdit()
        self.about_input.setPlaceholderText("Расскажите о себе...")
        self.about_input.setMaximumHeight(100)

        # Кнопки
        btn_save = QPushButton("Сохранить изменения")
        btn_save.clicked.connect(self.save_profile)

        btn_back = QPushButton("Назад")
        btn_back.clicked.connect(self.go_back)

        # Компоновка элементов
        main_layout.addWidget(title)
        main_layout.addWidget(photo_container, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(QLabel("Имя:"))
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(QLabel("О себе:"))
        main_layout.addWidget(self.about_input)
        main_layout.addWidget(btn_save)
        main_layout.addWidget(btn_back)

        self.setLayout(main_layout)

    def add_photo(self):
        """Добавление фотографии профиля"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите фото", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.photo_path = file_path
            pixmap = QPixmap(file_path).scaled(
                200, 200,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.photo_label.setPixmap(pixmap)

    def load_profile(self):
        """Загрузка данных профиля из БД"""
        conn = create_connection()
        if not conn:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить профиль")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, about, photo FROM users WHERE id = ?",
                (self.user_id,)
            )
            data = cursor.fetchone()

            if data:
                self.name_input.setText(data[0] if data[0] else "")
                self.about_input.setPlainText(data[1] if data[1] else "")

                if data[2]:  # Если есть фото в БД
                    pixmap = QPixmap()
                    pixmap.loadFromData(data[2])
                    self.photo_label.setPixmap(
                        pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
                    )
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить профиль:\n{str(e)}")
        finally:
            conn.close()

    def save_profile(self):
        """Сохранение изменений профиля"""
        name = self.name_input.text().strip()
        about = self.about_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым")
            return

        try:
            success = update_profile(
                user_id=self.user_id,
                name=name,
                about=about,
                photo_path=self.photo_path
            )

            if success:
                QMessageBox.information(self, "Успех", "Профиль успешно сохранен!")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось сохранить изменения")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при сохранении:\n{str(e)}")

    def go_back(self):
        """Возврат в главное меню"""
        from ui.main_window import MainWindow
        self.main_window = MainWindow(self.user_id)
        self.main_window.show()
        self.close()