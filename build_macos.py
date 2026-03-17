import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, QTextEdit
)
from PyQt5.QtCore import QThread, pyqtSignal
from pathlib import Path

class BuildThread(QThread):
    progress_update = pyqtSignal(int)
    log_update = pyqtSignal(str)
    finished = pyqtSignal()

    def run(self):
        try:
            self.log_update.emit("Starting macOS build...\n")
            self.progress_update.emit(10)
            
            # Build command for macOS
            script_path = os.path.join(os.path.dirname(__file__), "MoonshineBrowser.py")
            output_dir = os.path.join(os.path.dirname(__file__), "dist")
            
            self.log_update.emit("Building macOS app bundle with PyInstaller...\n")
            self.progress_update.emit(30)
            
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--onefile",
                "--name=MoonshineBrowser",
                "--osx-bundle-identifier=com.moonshine.browser",
                f"--distpath={output_dir}",
                "--specpath=build",
                "--buildpath=build",
                script_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            self.log_update.emit(result.stdout)
            self.progress_update.emit(70)
            
            if result.returncode == 0:
                self.log_update.emit("\n✓ Build successful!\n")
                self.log_update.emit(f"Application created at: {output_dir}/MoonshineBrowser\n")
                self.log_update.emit("To create a .dmg installer, use:\n")
                self.log_update.emit("$ hdiutil create -volname 'Moonshine Browser' -srcfolder ./dist -ov -format UDZO MoonshineBrowser.dmg\n")
                self.progress_update.emit(100)
            else:
                self.log_update.emit(f"\n✗ Build failed:\n{result.stderr}\n")
                self.progress_update.emit(0)
            
            self.finished.emit()
        except Exception as e:
            self.log_update.emit(f"\n✗ Error: {str(e)}\n")
            self.finished.emit()

class BuilderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.build_thread = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Moonshine Browser - macOS Installer Builder')
        self.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()

        title = QLabel('Moonshine Browser macOS Installer Builder')
        layout.addWidget(title)

        info = QLabel('Click "Start Build" to create a macOS executable')
        layout.addWidget(info)

        self.progressBar = QProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        layout.addWidget(self.progressBar)

        self.logText = QTextEdit(self)
        self.logText.setReadOnly(True)
        layout.addWidget(self.logText)

        self.startButton = QPushButton('Start Build', self)
        self.startButton.clicked.connect(self.startBuild)
        layout.addWidget(self.startButton)

        self.setLayout(layout)

    def startBuild(self):
        self.startButton.setEnabled(False)
        self.logText.clear()
        self.progressBar.setValue(0)
        
        self.build_thread = BuildThread()
        self.build_thread.progress_update.connect(self.updateProgress)
        self.build_thread.log_update.connect(self.updateLog)
        self.build_thread.finished.connect(self.buildFinished)
        self.build_thread.start()

    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def updateLog(self, message):
        self.logText.append(message)

    def buildFinished(self):
        self.startButton.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    builder = BuilderGUI()
    builder.show()
    sys.exit(app.exec_())