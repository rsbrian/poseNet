@echo off
start "PoseNet" /MIN startPoseNet.cmd
start "NodeJs" /MIN startNodeJs.cmd
rem start "Chrome" /MIN startChrome.cmd 

RunDll32.exe user32.dll,SetCursorPos 1080 1920
