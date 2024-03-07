from init import db

class Climate(db.Model):
    __tablename__ = "climates"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Climate {self.type}>"
