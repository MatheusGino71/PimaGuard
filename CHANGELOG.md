# 📅 CHANGELOG - PimaGuard

Todos as mudanças notáveis neste projeto serão documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/),
e este projeto segue [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Não Lançado]

### Planejado
- [ ] Autenticação JWT
- [ ] Banco de dados PostgreSQL
- [ ] Dashboard de administrador
- [ ] Export de relatórios em PDF
- [ ] Multi-idioma (i18n)
- [ ] Modelos adicionais (XGBoost, LightGBM)
- [ ] LIME para explicabilidade alternativa
- [ ] Mobile app (React Native)
- [ ] MLops com MLflow
- [ ] CI/CD pipeline completo

## [1.0.0] - 2025-05-29

### 🎉 Lançado
- Backend FastAPI completo com Machine Learning
- 2 algoritmos de classificação (Random Forest + Regressão Logística)
- SHAP para explicabilidade e transparência
- Pipeline automático de dados
- Download automático do dataset Pima com kagglehub
- Frontend HTML/CSS/JS elegante e responsivo
- API RESTful com validação Pydantic
- CORS configurado
- Documentação Swagger/ReDoc
- Docker e Docker Compose
- Testes básicos de estrutura
- README completo
- Guia de início rápido
- Documentação técnica detalhada

### Features Implementadas

#### Backend
- ✓ Autenticação de entrada com Pydantic
- ✓ Pipeline de ML completo
- ✓ Tratamento de dados ausentes
- ✓ Normalização com StandardScaler
- ✓ Split treino/teste com stratification
- ✓ Treinamento de 2 modelos
- ✓ Avaliação de performance
- ✓ SHAP TreeExplainer e KernelExplainer
- ✓ Persistência de modelos com joblib
- ✓ Carregamento automático de modelos salvos
- ✓ Endpoint /predict com explicabilidade
- ✓ Health check endpoints
- ✓ Informações de modelo

#### Frontend
- ✓ Design minimalista elegante (TailwindCSS)
- ✓ Menu responsivo
- ✓ Formulário com 8 inputs de dados médicos
- ✓ Validação de entrada
- ✓ Requisição assíncronas com Fetch API
- ✓ Exibição de resultados com animações
- ✓ Código de cores por nível de risco
- ✓ Exibição de fatores de risco com impacto
- ✓ Download de relatório em TXT
- ✓ Reset de formulário
- ✓ Estados de loading, sucesso e erro
- ✓ Smooth scrolling

#### Documentação
- ✓ README.md completo
- ✓ QUICK_START.md com guia rápido
- ✓ TECHNICAL.md com arquitetura
- ✓ CONTRIBUTING.md com guia de contribuição
- ✓ CHANGELOG.md
- ✓ API Documentation (Swagger)

#### DevOps
- ✓ requirements.txt com dependências
- ✓ requirements-dev.txt para desenvolvimento
- ✓ Dockerfile para containerização
- ✓ Docker Compose com frontend e backend
- ✓ nginx.conf para produção
- ✓ .env.example com configurações
- ✓ .gitignore
- ✓ Script run.bat para Windows
- ✓ Script run.sh para Linux/Mac

### Detalhes Técnicos

**Backend**:
- Python 3.9+
- FastAPI 0.109.1
- scikit-learn 1.4.1
- pandas 2.1.4
- numpy 1.24.3
- shap 0.45.1
- kagglehub 0.2.10
- joblib 1.3.2

**Frontend**:
- HTML5
- TailwindCSS via CDN
- JavaScript Vanilla (ES6+)
- Lucide Icons
- Google Fonts (Bebas Neue, Inter, JetBrains Mono, Playfair Display)

### Performance
- Tempo de startup: 15-30s (primeira vez)
- Tempo de predição: 50-100ms
- Tempo de explicação SHAP: 20-50ms
- Latência total: 100-200ms

### 🔒 Segurança
- Input validation com Pydantic
- CORS configurado
- Sem armazenamento de dados
- Sem autenticação (implementar em v2)
- Sem HTTPS (configurar em produção)

### Acurácia dos Modelos
- Random Forest: ~76-78%
- Regressão Logística: ~73-75%
- AUC-ROC: 0.82-0.84

---

## Formato de Versão

### Adicionado
Para novas features

### Alterado
Para mudanças em funcionalidade existente

### Deprecado
Para features que serão removidas em breve

### Removido
Para features removidas

### Consertado
Para correções de bugs

### Segurança
Para correções de segurança

---

## Como Contribuir

1. Abra uma issue descrevendo a mudança
2. Faça um fork do projeto
3. Crie uma branch: `git checkout -b feature/melhoria`
4. Faça commit das mudanças: `git commit -am 'feat: adiciona melhoria'`
5. Push para a branch: `git push origin feature/melhoria`
6. Abra um Pull Request

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes.

---

## Roadmap

### Q2 2025 (Próximo)
- [ ] Testes unitários completos
- [ ] Logging estruturado
- [ ] Cache de predições
- [ ] Rate limiting

### Q3 2025
- [ ] Autenticação JWT
- [ ] Banco de dados PostgreSQL
- [ ] Dashboard admin
- [ ] Export PDF

### Q4 2025
- [ ] Multi-idioma
- [ ] Modelos adicionais (XGBoost)
- [ ] LIME explanation
- [ ] Mobile app

### 2026
- [ ] MLops (MLflow)
- [ ] Kubernetes deployment
- [ ] Advanced analytics
- [ ] Integração com EHR

---

## 📞 Suporte

- 📧 Email: support@pimaguard.dev
- 🐛 Issues: https://github.com/user/pimaguard/issues
- 💬 Discussions: https://github.com/user/pimaguard/discussions
- 📖 Docs: https://pimaguard-docs.dev

---

**Obrigado por usar PimaGuard! 🙏**
