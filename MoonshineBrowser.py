import os

# --- Chromium / GPU tuning ---
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    "--enable-gpu-rasterization "
    "--enable-zero-copy "
    "--disable-http2 "
    "--ignore-certificate-errors "
)
os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QToolBar, QAction,
    QTabWidget, QFileDialog
)
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWebEngine import QtWebEngine

QtWebEngine.initialize()

HOME_HTML = """
<html>
<body style="background:#121212;color:white;font-family:Segoe UI;text-align:center">
<h1>🌙 Moonshine</h1>
<input style="width:60%;padding:12px;font-size:18px;border-radius:8px;border:none"
placeholder="Search or enter address"
onkeydown="if(event.key==='Enter'){location='https://duckduckgo.com/?q='+this.value}">
</body>
</html>
"""


class Moonshine(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Moonshine Browser")
        self.resize(1200, 800)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_urlbar)
        self.setCentralWidget(self.tabs)

        nav = QToolBar()
        self.addToolBar(nav)

        nav.addAction("◀", lambda: self.current().back())
        nav.addAction("▶", lambda: self.current().forward())
        nav.addAction("⟳", lambda: self.current().reload())

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate)
        nav.addWidget(self.urlbar)

        plus = QAction("+", self)
        plus.triggered.connect(self.add_tab)
        nav.addAction(plus)

        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.downloadRequested.connect(self.handle_download)
        self.profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/109 Safari/537.36"
        )
        self.profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)

        self.setStyleSheet("""
            QMainWindow { background:#121212; }
            QTabBar::tab { background:#222; color:white; padding:8px; }
            QTabBar::tab:selected { background:#333; }
            QToolBar { background:#1e1e1e; }
            QLineEdit { background:#2b2b2b; color:white; border-radius:6px; padding:6px; }
        """)

        self.add_tab()

    def current(self):
        return self.tabs.currentWidget()

    def add_tab(self):
        browser = QWebEngineView()
        browser.setHtml(HOME_HTML)
        i = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(i)
        browser.loadFinished.connect(lambda ok, b=browser: print("Loaded:", ok, b.url().toString()))

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def update_urlbar(self, i):
        browser = self.tabs.widget(i)
        if browser:
            self.urlbar.setText(browser.url().toString())

    def navigate(self):
        url = self.urlbar.text().strip()
        if not url.startswith("http"):
            url = "https://" + url
        self.current().setUrl(QUrl(url))

    def handle_download(self, item):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", item.path())
        if path:
            item.setPath(path)
            item.accept()


fmt = QSurfaceFormat()
fmt.setRenderableType(QSurfaceFormat.OpenGL)
fmt.setSwapBehavior(QSurfaceFormat.DoubleBuffer)
QSurfaceFormat.setDefaultFormat(fmt)

app = QApplication(sys.argv)
window = Moonshine()
window.show()
sys.exit(app.exec_())
