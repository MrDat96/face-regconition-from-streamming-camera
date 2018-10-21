from app import db

class CheckInStatus(db.Model):
    __tablename__ = 'checkin_status'

    checkin_status_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self, checkin_status_id, name):
        self.checkin_status_id = checkin_status_id
        self.name = name

    @staticmethod
    def getCheckInStatus(status_id):
        return CheckInStatus.query.filter_by(checkin_status_id=status_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()