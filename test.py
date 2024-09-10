import docker as d
from datetime import datetime, timedelta
client=d.from_env()
container=client.containers.get('17bbfcd07c42434c3cd8bb973344b70837553e47c2216fd67b2e4067d0f38f52')
since_time = datetime.utcnow() - timedelta(seconds=10)  # Adjust time delta as needed
since_timestamp = int(since_time.timestamp())
# log_stream = container.logs(stream=True, follow=True)
log_stream = container.logs(tail=50, stream=True, follow=True)
next_line=next(log_stream)
# next_line=next_line.decode('utf-8', errors='ignore').replace('\x00', '')
print(next_line)