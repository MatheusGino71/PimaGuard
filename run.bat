@echo off
REM PimaGuard - Script de Configuração Inicial
REM Este script configura o ambiente e executa o projeto

color 0a
cls

echo.
echo ========================================================
echo    PIMAGUARD - Preventor de Diabetes Tipo 2
echo    Setup Inicial do Projeto
echo ========================================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale Python 3.9+ e tente novamente.
    pause
    exit /b 1
)

echo [✓] Python detectado

REM Entrar no diretório backend
cd backend

REM Verificar se venv existe
if not exist "venv\" (
    echo.
    echo [CRIANDO] Ambiente virtual...
    python -m venv venv
    echo [✓] Ambiente virtual criado
) else (
    echo [✓] Ambiente virtual ja existe
)

REM Ativar venv
echo.
echo [ATIVANDO] Ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências
echo.
echo [INSTALANDO] Dependências Python...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERRO] Falha na instalacao de dependencias!
    pause
    exit /b 1
)

echo [✓] Dependências instaladas

REM Executar servidor
echo.
echo ========================================================
echo    INICIANDO SERVIDOR PIMAGUARD
echo ========================================================
echo.
echo [INFO] Servidor iniciando em http://localhost:8000
echo [INFO] API Docs: http://localhost:8000/docs
echo.
echo Pressione CTRL+C para parar o servidor
echo.
echo ========================================================
echo.

python app.py

pause
