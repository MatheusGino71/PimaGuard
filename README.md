# PimaGuard - Sistema de Prevenção e Predição de Diabetes Tipo 2

Sistema web inteligente que utiliza Machine Learning e SHAP para predizer o risco de desenvolvimento de Diabetes Tipo 2 com explicabilidade total dos fatores de risco.

## Características

- **Backend Python FastAPI**: API RESTful moderna e rápida
- **Machine Learning**: 2 algoritmos de classificação (Random Forest + Regressão Logística)
- **Explicabilidade SHAP**: Transparência completa nos resultados
- **Frontend Elegante**: Design minimalista e responsivo (TailwindCSS)
- **JavaScript Vanilla**: Sem dependências, requisições assíncronas puras
- **Download Automático**: Pipeline de dados com kagglehub
- **Predição em Tempo Real**: Respostas instantâneas com confiança

## Requisitos

- Python 3.9+
- Node.js (opcional, para desenvolvimento)
- Navegador moderno

## Instalação e Execução

### 1. Backend

```bash
# Entrar no diretório backend
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python app.py
```

O servidor estará disponível em: **http://localhost:8000**

Documentação interativa da API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. Frontend

```bash
# Entrar no diretório frontend
cd frontend

# Abrir no navegador
# Windows
start index.html

# Linux
xdg-open index.html

# Mac
open index.html
```

Ou servir com um servidor HTTP simples:

```bash
# Python 3
python -m http.server 8080

# Node.js (com http-server)
npx http-server -p 8080
```

Acesse: **http://localhost:8080**

## Estrutura do Projeto

```
PimaGuard/
├── backend/
│   ├── app.py                          # Aplicação FastAPI principal
│   ├── requirements.txt                # Dependências Python
│   ├── data/                           # Dados baixados
│   └── models/                         # Modelos treinados
├── frontend/
│   └── index.html                      # Aplicação web (HTML+CSS+JS)
└── README.md                           # Este arquivo
```

## API Endpoints

### GET `/`
Health check básico

```bash
curl http://localhost:8000/
```

### GET `/health`
Status detalhado da API

```bash
curl http://localhost:8000/health
```

### POST `/predict`
Predizer risco de diabetes

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

**Response:**
```json
{
  "diabetes_risk_percentage": 42.5,
  "risk_level": "Moderado",
  "risk_factors": [
    {
      "feature": "Glucose",
      "impact_value": 0.85,
      "impact_percentage": 45.3
    },
    // ... mais fatores
  ],
  "model_used": "Random Forest",
  "confidence": 89.2
}
```

### GET `/info`
Informações do modelo

```bash
curl http://localhost:8000/info
```

## Variáveis de Input

O formulário requer 8 variáveis médicas do dataset Pima:

| Variável | Unidade | Range | Descrição |
|----------|---------|-------|-----------|
| Pregnancies | vezes | 0+ | Número de gestações |
| Glucose | mg/dL | 0+ | Glicose em jejum |
| Blood Pressure | mmHg | 0+ | Pressão diastólica |
| Skin Thickness | mm | 0+ | Espessura tricipital |
| Insulin | µU/ml | 0+ | Insulina sérica 2h |
| BMI | kg/m² | 0+ | Índice de Massa Corporal |
| DiabetesPedigreeFunction | - | 0-1 | Histórico familiar |
| Age | anos | 0+ | Idade |

## Modelos de Machine Learning

### Random Forest
- **Estimadores**: 100 árvores
- **Profundidade Máxima**: 10 níveis
- **Métrica**: Acurácia + AUC-ROC

### Regressão Logística
- **Max Iterations**: 1000
- **Regularização**: L2 (default)
- **Métrica**: Acurácia + AUC-ROC

## SHAP (SHapley Additive exPlanations)

O sistema utiliza SHAP para calcular a contribuição de cada feature na predição:
- **TreeExplainer** para Random Forest (rápido)
- **KernelExplainer** para Regressão Logística (flexível)

Cada predição retorna os 5 principais fatores de risco com seus impactos percentuais.

## Design Frontend

- **Tipografia**: Bebas Neue, Inter, JetBrains Mono, Playfair Display
- **Paleta**: Preto (#111) e Off-white (#f4f3f0)
- **Framework**: TailwindCSS
- **Ícones**: Lucide Icons
- **Responsividade**: Mobile-first, tablet e desktop

## Aviso Importante

**Este sistema é uma ferramenta de auxílio educacional e não substitui diagnóstico médico profissional.**

- Resultados são predições baseadas em IA
- Sempre consulte um profissional de saúde qualificado
- Os dados não são armazenados (privacidade garantida)

## 🔒 Privacidade e Segurança

- Sem armazenamento de dados
- CORS ativado para frontend
- Validação de entrada com Pydantic
- Sem transmissão de dados sensíveis

## Dataset

Dataset original: **Pima Indians Diabetes Database**
- Fonte: UCI Machine Learning Repository
- Samples: 768 registros
- Features: 8 variáveis médicas
- Classes: Binária (Diabetes: Sim/Não)

Download automático via kagglehub.

## 🛠️ Troubleshooting

### Erro: "ModuleNotFoundError"
Certifique-se que o ambiente virtual está ativado e dependências instaladas:
```bash
pip install -r requirements.txt
```

### Erro: "Connection refused" no frontend
Verifique se o backend está rodando na porta 8000:
```bash
python app.py
```

### Erro: "CORS blocked"
O backend já possui CORS configurado. Se ainda tiver erro, verifique a URL no frontend.

### Dataset não download automático
O sistema cairá para um dataset sintético gerado localmente. Instale kagglehub:
```bash
pip install kagglehub
```

## 📞 Suporte

Para dúvidas, issues ou sugestões, abra uma issue no repositório.

## 📄 Licença

MIT License - Veja LICENSE para detalhes

## 👨‍💻 Desenvolvido por

**Seu Nome** | Full Stack Developer & Data Scientist  
2025 | PimaGuard

---

**Cuide de sua saúde. Previna diabetes. Use a tecnologia a seu favor.**
