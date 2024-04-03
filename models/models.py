import uuid
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class BlackList(db.Model):
    __tablename__ = 'blacklist'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String)
    blocked_reason = db.Column(db.String(255))
    app_uuid = db.Column(db.String)
    ip_address = db.Column(db.String)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

class BlacklistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BlackList
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()



    