import sqlite3

def conexaocombanco():
    banco = sqlite3.connect("cadastros.db")
    cursor = banco.cursor()

    cursor.execute("CREATE TABLE IF NOT Exists Pessoas (ID INTEGER PRIMARY KEY AUTOINCREMENT, Nome TEXT, Email TEXT, Senha TEXT, Nascimento DATE)")

    print("Conexão realizada com sucesso. Ref=cadastros.db!")
