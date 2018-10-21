from app import db

class Room(db.Model):
    __tablename__ = 'room'

    room_id = db.Column(db.String(10), primary_key = True)
    name = db.Column(db.String(50))
    position = db.Column(db.String(50))
    building = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, room_id, name, position, building):
        self.room_id = room_id
        self.name = name
        self.position = position
        self.building = building

    @staticmethod
    def get_all():
        return Room.query.all()

    @staticmethod
    def get_room_by_id(room_id):
        return Room.query.filter_by(room_id=room_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()