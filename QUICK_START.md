# GUIA RÁPIDO - PimaGuard

## Início Rápido (5 minutos)

### Windows

```bash
# 1. Abrir PowerShell na pasta do projeto
# 2. Executar o script (aceite a execução se pedido)
.\run.bat

# O servidor iniciará automaticamente na porta 8000
```

### Linux / Mac

```bash
# 1. Abrir terminal na pasta do projeto
# 2. Dar permissão ao script
chmod +x run.sh

# 3. Executar
./run.sh

# O servidor iniciará automaticamente na porta 8000
```

## Setup Manual

### 1. Backend Python

```bash
# Entrar na pasta
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar
python app.py
```

**Servidor rodando em**: http://localhost:8000

### 2. Frontend

```bash
# Em outra janela de terminal, na pasta frontend
cd frontend

# Python 3
python -m http.server 8000

# OU com Node.js
npx http-server -p 8000
```

**Aplicação rodando em**: http://localhost:8000

## Documentação da API

Depois que o servidor estiver rodando:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐳 Com Docker (Opcional)

### Docker Compose (Recomendado)

```bash
# Construir e executar
docker-compose up --build

# Acesso
# API: http://localhost:8000
# Frontend: http://localhost:80
```

### Docker Manual

```bash
# Construir imagem
docker build -t pimaguard .

# Executar
docker run -p 8000:8000 pimaguard
```

## Primeiro Teste

1. Abra http://localhost:8000 (ou :8080 para frontend)
2. Preencha o formulário com dados de exemplo:
   - Gestações: 1
   - Glicose: 120
   - Pressão: 70
   - Espessura Pele: 20
   - Insulina: 30
   - IMC: 25
   - Histórico Familiar: 0.5
   - Idade: 30

3. Clique em "Analisar Risco"
4. Veja a predição e fatores de risco!

## 🔗 Endpoints Principais

### Predição
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pregnancies": 1,
    "glucose": 120,
    "blood_pressure": 70,
    "skin_thickness": 20,
    "insulin": 30,
    "bmi": 25,
    "diabetes_pedigree_function": 0.5,
    "age": 30
  }'
```

### Status
```bash
curl http://localhost:8000/health
```

### Informações
```bash
curl http://localhost:8000/info
```

## ⚙️ Troubleshooting

### "ModuleNotFoundError"
```bash
# Reativar venv e reinstalar
pip install -r requirements.txt
```

### "Port already in use"
Mudar porta:
```bash
# Backend (Python)
python app.py --port 9000

# Frontend
python -m http.server 9000
```

### "Connection refused"
- Verificar se o backend está rodando (deve ver "Application startup complete")
- Verificar se a porta está correta (8000 por padrão)

### Kagglehub não funcionando
- O sistema cria um dataset sintético automaticamente
- Ou download manual: pip install kagglehub

## Dados de Teste

Dataset oficial: Pima Indians Diabetes Database (768 amostras)

**Valores típicos**:
- Glicose: 100-200 mg/dL
- Pressão: 60-100 mmHg
- IMC: 18-40 kg/m²
- Idade: 20-80 anos

## Dicas

1. **Desenvolvimento Frontend**: Editar index.html e recarregar página (F5)
2. **Desenvolvimento Backend**: O uvicorn recarrega automaticamente
3. **Debug API**: Abrir http://localhost:8000/docs para testar endpoints
4. **Ver Logs**: Verificar console do navegador (F12)

## Perguntas Frequentes

**P: Os dados são salvos?**
R: Não! Cada predição é feita apenas na memória. Sem armazenamento.

**P: Posso usar em produção?**
R: Sim! Configure HTTPS, CORS e autenticação conforme necessário.

**P: Como atualizar modelos?**
R: Reexecute app.py com novos dados (regenera arquivo .pkl)

**P: Funciona offline?**
R: Sim! Após treinar uma vez. O kagglehub precisa de internet apenas na primeira vez.

---

**Precisa de ajuda?** Abra uma issue ou consulte o README.md completo.

**Boa sorte!**
