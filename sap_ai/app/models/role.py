from app import db

class Role(db.Model):
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key = True)
    power = db.Column(db.Integer, default=0)
    name = db.Column(db.String(75))

    def __init__(self, name, power):
        self.power = power
        self.name = name

    @staticmethod
    def get_all():
        return Role.query.all()
    
    @staticmethod
    def getRoleById(role_id):
        return Role.query.filter_by(role_id=role_id).first()

    def exists(self):
        return db.session.query(db.exists().where(Role.name == self.name)).scalar()

    @staticmethod
    def isExist(name):
        return db.session.query(db.exists().where(Role.name == name)).scalar()

    def update(self):
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()