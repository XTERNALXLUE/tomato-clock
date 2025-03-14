import sys
from PyQt5.QtWidgets import QApplication
from window import TomatoWindow


def main():
    app = QApplication(sys.argv)
    window = TomatoWindow()
    window.setWindowTitle("番茄钟")
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()