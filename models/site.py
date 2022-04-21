from sql_alchemy import database

class SiteModel(database.Model):
    __tablename__ = 'sites'
    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(40))
    url = database.Column(database.String(80))
    hotels = database.relationship('HotelModel')


    def __init__(self, name, url):
        self.name = name
        self.url = url


    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'hotels': [hotel.json() for hotel in self.hotels]
        }


    @classmethod
    def find(cls, id):
        # SELECT * FROM hotels WHERE id = :id
        site = cls.query.filter_by(id=id).first()
        if site:
            return site
        return None


    @classmethod
    def find_by_url(cls, url):
        # SELECT * FROM hotels WHERE url = :url
        site = cls.query.filter_by(url=url).first()
        if site:
            return site
        return None


    def save(self):
        database.session.add(self)
        database.session.commit()


    def delete(self):
        # deletando todos os hoteis do site
        [hotel.delete() for hotel in self.hotels]

        database.session.delete(self)
        database.session.commit()