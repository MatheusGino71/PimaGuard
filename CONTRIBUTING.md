# 🛠️ DESENVOLVIMENTO E CONTRIBUIÇÃO

## 🔨 Setup para Desenvolvimento

### Pré-requisitos
- Python 3.9+
- Node.js 16+ (opcional)
- Git
- Editor: VS Code (recomendado)

### 1. Clone e Configure

```bash
git clone <repository>
cd PimaGuard

pip install -r requirements.txt
pip install -r requirements-dev.txt  # Para desenvolvimento
## Estrutura de Contribuição

### 2. Extensões VS Code Recomendadas

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.debugpy",
## Convenção de Commits
    "ms-vscode.makefile-tools",
    "bradlc.vscode-tailwindcss",
    "formulahendry.code-runner"
  ]
}
```

## Estrutura de Contribuição

### Branch Strategy

```
## Code Quality
  ├─ develop          ← Desenvolvimento (staging)
  │  ├─ feature/...   ← Novas features
  │  ├─ bugfix/...    ← Correções
  │  └─ refactor/...  ← Melhorias
  └─ hotfix/...       ← Correções críticas
```

### Workflow Exemplo

## Melhorias Planejadas
# 1. Criar branch
# 3. Commit
git add .
## Feature Request


## Performance e Otimização
```

## Convenção de Commits

```
feat:       Nova feature
## CI/CD (GitHub Actions)
docs:       Documentação
style:      Formatação (sem mudança de lógica)
refactor:   Refatoração de código
perf:       Melhoria de performance
test:       Testes
## Code Review Checklist
```
```

## 🧪 Testes


```
tests/
├── __init__.py
├── conftest.py                    # Fixtures
├── test_api.py
│   ├── test_health_endpoint()
│   ├── test_predict_endpoint()
│   ├── test_invalid_input()
│   └── test_cors()
├── test_models.py
│   ├── test_data_loading()
│   ├── test_train_models()
│   ├── test_model_persistence()
│   └── test_predictions()
└── test_explainer.py
    ├── test_shap_values()
    ├── test_feature_importance()
    └── test_risk_factors()
```

### Executar Testes

```bash
# Todos
pytest

# Específico
pytest tests/test_api.py::test_predict_endpoint

# Com cobertura
pytest --cov=app --cov-report=html

# Verbose
pytest -v
```

## Code Quality

### Linting com Ruff

```bash
# Instalar
pip install ruff

# Verificar
ruff check .

# Corrigir automaticamente
ruff check --fix .
```

### Formatação com Black

```bash
# Instalar
pip install black

# Formatar
black .
```

### Type Checking com Mypy

```bash
# Instalar
pip install mypy

# Verificar
mypy app.py
```

### Pre-commit Hook

```bash
# Instalar
pip install pre-commit

# Setup
pre-commit install

# Rodar manualmente
pre-commit run --all-files
```

**.pre-commit-config.yaml**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.245
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
```

## Melhorias Planejadas

### Curto Prazo (v1.1)
- [ ] Adicionar testes unitários
- [ ] Implementar logging estruturado
- [ ] Cache de predições
- [ ] Rate limiting
- [ ] Health check melhorado

### Médio Prazo (v2.0)
- [ ] Banco de dados (PostgreSQL)
- [ ] Autenticação (JWT)
- [ ] Dashboard admin
- [ ] Histórico de predições
- [ ] Export de relatórios (PDF)
- [ ] Multi-idioma

### Longo Prazo (v3.0)
- [ ] Mobile app (React Native)
- [ ] Integração com EHR
- [ ] Modelos adicionais (XGBoost)
- [ ] Explicabilidade avançada (LIME)
- [ ] ML ops (MLflow)
- [ ] API Gateway (Kong)

## 🐛 Bug Reporting

### Template de Issue

```markdown
## Descrição
[Descreva o bug]

## Steps to Reproduce
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

## Comportamento Esperado
[O que deveria acontecer]

## Comportamento Atual
[O que está acontecendo]

## Screenshots
[Se aplicável]

## Ambiente
- OS: [Windows/Linux/Mac]
- Python: [versão]
- Browser: [Chrome/Firefox/Safari]

## Logs
```
[Copie os logs aqui]
```
```

## Feature Request

### Template de Sugestão

```markdown
## Descrição
[Descreva a feature]

## Motivação
[Por que essa feature seria útil?]

## Casos de Uso
1. [Uso 1]
2. [Uso 2]

## Solução Proposta
[Como você gostaria que fosse implementado?]

## Alternativas Consideradas
[Outras abordagens?]
```

## 📖 Documentação

### Ao Adicionar Feature

1. Atualizar docstrings
2. Adicionar exemplos de uso
3. Atualizar README/TECHNICAL.md
4. Adicionar ao changelog

### Docstring Format

```python
def predict_with_explanation(self, X_input):
    """
    Fazer predição com explicação SHAP.
    
    Esta função recebe dados do paciente normalizados,
    realiza a predição do melhor modelo e calcula
    os SHAP values para explicabilidade.
    
    Args:
        X_input (np.ndarray): Array com 8 features médicas.
                             Deve estar na ordem:
                             [pregnancies, glucose, blood_pressure,
                              skin_thickness, insulin, bmi,
                              diabetes_pedigree_function, age]
    
    Returns:
        tuple: (probability, risk_factors)
            - probability (float): Probabilidade de diabetes (0-1)
            - risk_factors (list): Lista de dicts com:
              {
                'feature': str,
                'shap_value': float,
                'impact': float (absoluto)
              }
    
    Raises:
        ValueError: Se X_input não tem 8 features
        RuntimeError: Se modelos não estão carregados
    
    Examples:
        >>> pipeline.predict_with_explanation([1, 120, 70, 20, 30, 25, 0.5, 30])
        (0.425, [{'feature': 'Glucose', 'shap_value': 0.85, 'impact': 0.85}, ...])
    """
    pass
```

## Performance e Otimização

### Profiling

```bash
# Com cProfile
python -m cProfile -s cumulative app.py

# Com line_profiler
pip install line_profiler
kernprof -l -v app.py
```

### Benchmarks

```python
import time

# Medir tempo de predição
start = time.time()
result = pipeline.predict_with_explanation(X)
end = time.time()

print(f"Tempo: {(end-start)*1000:.2f}ms")
```

## 🔄 CI/CD (GitHub Actions)

### `.github/workflows/tests.yml`

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Lint
        run: |
          ruff check .
          black --check .
      
      - name: Type check
        run: mypy app.py
      
      - name: Run tests
        run: pytest --cov=app
      
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## 🤝 Code Review Checklist

Ao revisar PRs, verificar:

- [ ] Código segue convenções do projeto
- [ ] Tests são adicionados/atualizados
- [ ] Documentação é atualizada
- [ ] Sem breaking changes (ou bem documentadas)
- [ ] Performance não é degradada
- [ ] Segurança está ok
- [ ] Commit messages são claras

## 📞 Comunicação

### Canais
- 💬 GitHub Issues: Bugs e features
- 💭 GitHub Discussions: Dúvidas
- 📧 Email: Para assuntos sensíveis
- Wiki: Documentação compartilhada

## 📜 Licença

Este projeto é MIT licensed. Veja [LICENSE](LICENSE) para detalhes.

---

**Obrigado por contribuir! 🙏**
