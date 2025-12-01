
# Event Operations
def get_all_events():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events').fetchall()
    conn.close()
    result = {}
    for e in events:
        e_dict = dict(e)
        result[e_dict['id']] = e_dict
    return result

def create_event(event_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO events (id, name, schedule, location, capacity)
        VALUES (?, ?, ?, ?, ?)
    ''', (event_data['id'], event_data['name'], event_data['schedule'], 
          event_data['location'], event_data['capacity']))
    conn.commit()
    conn.close()

def delete_event(event_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()
