import sqlite3
import time

# Function to read and parse logs from a file
def read_logs(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            timestamp, level, message = parse_log(line)
            store_log(timestamp, level, message)

# Function to parse a log line
def parse_log(log_line):
    # Example log line format: "2025-02-09 11:04:00,INFO,This is an info message"
    parts = log_line.strip().split(',')
    timestamp = parts[0]
    level = parts[1]
    message = parts[2]
    return timestamp, level, message

# Function to store parsed logs in the SQLite database
def store_log(timestamp, level, message):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs
                      (timestamp TEXT, level TEXT, message TEXT)''')
    cursor.execute('INSERT INTO logs (timestamp, level, message) VALUES (?, ?, ?)',
                   (timestamp, level, message))
    conn.commit()
    conn.close()

# Path to the log file
log_file_path = 'log_file.log'

# Read and store logs continuously (similar to tail -f)
while True:
    read_logs(log_file_path)
    time.sleep(5)  # Check for new logs every 5 seconds
