from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QFont
import socket
import sys

class ClientApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MonitorMan - Client Control Panel")
        self.setGeometry(200, 200, 400, 350)  # Increased window size for IP display
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: 'Segoe UI';
            }
            QPushButton {
                background-color: #3498db;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #34495e;
                color: #ecf0f1;
            }
            QLabel {
                font-size: 14px;
            }
        """)

        # Retrieve local IP address
        self.client_ip = self.get_local_ip()

        # Status Label
        self.status_label = QLabel("🟢 Client is running.")
        self.status_label.setFont(QFont('Segoe UI', 12))

        # IP Address Label
        self.ip_label = QLabel(f"📡 Client IP: {self.client_ip}")
        self.ip_label.setFont(QFont('Segoe UI', 12))

        # Controls Section
        self.lock_btn = QPushButton("🔒 Lock PC")
        self.lock_btn.clicked.connect(self.lock_system)

        self.block_site_input = QLineEdit()
        self.block_site_input.setPlaceholderText("Enter website to block")
        self.block_site_btn = QPushButton("🌐 Block Website")
        self.block_site_btn.clicked.connect(self.block_website)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter IP address to block")
        self.block_ip_btn = QPushButton("🚫 Block IP")
        self.block_ip_btn.clicked.connect(self.block_ip)

        # Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.ip_label)  # Display IP Address here
        main_layout.addWidget(self.lock_btn)

        site_layout = QHBoxLayout()
        site_layout.addWidget(self.block_site_input)
        site_layout.addWidget(self.block_site_btn)
        main_layout.addLayout(site_layout)

        ip_layout = QHBoxLayout()
        ip_layout.addWidget(self.ip_input)
        ip_layout.addWidget(self.block_ip_btn)
        main_layout.addLayout(ip_layout)

        self.setLayout(main_layout)

    def get_local_ip(self):
        """Returns the local IP address of the client."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0)
            s.connect(('10.254.254.254', 1))  # This can be any IP, it's just to get the local address
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            print(f"[‼️] Error getting local IP: {e}")
            return "Unavailable"

    def lock_system(self):
        self.status_label.setText("🔒 Locking system...")
        # You can add code here to lock the system

    def block_website(self):
        domain = self.block_site_input.text().strip()
        if domain:
            self.status_label.setText(f"🌐 Blocking website: {domain}")
            # Add code here to block the website

    def block_ip(self):
        ip = self.ip_input.text().strip()
        if ip:
            self.status_label.setText(f"🚫 Blocking IP: {ip}")
            # Add code here to block the IP

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec_())
