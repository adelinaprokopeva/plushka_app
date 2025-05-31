from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
from database import register_user


class RegistrationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setFixedSize(400, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Регистрация нового пользователя")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")

        self.name_input = QLineEdit(placeholderText="Ваше имя")
        self.email_input = QLineEdit(placeholderText="Email")
        self.password_input = QLineEdit(placeholderText="Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Студент", "Преподаватель", "Администратор"])

        btn_register = QPushButton("Зарегистрироваться")
        btn_register.setStyleSheet("padding: 10px; background: #2196F3; color: white;")
        btn_register.clicked.connect(self.process_registration)

        layout.addWidget(title)
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Роль:"))
        layout.addWidget(self.role_combo)
        layout.addWidget(btn_register)

        self.setLayout(layout)

    def process_registration(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        role = self.role_combo.currentText().lower()

        if not all([name, email, password]):
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения")
            return

        user_id = register_user(name, email, password, role)
        if user_id > 0:
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно!\nТеперь вы можете войти.")
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось зарегистрироваться.\nВозможно, email уже занят.")