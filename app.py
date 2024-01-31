from flask import Flask, request, jsonify, make_response, render_template
from peoplecount_db import count
from flask_sqlalchemy import SQLAlchemy
from threading import Thread
import cv2
from os import environ
from ultralytics import YOLO


model = YOLO('yolov8x-seg.pt')

video_file1 = "KNJ1873\KNJ1873 - Front.mp4"
video_file2 = "KNJ1873\KNJ1873 - R.mp4"
video_file3 = "KNJ1873\KNJ1873-M.mp4"

video1 = cv2.VideoCapture(video_file1)
video2 = cv2.VideoCapture(video_file2)
video3 = cv2.VideoCapture(video_file3)
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
# app.config['DATABASE_HOST'] = environ.get('host')
# app.config['DB_HOST'] = environ.get('DB_HOST', 'flask_db')
db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    Bus_id = db.Column(db.String(80), nullable=False)   
    Bus_number = db.Column(db.String(120), nullable=False)
    camera_id = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(120), nullable=False)
    Latitude_point = db.Column(db.String(80), nullable=False)
    Longitude_point = db.Column(db.String(120), nullable=False)
    People_count = db.Column(db.String(120), nullable=False)
    Time = db.Column(db.String(120), nullable=False)

    def json(self):
        return {'id': self.id, 'Bus id': self.Bus_id, 'bus number': self.Bus_number, 'camera id': self.camera_id, 'date': self.date, 'People_count': self.People_count, 'Time': self.Time,'Latitude_point':'34.4232','Longitude_point':'56.544232'}
with app.app_context():
    db.create_all()

def values_get():
    while True:
        ret, frame1 = video1.read()
        ret, frame2 = video2.read()
        ret, frame3 = video3.read()
        data = count(frame1, frame2, frame3, model)
        print("dictinary........",data)
        new_user = User(date=data['Date '], Time=data['Time '], Bus_number =data['Bus number '],Latitude_point=data['Latitude point'], Longitude_point=data['Longitude point'], Bus_id=data['Bus id'], camera_id=data['Camera id'],People_count=data['People count'])
        print("new user created")
        try:
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()
                print("new_user....",new_user.json())
        except Exception as e:
            print("error",e)

t1 = Thread(target=values_get,daemon=True)
t1.start()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_data', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting users'}), 500)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
