from PyQt5.QtWidgets import *
from dbhelper import DB, DB_CONFIG

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("제품 관리")
        self.db = DB(**DB_CONFIG)

        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)
        form_box1 = QHBoxLayout()
        form_box2 = QHBoxLayout()
        #grid_box = QGridLayout()
        
        # 상단 : 입력창, 버튼 
        self.input_code = QLineEdit()
        form_box1.addWidget(self.input_code)
        #grid_box.addWidget(self.input_code,0,0)
        self.input_code.setPlaceholderText("제품코드")
        self.input_name = QLineEdit()
        form_box1.addWidget(self.input_name)
        #grid_box.addWidget(self.input_code,0,1)
        self.input_name.setPlaceholderText("제품명")
        self.input_price = QLineEdit()
        form_box1.addWidget(self.input_price)
        #grid_box.addWidget(self.input_code,0,2)
        self.input_price.setPlaceholderText("가격")
        self.input_amount = QLineEdit()
        form_box1.addWidget(self.input_amount)
        #grid_box.addWidget(self.input_code,0,3)
        self.input_amount.setPlaceholderText("수량")

        self.btn_clear = QPushButton("초기화")
        self.btn_clear.clicked.connect(self.clear)
        form_box2.addWidget(self.btn_clear)
        self.btn_add = QPushButton("추가")
        self.btn_add.clicked.connect(self.add_product)
        form_box2.addWidget(self.btn_add)
        self.btn_change = QPushButton("수정")
        self.btn_change.clicked.connect(self.change_product)
        form_box2.addWidget(self.btn_change)
        self.btn_delete = QPushButton("삭제")
        self.btn_delete.clicked.connect(self.delete_product)
        form_box2.addWidget(self.btn_delete)

        # 중앙 : 테이블 위젯
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["제품코드", "제품명", "가격", "개수"])
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        #vbox.addLayout(grid_box)
        vbox.addLayout(form_box1)
        vbox.addLayout(form_box2)
        vbox.addWidget(self.table)

        self.load_products()

        self.table.cellClicked.connect(self.cell_clicked)

    def clear(self):
        self.input_code.clear()
        self.input_name.clear()
        self.input_price.clear()
        self.input_amount.clear()
        self.load_products()

    # 목록 불러오기
    def load_products(self):
            rows = self.db.fetch_products()
            self.table.setRowCount(len(rows))
            for r, (code, name, price, amount) in enumerate(rows):
                self.table.setItem(r,0,QTableWidgetItem(str(code)))
                self.table.setItem(r,1,QTableWidgetItem(str(name)))
                self.table.setItem(r,2,QTableWidgetItem(str(price)))
                self.table.setItem(r,3,QTableWidgetItem(str(amount)))
            self.table.resizeColumnsToContents()
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            

    # 제품 추가
    def add_product(self):
        code = self.input_code.text().strip()
        name = self.input_name.text().strip()
        price = self.input_price.text().strip()
        amount = self.input_amount.text().strip()
        if not code or not name or not price or not amount:
            QMessageBox.warning(self,"오류","제품코드, 제품명, 가격, 개수를 모두 입력해 주세요")
            return
        ok = self.db.add_product(code,name,price,amount)
        if ok:
            QMessageBox.information(self,"완료","추가완료")
            self.input_code.clear()
            self.input_name.clear()
            self.input_price.clear()
            self.input_amount.clear()
            self.load_products()
        else:
            QMessageBox.critical(self,"실패","추가 실패")

    # 제품 삭제
    def delete_product(self):
        code = self.input_code.text().strip()
        if not code:
            QMessageBox.warning(self,"오류","존재하지 않는 제품코드입니다")
            return
        ok = self.db.delete_product(code)
        if ok:
            QMessageBox.information(self,"완료","삭제완료")
            self.input_code.clear()
            self.input_name.clear()
            self.input_price.clear()
            self.input_amount.clear()
            self.load_products()
        else:
            QMessageBox.critical(self,"실패","삭제실패")

    # 제품 수정
    def change_product(self):
        target_code = self.input_code.text().strip()
        new_name = self.input_name.text().strip()
        new_price = self.input_price.text().strip()
        new_amount = self.input_amount.text().strip()

        if not target_code or not new_name or not new_price or not new_amount:
            QMessageBox.warning(self, "입력 오류", "모든 필드를 입력해주세요.")
            return
        ok = self.db.change_product(target_code,new_name,new_price,new_amount)
        if ok:
            QMessageBox.information(self,"완료","수정완료")
            self.input_code.clear()
            self.input_name.clear()
            self.input_price.clear()
            self.input_amount.clear()
            self.load_products()
        else:
            QMessageBox.critical(self,"실패","수정실패")

    def cell_clicked(self,row,col):
        code = self.table.item(row,0).text()
        name = self.table.item(row,1).text()
        price = self.table.item(row,2).text()
        amount = self.table.item(row,3).text()

        self.input_code.setText(code)
        self.input_name.setText(name)
        self.input_price.setText(price)
        self.input_amount.setText(amount)

