import sqlite3

class ConfigDatabase:
    def __init__(self, db_name) -> None:
        self.db_name = db_name
        connection = sqlite3.connect(f'{db_name}.db')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Config (
            id INTEGER PRIMARY KEY,
            var_name TEXT NOT NULL,
            var_val TEXT NOT NULL)
        ''')
        connection.commit()
        connection.close()

    def add_var(self, var_name, var_value):
        connection = sqlite3.connect(f'{self.db_name}.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Config WHERE var_name = ?',(var_name,))
        if(cursor.fetchall()):
            cursor.execute('UPDATE Config SET var_val = ? WHERE var_name = ?', (var_value, var_name))
        else:
            cursor.execute('INSERT INTO Config (var_name, var_val) VALUES (?, ?)', (var_name, var_value))
        connection.commit()
        connection.close()

    def get_var(self, var_name):
        connection = sqlite3.connect(f'{self.db_name}.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Config WHERE var_name = ?',(var_name,))
        res = cursor.fetchall()
        connection.commit()
        connection.close()
        return(res[0][2] if res else None )
    
