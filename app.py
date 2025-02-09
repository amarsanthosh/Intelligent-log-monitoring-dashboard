from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

# Function to fetch logs from the database
def fetch_logs(severity=None, start_date=None, end_date=None):
    query = "SELECT * FROM logs WHERE 1=1"
    params = []

    if severity:
        query += " AND level=?"
        params.append(severity)
    if start_date:
        query += " AND timestamp>=?"
        params.append(start_date)
    if end_date:
        query += " AND timestamp<=?"
        params.append(end_date)

    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    logs = cursor.fetchall()
    conn.close()
    return logs

# Endpoint to serve the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to fetch all logs
@app.route('/api/logs', methods=['GET'])
def get_logs():
    severity = request.args.get('severity')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    logs = fetch_logs(severity, start_date, end_date)
    return jsonify(logs)

# Endpoint to fetch logs for real-time updates
@app.route('/api/logs/realtime', methods=['GET'])
def get_realtime_logs():
    logs = fetch_logs()
    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True)
