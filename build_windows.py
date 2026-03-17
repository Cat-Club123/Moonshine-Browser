import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QProgressBar, QPushButton, QVBoxLayout, QWidget
import time

class InstallerBuilder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Windows Installer Builder')
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel('Installation Steps:', self)
        self.progressBar = QProgressBar(self)
        self.startButton = QPushButton('Start Installation', self)
        self.startButton.clicked.connect(self.startInstallation)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progressBar)
        layout.addWidget(self.startButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def startInstallation(self):
        self.label.setText('Installing...')
        total_steps = 5
        self.progressBar.setMaximum(total_steps)
        for i in range(total_steps):
            time.sleep(1)  # Simulate each installation step
            self.progressBar.setValue(i + 1)
        self.label.setText('Installation Complete!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InstallerBuilder()
    ex.show()
    sys.exit(app.exec_())
