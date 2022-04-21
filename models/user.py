from sql_alchemy import database

class UserModel(database.Model):
    __tablename__ = 'users'
    id = database.Column(database.Integer, primary_key = True)
    login = database.Column(database.String(40))
    password = database.Column(database.String(40))


    def __init__(self, login, password):
        self.login = login
        self.password = password


    def json(self):
        return {
            'id': self.id,
            'login': self.login
        }


    @classmethod
    def find(cls, id):
        # SELECT * FROM users WHERE id = :id
        user = cls.query.filter_by(id=id).first()
        if user:
            return user
        return None


    @classmethod
    def find_by_login(cls, login):
        # SELECT * FROM users WHERE login = :login
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None


    def save(self):
        database.session.add(self)
        database.session.commit()


    def delete(self):
        database.session.delete(self)
        database.session.commit()