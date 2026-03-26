@echo off
echo =========================================
echo  Configurando el entorno de Mineria de Datos
echo =========================================

IF NOT EXIST "venv\" (
    echo Creando entorno virtual venv...
    python -m venv venv
) ELSE (
    echo El entorno virtual ya existe.
)

echo Activando el entorno virtual...
call venv\Scripts\activate

echo Instalando/Actualizando librerias desde requirements.txt...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo =========================================
echo  ¡Listo! Para empezar a trabajar, ejecuta:
echo  venv\Scripts\activate
echo =========================================
pause