import sqlite3


class BudgetManager:
    def __init__(self):
        self.conn = sqlite3.connect('/home/beresh/Documents/BudgetManager/DB/budget_manager.db')
        self.cur = self.conn.cursor()
        self.__create_tables()

    def __create_tables(self):

        create_users_table_query = '''CREATE TABLE IF NOT EXISTS users
                                (EMAIL TEXT PRIMARY KEY NOT NULL,
                                PASSWORD TEXT NOT NULL,
                                USERNAME TEXT NOT NULL,
                                BALANCE REAL NOT NULL)'''

        self.conn.execute(create_users_table_query)

        create_budget_table_query = '''CREATE TABLE IF NOT EXISTS income_expense
                                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                DATE TEXT NOT NULL,
                                CATEGORY TEXT NOT NULL,
                                INCOME REAL,
                                EXPENSE REAL,
                                USER_ID INTEGER)'''

        self.conn.execute(create_budget_table_query)

    def insert(self, item):
        insert_row_query = '''INSERT INTO income_expense VALUES(NULL,?,?,?,?,?)'''
        self.cur.execute(insert_row_query, item)
        self.conn.commit()

    def delete(self, row_id):
        delete_row_query = '''DELETE FROM income_expense WHERE id=?'''
        self.cur.execute(delete_row_query, (row_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def get_user_data(self, user_id, from_date, to_date):
        get_user_data_query = '''SELECT * FROM income_expense 
                                WHERE USER_ID=?
                                AND DATE BETWEEN ? and ?
                                ORDER BY DATE DESC'''
        self.cur.execute(get_user_data_query, (user_id, from_date, to_date))
        data = self.cur.fetchall()
        return data

    def insert_user(self, user):
        insert_user_query = '''INSERT INTO users VALUES(?,?,?,?)'''
        self.cur.execute(insert_user_query, user)
        self.conn.commit()

    def get_user_by_email(self, email):
        get_user_by_email_query = '''SELECT rowid, * FROM users WHERE EMAIL=?'''
        self.cur.execute(get_user_by_email_query, (email,))
        user = self.cur.fetchall()
        return user[0]

    def get_expenses_by_category(self, user_id, from_date, to_date):
        get_expenses_by_category_query = '''SELECT CATEGORY, sum(EXPENSE)
                                            FROM income_expense
                                            WHERE USER_ID=? 
                                            AND EXPENSE IS NOT ""
                                            AND date BETWEEN ? and ?
                                            GROUP BY CATEGORY
                                            '''
        self.cur.execute(get_expenses_by_category_query, (user_id, from_date, to_date))
        data = self.cur.fetchall()
        return data

    def get_income_by_category(self, user_id, from_date, to_date):
        get_income_by_category_query = '''SELECT CATEGORY, sum(INCOME)
                                            FROM income_expense
                                            WHERE USER_ID=? 
                                            AND INCOME IS NOT ""
                                            AND date BETWEEN ? and ?
                                            GROUP BY CATEGORY'''

        self.cur.execute(get_income_by_category_query, (user_id, from_date, to_date))
        data = self.cur.fetchall()
        return data


    def get_monthly_expense(self, user_id, from_date, to_date):
        get_monthly_expense_query = '''SELECT strftime('%m',DATE) month, sum(EXPENSE)
                                        FROM income_expense
                                        WHERE USER_ID = ?
                                        AND EXPENSE is not ""
                                        AND DATE BETWEEN ? and ?
                                        GROUP BY month'''

        self.cur.execute(get_monthly_expense_query, (user_id, from_date, to_date))
        data = self.cur.fetchall()
        return data
