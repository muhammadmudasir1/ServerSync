from flask import Flask,render_template,request,Response,jsonify,session,url_for,redirect
import requests
from flask_sqlalchemy import SQLAlchemy
import subprocess
import logging
import time
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

authentication_url = 'http://localhost:1721/serversync_auth'

def read_logs():
    def tail(f, num_lines=10):
        f.seek(0, 2)  # Move to the end of the file
        end = f.tell()
        buffer_size = 1024
        buffer = ''
        while end > 0 and num_lines > 0:
            end -= buffer_size
            if end < 0:
                end = 0
            f.seek(end)
            buffer = f.read(buffer_size) + buffer
            num_lines = buffer.count('\n') - num_lines
        return buffer.splitlines()[-num_lines:]
    
    with open('flask_app.log', 'r') as f:
        for line in tail(f, 10):
            yield f"data: {line}\n\n" 
            
        f.seek(0,2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)  # Wait before trying again
                continue
            yield f"data: {line}\n\n"  # SSE format: 'data: message\n\n'


@app.route('/')
def index():
    if session.get('authenticated'):
        return render_template('index.html',user=session.get('username'))
    else:
        return redirect(url_for('login_page'))

@app.route('/login',methods=['GET','POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        data =request.json 
        username=data.get('username')
        password=data.get('password')
        payload = {
            "email": username,
            "password": password
        }
        try:
            response = requests.post(authentication_url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            result=result.get('result')
            # print(result)
            if result.get('login_success'):
                cookies = response.cookies
                session['session_id']=cookies['session_id']
                session['username']=result['data']['name']
                session['authenticated']=True
                return redirect(url_for('index'))
                
            else:
                return jsonify({'message': "Login Failed"}), 401
        
        
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500

@app.route('/logout')
def logout():
    session.clear(), 200
    return redirect(url_for('login_page'))
        
@app.route('/setting')
def setting():
    if session.get('authenticated'):
        with open('./script/script.sh', 'r') as file:
            lines = file.readlines()
        script="".join(lines)
        
        with open('./script/logfilepath.txt', 'r') as file:
            lines = file.readlines()
        logfilepath="".join(lines)
        return render_template('setting.html',user=session.get('username'),script=script,logfilepath=logfilepath)
    else:
        return redirect(url_for('login_page'))
    
@app.route('/save_script',methods=['POST'])
def saveScript():
    if session.get('authenticated'):
        data =request.json 
        script=data.get('script')
        script_lines=script.split('\n')
        with open('./script/script.sh', 'w') as file:
            for line in script_lines:
                file.write(line + '\n')
        return 'ok',200
        
    else:
        return redirect(url_for('login_page'))
    
@app.route('/save_logpath',methods=['POST'])
def saveLogpath():
    if session.get('authenticated'):
        data =request.json 
        path=data.get('logpath')
        with open('./script/logfilepath.txt', 'w') as file:
                file.write(path)
        return 'ok', 200
    else:
        return redirect(url_for('login_page'))
        


@app.route('/rebuild',methods=['POST'])
def reBuild():
    if session.get('authenticated'):
        lock_file="./script/script_running.lock"
        if os.path.exists(lock_file):
            return "Script Is already running", 403
        
        open(lock_file, 'w').close()
        
        if os.name=='nt':
            res=subprocess.run(['./script/script.bat'], capture_output=True, text=True)
            print(res.stdout)
        else:
            res=subprocess.run(['./script/script.sh'], capture_output=True, text=True)
            print(res.stdout)
        os.remove(lock_file)
        return "ok"
    else:
        return redirect(url_for('login_page'))
    
@app.route('/build_status')
def scriptStatus():
    def check_status():
        lock_file="./script/script_running.lock"
        while True:
            if os.path.exists(lock_file):
                yield "data: running\n\n"
            else:
                yield "data: idle\n\n"
            time.sleep(1)
    
    
    if session.get('authenticated'):
        return Response(check_status(), mimetype='text/event-stream')
    else:
        return redirect(url_for('login_page'))
        

    
@app.route('/logs')
def stream_logs():
    if session.get('authenticated'):
        return Response(read_logs(), content_type='text/event-stream')




if __name__ == '__main__':
    logging.basicConfig(filename='flask_app.log', level=logging.DEBUG)
    app.run(debug=True)