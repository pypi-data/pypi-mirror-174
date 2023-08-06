# database che gestisce gli utenti iscritti
import sqlite3


class UserDB():
    def __init__(self, name):
        self.db_name = f"{name}.db"
        #self.table_name = name
        self.generate_user_table()

    def run_query(self, query):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        con.close()

    def generate_user_table(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS
                    users(ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    USERNAME TEXT NOT NULL UNIQUE, EMAIL TEXT NOT NULL,
                    PASSWORD TEXT NOT NULL, NAME TEXT NOT NULL, GENDER TEXT NOT NULL,
                    AGE INTEGER NOT NULL);""")
        con.commit()
        con.close()

    def add_user(self, args):
        # mettere lista
        #[username, email, password, name, gender, age]
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute(f"""INSERT INTO users(USERNAME, EMAIL, PASSWORD, NAME, GENDER, AGE)
                     VALUES('{args[0]}', '{args[1]}', '{args[2]}', '{args[3]}', '{args[4]}', '{int(args[5])}');""")
        con.commit()
        con.close()

    def delete_user(self, user_id):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        #cur.execute(f"DELETE from users WHERE USERNAME = '{user_id}'")
        cur.execute("DELETE from users WHERE USERNAME = %s;", (user_id, ))
        con.commit()
        con.close()

    def update_user(self, name, value, username):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        #cur.execute("UPDATE users SET %()s = %()s WHERE USERNAME = %s;", dict)
        if name == "AGE":
            values = (value, username)
            cur.execute("UPDATE users SET AGE = ? WHERE USERNAME = ?;", values)
        if name == "NAME":
            values = (value, username)
            cur.execute("UPDATE users SET NAME=? WHERE USERNAME = ?;", values)
        if name == "USERNAME":
            values = (value, username)
            cur.execute("UPDATE users SET USERNAME=? WHERE USERNAME = ?;", values)
        if name == "EMAIL":
            values = (value, username)
            cur.execute("UPDATE users SET EMAIL=? WHERE USERNAME = ?;", values)
        if name == "PASSWORD":
            values = (value, username)
            cur.execute("UPDATE users SET PASSWORD=? WHERE USERNAME = ?;", values)
        if name == "GENDER":
            values = (value, username)
            cur.execute("UPDATE users SET GENDER=? WHERE USERNAME = ?;", values)
        else:
            pass
        
        con.commit()
        con.close()

    def get_user_info(self, username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.execute("SELECT USERNAME, NAME, GENDER, AGE FROM users WHERE USERNAME = ?;", (username, ))
        rows = cursor.fetchall()
        res = rows[0]
        user_data = {
            "username": res[0], 
            "name": res[1], 
            "gender": res[2], 
            "age": res[3]
        }
        conn.commit()
        conn.close()
        return user_data

    def get_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.execute("SELECT USERNAME, NAME, GENDER, AGE FROM users;")
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows


    def testout(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.execute("SELECT * FROM users;")
        for row in cursor:
            print(row)
        conn.commit()
        conn.close()