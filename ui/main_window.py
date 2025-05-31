from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Плюшка - Главная")
        self.setFixedSize(600, 400)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Главное меню")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 40px;")

        btn_events = QPushButton("Афиша мероприятий")
        btn_events.setStyleSheet("padding: 15px; font-size: 16px;")
        btn_events.clicked.connect(self.show_events)

        btn_profile = QPushButton("Мой профиль")
        btn_profile.setStyleSheet("padding: 15px; font-size: 16px;")
        btn_profile.clicked.connect(self.show_profile)

        layout.addWidget(title)
        layout.addWidget(btn_events)
        layout.addWidget(btn_profile)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_events(self):
        from ui.events_window import EventsWindow
        self.events_window = EventsWindow(self.user_id)
        self.events_window.show()
        self.close()

    def show_profile(self):
        from ui.profile_window import ProfileWindow
        self.profile_window = ProfileWindow(self.user_id)
        self.profile_window.show()
        self.close()