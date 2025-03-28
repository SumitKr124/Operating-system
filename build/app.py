from flask import Flask, jsonify, request, render_template
import psutil
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/system')
def system_info():
    return jsonify({
        'cpu_percent': psutil.cpu_percent(interval=0.5),
        'memory': psutil.virtual_memory()._asdict(),
        'processes': [{
            'pid': p.info['pid'],
            'name': p.info['name'],
            'status': p.info['status'],
            'cpu_percent': p.info['cpu_percent'],
            'memory_percent': p.info['memory_percent']
        } for p in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent'])]
    })

@app.route('/api/kill', methods=['POST'])
def kill_process():
    pid = request.json.get('pid')
    try:
        p = psutil.Process(pid)
        p.kill()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
