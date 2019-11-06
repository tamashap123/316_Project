from sqlalchemy import sql, orm
from sqlalchemy.ext.hybrid import hybrid_method
from app import db

class Bill(db.Model):
    __tablename__ = 'bill'
    type = db.Column('type', db.String(2), primary_key=True)
    num = db.Column('num', db.INTEGER(), primary_key=True)
    cong_year = db.Column('cong_year', db.INTEGER(), primary_key=True)
    enacted = db.Column('enacted', db.BOOLEAN())
    summary = db.Column('summary', db.String(100000))
    category = db.Column('category', db.String(256))
    introduction_date = db.Column('introduction_date', db.DATE())

#String vs String?
class Congressman(db.Model):
    __tablename__ = 'congressman'
    id = db.Column('id', db.String(15),
                    primary_key=True)
    name = db.Column('name', db.String(256))
    house_or_senate = db.Column('house_or_senate', db.String(5))
    state = db.Column('state', db.String(2))
    district = db.Column('district', db.Integer())
    party = db.Column('party', db.String(15))
    phone = db.Column('phone', db.String(15))
    address = db.Column('address', db.String(256))
    contact_form = db.Column('contact_form', db.String(256))

class SponsoredBy(db.Model):
    __tablename__ = 'SponsoredBy'
    bill_type = db.Column('bill_type',db.String(2),
                            db.ForeignKey('bill.type'),
                            primary_key=True)
    bill_num = db.Column('bill_num',db.Integer(),
                            db.ForeignKey('bill.num'),
                            primary_key=True)
    cong_year = db.Column('cong_year',db.Integer(),
                            db.ForeignKey('bill.cong_year'),
                            primary_key=True)
    rep_id = db.Column('rep_id',db.String(),
                            primary_key=True)

class Vote(db.Model):
    __tablename__ = 'vote'
    rep_id = db.Column('rep_id', db.String(15),
                            primary_key=True)
    bill_type = db.Column('bill_type', db.String(2),
                            db.ForeignKey('bill.type'),
                            primary_key=True)
    bill_num = db.Column('bill_num', db.Integer(),
                            db.ForeignKey('bill.num'),
                            primary_key=True)
    cong_year = db.Column('cong_year', db.Integer(),
                            db.ForeignKey('bill.cong_year'),
                            primary_key=True)
    decision = db.Column('decision', db.String(10))

class RegisteredUser(db.Model):
    __tablename__ = 'registereduser'
    email = db.Column('email', db.String(256), primary_key = True)
    # password = db.Column('password', db.String(256))
    name = db.Column('name', db.String(256))
    state = db.Column('state', db.String(2))
    district = db.Column('district', db.Integer())

    @staticmethod
    def create(name, email, state, district):
        try: 
            # db.session.execute(registereduser.insert(), [{"email": email, "name": name, "state": state, "district": district}])
            db.session.execute("insert into registereduser values(:email, :name, :state, :district)", dict(email = email, name = name, state = state, district = district))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    # @hybrid_method
    # def is_correct_password(self, plaintext_password):
    #     return self.password_plaintext == plaintext_password
 
    # @property
    # def is_authenticated(self):
    #     """Return True if the user is authenticated."""
    #     return self.authenticated
 
    # @property
    # def is_active(self):
    #     """Always True, as all users are active."""
    #     return True
 
    # @property
    # def is_anonymous(self):
    #     """Always False, as anonymous users aren't supported."""
    #     return False
 
    # def get_id(self):
    #     """Return the email address to satisfy Flask-Login's requirements."""
    #     """Requires use of Python 3"""
    #     return str(self.id)
    
    def __repr__(self):
        return '<User {0}>'.format(self.name)
    

class RepresentedBy(db.Model):
    __tablename__ = 'representedby'
    email = db.Column('email', db.String(256), 
                    db.ForeignKey('registereduser.email'),
                    primary_key=True)
    rep_id = db.Column('rep', db.String(256), 
                    db.ForeignKey('congressman.id'),
                    primary_key=True)