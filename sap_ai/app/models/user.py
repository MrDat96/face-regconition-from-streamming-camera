from app import db
from app.models.role import Role

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.String(10), primary_key = True)
    first_name = db.Column(db.String(75))
    last_name = db.Column(db.String(75))
    date_of_birth = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    occupancies = db.Column(db.String(50))

    def __init__(self, user_id, first_name, last_name, date_of_birth, role_id, occupancies):
        """initialize with name."""
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.role_id = role_id
        self.date_of_birth = date_of_birth
        self.occupancies = occupancies

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_all_with_Role():
        return db.session.query(User, Role).filter(User.role_id == Role.role_id).all()

    @staticmethod
    def getUserById(user_id):
        return User.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def getUserWithRoleById(user_id):
        return db.session.query(User, Role).filter(User.user_id == user_id).filter(User.role_id == Role.role_id).all()

    @staticmethod
    def isExist(user_id):
        return db.session.query(db.exists().where(User.user_id == user_id)).scalar()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<User: {}>".format(self.first_name)

