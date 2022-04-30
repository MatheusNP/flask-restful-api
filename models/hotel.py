from sql_alchemy import database

class HotelModel(database.Model):
    __tablename__ = 'hotels'
    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(80))
    grade = database.Column(database.Float(precision = 1))
    daily = database.Column(database.Float(precision = 2))
    city = database.Column(database.String(40))
    site_id = database.Column(database.Integer, database.ForeignKey('sites.id'))


    def __init__(self, name, grade, daily, city, site_id):
        self.name = name
        self.grade = grade
        self.daily = daily
        self.city = city
        self.site_id = site_id


    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'grade': self.grade,
            'daily': self.daily,
            'city': self.city,
            'site_id': self.site_id
        }


    @classmethod
    def find(cls, id):
        # SELECT * FROM hotels WHERE id = :id
        hotel = cls.query.filter_by(id=id).first()
        if hotel:
            return hotel
        return None


    @classmethod
    def findByName(cls, name):
        # SELECT * FROM hotels WHERE name = :name
        hotel = cls.query.filter_by(name=name).first()
        if hotel:
            return hotel
        return None


    def save(self):
        database.session.add(self)
        database.session.commit()


    def update(self, name, grade, daily, city, site_id):
        self.name = name
        self.grade = grade
        self.daily = daily
        self.city = city
        self.site_id = site_id


    def delete(self):
        database.session.delete(self)
        database.session.commit()