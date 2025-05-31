from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from database import check_credentials
from ui.main_window import MainWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в Плюшку")
        self.setFixedSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Добро пожаловать в Плюшку!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 30px;")

        self.email_input = QLineEdit(placeholderText="Email")
        self.password_input = QLineEdit(placeholderText="Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        btn_login = QPushButton("Войти")
        btn_login.setStyleSheet("padding: 10px; background: #4CAF50; color: white;")
        btn_login.clicked.connect(self.attempt_login)

        btn_register = QPushButton("Зарегистрироваться")
        btn_register.clicked.connect(self.show_registration)

        layout.addWidget(title)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)
        layout.addWidget(btn_login)
        layout.addWidget(btn_register)

        self.setLayout(layout)

    def attempt_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()

        user_id = check_credentials(email, password)
        if user_id > 0:
            self.main_window = MainWindow(user_id)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный email или пароль")

    def show_registration(self):
        from ui.registration_window import RegistrationWindow
        self.registration_window = RegistrationWindow()
        self.registration_window.show()