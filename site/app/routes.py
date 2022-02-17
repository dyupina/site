from bdb import effective
from crypt import methods
from datetime import datetime
from http import HTTPStatus
from re import sub
from app import app, db
from app.forms import LoginForm, AddUserForm, ChoseData, MakeChartForm
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.models import Measurement, User, UserSN
from flask_login import login_user, logout_user, current_user
from werkzeug.utils import secure_filename 
import re
import os
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure



@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    SNs = db.session.query(User, UserSN).filter(User.id==UserSN.user_id).with_entities(db.column('SN'))
    return render_template('index.html', user=current_user, SNs=SNs)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)




@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

ALLOWED_EXTENSIONS = ['csv']
UPLOAD_FOLDER = 'data'

def allowed_filename(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/add_new_user', methods=['GET', 'POST'])
def add_new_user():
    if current_user.user_type==True:
        form = AddUserForm()
        SNs = db.session.query(Measurement).with_entities(Measurement.SN).all()
        form.SNs.choices = [(str(s[0]), str(s[0])) for s in SNs]
        if form.validate_on_submit():
            user = User(username=form.username.data, password=form.password.data, user_type=form.user_type.data)
            db.session.add(user)
            db.session.commit()
            if form.user_type.data:
                pass
            else:
                for SN in form.SNs.data:
                    usrSN = UserSN(user_id=user.id, SN=SN)
                    db.session.add(usrSN)
                    db.session.commit()
            return redirect(url_for('index'))
        else:
            print(form.SNs.data)      
        return render_template('add_new_user.html', title='Add new user', form=form)
    return redirect(url_for('index'))

@app.route('/watch_data/<SN>', methods=['GET', 'POST'])
def watch_data(SN):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if not current_user.user_type:
        SNs = UserSN.query.join(User, UserSN.user_id==User.id).filter(User.id==current_user.id).with_entities(UserSN.SN).all()
        SNs = [str(SN[0]) for SN in SNs]
        if SN not in SNs:
            return redirect(url_for('watch_list'))
    data = None
    start = request.args.get('start').split('-')
    end = request.args.get('end').split("-")
    start = [int(a) for a in start]
    end = [int(a) for a in end]
    print(datetime(start[0], start[1], start[2]))
    form1=MakeChartForm()
    if not current_user.user_type:
        data = Measurement.query\
            .join(UserSN, Measurement.SN==UserSN.SN)\
            .join(User, User.id==UserSN.user_id)\
            .filter(Measurement.start_time.between(datetime(start[0], start[1], start[2]), datetime(end[0], end[1], end[2])))\
            .filter(Measurement.SN==SN) 
    else:
        data = Measurement.query\
            .filter(Measurement.start_time.between(datetime(start[0], start[1], start[2]), datetime(end[0], end[1], end[2])))\
            .filter(Measurement.SN==SN)       
    if data is None:
       return render_template('nodata.html')
    if form1.validate_on_submit():
         return redirect(url_for('plot_png', SN=SN, start=request.args.get('start'), end=request.args.get('end')))
    return render_template('table_data.html', SN=SN, data=data, form1=form1)


      
@app.route('/watch_list', methods=['GET', 'POST'])
def watch_list():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    chose_data_form = ChoseData()
    SNs = db.session.query(Measurement).with_entities(Measurement.SN).all()
    if current_user.user_type:
        SNs = db.session.query(Measurement).with_entities(Measurement.SN).all()
    else:
        SNs = UserSN.query.join(User, UserSN.user_id==User.id).filter(User.id==current_user.id).with_entities(UserSN.SN).all()
    chose_data_form.SNs.choices = [(str(s[0]), str(s[0])) for s in SNs]
    if chose_data_form.validate_on_submit():
        return redirect(url_for('watch_data', SN=chose_data_form.SNs.data, start=chose_data_form.start.data, end=chose_data_form.end.data))
    
    return render_template('watch_list.html', form=chose_data_form)


@app.route('/plot/<SN>')
def plot_png(SN):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))    
    
    if not current_user.user_type:
        SNs = UserSN.query.join(User, UserSN.user_id==User.id).filter(User.id==current_user.id).with_entities(UserSN.SN).all()
        SNs = [str(SN[0]) for SN in SNs]
        if SN not in SNs:
            return redirect(url_for('watch_list')) 
    start = request.args.get('start').split('-')
    end = request.args.get('end').split("-")
    start = [int(a) for a in start]
    end = [int(a) for a in end]        
    if not current_user.user_type:
        data = Measurement.query\
            .join(UserSN, Measurement.SN==UserSN.SN)\
            .join(User, User.id==UserSN.user_id)\
            .filter(Measurement.start_time.between(datetime(start[0], start[1], start[2]), datetime(end[0], end[1], end[2])))\
            .filter(Measurement.SN==SN) 
    else:
        data = Measurement.query\
            .filter(Measurement.start_time.between(datetime(start[0], start[1], start[2]), datetime(end[0], end[1], end[2])))\
            .filter(Measurement.SN==SN) 

    effs = data.with_entities(Measurement.efficicency).all()
    time = data.with_entities(Measurement.start_time).all()
    time = [str(t[0]) for t in time]
    effs = [t[0] if t[0]!=None else 0 for t in effs] 
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(time, effs)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
 
    
@app.route("/<SN>/<FILE_NAME>", methods=['POST'])
def get_file(SN, FILE_NAME):
    try:
        submitted_file = request.get_data(as_text=True)
        a = []
        while (re.search(r"\d+\n?\d\d\.\d\d\.\d\d\d\d \d\d:\d\d:\d\d", submitted_file)!=None):        
            c = re.search(r"\d+\n?\d\d\.\d\d\.\d\d\d\d \d\d:\d\d:\d\d", submitted_file).start()
            i = re.search(r"\d\d\.\d\d\.\d\d\d\d \d\d:\d\d:\d\d", submitted_file[c:]).start()
            a.append(submitted_file[:c+i-1])
            submitted_file = submitted_file[c+i:]
        a.append(submitted_file[:-1])
        for i in range(len(a)):
            a[i]=a[i].split(';')
        for i in range(len(a)):
            for j in range(len(a[i])):
                if a[i][j]=='':
                    a[i][j]=None
                elif not re.match(r'^-?\d+$', a[i][j]) is None:
                    a[i][j]=int(a[i][j])
                elif not re.match(r'^-?\d+(?:\.\d+)?$', a[i][j]) is None:
                    a[i][j]=float(a[i][j])
        for i in range(len(a)):
            efficiency = None
            if a[i][17]!=None:
                   efficiency = ((a[i][17]+a[i][18]+a[i][19])-(a[i][5]+a[i][6]+a[i][7]))/(a[i][17]+a[i][18]+a[i][19])*100
            m = Measurement(datetime.strptime(a[i][0], '%d.%m.%Y %H:%M:%S'),  datetime.strptime(a[i][1], '%d.%m.%Y %H:%M:%S'),
            a[i][2], a[i][3], a[i][4], a[i][5], 
            a[i][6],a[i][7],a[i][8], a[i][9], a[i][10],
            a[i][11], a[i][12], a[i][13], a[i][14], a[i][15],a[i][16],a[i][17], a[i][18], a[i][19], a[i][20], a[i][21], a[i][22],a[i][23], a[i][24], a[i][25], a[i][26], int(SN), efficiency)
            db.session.add(m)
            db.session.commit()
    except:
        print("OOps. Wrong data")    
    return 'OK'