from flask import request, jsonify
from app import app
from app.models import get_sensor, add_sensor, log_input

@app.route('/api/sensor_data', methods=['POST'])
def sensor_data():
    data = request.get_json()
    sensor_name = data['sensor_name']
    distance = data['distance']
    
    sensor = get_sensor(sensor_name)
    if not sensor:
        sensor_id = add_sensor(sensor_name)
    else:
        sensor_id = sensor['sensor_ID']
    
    log_input(sensor_id, distance)
    return jsonify({"status": "success"}), 201

@app.route('/api/notes', methods=['GET', 'POST'])
def manage_notes():
    if request.method == 'POST':
        data = request.get_json()
        note_name = data['note_name']
        note_location = data['note_location']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO note (note_name, note_location) VALUES (%s, %s)", (note_name, note_location))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"status": "note added"}), 201
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM note")
    notes = cursor.fetchall()
    cursor.close()
    return jsonify(notes)
