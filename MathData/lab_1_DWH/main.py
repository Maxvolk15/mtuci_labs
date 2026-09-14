import duckdb
con = duckdb.connect("bank.duckdb")
print(con.sql("call start_ui()"))
input("Тапни для закрытия")