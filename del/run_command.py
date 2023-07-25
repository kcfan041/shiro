import subprocess
import sys

# 获取命令行参数
parameter = sys.argv[1]

# 定义要运行的命令
command = f'"C:\\Program Files\\AutoHotkey\\v1.1.36.02\\AutoHotkeyA32.exe" "H:\\kuro_bot1\\run_commands.ahk" "{parameter}"'

# 使用 subprocess.Popen 执行 AutoHotkey 脚本
subprocess.Popen(command, shell=True)


