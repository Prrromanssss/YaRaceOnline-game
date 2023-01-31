import sqlite3

from settings import DATABASE


class UserModel:
    @staticmethod
    def select_user(*, login):
        con = sqlite3.connect(DATABASE)
        request = f''' SELECT
                          coins, music, sounds,
                          record, password, id, selected_car
                      FROM user
                      WHERE login = '{login}'
                   '''
        data = con.execute(request).fetchall()
        con.commit()
        return data

    @staticmethod
    def select_user_value(*, key, value):
        con = sqlite3.connect(DATABASE)
        request = f'''SELECT
                          {key}
                      FROM user
                      WHERE {key} = '{value}'
                   '''
        data = con.execute(request).fetchall()
        con.commit()
        return data

    @staticmethod
    def update_user(*, login, key, value):
        con = sqlite3.connect(DATABASE)
        request = f'''UPDATE user
                      SET {key} = '{value}'
                      WHERE login = '{login}'
                   '''
        con.execute(request)
        con.commit()

    @staticmethod
    def delete_user(*, login):
        con = sqlite3.connect(DATABASE)
        request = f'''DELETE user
                      WHERE login = '{login}'
                    '''
        con.execute(request)
        con.commit()

    @staticmethod
    def insert_user(*, login, password):
        con = sqlite3.connect(DATABASE)
        request = f'''INSERT INTO user
                          ('login', 'password', selected_car, coins)
                      VALUES ('{login}', '{password}', 1, 0)
                   '''
        con.execute(request)
        con.commit()


users_model = UserModel()


class User:
    def __init__(self, login):
        self.login = login
        user_data = users_model.select_user(login=login)
        try:
            user_data = user_data[0]
            self.user_data = user_data
            self.coins = user_data[0]
            self.music = user_data[1]
            self.sounds = user_data[2]
            self.record = user_data[3]
            self.password = user_data[4]
            self.id = user_data[5]
            self.selected_car = user_data[6]
        except LookupError:
            self.user_data = user_data

    def __setitem__(self, key, value):
        self.__dict__[key] = value
        users_model.update_user(login=self.login, key=key, value=value)

    def __delitem__(self, key):
        users_model.delete_user(login=self.login)
        del self.__dict__[key]

    @property
    def all_data(self):
        return self.user_data