call C:\chenchang\study\sphinx_rtd_theme\.venv\Scripts\activate.bat

@echo off
REM 执行 sphinx-autobuild 命令
start "" sphinx-autobuild.exe source build

REM 等待一段时间，确保服务器启动
ping -n 3 127.0.0.1 >nul

REM 使用默认浏览器打开页面
start "" http://127.0.0.1:8000    
