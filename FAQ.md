# FAQ e SUPORTE - PimaGuard

## Perguntas Frequentes

### Instalação & Setup

#### P: Como instalar o PimaGuard?
**R:** Veja [QUICK_START.md](QUICK_START.md) para guia rápido ou [README.md](README.md) para instruções detalhadas.

#### P: Qual é a versão mínima de Python necessária?
**R:** Python 3.9+ é obrigatório. Testado em Python 3.9, 3.10 e 3.11.

#### P: Como faço se não consigo baixar o dataset do Kaggle?
**R:** O sistema cria automaticamente um dataset sintético como fallback. A funcionalidade não é afetada.

#### P: Posso usar em Windows/Mac/Linux?
**R:** Sim! PimaGuard é compatível com todos os sistemas operacionais. Use:
- Windows: `run.bat`
- Linux/Mac: `run.sh` (com `chmod +x run.sh`)

---

### Uso da Aplicação

#### P: Os meus dados são seguros?
**R:** Sim! Os dados:
- ❌ NÃO são armazenados em nenhum lugar
- ❌ NÃO são enviados para servidores externos
- ❌ NÃO são rastreados
- ✓ Processados apenas para a predição
- ✓ Deletados imediatamente após

#### P: Qual é a acurácia do modelo?
**R:** 
- Random Forest: ~76-78%
- Regressão Logística: ~73-75%

Não é diagnóstico médico - sempre consulte um profissional!

#### P: Por quanto tempo funciona a predição?
**R:** Tipicamente 100-200ms incluindo:
- Normalização: ~20ms
- Predição: ~50-100ms
- SHAP explanation: ~20-50ms

#### P: Posso usar o sistema offline?
**R:** Sim! Após o primeiro treino, todos os modelos são salvos e funcionam completamente offline.

#### P: Os resultados são diferentes cada vez?
**R:** Não, porque usamos `random_state=42` para reprodutibilidade. Mesmos dados = mesmos resultados.

---

### Técnico & Desenvolvimento

#### P: Como adiciono novos modelos?
**R:** Edite `app.py`, na função `train_models()`:

```python
def train_models(self):
    # ... modelos existentes ...
    
    # Adicione seu modelo
    self.model_xgboost = XGBClassifier(...)
    self.model_xgboost.fit(self.X_train, self.y_train)
```

#### P: Como mudo o algoritmo selecionado?
**R:** Em `app.py`, na função `train_models()`, altere:

```python
# Atual: usa o melhor (por acurácia)
self.best_model = self.model_rf if rf_score >= lr_score else self.model_lr

# Sempre usar Random Forest:
self.best_model = self.model_rf
```

#### P: Como adiciono mais variáveis?
**R:** Requer retreinamento com novo dataset. O Pima tem apenas 8 variáveis.

#### P: Posso treinar com meu próprio dataset?
**R:** Sim! Coloque um CSV em `backend/data/` e modifique:

```python
def download_dataset(self):
    self.df = pd.read_csv('backend/data/seu_dataset.csv')
```

#### P: Como ativo mode de debug?
**R:** Em `app.py`, adicione:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, log_level="debug")
```

---

### Deployment & Produção

#### P: Como faço deploy em produção?
**R:** Opções:

1. **Heroku**:
   ```bash
   git push heroku main
   ```

2. **Docker**:
   ```bash
   docker-compose up
   ```

3. **AWS/Azure/Google Cloud**:
   Use container services ou App Services

4. **On-premise**:
   Configure nginx + gunicorn + supervisor

#### P: Como faço deploy no Vercel/Netlify?
**R:** Apenas o frontend pode ir nesses. Backend precisa de suporte a Python (não suportado).

#### P: Como implemento autenticação?
**R:** Use JWT. Exemplo:

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()

@app.post("/predict")
async def predict(
    input_data: PredictionInput,
    credentials: HTTPAuthCredentials = Depends(security)
):
    # Validar token...
    pass
```

#### P: Como adiciono banco de dados?
**R:** Instale SQLAlchemy:

```bash
pip install sqlalchemy psycopg2
```

Crie models e migrações (Alembic):

```bash
pip install alembic
alembic init migrations
```

#### P: Como aumenta a performance?
**R:** 
1. Use Gunicorn com múltiplos workers
2. Configure cache (Redis)
3. Use CDN para frontend
4. Implemente rate limiting
5. Considere model quantization

---

### Troubleshooting

#### P: "ModuleNotFoundError: No module named 'kagglehub'"
**R:** Instale:
```bash
pip install kagglehub
```

#### P: "Port 8000 already in use"
**R:** Mude de porta:
```bash
python app.py --port 9000
```

Ou mate o processo na porta:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

#### P: "Connection refused" no frontend
**R:** Verifique:
1. Backend rodando? `python app.py`
2. Porta correta? (deve ser 8000)
3. URL frontend? (http://localhost:8000)
4. CORS habilitado? (deve estar)

#### P: "CORS error" no navegador
**R:** O backend já tem CORS configurado. Se ainda ter erro:

```python
# Em app.py, aumentar permissões:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### P: Modelos não carregam
**R:** Delete arquivos .pkl e retreine:

```bash
rm backend/models/*.pkl
python app.py
```

#### P: Muito lento na primeira execução
**R:** Normal! Coisas que levam tempo:
- Download do dataset: 5-10s
- Treinamento RF: 5-10s
- Criação SHAP: 5-15s

**Total: 15-30s primeira vez**

Segunda vez é rápido (carrega .pkl)

#### P: "ImportError: cannot import name..."
**R:** Dependências faltando:

```bash
pip install -r requirements.txt --upgrade
```

---

### Contribuição

#### P: Como reporto um bug?
**R:** Abra uma issue com:
- Descrição clara
- Steps to reproduce
- Resultado esperado vs. atual
- Screenshots/logs

Template: [bug_report.md](.github/ISSUE_TEMPLATE/bug_report.md)

#### P: Como sugiro uma feature?
**R:** Abra uma discussion ou issue tipo "Feature Request":
- Motivação clara
- Casos de uso
- Solução proposta

Template: [feature_request.md](.github/ISSUE_TEMPLATE/feature_request.md)

#### P: Como contribuo código?
**R:** Veja [CONTRIBUTING.md](CONTRIBUTING.md) para workflow completo.

#### P: Qual é a licença?
**R:** MIT License. Libre para uso comercial.

---

### Conceitos

#### P: O que é SHAP?
**R:** SHapley Additive exPlanations - técnica que explica cada predição mostrando qual feature teve mais impacto.

Exemplo:
```
Risco: 42.5%

Fatores (por impacto):
- Glicose: +15% (maior impacto)
- IMC: +10%
- Idade: +5%
```

#### P: Qual a diferença entre os modelos?
**R:**
| Aspecto | Random Forest | Regressão Logística |
|---------|---|---|
| Acurácia | 78% | 75% |
| Velocidade | Média | Rápida |
| Interpretabilidade | Média | Alta |
| Complexidade | Alta | Baixa |

#### P: O que é o dataset Pima?
**R:** Base de dados do UCI com 768 registros de saúde de mulheres Pima com 8 variáveis médicas e diagnóstico de diabetes.

#### P: Como funciona o split treino/teste?
**R:** 
- Treino: 614 samples (80%) - usado para treinar
- Teste: 154 samples (20%) - usado para avaliar

Com stratification para manter proporção de classes.

---

### Roadmap & Futuro

#### P: Quando sai a próxima versão?
**R:** Veja [CHANGELOG.md](CHANGELOG.md) para roadmap. Planejado:
- v1.1 (Q2 2025): Testes + logging + cache
- v2.0 (Q3 2025): Auth + DB + Dashboard
- v3.0 (2026): Mobile app + MLops

#### P: Posso usar em produção agora?
**R:** Sim! Mas configure:
- [ ] HTTPS
- [ ] Autenticação
- [ ] Rate limiting
- [ ] Banco de dados
- [ ] Logging
- [ ] Monitoramento

---

## 📞 Canais de Suporte

### Rápida Resposta
1. **GitHub Issues**: Bugs, features
   - Público
   - Histórico permanente
   - Melhor para dúvidas técnicas

### Discussões
2. **GitHub Discussions**: Dúvidas gerais
   - Fórum estilo
   - Bom para comunidade

### Contato Direto
3. **Email**: support@pimaguard.dev
   - Para tópicos sensíveis
   - Comercial/enterprise

### Comunidade
4. **Discord** (futuro): Chat em tempo real

---

## 🆘 Precisa de Ajuda Urgente?

### Checklist de Debugging

```bash
# 1. Verificar Python
python --version

# 2. Verificar dependências
pip list | grep -E "fastapi|scikit-learn|shap"

# 3. Testar imports
python -c "from app import app; print('OK')"

# 4. Verificar porta
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Linux/Mac

# 5. Limpar cache
rm -rf __pycache__
rm backend/models/*.pkl

# 6. Reinstalar
pip install -r requirements.txt --force-reinstall
```

### Logs para Compartilhar

Ao abrir issue, inclua:
```bash
# Versão
python --version
pip list

# Log de startup
python app.py > app.log 2>&1

# Log do erro (stdout)
# (copie a mensagem de erro completa)
```

---

## Recursos Adicionais

- [Documentação FastAPI](https://fastapi.tiangolo.com)
- [Documentação Scikit-learn](https://scikit-learn.org)
- [Documentação SHAP](https://shap.readthedocs.io)
- [Dataset Pima](https://archive.ics.uci.edu/ml/datasets/pima+indians+diabetes)
- [TailwindCSS Docs](https://tailwindcss.com/docs)

---

**Dúvidas? Abra uma issue ou contacte suporte!**

**Últimas dúvidas? Leia o README.md completo ou TECHNICAL.md** 📖
