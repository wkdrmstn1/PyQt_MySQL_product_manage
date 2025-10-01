import sys
from PyQt5.QtWidgets import *
from login import LoginDialog
from main_window import MainWindow

# 로그인창으로 실행
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginDialog()

    if login.exec_() == LoginDialog.Accepted:
        w = MainWindow()
        w.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
'''
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
