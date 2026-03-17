import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar
import time

class InstallerBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Linux Installer Builder')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel('Installation Progress:')
        layout.addWidget(self.label)

        self.progressBar = QProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        layout.addWidget(self.progressBar)

        self.startButton = QPushButton('Start Installation', self)
        self.startButton.clicked.connect(self.startInstallation)
        layout.addWidget(self.startButton)

        self.setLayout(layout)

    def startInstallation(self):
        for i in range(101):
            time.sleep(0.05)  # Simulate installation time
            self.progressBar.setValue(i)
            self.label.setText(f'Installing... {i}%')

        self.label.setText('Installation Complete!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InstallerBuilder()
    ex.show()
    sys.exit(app.exec_())