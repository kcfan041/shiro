SetTitleMatchMode, 2
Run, wt

Sleep, 10000

SendInput, {Raw}conda activate kmaid
Sleep, 100
SendEvent, {Enter}
Sleep, 3000
SendInput, {Raw}cd G:/twitch-stream-recorder-1.0.2
Sleep, 100
SendEvent, {Enter}
Sleep, 3000
SendInput, {Raw}python ./twitch-recorder.py
Sleep, 100
SendEvent, {Enter}
Sleep, 500
SendInput, {Raw}%1%
Sleep, 100
SendEvent, {Enter}


