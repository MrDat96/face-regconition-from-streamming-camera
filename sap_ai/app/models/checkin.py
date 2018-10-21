from app import db
from app.models.user import User
from app.models.camera import Camera
from app.models.checkin_status import CheckInStatus

class CheckIn(db.Model):
    __tablename__ = 'checkin'

    user_id = db.Column(db.String(10), db.ForeignKey('user.user_id'), nullable=False, primary_key=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.camera_id'), nullable=False, primary_key=True)
    time_stamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    checkin_status_id = db.Column(db.Integer, db.ForeignKey('checkin_status.checkin_status_id'), nullable=False)

    def __init__(self, user_id, camera_id, time_stamp, checkin_status_id):
        """initialize with name."""
        self.user_id = user_id
        self.camera_id = camera_id
        self.time_stamp = time_stamp
        self.checkin_status_id = checkin_status_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return CheckIn.query.all()

    @staticmethod
    def get_all_with_user_camera_status():
        return db.session.query(CheckIn, User, Camera, CheckInStatus) \
                                .filter(CheckIn.user_id == User.user_id) \
                                .filter(CheckIn.camera_id == Camera.camera_id) \
                                .filter(CheckIn.checkin_status_id == CheckInStatus.checkin_status_id) \
                                .all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()