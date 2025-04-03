import sqlite3 as sl


def create_new_db():
    with sl.connect('alibaba.db') as db:
        cursor = db.cursor()

        cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY,
                            tg_id INT NOT NULL UNIQUE,
                            name_user TEXT,
                            first_name TEXT,
                            last_name TEXT,
                            language TEXT,
                            page INT DEFAULT 1,
                            page_now INT DEFAULT 1,
                            work_table TEXT
                        )""")

        cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS tables (
                            table_id INTEGER PRIMARY KEY,
                            name_table TEXT,
                            name_product TEXT DEFAULT 'пусто',
                            description_table TEXT DEFAULT 'пусто',
                            update_date DATE,
                            user_id INT,
                            result TEXT DEFAULT 'пусто',
                            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                        )""")

        cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS table_contents (
                            table_contents INTEGER PRIMARY KEY,
                            text TEXT,
                            first_price DECIMAL(10, 2) DEFAULT 0,
                            second_price DECIMAL(10, 2) DEFAULT 0,
                            third_price DECIMAL(10, 2) DEFAULT 0,
                            finally_price DECIMAL(10, 2) DEFAULT 0,
                            min_order INT, 
                            delivery DECIMAL(10, 2) DEFAULT 0,
                            href TEXT, 
                            img BLOB, 
                            company TEXT, 
                            country TEXT, 
                            first_quantity INT DEFAULT inf, 
                            second_quantity INT DEFAULT inf, 
                            third_quantity INT DEFAULT inf,
                            finally_quantity INT DEFAULT inf,
                            table_id INT,
                            FOREIGN KEY (table_id) REFERENCES tables (table_id) ON DELETE CASCADE
                        )""")

        cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS state_machine (
                            previous_step TEXT,
                            this_step TEXT, 
                            user_id INT,
                            FOREIGN KEY (user_id) REFERENCES users (user_id)
                        )""")

        db.commit()


create_new_db()

