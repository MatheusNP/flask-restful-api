class HotelModel:
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