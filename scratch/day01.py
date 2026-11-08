import sqlite3
con = sqlite3.connect("../一季一鲜助农电商平台源代码/源代码/backend/db.sqlite")
for row in con.execute("SELECT id, name, price, stock FROM products LIMIT 3"):
    print(f"[{row[0]}] {row[1]}  {row[2]}  库存={row[3]}")
con.close()
