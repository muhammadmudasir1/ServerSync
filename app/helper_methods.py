import time
import docker
from datetime import datetime, timedelta

def read_logs(container_id=None,file_name=None):
    
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
    
    
    if container_id:
        client = docker.from_env()
        container=client.containers.get(container_id)
        log_stream = container.logs(tail=50,stream=True, follow=True)
        try:
            
            while True:
                line = next(log_stream)
                if line:
                    yield f"data: {line.decode('utf-8')}\n\n"
                    # time.sleep(0.1)
                else:
                    time.sleep(1)  
        except StopIteration:
            pass
        
    else:
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
        
                

