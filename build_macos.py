import sys
from PyQt5.QtWidgets import ( QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, )

class InstallerBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('macOS Installer Builder')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel('Installation Steps')
        layout.addWidget(self.label)

        self.progress = QProgressBar(self)
        layout.addWidget(self.progress)

        self.btnStart = QPushButton('Start Installation', self)
        self.btnStart.clicked.connect(self.startInstallation)
        layout.addWidget(self.btnStart)

        self.setLayout(layout)

    def startInstallation(self):
        self.progress.setValue(0)
        for i in range(1, 101):
            self.progress.setValue(i)
            QApplication.processEvents()  # Update the GUI
            QThread.sleep(1)  # Simulate work being done

if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = InstallerBuilder()
    exe.show()
    sys.exit(app.exec_())