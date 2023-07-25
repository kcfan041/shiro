import subprocess
import json

# 定义要运行的参数
with open('H:\\kuro_bot1\\twitch_id.json','r',encoding='utf8') as jfile:
    commands_data = json.load(jfile)

# 定义要运行的命令
for x in commands_data:
    command = f'python H:\\kuro_bot1\\run_command.py "{x}"'
    subprocess.Popen(command, shell=True)
