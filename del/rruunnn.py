import subprocess
import time
command = 'start /WAIT wt -d "G:/twitch-stream-recorder-1.0.2"'
subprocess.run(command, shell=True)
command_to_execute = 'conda activate kmaid\npython ./twitch-recorder.py\n ukuruniru\n'
time.sleep(10)
terminal_process.stdin.write(command_to_execute.encode('utf-8'))