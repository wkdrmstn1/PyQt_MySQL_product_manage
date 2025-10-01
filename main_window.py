from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
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
        self.input_code.setAlignment(Qt.AlignCenter)
        form_box1.addWidget(self.input_code)
        #grid_box.addWidget(self.input_code,0,0)
        self.input_code.setPlaceholderText("제품코드")
        
        self.input_name = QLineEdit()
        self.input_name.setAlignment(Qt.AlignCenter)
        form_box1.addWidget(self.input_name)
        #grid_box.addWidget(self.input_code,0,1)
        self.input_name.setPlaceholderText("제품명")
        
        self.input_price = QLineEdit()
        self.input_price.setAlignment(Qt.AlignCenter)
        form_box1.addWidget(self.input_price)
        #grid_box.addWidget(self.input_code,0,2)
        self.input_price.setPlaceholderText("가격")
        
        self.input_amount = QLineEdit()
        self.input_amount.setAlignment(Qt.AlignCenter)
        form_box1.addWidget(self.input_amount)
        #grid_box.addWidget(self.input_code,0,3)
        self.input_amount.setPlaceholderText("수량")


        # 버튼
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
        self.table.setStyleSheet("""
            QHeaderView::section {
                background-color: #FFFE91;
                color: black;
            } 
            QTableWidget::item:selected {
                background-color: #C3C3C3; 
                color: black;
            }
                                 """)
        
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # vbox.addLayout(grid_box)
        vbox.addLayout(form_box1)
        vbox.addWidget(self.table)
        vbox.addLayout(form_box2)
    
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
            if rows is None:
                rows = []
            self.table.setRowCount(len(rows))
            for r, (code, name, price, amount) in enumerate(rows):
                Center_code = QTableWidgetItem(str(code))
                Center_code.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r, 0, Center_code)

                Center_name = QTableWidgetItem(str(name))
                Center_name.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r, 1, Center_name)

                Center_price = QTableWidgetItem(str(price))
                Center_price.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r, 2, Center_price)

                Center_amount = QTableWidgetItem(str(amount))
                Center_amount.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r, 3, Center_amount)

            self.table.resizeColumnsToContents()
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)

            ####
            '''
            self.update_header_totals()
            '''

            count = len(str(price))
            if count >= 4:
                # 4자리수 이상이면 , 표기
                pass 
            
    # 제품 추가
    def add_product(self):
        code = self.input_code.text().strip().upper()
        name = self.input_name.text().strip().upper()
        price = self.input_price.text().strip().upper()
        amount = self.input_amount.text().strip().upper()
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
        target_code = self.input_code.text().strip().upper()
        new_name = self.input_name.text().strip().upper()
        new_price = self.input_price.text().strip().upper()
        new_amount = self.input_amount.text().strip().upper()

        if not target_code or not new_name or not new_price or not new_amount:
            QMessageBox.warning(self, "오류", "모든 필드를 입력해주세요.")
            return
        
        if target_code != self.selected_code:
            QMessageBox.critical(self,"실패","제품코드는 변경이 불가능합니다.")
            self.clear()
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

    def cell_clicked(self,row):
        code = self.table.item(row,0).text()
        name = self.table.item(row,1).text()
        price = self.table.item(row,2).text()
        amount = self.table.item(row,3).text()

        self.selected_code = code       # 제품코드변경 방지를 위한 code 저장 

        self.input_code.setText(code)
        self.input_name.setText(name)
        self.input_price.setText(price)
        self.input_amount.setText(amount)


    ####
    '''
    def update_header_totals(self):
        total_price = 0
        total_amount = 0

        for row in range(self.table.rowCount()):
            try:
                price_item = self.table.item(row,2)
                amount_item = self.table.item(row,3)

                if price_item and price_item.text():
                    price = int(price_item.text())
                    amount = int(amount_item.text())
                    total_price += price * amount

                if amount_item and amount_item.text():
                    total_amount += int(amount_item.text())
            
            except (ValueError, AttributeError):
                continue
        header_model = self.table.horizontalHeader().model()
        header_model.setHeaderData(2, Qt.Horizontal, f"가격\n(총: {total_price:,} 원)")
        header_model.setHeaderData(3, Qt.Horizontal, f"개수\n(총: {total_amount:,} 개)")
    '''
