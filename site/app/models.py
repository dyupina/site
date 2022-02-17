from app import db, login
from flask_login import UserMixin
from sqlalchemy.types import DateTime
 
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    user_type = db.Column(db.Boolean)
 
    def __repr__(self):
        return '<User {}>'.format(self.username)
 
 
    def check_password(self, password):
        return self.password==password
 

 
class Measurement(db.Model):
    __tablename__ = 'measurement'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(DateTime)
    end_time = db.Column(DateTime)
    reactive_power_A_1 = db.Column(db.Float)
    reactive_power_B_1 = db.Column(db.Float)
    reactive_power_C_1 = db.Column(db.Float)
    active_power_A_1 = db.Column(db.Float)
    active_power_B_1 = db.Column(db.Float)
    active_power_C_1 = db.Column(db.Float)
    voltage_A_1 = db.Column(db.Float)
    voltage_B_1 = db.Column(db.Float)
    voltage_C_1 = db.Column(db.Float)
    cosA_1 = db.Column(db.Float)
    cosB_1 = db.Column(db.Float)
    cosC_1 = db.Column(db.Float)
    reactive_power_A_2 = db.Column(db.Float)
    reactive_power_B_2 = db.Column(db.Float)
    reactive_power_C_2 = db.Column(db.Float)
    active_power_A_2 = db.Column(db.Float)
    active_power_B_2 = db.Column(db.Float)
    active_power_C_2 = db.Column(db.Float)
    voltage_A_2 = db.Column(db.Float)
    voltage_B_2 = db.Column(db.Float)
    voltage_C_2 = db.Column(db.Float)
    cosA_2 = db.Column(db.Float)
    cosB_2 = db.Column(db.Float)
    cosC_2 = db.Column(db.Float)
    blocks_number = db.Column(db.Integer)
    SN = db.Column(db.Integer, nullable=False)
    efficicency = db.Column(db.Float)
    def __init__(self, start_time, end_time, reactive_power_A_1, reactive_power_B_1, reactive_power_C_1,
                    active_power_A_1, active_power_B_1, active_power_C_1, voltage_A_1, voltage_B_1, voltage_C_1,
                    cosA_1, cosB_1, cosC_1, 
                    reactive_power_A_2, reactive_power_B_2, reactive_power_C_2,
                    active_power_A_2, active_power_B_2, active_power_C_2, voltage_A_2, voltage_B_2, voltage_C_2,
                    cosA_2, cosB_2, cosC_2, blocks_number, SN, efficiency):
        self.start_time = start_time
        self.end_time = end_time
        self.reactive_power_A_1 = reactive_power_A_1
        self.reactive_power_B_1 = reactive_power_B_1
        self.reactive_power_C_1 = reactive_power_C_1
        self.active_power_A_1 = active_power_A_1
        self.active_power_B_1 = active_power_B_1
        self.active_power_C_1 = active_power_C_1
        self.voltage_A_1 = voltage_A_1
        self.voltage_B_1 = voltage_B_1
        self.voltage_C_1 = voltage_C_1
        self.cosA_1 = cosA_1
        self.cosB_1 = cosB_1
        self.cosC_1 = cosC_1
        self.reactive_power_A_2 = reactive_power_A_2
        self.reactive_power_B_2 = reactive_power_B_2
        self.reactive_power_C_2 = reactive_power_C_2
        self.active_power_A_2 = active_power_A_2
        self.active_power_B_2 = active_power_B_2
        self.active_power_C_2 = active_power_C_2
        self.voltage_A_2 = voltage_A_2
        self.voltage_B_2 = voltage_B_2
        self.voltage_C_2 = voltage_C_2
        self.cosA_2 = cosA_2
        self.cosB_2 = cosB_2
        self.cosC_2 = cosC_2
        self.blocks_number = blocks_number
        self.SN = SN
        self.efficicency = efficiency
    
 

class UserSN(db.Model):
    __tablensame__='usersn'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    SN = db.Column(db.Integer, nullable=False)
 
 
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
 