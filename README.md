# 番茄钟（基于Pyqt5）

一个基于 PyQt5 的番茄工作法计时器应用，支持背景图片自定义、系统托盘、休息提醒等功能

![img_demo2](./img/img_demo2.png)

![img_demo3](./img/img_demo3.png)

## 功能特点

- 25分钟工作时间计时
- 智能休息提醒（5分钟短休息/25分钟长休息）
- 连续完成4个番茄钟后自动进入25分钟长休息
- 自定义背景图片（支持 png/jpg/jpeg/bmp）
- 系统托盘支持（最小化/显示/退出）
- 计时结束提示音
- 计时记录本地保存

## 项目结构

project/</br>
│</br>
├── main.py          # 主程序</br>
├── ui/</br>
│   └── tomato.py    # UI文件</br>
├── img/</br>
│   ├── icon.png     # 程序图标</br>
│   └── background.* # 背景图片（可选）</br>
├── music/</br>
│   └── finish.wav   # 提示音效</br>
├── record.txt       # 记录完成次数</br>
├── requirements.txt # 项目依赖</br>
└── README.md        # 项目说明</br>

## 运行环境

- Python 3.6+
- PyQt5 及相关依赖

## 快速开始

1. 克隆或下载项目到本地
2. 创建并激活虚拟环境（推荐）

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行程序
```bash
python main.py
```

## 使用说明

- **开始计时**：点击"开始"按钮，开始25分钟的专注时间
- **暂停/继续**：点击"暂停"或"继续"按钮控制计时
- **结束番茄钟**：点击"结束"按钮终止当前计时
- **设置背景图片**：点击"设置背景"按钮，选择图片（支持 png/jpg/jpeg/bmp）
- **最小化到托盘**：点击最小化按钮，程序会隐藏到系统托盘
- **显示主窗口**：单击托盘图标可重新显示程序窗口
- **退出程序**：点击关闭按钮或托盘菜单中的"退出"

## 特色功能

- **智能休息提醒**：每个番茄钟结束后自动进入休息时间
- **连续计数**：连续完成4个番茄钟后自动延长休息时间至25分钟
- **自动显示**：番茄钟或休息时间结束时，如果窗口最小化会自动显示
- **进度保存**：自动记录累计完成的番茄钟数量

## 注意事项

- 提示音效必须是 WAV 格式
- 更换背景图片时建议保持与当前背景图片相同的格式
- 连续番茄钟计数在手动结束或关闭程序后会重置

## 贡献

欢迎提交 Issue 和 Pull Request

## 许可

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件