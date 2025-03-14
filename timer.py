from config import TomatoConfig


class TomatoTimer:
    """番茄钟计时器类"""
    def __init__(self):
        self.remaining_time = TomatoConfig.WORK_TIME
        self.is_break = False
        self.continuous_times = 0
        self.total_times = 0
        self._load_total_times()

    def _load_total_times(self):
        """从文件加载总计完成次数"""
        try:
            with open(TomatoConfig.RECORD_FILE_PATH, 'r+') as f:
                try:
                    self.total_times = int(f.read())
                except ValueError:
                    self.total_times = 0
                    f.seek(0)
                    f.write('0')
        except FileNotFoundError:
            with open(TomatoConfig.RECORD_FILE_PATH, 'w') as f:
                f.write('0')

    def save_total_times(self):
        """保存总计完成次数到文件"""
        with open(TomatoConfig.RECORD_FILE_PATH, 'w') as f:
            f.write(str(self.total_times))

    def reset(self):
        """重置计时器"""
        self.remaining_time = TomatoConfig.WORK_TIME
        self.is_break = False
        self.continuous_times = 0

    def tick(self):
        """计时器计时，返回是否结束"""
        self.remaining_time -= 1
        return self.remaining_time <= 0

    def start_break(self):
        """开始休息时间"""
        self.is_break = True
        self.continuous_times += 1
        self.total_times += 1
        self.save_total_times()
        
        if self.continuous_times % TomatoConfig.LONG_BREAK_INTERVAL == 0:
            self.remaining_time = TomatoConfig.LONG_BREAK
        else:
            self.remaining_time = TomatoConfig.SHORT_BREAK

    def start_work(self):
        """开始工作时间"""
        self.is_break = False
        self.remaining_time = TomatoConfig.WORK_TIME 