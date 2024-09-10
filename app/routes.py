import os
import requests
import subprocess
from flask import Blueprint,render_template,request,Response,jsonify,session,url_for,redirect
from .helper_methods import read_logs
from .config import authentication_url,batch_script_content_for_container,batch_script_content_for_service,bash_script_content_for_container,bash_script_content_for_service
import time
from .models import ServerInstance
from .models import db

main = Blueprint('main', __name__)

@main.route('/')
def index():    
    if session.get('authenticated'):
        ServerInstances=ServerInstance.query.all()
        if len(ServerInstances)>0:
            instance=ServerInstances[0]
            return redirect(url_for('main.buildHome',instanceId=instance.id))
        else:
            return redirect(url_for('main.createServerInstance'))
        
    else:
        return redirect(url_for('main.login_page'))
    
@main.route('/build/<int:instanceId>')
def buildHome(instanceId):    
    if session.get('authenticated'):
        currentInstance=ServerInstance.query.get(instanceId)
        # print(ServerInstances)
        ServerInstances=ServerInstance.query.all()
        return render_template('index.html',user=session.get('username'),ServerInstances=ServerInstances,currentInstance=currentInstance)
    else:
        return redirect(url_for('main.login_page'))

@main.route('/login',methods=['GET','POST'])
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
                return redirect(url_for('main.index'))
                
            else:
                return jsonify({'message': "Login Failed"}), 401
        
        
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500

@main.route('/logout')
def logout():
    session.clear(), 200
    return redirect(url_for('main.login_page'))
        
@main.route('/setting')
def setting():
    if session.get('authenticated'):
        # with open('./script/script.sh', 'r') as file:
        #     lines = file.readlines()
        # script="".join(lines)
        
        ServerInstances=ServerInstance.query.all()

        if len(ServerInstances)>0:
            instance=ServerInstances[0]
            with open(instance.scriptPath, 'r') as file:
                lines = file.readlines()
            script="".join(lines)
            logfilepath=instance.logFilePath
            return render_template('setting.html',user=session.get('username'),script=script,logfilepath=logfilepath,ServerInstances=ServerInstances,currentInstance=instance)
            
        else:  
            return redirect(url_for('main.createServerInstance'))
        # instance_names=[instance.name for instance in ServerInstances]
        # print(instance_names)
    else:
        return redirect(url_for('main.login_page'))
    
@main.route('/createServerInstance',methods=['GET','POST'])
def createServerInstance():
    if session.get('authenticated'):
        if request.method == 'GET':
            return render_template('createNewInstance.html',user=session.get('username'))
        else:
            data=request.json
            name=data['instanceName']
            logFilePath=data['logFile']
            containerized=data['containerized']=='on'
            directory=os.makedirs('./script', exist_ok=True)
            
            if os.name=='nt':
                scriptPath=os.path.join(directory, name +".bat")
            else:
                scriptPath=os.path.join(directory, name +".sh")
                
            new_instance=ServerInstance(
                name=name,
                scriptPath=scriptPath,
                logFilePath=logFilePath,
                is_containerized=containerized)
            
            db.session.add(new_instance)
            db.session.commit()
            
            with open(new_instance.scriptPath, 'w') as file:
                if new_instance.is_containerized:
                    if os.name=='nt':
                        file.write(batch_script_content_for_container)
                    else:
                        file.write(bash_script_content_for_container)
                else:
                    if os.name=='nt':
                        file.write(batch_script_content_for_service)
                    else:
                        file.write(bash_script_content_for_service)
                        
            os.chmod(new_instance.scriptPath, 0o755)
            
            return redirect(url_for('main.setting'))
    else:
        return redirect(url_for('main.login_page'))
    
@main.route('/DeleteServerInstance/<int:instanceId>')
def deleteServerInstance(instanceId):
    if session.get('authenticated'):
        instance=ServerInstance.query.get(instanceId)
        file_path=instance.scriptPath
        if instance:
            if os.path.exists(file_path):
                os.remove(file_path)
            db.session.delete(instance)  # Mark the record for deletion
            db.session.commit()
        return redirect(url_for('main.setting'))
    else:
        return redirect(url_for('main.login_page'))
    
@main.route('/save_script',methods=['POST'])
def saveScript():
    if session.get('authenticated'):
        data =request.json 
        script=data.get('script')
        logFilePath=data.get('logFilePath')
        serverInstance=data.get('serverInstance')
        serverInstance=ServerInstance.query.get(serverInstance)
        
        script_lines=script.split('\n')
        with open(serverInstance.scriptPath, 'w') as file:
            for line in script_lines:
                file.write(line + '\n')
                
        serverInstance.logFilePath=logFilePath
        
        print(serverInstance.logFilePath)
        db.session.commit()
        return 'ok',200
    
        
    else:
        return redirect(url_for('main.login_page'))
    
@main.route('/save_logpath',methods=['POST'])
def saveLogpath():
    if session.get('authenticated'):
        data =request.json 
        path=data.get('logpath')
        with open('./script/logfilepath.txt', 'w') as file:
                file.write(path)
        return 'ok', 200
    else:
        return redirect(url_for('main.login_page'))
        
@main.route('/rebuild/<int:instanceId>',methods=['POST'])
def reBuild(instanceId):
    if session.get('authenticated'):
        instance=ServerInstance.query.get(instanceId)
        scriptPath=instance.scriptPath
        lock_file=scriptPath+".lock"
        if os.path.exists(lock_file):
            return "Script Is already running", 403
        
        open(lock_file, 'w').close()
        
        res=subprocess.run([scriptPath], capture_output=True, text=True)
        print(res.stdout)
        
        os.remove(lock_file)
        return "ok"
    else:
        return redirect(url_for('main.login_page'))
    
@main.route('/getSettingDetails/<int:instanceId>')
def getSettingDetails(instanceId):
    if session.get('authenticated'):
        instance=ServerInstance.query.get(instanceId)
        if not os.path.exists(instance.scriptPath):
            open(instance.scriptPath, 'w').close()
            
        with open(instance.scriptPath, 'r') as file:
            lines = file.readlines()
        script="".join(lines)
        return {
            "script": script,
            "logfilepath": instance.logFilePath
        }
        
        
    else:
        return redirect(url_for('main.login_page'))
    
@main.route('/build_status/<int:instance_id>')
def scriptStatus(instance_id):
    instance=ServerInstance.query.get(instance_id)
    def check_status():
        lock_file=instance.scriptPath+".lock"
        while True:
            if os.path.exists(lock_file):
                yield "data: running\n\n"
            else:
                yield "data: idle\n\n"
            time.sleep(1)
    
    
    if session.get('authenticated'):
        return Response(check_status(), mimetype='text/event-stream')
    else:
        return redirect(url_for('main.login_page'))
        
@main.route('/logs/<int:instanceId>')
def stream_logs(instanceId):
    if session.get('authenticated'):
        instance=ServerInstance.query.get(instanceId)
        if instance.is_containerized:
            return Response(read_logs(container_id=instance.logFilePath), content_type='text/event-stream')
        else:
            return Response(read_logs(logFilePath=instance.file_name), content_type='text/event-stream')
