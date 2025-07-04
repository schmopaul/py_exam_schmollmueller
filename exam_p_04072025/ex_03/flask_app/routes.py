from flask import Blueprint, request, jsonify, render_template, g
import sqlite3

# Blueprint and database setup
bp = Blueprint('tasks', __name__)
DATABASE = 'tasks.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@bp.teardown_app_request
def close_db(exception):
    db = g.pop('db', None)
    if db:
        db.close()

# Index route (HTML view)
@bp.route('/')
def index():
    tasks = get_db().execute('SELECT * FROM tasks').fetchall()
    return render_template('index.html', tasks=tasks)

# GET all tasks
@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = get_db().execute('SELECT * FROM tasks').fetchall()
    return jsonify([dict(t) for t in tasks])

# GET single task by ID
@bp.route('/tasks/<int:id>>', methods=['GET'])
def get_task(id):
    task = get_db().execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()
    return (jsonify(dict(task)) if task else jsonify({'error': 'Not found'}), 404)[::2][not task]

# POST new task
@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Bad request'}), 400
    db = get_db()
    cur = db.execute('INSERT INTO tasks (title) VALUES (?)', (data['title'],))
    db.commit()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (cur.lastrowid,)).fetchone()
    return jsonify(dict(task)), 201

# PUT update task
@bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    if not data or 'title' not in data or 'done' not in data:
        return jsonify({'error': 'Bad request'}), 400
    db = get_db()
    db.execute('UPDATE tasks SET title = ?, done = ? WHERE id = ?', (data['title'], int(data['done']), id))
    db.commit()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()
    return jsonify(dict(task)) if task else (jsonify({'error': 'Not found'}), 404)

# DELETE task
@bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (id,))
    db.commit()
    return jsonify({'result': True})
