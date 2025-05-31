from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from database import register_for_event, is_registered_for_event


class EventsWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Афиша мероприятий")
        self.setFixedSize(800, 600)
        self.setup_ui()
        self.check_registration_status()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок мероприятия
        title = QLabel("Бал ОмГТУ")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Изображение мероприятия
        image = QLabel()
        try:
            pixmap = QPixmap("event1.jpg").scaled(
                600, 400,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            image.setPixmap(pixmap)
        except:
            image.setText("Изображение не найдено")
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Описание мероприятия
        description = QLabel("""
        <div style='font-size: 16px; color: #34495e;'>
            <p><b>Дата:</b> 23 мая 2025</p>
            <p><b>Место:</b> Ангар</p>
            <p style='margin-top: 15px;'>
            Давно хотели окунуться в любимую сказку? Тогда это точно для вас! 
            Совсем скоро состоится студенческий бал ОмГТУ «В гостях у сказки», 
            поэтому не упустите шанс стать частью сказочной истории!
            </p>
        </div>
        """)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)

        # Кнопка записи
        self.btn_attend = QPushButton("Я пойду!")
        self.btn_attend.setStyleSheet("""
            QPushButton {
                padding: 15px;
                font-size: 16px;
                background: #e74c3c;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: #c0392b;
            }
            QPushButton:disabled {
                background: #95a5a6;
            }
        """)
        self.btn_attend.clicked.connect(self.register_attendance)

        # Кнопка назад
        btn_back = QPushButton("Назад")
        btn_back.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: #bdc3c7;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: #95a5a6;
            }
        """)
        btn_back.clicked.connect(self.go_back)

        # Компоновка элементов
        layout.addWidget(title)
        layout.addWidget(image)
        layout.addWidget(description)
        layout.addWidget(self.btn_attend, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)

    def check_registration_status(self):
        """Проверяет статус записи и обновляет кнопку"""
        if is_registered_for_event(self.user_id):
            self.btn_attend.setText("Вы уже идёте!")
            self.btn_attend.setDisabled(True)

    def register_attendance(self):
        """Обработчик записи на мероприятие"""
        try:
            if register_for_event(self.user_id):
                QMessageBox.information(
                    self,
                    "Успех",
                    "Вы успешно записаны на мероприятие!"
                )
                self.check_registration_status()
            else:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Не удалось записаться. Попробуйте позже."
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Произошла ошибка: {str(e)}"
            )

    def go_back(self):
        """Возврат в главное меню"""
        from ui.main_window import MainWindow
        self.main_window = MainWindow(self.user_id)
        self.main_window.show()
        self.close()