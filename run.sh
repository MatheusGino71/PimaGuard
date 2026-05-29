#!/bin/bash
# PimaGuard - Script de Configuração Inicial (Linux/Mac)
# Este script configura o ambiente e executa o projeto

clear

echo ""
echo "=========================================================="
echo "   PIMAGUARD - Preventor de Diabetes Tipo 2"
echo "   Setup Inicial do Projeto"
echo "=========================================================="
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python3 não encontrado!"
    echo "Por favor, instale Python 3.9+ e tente novamente."
    exit 1
fi

echo "[✓] Python detectado"

# Entrar no diretório backend
cd backend

# Verificar se venv existe
if [ ! -d "venv" ]; then
    echo ""
    echo "[CRIANDO] Ambiente virtual..."
    python3 -m venv venv
    echo "[✓] Ambiente virtual criado"
else
    echo "[✓] Ambiente virtual já existe"
fi

# Ativar venv
echo ""
echo "[ATIVANDO] Ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo ""
echo "[INSTALANDO] Dependências Python..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERRO] Falha na instalação de dependências!"
    exit 1
fi

echo "[✓] Dependências instaladas"

# Executar servidor
echo ""
echo "=========================================================="
echo "   INICIANDO SERVIDOR PIMAGUARD"
echo "=========================================================="
echo ""
echo "[INFO] Servidor iniciando em http://localhost:8000"
echo "[INFO] API Docs: http://localhost:8000/docs"
echo ""
echo "Pressione CTRL+C para parar o servidor"
echo ""
echo "=========================================================="
echo ""

python app.py
