from app import db
from app.models.room import Room

class Camera(db.Model):
    __tablename__ = 'camera'

    camera_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(75))
    type = db.Column(db.String(75))
    http_gateway = db.Column(db.String(75))
    http_port = db.Column(db.Integer)
    rtsp_gateway = db.Column(db.String(75))
    rtsp_port = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    room_id = db.Column(db.String(10), db.ForeignKey('room.room_id'), nullable=False)

    def __init__(self, camera_id, name, type, http_gateway, http_port, rtsp_gateway, rtsp_port, room_id):
        """initialize with name."""
        self.camera_id = camera_id
        self.name = name
        self.type = type
        self.http_gateway = http_gateway
        self.http_port = http_port
        self.rtsp_gateway = rtsp_gateway
        self.rtsp_port = rtsp_port
        self.room_id = room_id

    @staticmethod
    def get_all_with_room():
        return db.session.query(Camera, Room).filter(Camera.room_id == Room.room_id).all()

    @staticmethod
    def get_all():
        return Camera.query.all()

    @staticmethod
    def get_camera_by_id(camera_id):
        return Camera.query.filter_by(camera_id=camera_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()