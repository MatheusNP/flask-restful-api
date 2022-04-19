from sql_alchemy import database

class HotelModel(database.Model):
    __tablename__ = 'hotels'
    id = database.Column(database.String, primary_key = True)
    name = database.Column(database.String(80))
    grade = database.Column(database.Float(precision = 1))
    daily = database.Column(database.Float(precision = 2))
    city = database.Column(database.String(40))


    def __init__(self, id, name, grade, daily, city):
        self.id = id
        self.name = name
        self.grade = grade
        self.daily = daily
        self.city = city


    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'grade': self.grade,
            'daily': self.daily,
            'city': self.city
        }


    @classmethod
    def find(cls, id):
        # SELECT * FROM hotels WHERE id = :id
        hotel = cls.query.filter_by(id=id).first()
        if hotel:
            return hotel
        return None


    def save(self):
        database.session.add(self)
        database.session.commit()


    def update(self, name, grade, daily, city):
        self.name = name
        self.grade = grade
        self.daily = daily
        self.city = city


    def delete(self):
        database.session.delete(self)
        database.session.commit()