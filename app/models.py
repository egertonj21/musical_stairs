from app import mysql

def get_sensor(sensor_name):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT sensor_ID FROM sensor WHERE sensor_name = %s", (sensor_name,))
    result = cursor.fetchone()
    cursor.close()
    return result

def add_sensor(sensor_name):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO sensor (sensor_name) VALUES (%s)", (sensor_name,))
    sensor_id = cursor.lastrowid
    cursor.execute("INSERT INTO alive (sensor_id, active) VALUES (%s, %s)", (sensor_id, 1))
    cursor.execute("INSERT INTO action_table (sensor_id) VALUES (%s)", (sensor_id,))
    mysql.connection.commit()
    cursor.close()
    return sensor_id

def log_input(sensor_id, distance):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO input (distance, timestamp, sensor_ID) VALUES (%s, NOW(), %s)",
        (distance, sensor_id)
    )
    mysql.connection.commit()
    cursor.close()
