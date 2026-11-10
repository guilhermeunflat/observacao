@echo off
REM Sobe o servidor de câmeras do notebook. Deixe esta janela aberta.
cd /d %~dp0src
..\.venv\Scripts\python -m observacao.servidor
pause
