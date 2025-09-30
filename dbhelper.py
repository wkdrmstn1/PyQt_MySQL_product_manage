import pymysql

DB_CONFIG = dict(
    host = "localhost",
    user = "root",
    password = "20011030",
    database = "fruitdb",
    charset = "utf8"
)

class DB:
    def __init__(self,**config):
        self.config = config

    def connect(self):
        return pymysql.connect(**self.config)
    
    # 제품 조회
    def fetch_products(self):
        sql = "SELECT code, name, price, amount FROM products ORDER BY code"
        with self.connect() as con:
            with con.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
    
    # 제품 추가
    def add_product(self,code,name,price,amount):
        sql = "INSERT INTO products (code, name, price, amount) VALUES (%s, %s, %s, %s)"
        with self.connect() as con:
            try:
                with con.cursor() as cur:
                    cur.execute(sql,(code, name, price,amount))
                con.commit()
                return True
            
            except Exception as e:
                print(f"추가 실패 : {e}")
                con.rollback()
                return False
            
    # 제품 삭제 - 코드에 맞는 제품 삭제
    def delete_product(self, code):
        sql = "DELETE FROM products WHERE code = %s"
        with self.connect() as con:
            try:
                with con.cursor() as cur:
                    cur.execute(sql, (code,))
                con.commit() 
                
                print(f"제품코드 : '{code}'삭제")
                return True 

            except Exception as e:
                print(f"삭제 실패 : {e}")
                con.rollback() 
                return False

    # 제품 수정 - 개수 조정 
    def change_product(self, target_code, new_name, new_price,new_amount):
        sql = "UPDATE products SET name = %s, price = %s, amount = %s WHERE code = %s"    
        with self.connect() as con:
            try:
                with con.cursor() as cur:
                    cur.execute(sql,(new_name,new_price,new_amount,target_code))
                con.commit()

                print(f"제품코드 : '{target_code}'의 새로운 이름 '{new_name}'가격 '{new_price}' 개수'{new_amount}'")
                return True
            
            except Exception as e:
                print(f"수정 실패 : {e}")
                con.rollback()
                return False    
        
                
        