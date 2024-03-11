from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100))
    check_in_date = db.Column(db.Date, nullable=False)
    departure_date = db.Column(db.Date, nullable=False)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(8), nullable=False)
    guests_number = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Integer, nullable=False)
    has_bath = db.Column(db.Boolean, nullable=False)
    has_balcony = db.Column(db.Boolean, nullable=False)

class Occupancy(db.Model):
    room_type = db.Column(db.String(8), primary_key=True)
    free_rooms = db.Column(db.Integer, nullable=False)


@app.route('/check_guest')
def check_guest():
    return render_template('check_guest.html')


@app.route('/api/check_guest', methods=['POST'])
def check_guest_api():
    last_name = request.form['last_name']
    phone = request.form['phone']
    exists = db.session.query(Guest).filter_by(last_name=last_name).first() is not None and db.session.query(Guest).filter_by(phone=phone).first() is not None
    if exists:
        return redirect('/guest_exists')
    else:
        return redirect('/guest_not_exists')


@app.route('/guest_exists')
def guest_exists():
    return render_template('guest_exists.html')


@app.route('/guest_not_exists')
def guest_not_exists():
    return render_template('guest_not_exists.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/api/registration', methods=['POST'])
def registration_api():
    last_name = request.form['last_name']
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    phone = request.form['phone']
    email = request.form['email']
    check_in_date = request.form['check_in_date']
    departure_date = request.form['departure_date']
    new_id = db.session.query(db.func.max(Guest.id)).scalar() + 1
    new_guest = Guest(id=new_id, last_name=last_name, first_name=first_name, middle_name=middle_name, phone=phone, email=email, check_in_date=datetime.datetime.strptime(check_in_date, '%Y-%m-%d').date(), departure_date=datetime.datetime.strptime(departure_date, '%Y-%m-%d').date())
    db.session.add(new_guest)
    db.session.commit()
    return redirect('/successful_registration')


@app.route('/successful_registration')
def successful_registration():
    return render_template('successful_registration.html')


if __name__ == '__main__':
    app.run(debug=True)
