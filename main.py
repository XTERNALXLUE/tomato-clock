import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
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
        self.times

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

    def update_time(self):
        self.remaining_time -= 1
        if self.remaining_time <= 0:
            self.timer.stop()
            self.time_remain.setText("00:00")
            
            # 判断是否在休息时间
            if self.text.text() == "      休息时间...":
                QSound.play('music/finish.wav')  # 休息结束时也播放提示音
                self.text.setText(f"已完成 {self.times} 次番茄时间")
                self.start_time()
                return 
                
            # 番茄钟结束，开始休息
            with open("record.txt", 'r+') as f:
                try:
                    self.times = int(f.read())
                except ValueError:
                    self.times = 0
                self.times += 1
                f.seek(0)
                f.write(str(self.times))
            self.text.setText(f"已完成 {self.times} 次番茄时间")
            QSound.play('music/finish.wav')
            # 设置5分钟休息时间
            self.remaining_time = 5 * 60 # 5分钟休息
            self.time_remain.setText("05:00")
            self.text.setText("      休息时间...")
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


app = QApplication(sys.argv)
window = MainWindow()
window.setWindowTitle("番茄钟")
window.show()
app.exec()
