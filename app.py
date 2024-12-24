from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import math
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    calories = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_record():
    data = request.json
    try:
        # Parse and validate date
        date = data['date']
        parsed_date = datetime.strptime(date, '%Y-%m-%d')
        if parsed_date.year < 1950:
            return jsonify({"error": "Year must be 1950 or later."}), 400

        weight = float(data['weight'])
        height = float(data['height'])
        bmi = float(data['bmi'])
        calories = data['calories']

        # Save record to database
        record = HealthRecord(date=date, weight=weight, height=height, bmi=bmi, calories=calories)
        db.session.add(record)
        db.session.commit()

        return jsonify({"message": "Record added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/records', methods=['GET'])
def get_records():
    records = HealthRecord.query.all()
    return jsonify([
        {
            "date": record.date,
            "weight": record.weight,
            "height": record.height,
            "bmi": record.bmi,
            "calories": record.calories
        }
        for record in records
    ])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
