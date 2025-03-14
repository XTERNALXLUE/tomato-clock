import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog,
    QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound

from config import TomatoConfig
from timer import TomatoTimer
from ui.tomato import Ui_MainWindow


class TomatoWindow(QMainWindow, Ui_MainWindow):
    """番茄钟主窗口类"""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(640, 360)
        self.timer = TomatoTimer()
        self.qt_timer = None
        self.tray_icon = None
        
        self._init_ui()
        self._init_timer()
        self._init_tray()
        self._update_display()

    def _init_ui(self):
        """初始化UI"""
        self.setWindowIcon(QIcon(TomatoConfig.ICON_PATH))
        self.set_background_img()
        
        # 连接按钮信号
        self.button_start.clicked.connect(self.start_time)
        self.button_stop.clicked.connect(self.stop_time)
        self.button_finish.clicked.connect(self.finish_time)
        self.button_setbackground.clicked.connect(self.set_background)

    def _init_timer(self):
        """初始化计时器"""
        self.qt_timer = QTimer(self)
        self.qt_timer.timeout.connect(self.update_time)

    def _init_tray(self):
        """初始化系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(TomatoConfig.ICON_PATH))
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        tray_menu = QMenu()
        show_action = QAction("显示", self)
        quit_action = QAction("退出", self)
        show_action.triggered.connect(self.show_window)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def _update_display(self):
        """更新显示"""
        if self.timer.is_break:
            self.text.setText("      休息时间...")
        else:
            self.text.setText(f"已完成 {self.timer.total_times} 次番茄时间")
            
        minutes, seconds = divmod(self.timer.remaining_time, 60)
        self.time_remain.setText(f"{minutes:02}:{seconds:02}")

    def start_time(self):
        """开始计时"""
        self.button_start.setEnabled(False)
        self.button_stop.setEnabled(True)
        self.button_finish.setEnabled(True)
        self.timer.start_work()
        self.qt_timer.start(1000)
        
        self.tray_icon.showMessage(
            "番茄钟",
            "开始专注时间！",
            QSystemTrayIcon.Information,
            TomatoConfig.NOTIFICATION_DURATION
        )

    def update_time(self):
        """更新时间"""
        if self.timer.tick():
            self.qt_timer.stop()
            QSound.play(TomatoConfig.FINISH_SOUND_PATH)
            
            if self.timer.is_break:
                self.timer.start_work()
                self.qt_timer.start(1000)
            else:
                self.timer.start_break()
                self.show()
                self.showNormal()
                self.qt_timer.start(1000)
                
        self._update_display()

    def stop_time(self):
        """暂停/继续计时"""
        if self.button_stop.text() == "暂停":
            self.button_stop.setText("继续")
            self.qt_timer.stop()
        else:
            self.button_stop.setText("暂停")
            self.qt_timer.start()

    def finish_time(self):
        """结束当前番茄钟"""
        self.qt_timer.stop()
        self.timer.reset()
        self.button_start.setEnabled(True)
        self.button_stop.setEnabled(False)
        self.button_finish.setEnabled(False)
        self._update_display()

    def set_background(self):
        """设置背景图片"""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        
        if file_dialog.exec_():
            source_file = file_dialog.selectedFiles()[0]
            img_dir = os.path.join(os.getcwd(), TomatoConfig.IMG_DIR)
            os.makedirs(img_dir, exist_ok=True)
            _, ext = os.path.splitext(source_file)
            target_file = os.path.join(img_dir, f'background{ext}')
            shutil.copy(source_file, target_file)
            self.set_background_img()

    def set_background_img(self):
        """设置背景图片样式"""
        img_dir = os.path.join(os.getcwd(), TomatoConfig.IMG_DIR)
        if os.path.exists(img_dir):
            for ext in ['.png', '.jpg', '.jpeg', '.bmp']:
                bg_path = os.path.join(img_dir, f'background{ext}').replace('\\', '/')
                if os.path.exists(bg_path):
                    self.setStyleSheet(f"""
                        QMainWindow {{
                            background-image: url({bg_path});
                            background-position: center;
                            background-repeat: no-repeat;
                        }}
                    """)

    def closeEvent(self, event):
        """处理关闭事件"""
        self.timer.reset()
        event.accept()
        self.quit_app()

    def changeEvent(self, event):
        """处理窗口状态改变事件"""
        if event.type() == event.WindowStateChange and self.isMinimized():
            self.hide()
            self.tray_icon.showMessage(
                "番茄钟",
                "程序已最小化到托盘！",
                QSystemTrayIcon.Information,
                TomatoConfig.NOTIFICATION_DURATION
            )

    def show_window(self):
        """显示窗口"""
        self.show()
        self.showNormal()

    def quit_app(self):
        """退出应用"""
        self.tray_icon.hide()
        QApplication.quit()

    def tray_icon_activated(self, reason):
        """处理托盘图标点击事件"""
        if reason == QSystemTrayIcon.Trigger:
            self.show_window() 