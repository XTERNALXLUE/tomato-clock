import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
from ui.tomato import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.remaining_time = 25 * 60
        self.setupUi(self)
        self.setFixedSize(640, 360)
        self.setWindowIcon(QIcon('img/icon.png'))
        self.set_background_img()
        self.init()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)  # 连接计时器的 timeout 信号到 update_time 方法
        self.button_start.clicked.connect(self.start_time)
        self.button_stop.clicked.connect(self.stop_time)
        self.button_finish.clicked.connect(self.finish_time)
        self.button_setbackground.clicked.connect(self.set_background)
        self.times = 0
        self.continuous_times = 0  # 添加连续计数器
        
        # 创建系统托盘
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('img/icon.png'))
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        # 创建托盘菜单
        tray_menu = QMenu()
        show_action = QAction("显示", self)
        quit_action = QAction("退出", self)
        show_action.triggered.connect(self.show_window)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def init(self):
        self.times = 0
        try:
            with open("record.txt", 'r+') as f:
                try:
                    self.times = int(f.read())
                except ValueError:
                    self.times = 0
                    f.write('0')
        except FileNotFoundError:
            with open("record.txt", 'w') as f:
                f.write('0')

        self.text.setText(f"已完成 {self.times} 次番茄时间")
        self.time_remain.setText("25:00")

    def start_time(self):
        self.button_start.setEnabled(False)
        self.button_stop.setEnabled(True)
        self.button_finish.setEnabled(True)
        self.remaining_time = 25 * 60
        self.time_remain.setText("25:00")
        self.timer.start(1000)  # 计时器每秒触发一次
        # 显示托盘气泡提示
        self.tray_icon.showMessage(
            "番茄钟",
            "开始专注时间！",
            QSystemTrayIcon.Information,
            3000  # 显示3秒
        )

    def update_time(self):
        self.remaining_time -= 1
        if self.remaining_time <= 0:
            self.timer.stop()
            self.time_remain.setText("00:00")
            
            # 判断是否在休息时间
            if self.text.text() == "      休息时间...":
                QSound.play('music/finish.wav')  # 休息结束时也播放提示音
                self.text.setText(f"已完成 {self.times} 次番茄时间")
                self.show()  # 显示窗口
                self.showNormal()  # 确保窗口不是最小化状态
                self.start_time()
                return 
                
            # 番茄钟结束，开始休息
            with open("record.txt", 'r+') as f:
                try:
                    self.times = int(f.read())
                except ValueError:
                    self.times = 0
                self.times += 1
                self.continuous_times += 1  # 增加连续计数
                f.seek(0)
                f.write(str(self.times))
            
            self.text.setText(f"已完成 {self.times} 次番茄时间")
            QSound.play('music/finish.wav')
            
            # 判断是否连续完成四个番茄钟
            if self.continuous_times % 4 == 0:
                # 设置25分钟休息时间
                self.remaining_time = 25 * 60
                self.time_remain.setText("25:00")
            else:
                # 设置5分钟休息时间
                self.remaining_time = 5 * 60
                self.time_remain.setText("05:00")
            
            self.text.setText("      休息时间...")
            self.show()
            self.showNormal()
            self.timer.start(1000)
        else:
            minutes, seconds = divmod(self.remaining_time, 60)
            self.time_remain.setText(f"{minutes:02}:{seconds:02}")

    def stop_time(self):
        if self.button_stop.text() == "暂停":
            self.button_stop.setText("继续")
            self.timer.stop()
        elif self.button_stop.text() == "继续":
            self.button_stop.setText("暂停")
            self.timer.start()

    def finish_time(self):
        self.timer.stop()
        self.text.setText(f"已完成 {self.times} 次番茄时间")
        self.time_remain.setText("25:00")
        self.button_start.setEnabled(True)
        self.button_stop.setEnabled(False)
        self.button_finish.setEnabled(False)
        self.continuous_times = 0  # 重置连续计数

    def set_background(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        
        if file_dialog.exec_():
            # 获取选择的文件路径
            source_file = file_dialog.selectedFiles()[0]
            
            # 先复制图片到img目录
            img_dir = os.path.join(os.getcwd(), 'img')
            os.makedirs(img_dir, exist_ok=True)
            _, ext = os.path.splitext(source_file)
            target_file = os.path.join(img_dir, f'background{ext}')
            shutil.copy(source_file, target_file)
            self.set_background_img()

    def set_background_img(self):
        img_dir = os.path.join(os.getcwd(), 'img')
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
        self.continuous_times = 0  # 关闭程序时重置连续计数
        event.accept()
        self.quit_app()

    def changeEvent(self, event):
        # 处理最小化事件
        if event.type() == event.WindowStateChange and self.isMinimized():
            self.hide()
            self.tray_icon.showMessage(
                "番茄钟",
                "程序已最小化到托盘！",
                QSystemTrayIcon.Information,
                3000
            )
    
    def quit_app(self):
        self.tray_icon.hide()  # 确保托盘图标被移除
        QApplication.quit()

    def show_window(self):
        self.show()
        self.showNormal()  # 确保窗口不是最小化状态

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show_window()  


app = QApplication(sys.argv)
window = MainWindow()
window.setWindowTitle("番茄钟")
window.show()
app.exec()
