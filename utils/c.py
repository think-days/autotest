import pymysql

db = pymysql.connect(
    host="10.90.18.11",
    port=3306,
    user="dbdgj",
    password="nP8gKlCGBFSZNOFl",
    database="dgj"
)
cursor = db.cursor()
cursor.execute("SELECT * FROM t_scm_po_order WHERE billNo='PO1175220830182344171'")
res = cursor.fetchone()
cursor.execute("SELECT count(*) FROM t_bs_goods_barcode WHERE itemCode='1601000498'")
a = cursor.fetchone()

db.commit()
print(res)
print(a)
db.close()
