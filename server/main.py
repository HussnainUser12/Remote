from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QGroupBox, QAction
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import socket
import sys


class AdminApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MonitorMan - Admin Control Panel")
        self.setGeometry(100, 100, 600, 450)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #ffffff;
                font-family: 'Segoe UI';
            }
            QPushButton {
                background-color: #5dade2;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #f0f0f0;
                color: #000;
            }
            QLabel {
                font-size: 13px;
            }
        """)

        # Create Menu Bar
        self.create_menu_bar()

        self.status_label = QLabel("🟢 MonitorMan ready.")
        self.status_label.setFont(QFont('Segoe UI', 12))

        # ========== Target Client ========== #
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter Client IP (e.g. 192.168.0.4 or no-ip domain)")

        # ========== Controls ========== #
        self.lock_btn = QPushButton("🔒 Lock PC")
        self.stream_btn = QPushButton("🖥️ Stream Desktop")
        self.lock_btn.clicked.connect(lambda: self.send_command("lock"))
        self.stream_btn.clicked.connect(lambda: self.send_command("stream"))

        # ========== Website Block ========== #
        self.block_site_input = QLineEdit()
        self.block_site_input.setPlaceholderText("e.g. facebook.com")
        self.block_site_btn = QPushButton("🌐 Block Website")
        self.block_site_btn.clicked.connect(self.block_website)

        # ========== IP Block ========== #
        self.block_ip_input = QLineEdit()
        self.block_ip_input.setPlaceholderText("e.g. 192.168.1.20")
        self.block_ip_btn = QPushButton("🚫 Block IP")
        self.block_ip_btn.clicked.connect(self.block_ip)

        # ========== Group Boxes ========== #
        control_group = QGroupBox("Client Control")
        control_layout = QVBoxLayout()
        control_layout.addWidget(self.lock_btn)
        control_layout.addWidget(self.stream_btn)
        control_group.setLayout(control_layout)

        site_group = QGroupBox("Block Website")
        site_layout = QHBoxLayout()
        site_layout.addWidget(self.block_site_input)
        site_layout.addWidget(self.block_site_btn)
        site_group.setLayout(site_layout)

        ip_group = QGroupBox("Block IP Address")
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(self.block_ip_input)
        ip_layout.addWidget(self.block_ip_btn)
        ip_group.setLayout(ip_layout)

        # ========== Main Layout ========== #
        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Target Client IP:"))
        main_layout.addWidget(self.ip_input)
        main_layout.addWidget(control_group)
        main_layout.addWidget(site_group)
        main_layout.addWidget(ip_group)
        main_layout.addWidget(self.status_label)
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu('File')
        fullscreen_action = QAction('Full Screen', self)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        file_menu.addAction(fullscreen_action)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()  # Exit full screen
        else:
            self.showFullScreen()  # Enter full screen

    def send_command(self, command):
        try:
            client_ip = self.ip_input.text().strip()
            if not client_ip:
                self.status_label.setText("❌ Please enter a valid client IP.")
                return

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((client_ip, 9090))
            s.send(command.encode())
            self.status_label.setText(f"✅ Sent: {command}")
            s.close()
        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")

    def block_website(self):
        domain = self.block_site_input.text().strip()
        if domain:
            self.send_command(f"block {domain}")
        else:
            self.status_label.setText("❌ Please enter a domain to block.")

    def block_ip(self):
        ip = self.block_ip_input.text().strip()
        if ip:
            self.send_command(f"blockip {ip}")
        else:
            self.status_label.setText("❌ Please enter an IP address to block.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminApp()
    window.show()
    sys.exit(app.exec_())
