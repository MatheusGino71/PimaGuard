# 🏗️ ARQUITETURA E DOCUMENTAÇÃO TÉCNICA - PimaGuard

## Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (HTML/CSS/JS)                  │
│                     Browser do Usuário                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  index.html (TailwindCSS + Vanilla JS)               │  │
│  │  - Formulário Elegante                               │  │
│  │  - Requisições Fetch Assíncronas                     │  │
│  │  - Exibição de Resultados com Animações             │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP POST /predict
                     │ (JSON)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND (Python FastAPI)                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              FastAPI Server (app.py)                 │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  Pydantic Validation                         │   │  │
│  │  │  - Input: PredictionInput                    │   │  │
│  │  │  - Output: PredictionOutput                  │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  │                       │                              │  │
│  │  ┌────────────────────▼────────────────────────┐   │  │
│  │  │  PimaMLPipeline (Orquestrador)             │   │  │
│  │  │  ├─ download_dataset()                      │   │  │
│  │  │  ├─ prepare_data()                          │   │  │
│  │  │  ├─ split_data()                            │   │  │
│  │  │  ├─ scale_features()                        │   │  │
│  │  │  ├─ train_models()                          │   │  │
│  │  │  ├─ create_explainers()                     │   │  │
│  │  │  └─ predict_with_explanation()              │   │  │
│  │  └────────────────────────────────────────────┘   │  │
│  │                  ├─ ▼                              │  │
│  │                  │                                │  │
│  │  ┌──────────────┴──────────────────────────────┐  │  │
│  │  │  Modelos Treinados                          │  │  │
│  │  ├─ RandomForestClassifier (100 árvores)      │  │  │
│  │  ├─ LogisticRegression (max_iter=1000)       │  │  │
│  │  ├─ StandardScaler (normalização)             │  │  │
│  │  └─ SHAP Explainers                           │  │  │
│  │      ├─ TreeExplainer (RF)                    │  │  │
│  │      └─ KernelExplainer (LR)                  │  │  │
│  │  ┌──────────────────────────────────────────┐  │  │
│  │  │  Dataset Pima                             │  │  │
│  │  │  768 samples × 8 features + target        │  │  │
│  │  └──────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP Response 200 OK
                     │ (JSON com Predição)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   RESPOSTA AO USUÁRIO                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Risco: 42.5%                                        │  │
│  │ Nível: Moderado                                     │  │
│  │ Modelo: Random Forest                               │  │
│  │ Confiança: 89.2%                                    │  │
│  │                                                      │  │
│  │ Principais Fatores:                                 │  │
│  │ 1. Glucose (45.3%)                                 │  │
│  │ 2. BMI (30.2%)                                     │  │
│  │ 3. Age (15.1%)                                     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Fluxo de Dados

### 1️⃣ Inicialização (Startup)

```
app.py iniciado
    ↓
initialize_pipeline()
    ├─ check modelos salvos (.pkl)
    │  ├─ SIM → load_pipeline()
    │  └─ NÃO → continuar
    ├─ download_dataset() [kagglehub]
    ├─ prepare_data()
    ├─ split_data()
    ├─ scale_features()
    ├─ train_models()
    │  ├─ RandomForest → model_rf
    │  └─ LogisticRegression → model_lr
    ├─ evaluate_models()
    ├─ create_explainers()
    │  ├─ TreeExplainer para RF
    │  └─ KernelExplainer para LR
    └─ save_pipeline()
        └─ Salva .pkl em /backend/models/
```

### 2️⃣ Predição (Request)

```
Browser
  ↓
JavaScript captura input do formulário
  ↓
fetch() → POST /predict
{
  "pregnancies": 1,
  "glucose": 120,
  "blood_pressure": 70,
  "skin_thickness": 20,
  "insulin": 30,
  "bmi": 25,
  "diabetes_pedigree_function": 0.5,
  "age": 30
}
  ↓
FastAPI recebe
  ↓
Pydantic valida entrada
  ↓
scaler.transform() → normalização
  ↓
best_model.predict_proba() → probabilidade
  ↓
SHAP explainer.shap_values() → impacto features
  ↓
Classificação de Nível de Risco
  ├─ Baixo: < 25%
  ├─ Moderado: 25-50%
  ├─ Alto: 50-75%
  └─ Muito Alto: > 75%
  ↓
Retorna PredictionOutput (JSON)
  ↓
JavaScript renderiza resultado
  ↓
Exibe para usuário com animações
```

## Estrutura de Dados

### Input: PredictionInput
```python
{
    "pregnancies": float,                    # Número de gestações
    "glucose": float,                        # Glicose em mg/dL
    "blood_pressure": float,                 # Pressão em mmHg
    "skin_thickness": float,                 # Espessura em mm
    "insulin": float,                        # Insulina em µU/ml
    "bmi": float,                            # IMC em kg/m²
    "diabetes_pedigree_function": float,     # Histórico familiar (0-1)
    "age": float                             # Idade em anos
}
```

### Output: PredictionOutput
```python
{
    "diabetes_risk_percentage": float,       # 0.0 - 100.0
    "risk_level": str,                       # "Baixo", "Moderado", "Alto", "Muito Alto"
    "risk_factors": [
        {
            "feature": str,                  # Nome da feature
            "impact_value": float,           # Valor SHAP
            "impact_percentage": float       # Percentual de impacto
        }
    ],
    "model_used": str,                       # "Random Forest" ou "Regressão Logística"
    "confidence": float                      # 0.0 - 100.0
}
```

## Modelos de Machine Learning

### Random Forest Classifier
```python
RandomForestClassifier(
    n_estimators=100,      # 100 árvores de decisão
    max_depth=10,          # Profundidade máxima
    random_state=42,       # Reprodutibilidade
    n_jobs=-1              # Usar todos os cores
)
```

**Vantagens**:
- Melhor acurácia em geral
- Resistente a overfitting
- Feature importance nativa
- SHAP TreeExplainer rápido

**Performance típica**:
- Acurácia: 76-78%
- AUC-ROC: 0.82-0.84

### Regressão Logística
```python
LogisticRegression(
    max_iter=1000,         # Máximo de iterações
    random_state=42
)
```

**Vantagens**:
- Mais rápido
- Mais interpretável
- Menos overhead computacional
- Bom para features lineares

**Performance típica**:
- Acurácia: 73-75%
- AUC-ROC: 0.78-0.80

### Seleção de Modelo
- Usa o modelo com **melhor acurácia** em validação
- Tipicamente: **Random Forest**

## SHAP (SHapley Additive exPlanations)

### O que é?
Técnica baseada em teoria dos jogos para explicar predições de ML.

### Como funciona?
```
Para cada feature:
  1. Calcula contribuição marginal
  2. Média sobre todas as permutações
  3. Atribui "Shapley Value"
  
Resultado:
  ✓ Explica EXATAMENTE que feature influenciou a predição
  ✓ Mostra direção (aumenta/diminui risco)
  ✓ Mostra magnitude (quanto influenciou)
```

### Implementação

**Para Random Forest** (TreeExplainer - Rápido):
```python
explainer = shap.TreeExplainer(model_rf)
shap_values = explainer.shap_values(X)[1]  # Class 1 (Diabetes)
```

**Para Regressão Logística** (KernelExplainer - Flexível):
```python
explainer = shap.KernelExplainer(
    model_lr.predict_proba,
    shap.sample(X_train, 50)
)
shap_values = explainer.shap_values(X)
```

### Exemplo de Output
```
Feature                 SHAP Value  Impact %
────────────────────────────────────────────
Glucose                    0.45      45.3%
BMI                        0.30      30.2%
Age                        0.15      15.1%
BloodPressure             -0.08      8.1%
Insulin                   -0.02      2.0%
────────────────────────────────────────────
Total                      0.99      100.0%
```

## Segurança

### Input Validation (Pydantic)
```python
# Valida automaticamente:
✓ Tipos de dados
✓ Range de valores
✓ Presença de campos obrigatórios
✗ Rejeita entrada inválida
```

### CORS
```python
# Permite requisições de qualquer origem
app.add_middleware(CORSMiddleware, allow_origins=["*"])
```

### Sem Armazenamento
```
✓ Dados não são salvos em banco de dados
✓ Nenhum rastreamento do usuário
✓ Sem cookies de tracking
✓ Compliant com LGPD/GDPR
```

## Performance

### Tempos Típicos

| Operação | Tempo |
|----------|-------|
| Startup | 15-30s (primeira vez) |
| Predição | 50-100ms |
| SHAP Explanation | 20-50ms |
| Total Request | 100-200ms |

### Escalabilidade

- **Concurrent Users**: 100+ (com gunicorn workers)
- **Requests/sec**: 5-10 (single worker)
- **Memory Footprint**: ~200MB (modelos + dados)

## Deployment

### Opção 1: Desenvolvimento Local
```bash
python app.py
# http://localhost:8000
```

### Opção 2: Docker
```bash
docker build -t pimaguard .
docker run -p 8000:8000 pimaguard
```

### Opção 3: Docker Compose (Recomendado)
```bash
docker-compose up
# API: http://localhost:8000
# Frontend: http://localhost:80
```

### Opção 4: Production (Gunicorn + Nginx)
```bash
# Backend
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Nginx (reverse proxy)
# Servir static files + proxy para API
```

## Variáveis de Ambiente

```bash
# .env
PORT=8000
WORKERS=4
DEBUG=False
CORS_ORIGINS=*
MODEL_PATH=./models
DATA_PATH=./data
```

## 📝 Logs e Debugging

### Log Levels
```python
# Desenvolvimento
uvicorn app:app --log-level debug

# Produção
uvicorn app:app --log-level warning
```

### Estrutura de Logs
```
2025-05-29 10:15:32 [INFO] Iniciando servidor
2025-05-29 10:15:35 [INFO] ✓ Models loaded successfully
2025-05-29 10:15:45 [INFO] POST /predict - 200 OK (125ms)
```

## 🧪 Testes (Futuro)

Estrutura recomendada:
```
tests/
├── test_api.py           # Testes de endpoints
├── test_models.py        # Testes de ML
├── test_explainer.py     # Testes SHAP
└── conftest.py           # Fixtures
```

---

**Questões? Abra uma issue no repositório!**
