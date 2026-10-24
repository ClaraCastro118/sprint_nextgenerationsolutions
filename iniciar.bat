@echo off
title Creative AI - Inicializador
echo ========================================================
echo Instalando/Atualizando dependencias (Aguarde)...
echo ========================================================
python -m pip install -r requirements.txt --quiet

echo.
echo ========================================================
echo Iniciando o Creative AI...
echo Nao feche esta janela preta enquanto estiver usando o app!
echo ========================================================
python -m streamlit run src/app.py
pause