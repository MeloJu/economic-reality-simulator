# 📚 Índice de Documentação

**Pipeline Socioeconômico — Guia Completo de Navegação**

---

## 🚀 INÍCIO RÁPIDO

**Novo no projeto? Comece aqui:**

1. 📖 [README.md](README.md) — Visão geral do projeto
2. 🏆 [GOLD_SUMMARY.md](GOLD_SUMMARY.md) — Resultados principais
3. 🚀 [QUICK_REFERENCE.md](QUICK_REFERENCE.md) — Referência rápida

---

## 📊 POR CAMADA

### 🥉 RAW (Bronze) — Dados Brutos

| Documento | Descrição |
|-----------|-----------|
| [raw/README.md](raw/README.md) | Documentação completa da camada RAW |

**Datasets:**
- `people_raw.csv` — 10.000 indivíduos
- `economic_context_raw.csv` — 18 cidades/países
- `cultural_costs_raw.csv` — Custos culturais
- `opportunity_costs_raw.csv` — Custos de oportunidades
- `social_benefits_raw.csv` — Benefícios sociais

**Script:** [generate_raw_data.py](src/generate_raw_data.py)

---

### 🥈 SILVER (Enriched) — Feature Engineering

| Documento | Descrição |
|-----------|-----------|
| [enriched/README.md](enriched/README.md) | Documentação técnica detalhada |
| [SILVER_SUMMARY.md](SILVER_SUMMARY.md) | Sumário executivo |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Referência rápida |

**Datasets:**
- `people_enriched.csv` — Métricas individuais (27 colunas)
- `household_costs_enriched.csv` — Composição de custos
- `cultural_access_enriched.csv` — IAC (Índice de Acesso Cultural)
- `opportunity_access_enriched.csv` — IOE (Índice de Oportunidades)
- `cross_country_family_simulation.csv` — Simulação internacional
- `cross_country_family_comparison.csv` — Comparações familiares

**Scripts:**
- [generate_enriched_data.py](src/generate_enriched_data.py) — Pipeline principal
- [validate_enriched_data.py](src/validate_enriched_data.py) — Validação
- [exemplos_uso_silver.py](src/exemplos_uso_silver.py) — Exemplos práticos

---

### 🏆 GOLD (Business) — Decisão e Insights

| Documento | Descrição |
|-----------|-----------|
| [gold/README.md](gold/README.md) | Documentação técnica completa (500+ linhas) |
| [GOLD_SUMMARY.md](GOLD_SUMMARY.md) | Sumário executivo para gestores |
| [GOLD_QUICK_REFERENCE.md](GOLD_QUICK_REFERENCE.md) | Referência rápida |
| [POWER_BI_INTEGRATION.md](POWER_BI_INTEGRATION.md) | Guia de integração Power BI |

**Datasets:**
- `quality_of_life_score.csv` — Score QLES (0-100)
- `socioeconomic_clusters.csv` — 6 clusters interpretativos
- `country_rankings_by_profile.csv` — Rankings contextuais
- `vulnerability_and_risk.csv` — Análise de risco
- `policy_scenarios.csv` — Simulações de políticas

**Scripts:**
- [generate_gold_data.py](src/generate_gold_data.py) — Pipeline GOLD (470+ linhas)
- [exemplos_uso_gold.py](src/exemplos_uso_gold.py) — Exemplos práticos

---

## 🎯 POR OBJETIVO

### Quero entender o projeto
→ [README.md](README.md)

### Quero ver os resultados principais
→ [GOLD_SUMMARY.md](GOLD_SUMMARY.md)

### Quero executar o pipeline
→ README.md (seção "Quick Start")

### Quero analisar dados no Python
→ [exemplos_uso_silver.py](src/exemplos_uso_silver.py)  
→ [exemplos_uso_gold.py](src/exemplos_uso_gold.py)

### Quero criar dashboard no Power BI
→ [POWER_BI_INTEGRATION.md](POWER_BI_INTEGRATION.md)

### Quero entender as métricas
→ [SILVER_SUMMARY.md](SILVER_SUMMARY.md) (features)  
→ [GOLD_SUMMARY.md](GOLD_SUMMARY.md) (scores e clusters)

### Quero referência rápida
→ [QUICK_REFERENCE.md](QUICK_REFERENCE.md) (SILVER)  
→ [GOLD_QUICK_REFERENCE.md](GOLD_QUICK_REFERENCE.md) (GOLD)

### Quero contribuir ou modificar
→ [CHANGELOG.md](CHANGELOG.md)  
→ Documentação técnica por camada

---

## 👥 POR PERFIL

### 📊 Data Analyst
**Objetivo:** Análises exploratórias

1. [SILVER_SUMMARY.md](SILVER_SUMMARY.md) — Entender features
2. [exemplos_uso_silver.py](src/exemplos_uso_silver.py) — Exemplos práticos
3. [enriched/README.md](enriched/README.md) — Detalhes técnicos

### 🧠 Data Scientist
**Objetivo:** Modelagem e insights

1. [GOLD_SUMMARY.md](GOLD_SUMMARY.md) — Scores e clusters
2. [gold/README.md](gold/README.md) — Metodologia técnica
3. [generate_gold_data.py](src/generate_gold_data.py) — Implementação

### 💼 Business Intelligence
**Objetivo:** Dashboards e relatórios

1. [POWER_BI_INTEGRATION.md](POWER_BI_INTEGRATION.md) — Guia completo
2. [GOLD_QUICK_REFERENCE.md](GOLD_QUICK_REFERENCE.md) — Datasets disponíveis
3. [GOLD_SUMMARY.md](GOLD_SUMMARY.md) — Insights para storytelling

### 🎯 Product Manager / Gestor
**Objetivo:** Decisão executiva

1. [GOLD_SUMMARY.md](GOLD_SUMMARY.md) — Visão executiva
2. [README.md](README.md) — Contexto geral
3. Power BI Dashboard (quando disponível)

### 🔧 Data Engineer
**Objetivo:** Pipeline e infraestrutura

1. [README.md](README.md) — Arquitetura
2. [generate_raw_data.py](src/generate_raw_data.py) → [generate_enriched_data.py](src/generate_enriched_data.py) → [generate_gold_data.py](src/generate_gold_data.py)
3. [validate_enriched_data.py](src/validate_enriched_data.py) — Validação

---

## 📈 MÉTRICAS E INDICADORES

### Econômicas (SILVER)
- **RDR** (Renda Disponível Real) → [enriched/README.md](enriched/README.md#renda-disponível-real)
- **EPR** (Economic Pressure Ratio) → [enriched/README.md](enriched/README.md#economic-pressure-ratio)
- **IAC** (Índice de Acesso Cultural) → [enriched/README.md](enriched/README.md#índice-de-acesso-cultural)
- **IOE** (Índice de Oportunidades) → [enriched/README.md](enriched/README.md#índice-de-oportunidades-econômicas)

### Scores (GOLD)
- **QLES** (Quality of Life Economic Score) → [GOLD_SUMMARY.md](GOLD_SUMMARY.md#score-principal-qles)

### Segmentação (GOLD)
- **6 Clusters Socioeconômicos** → [GOLD_SUMMARY.md](GOLD_SUMMARY.md#segmentação-6-clusters)

### Risco (GOLD)
- **Vulnerability Flags** → [gold/README.md](gold/README.md#vulnerability-and-risk)
- **Risk Groups** → [GOLD_SUMMARY.md](GOLD_SUMMARY.md#vulnerabilidade-e-risco)

---

## 🛠️ CÓDIGO

| Script | Função | Linhas | Camada |
|--------|--------|--------|--------|
| [generate_raw_data.py](src/generate_raw_data.py) | Gera dados sintéticos | 200+ | RAW |
| [generate_enriched_data.py](src/generate_enriched_data.py) | Feature engineering | 350+ | SILVER |
| [generate_gold_data.py](src/generate_gold_data.py) | Scores e clusters | 470+ | GOLD |
| [validate_enriched_data.py](src/validate_enriched_data.py) | Validação SILVER | 100+ | SILVER |
| [exemplos_uso_silver.py](src/exemplos_uso_silver.py) | Exemplos SILVER | 300+ | SILVER |
| [exemplos_uso_gold.py](src/exemplos_uso_gold.py) | Exemplos GOLD | 400+ | GOLD |

**Total:** ~2.770+ linhas de código Python

---

## 📦 DATASETS

### Camada RAW
- 5 arquivos CSV
- 10.018 registros totais

### Camada SILVER
- 6 arquivos CSV
- 10.145 registros totais
- 27 colunas em `people_enriched.csv`

### Camada GOLD
- 6 arquivos CSV
- 40.145 registros totais (incluindo cenários)
- Design otimizado para Power BI

---

## 🔄 FLUXO DE TRABALHO

```
1. GERAÇÃO
   python src/generate_raw_data.py
   python src/generate_enriched_data.py
   python src/generate_gold_data.py

2. VALIDAÇÃO
   python src/validate_enriched_data.py

3. ANÁLISE
   python src/exemplos_uso_silver.py
   python src/exemplos_uso_gold.py

4. VISUALIZAÇÃO
   Power BI → POWER_BI_INTEGRATION.md
```

---

## 📊 DASHBOARDS RECOMENDADOS

1. **Visão Executiva** → KPIs principais
2. **Análise de Clusters** → Segmentação socioeconômica
3. **Vulnerabilidade e Risco** → Populações críticas
4. **Simulação de Cenários** → Impacto de políticas
5. **Rankings Comparativos** → Análise por perfil familiar

Ver detalhes: [POWER_BI_INTEGRATION.md](POWER_BI_INTEGRATION.md#visualizações-recomendadas)

---

## 🔍 BUSCA RÁPIDA

### Preciso saber sobre...

**Arquitetura do projeto**  
→ [README.md](README.md#arquitetura)

**Camadas do pipeline**  
→ [README.md](README.md#camadas-do-pipeline)

**Resultados principais**  
→ [README.md](README.md#principais-resultados)

**Como executar**  
→ [README.md](README.md#quick-start)

**Métricas implementadas**  
→ [SILVER_SUMMARY.md](SILVER_SUMMARY.md) e [GOLD_SUMMARY.md](GOLD_SUMMARY.md)

**Clusters socioeconômicos**  
→ [GOLD_SUMMARY.md](GOLD_SUMMARY.md#segmentação-6-clusters)

**Score QLES**  
→ [GOLD_SUMMARY.md](GOLD_SUMMARY.md#score-principal-qles)

**Integração Power BI**  
→ [POWER_BI_INTEGRATION.md](POWER_BI_INTEGRATION.md)

**Histórico de versões**  
→ [CHANGELOG.md](CHANGELOG.md)

---

## 📞 SUPORTE

### Issues e dúvidas
- Consultar documentação relevante acima
- Verificar [CHANGELOG.md](CHANGELOG.md) para atualizações

### Contribuições
- Ler [CHANGELOG.md](CHANGELOG.md#contribuições)
- Abrir Pull Request no repositório

---

## ✅ STATUS DO PROJETO

| Camada | Status | Datasets | Documentação |
|--------|--------|----------|--------------|
| RAW | ✅ Completo | 5 | ✅ |
| SILVER | ✅ Completo | 6 | ✅ |
| GOLD | ✅ Completo | 6 | ✅ |
| Power BI | 🔄 Guia pronto | - | ✅ |

**Versão atual:** 1.2.0  
**Última atualização:** 2026-01-08

---

**💡 Dica:** Use Ctrl+F neste documento para buscar palavras-chave específicas!
