# 📝 CHANGELOG

Todas as mudanças notáveis neste projeto serão documentadas aqui.

---

## [1.2.0] - 2026-01-08 🏆

### ✨ Adicionado - GOLD LAYER

#### Datasets
- `quality_of_life_score.csv` — Score QLES consolidado (0-100)
- `socioeconomic_clusters.csv` — 6 clusters interpretativos (K-Means)
- `country_rankings_by_profile.csv` — Rankings contextuais por perfil
- `vulnerability_and_risk.csv` — Flags de risco + classificação
- `policy_scenarios.csv` — 2 cenários de política simulados
- `cluster_statistics.csv` — Estatísticas agregadas por cluster

#### Scripts
- `src/generate_gold_data.py` — Pipeline GOLD (470+ linhas)
  - Cálculo do QLES (Quality of Life Economic Score)
  - Clusterização K-Means com validação por silhouette
  - Análise de vulnerabilidade com flags interpretáveis
  - Simulação de cenários de políticas públicas
  - Rankings por perfil familiar
  
- `src/exemplos_uso_gold.py` — 6 exemplos práticos de análise GOLD
  - Análise do QLES por categoria e cidade
  - Distribuição de clusters por cidade
  - Análise de vulnerabilidade e risco
  - Rankings por perfil familiar
  - Simulação de cenários
  - Análise integrada (QLES + Cluster + Vulnerabilidade)

#### Documentação
- `gold/README.md` — Documentação técnica completa (500+ linhas)
- `GOLD_SUMMARY.md` — Sumário executivo para gestores
- `GOLD_QUICK_REFERENCE.md` — Referência rápida
- `POWER_BI_INTEGRATION.md` — Guia de integração Power BI
  - Modelo de dados dimensional
  - 30+ medidas DAX prontas
  - 5 dashboards recomendados
  - Design system e paleta de cores
  - Checklist de implementação

### 🔧 Melhorado
- `README.md` — Atualizado com informações GOLD
  - Nova seção "Documentação Completa"
  - Resultados principais GOLD
  - Badges atualizados
  - Estrutura do projeto expandida

### 📊 Métricas
- **QLES médio nacional**: 18.09/100
- **6 clusters identificados** (silhouette: 0.371)
- **65% da população em Risco Alto**
- **2 cenários simulados** (impacto médio: -5% e -10%)
- **72 rankings gerados** (4 perfis familiares)

---

## [1.1.0] - 2026-01-07

### ✨ Adicionado - SILVER LAYER

#### Datasets
- `people_enriched.csv` — 10.000 registros com 27 colunas
- `household_costs_enriched.csv` — Composição detalhada de custos
- `cultural_access_enriched.csv` — Índice de Acesso Cultural (IAC)
- `opportunity_access_enriched.csv` — Índice de Oportunidades Econômicas (IOE)
- `cross_country_family_simulation.csv` — Simulação cross-country (73 registros)
- `cross_country_family_comparison.csv` — Comparações familiares (72 registros)

#### Scripts
- `src/generate_enriched_data.py` — Pipeline SILVER (350+ linhas)
  - Feature engineering completo
  - Normalização Z-score e Min-Max
  - Métricas compostas (IAC, IOE)
  - Simulação cross-country
  
- `src/validate_enriched_data.py` — Validação automática
  - 22 validações implementadas
  - Verificação de ranges, tipos e integridade
  
- `src/exemplos_uso_silver.py` — 6 exemplos práticos

#### Documentação
- `enriched/README.md` — Documentação técnica (400+ linhas)
- `SILVER_SUMMARY.md` — Sumário executivo
- `QUICK_REFERENCE.md` — Referência rápida

### 📊 Métricas
- **RDR médio**: R$ 1.557,31
- **58,98% com déficit** (custo > renda)
- **EPR mediano**: 1,28
- **IAC médio**: 5,55 meses
- **IOE médio**: 16,95 meses

---

## [1.0.0] - 2026-01-06

### ✨ Adicionado - RAW LAYER

#### Datasets
- `people_raw.csv` — 10.000 indivíduos sintéticos
  - Dados demográficos realistas
  - Salários por categoria e região
  - Composição familiar
  
- `economic_context_raw.csv` — 18 cidades/países
  - Brasil: 15 cidades
  - Internacional: Portugal (3 cidades)
  - Custo de vida por localização
  
- `cultural_costs_raw.csv` — Custos culturais
  - Streaming, internet, cinema
  - Eventos culturais, música
  
- `opportunity_costs_raw.csv` — Custos de oportunidades
  - Cursos técnicos, faculdade privada
  - Idiomas, mobilidade, poupança
  
- `social_benefits_raw.csv` — Benefícios sociais
  - Bolsa família
  - Auxílio emergencial
  - BPC

#### Scripts
- `src/generate_raw_data.py` — Gerador de dados sintéticos (200+ linhas)
  - Distribuições realistas por região
  - Correlações job_category × salary
  - Mapeamento de cidades brasileiras

#### Documentação
- `raw/README.md` — Documentação da camada RAW
- `README.md` — Documentação principal do projeto

### 🎯 Fundação
- Arquitetura Medallion implementada
- Pipeline de 3 camadas definido
- Estrutura de pastas organizada

---

## 🏗️ Roadmap Futuro

### [1.3.0] - Planejado
- [ ] Dashboard Power BI completo
- [ ] API REST para acesso aos dados
- [ ] Sistema de alertas (vulnerabilidade crítica)
- [ ] Análise temporal (dados históricos)

### [2.0.0] - Visão
- [ ] Machine Learning
  - Predição de vulnerabilidade
  - Recomendação de políticas
  - Otimização de alocação de recursos
- [ ] Dados reais (integração com fontes oficiais)
- [ ] Streaming analytics
- [ ] Deploy em nuvem (Azure/AWS)

---

## 📊 Estatísticas do Projeto

### Código
- **Total de linhas**: ~2.770+
- **Scripts Python**: 6
- **Datasets gerados**: 11
- **Documentos**: 10+

### Cobertura
- **RAW**: 5 datasets, 10.018 registros
- **SILVER**: 6 datasets, 10.145 registros
- **GOLD**: 6 datasets, 40.145 registros (com cenários)

### Métricas Implementadas
- **Econômicas**: 8 métricas
- **Normalizações**: 2 tipos (Z-score, Min-Max)
- **Compostas**: 2 índices (IAC, IOE)
- **Comparativas**: 3 métricas cross-country
- **Scores**: 1 consolidado (QLES)
- **Clusters**: 6 segmentos

### Análises
- **Vulnerabilidade**: 4 flags
- **Risco**: 4 níveis
- **Cenários**: 2 simulações
- **Rankings**: 4 perfis familiares

---

## 🤝 Contribuições

Este é um projeto educacional. Para sugestões ou melhorias:

1. Abra uma issue descrevendo a proposta
2. Fork o repositório
3. Crie uma branch (`feature/nova-funcionalidade`)
4. Commit suas mudanças
5. Push para a branch
6. Abra um Pull Request

---

## 📄 Licença

Este projeto é de código aberto para fins educacionais.

---

## 👥 Autores

- **Pipeline de Dados** — Implementação completa RAW → SILVER → GOLD
- **Feature Engineering** — Métricas socioeconômicas avançadas
- **Data Science** — Clusterização, scores consolidados
- **Documentação** — 10+ documentos técnicos

---

## 🙏 Agradecimentos

- **IBGE** — Referências de dados demográficos
- **DIEESE** — Índices de custo de vida
- **Kaggle Community** — Inspiração para feature engineering
- **Power BI Community** — Best practices de BI

---

**Última atualização**: 2026-01-08  
**Versão atual**: 1.2.0  
**Status**: ✅ Produção (GOLD Layer completa)
