class TomatoConfig:
    """番茄钟配置类"""
    WORK_TIME = 25 * 60  # 工作时间（秒）
    SHORT_BREAK = 5 * 60  # 短休息时间（秒）
    LONG_BREAK = 25 * 60  # 长休息时间（秒）
    LONG_BREAK_INTERVAL = 4  # 长休息间隔（番茄钟次数）
    NOTIFICATION_DURATION = 3000  # 通知显示时间（毫秒）

    # 资源路径配置
    ICON_PATH = 'img/icon.png'
    FINISH_SOUND_PATH = 'music/finish.wav'
    RECORD_FILE_PATH = 'record.txt'
    IMG_DIR = 'img'