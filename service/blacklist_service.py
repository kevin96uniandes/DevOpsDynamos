from ..models.models import BlackList, BlacklistSchema, db

blacklist_schema = BlacklistSchema()

class BlacklistService():
    def crear_email_blacklist(self, datos_email):
        email_blacklist = BlackList(
            email = datos_email.get('email'),
            blocked_reason = datos_email.get('blocked_reason')
        )

        db.session.add(email_blacklist)
        db.session.commit()

        return email_blacklist

    def consultar_by_email(self, email):
        blacklist_item = db.session.query(BlackList).filter_by(email=email).first() 
        return blacklist_schema.dump(blacklist_item)

