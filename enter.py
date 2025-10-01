# 타이틀 화면 제작
from PyQt5.QtWidgets import *

class Enter(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("제품 관리")
        
