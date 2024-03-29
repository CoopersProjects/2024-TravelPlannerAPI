from init import db

# Transport model, no schema due to preset types.

class TransportType(db.Model):
    __tablename__ = "transport_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<TransportType {self.name}>"
