# 🏗️ Pipeline Socioeconômico — RAW → SILVER → GOLD

**Análise de Dados Socioeconômicos com Feature Engineering**

[![Status](https://img.shields.io/badge/Status-GOLD%20Layer%20Completa-success)]()
[![Python](https://img.shields.io/badge/Python-3.14+-blue)]()
[![Data](https://img.shields.io/badge/Registros-10%2C000-orange)]()
[![Clusters](https://img.shields.io/badge/Clusters-6-purple)]()
[![Power BI](https://img.shields.io/badge/Power%20BI-Ready-yellow)]()

---

## 📋 VISÃO GERAL

Este projeto implementa um **pipeline completo de engenharia de dados** para análise socioeconômica, seguindo a arquitetura **Medallion** (Bronze → Silver → Gold).

**Novo:** 🏆 **Camada GOLD** completa com scores consolidados, clusterização interpretável e simulação de cenários prontos para Power BI!

### Arquitetura

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│             │      │             │      │             │
│  RAW        │ ───► │  SILVER     │ ───► │  GOLD       │
│  (Bronze)   │      │  (Enriched) │      │  (Business) │
│             │      │             │      │             │
│ Dados       │      │ Features    │      │ Decisões    │
│ Brutos      │      │ Derivadas   │      │ Scores      │
│             │      │             │      │ Rankings    │
└─────────────┘      └─────────────┘      └─────────────┘
```

---

## 📂 ESTRUTURA DO PROJETO

```
project-root/
│
├── raw/                              # 🥉 Camada RAW (Bronze)
│   ├── people_raw.csv                # 10.000 indivíduos
│   ├── economic_context_raw.csv      # 18 cidades/países
│   ├── cultural_costs_raw.csv        # Custos culturais
│   ├── opportunity_costs_raw.csv     # Custos de oportunidades
│   ├── social_benefits_raw.csv       # Benefícios sociais
│   └── README.md
│
├── enriched/                         # 🥈 Camada SILVER (Enriched)
│   ├── people_enriched.csv           # Métricas individuais
│   ├── household_costs_enriched.csv  # Composição de custos
│   ├── cultural_access_enriched.csv  # Acesso cultural (IAC)
│   ├── opportunity_access_enriched.csv # Oportunidades (IOE)
│   ├── cross_country_family_simulation.csv
│   ├── cross_country_family_comparison.csv
│   └── README.md
│
├── gold/                             # 🏆 Camada GOLD (Business)
│   ├── quality_of_life_score.csv     # Score QLES consolidado
│   ├── socioeconomic_clusters.csv    # 6 clusters interpretativos
│   ├── country_rankings_by_profile.csv # Rankings contextuais
│   ├── vulnerability_and_risk.csv    # Flags de risco
│   ├── policy_scenarios.csv          # Simulações de política
│   └── README.md
│
│
├── src/                              # 🐍 Scripts Python
│   ├── generate_raw_data.py          # Gera camada RAW
│   ├── generate_enriched_data.py     # Gera camada SILVER
│   ├── generate_gold_data.py         # Gera camada GOLD ⭐
│   ├── validate_enriched_data.py     # Valida SILVER
│   ├── exemplos_uso_silver.py        # Exemplos SILVER
│   └── exemplos_uso_gold.py          # Exemplos GOLD ⭐
│
├── SILVER_SUMMARY.md                 # 📊 Resumo SILVER
├── GOLD_QUICK_REFERENCE.md           # 🏆 Referência GOLD ⭐
├── QUICK_REFERENCE.md                # 📋 Referência rápida
├── StoryTelling.pbix                 # 📖 Analise dos dados e StoryTelling ⭐
└── README.md                         # 📖 Este arquivo
```

---

## 🚀 QUICK START

### 1️⃣ Instalação

```bash
# Clone o repositório
cd project-root

# Crie ambiente virtual
python -m venv .venv

# Ative o ambiente
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instale dependências
pip install pandas numpy scikit-learn
```

Nota (Windows): se aparecer erro de encoding ao imprimir emojis, execute antes do script:

```powershell
$env:PYTHONIOENCODING = 'utf-8'
```

### 2️⃣ Gerar Pipeline Completo

```bash
# Camada RAW (se ainda não existir)
python src/generate_raw_data.py

# Camada SILVER
python src/generate_enriched_data.py

# Camada GOLD ⭐
python src/generate_gold_data.py
```

### 3️⃣ Validar

```bash
python src/validate_enriched_data.py
```

### 4️⃣ Explorar

```bash
# Análises SILVER
python src/exemplos_uso_silver.py

# Análises GOLD ⭐
python src/exemplos_uso_gold.py
```

---

## 📊 CAMADAS DO PIPELINE

### 🥉 **RAW (Bronze)** — Dados Brutos
- 10.000 indivíduos sintéticos
- 18 cidades/países
- Custos culturais e de oportunidades
- Contexto econômico
- **Objetivo**: Dados realistas sem transformações

### 🥈 **SILVER (Enriched)** — Feature Engineering

**Métricas Econômicas:**
- ✅ **Total Household Cost** — custo doméstico total
- ✅ **Renda Disponível Real (RDR)** — renda após custos essenciais
- ✅ **Economic Pressure Ratio (EPR)** — pressão de custos sobre renda
- ✅ **Custo per Capita** — custo por pessoa da família
- ✅ **Gap de Subsistência** — valor disponível após custos

### 📊 **Comparativas**
- ✅ **Salário Mínimo Ajustado** — mínimo ajustado por dependentes
- ✅ **Distância do Salário Mínimo (DSMA)** — distância percentual
- ✅ **Social Support Ratio (SSR)** — proporção de benefícios

### 🎭 **Acesso Cultural**
- ✅ **Cultural Basic Cost** — custo de cultura básica
- ✅ **Índice de Acesso Cultural (IAC)** — capacidade de acessar cultura

### 🎯 **Oportunidades**
- ✅ **Índice de Oportunidades Econômicas (IOE)** — acesso a educação/mobilidade
  - Curso técnico
  - Faculdade privada
  - Idiomas
  - Poupança de emergência
  - Mobilidade

### 🌍 **Cross-Country**
- ✅ **Family Purchasing Power Delta (FPPΔ)** — diferença absoluta entre países
- ✅ **Relative Family Power Gap (RFPG)** — diferença percentual
- ✅ **Per Capita Family Delta** — impacto por pessoa

### 📐 **Normalização**
- ✅ **Z-score** — normalização por país
- ✅ **Min-Max (0-1)** — para dashboards

---

## 📊 PRINCIPAIS RESULTADOS

### 🥈 SILVER — Feature Engineering

**Situação Econômica Brasileira:**
- **RDR médio**: R$ 1.557,31
- **58,98%** da população com **déficit** (custo > renda)
- **EPR mediano**: 1,28 (custos = 128% da renda)

**Composição de Custos:**
| Item | % do Total |
|------|------------|
| Moradia | 41,27% |
| Alimentação | 23,16% |
| Dependentes | 13,43% |
| Outros | 22,14% |

### Acesso Cultural
- **68,36%** com **baixo acesso** (IAC < 3)
- Apenas **20,22%** com alto acesso

### Educação e Oportunidades
- **Gap de 90,82 pontos** de IOE entre superior e sem ensino médio
- Educação é o **maior preditor** de oportunidades

### Migração Internacional
- **Faro (Portugal)**: melhor destino para todas famílias
- Ganho médio: **+$8.143 USD** (profissional solteiro)
- Aumento de poder de compra: **+612%**

### 🏆 GOLD — Decisão e Insights

**Qualidade de Vida Econômica:**
- **QLES médio**: 18.09/100 (crise generalizada)
- **87% da população** em Very Low ou Low
- **Componentes críticos**: RDR (35%) e EPR (25%)

**Segmentação Socioeconômica:**
- **71% em vulnerabilidade** (Crítica + Sobrevivência)
- **24% classe média** com mobilidade limitada
- **Apenas 3.6%** com mobilidade ascendente ou alta renda

**Vulnerabilidade e Risco:**
- **65% em Risco Alto** — população crítica
- **63% com pressão extrema** (EPR > 0.9)
- **59% com renda negativa** (não cobrem custos básicos)

**Impacto de Políticas:**
- **Aumento de aluguel +20%**: impacto -5% no QLES
- **Corte de benefícios -15%**: impacto -10% no QLES
- **Cenários pioram situação crítica** — necessidade de expansão

---

## 📚 DOCUMENTAÇÃO

### Principais Documentos
- 🏆 **[GOLD_QUICK_REFERENCE.md](GOLD_QUICK_REFERENCE.md)** — Referência rápida GOLD ⭐
- 📖 **[SILVER_SUMMARY.md](SILVER_SUMMARY.md)** — Resumo executivo SILVER
- 📁 **[gold/README.md](gold/README.md)** — Documentação detalhada GOLD ⭐
- 📁 **[enriched/README.md](enriched/README.md)** — Documentação detalhada SILVER
- 📁 **[raw/README.md](raw/README.md)** — Documentação RAW

### Scripts
- 🏆 **generate_gold_data.py** — Pipeline GOLD (470+ linhas) ⭐
- 🐍 **generate_enriched_data.py** — Pipeline SILVER (350+ linhas)
- 🔍 **validate_enriched_data.py** — Validação e sanity checks
- 📊 **exemplos_uso_gold.py** — 6 exemplos práticos GOLD ⭐
- 📊 **exemplos_uso_silver.py** — 6 exemplos práticos SILVER

---

## 🎯 PRÓXIMOS PASSOS

### 1️⃣ **Power BI Dashboard** ⭐
- [ ] Conectar datasets GOLD
- [ ] Dashboard executivo com KPIs
- [ ] Drill-down por cluster e cidade
- [ ] Análise comparativa de cenários

### 2️⃣ **EDA Avançada**
- [ ] Distribuições por região/cidade
- [ ] Análise de outliers
- [ ] Visualizações (matplotlib/seaborn)
- [ ] Análise temporal (simulada)

### 3️⃣ **Melhorias GOLD** ⭐
- [x] Score consolidado (QLES) ✅
- [x] Clusterização interpretável ✅
- [x] Rankings contextuais ✅
- [x] Análise de vulnerabilidade ✅
- [x] Simulação de cenários ✅
- [ ] Modelo preditivo de vulnerabilidade
- [ ] Análise temporal (dados históricos)
- [ ] Benchmark internacional expandido
- [ ] Otimização de políticas (what-if analysis)

### 4️⃣ **Machine Learning**

### 3️⃣ **Features Avançadas (Bônus)**
- [ ] **Shock Impact Analysis**: Sensibilidade a choques econômicos
- [ ] **Financial Robustness**: Simulação de volatilidade
- [ ] **Endogenous Poverty Line**: Linha de pobreza dinâmica

### 4️⃣ **Dashboards**
- [ ] Power BI / Tableau
- [ ] Streamlit interativo
- [ ] Mapa de calor geográfico
- [ ] Simulador de migração

---

## 🔥 DESTAQUES TÉCNICOS

### ✨ Implementações de Qualidade

1. **Mapeamento de Cidades**
   - 30+ cidades brasileiras mapeadas
   - 5 contextos econômicos distintos
   - Fallback inteligente para cidades não mapeadas

2. **Ajuste por Dependentes**
   - Fator de 0.40 (baseado em OECD)
   - Escala de consumo infantil diferenciada
   - Custo per capita normalizado

3. **Normalização Dupla**
   - Z-score para comparação intra-país
   - Min-Max para dashboards
   - Valores absolutos preservados

4. **Comparação Cross-Country**
   - 4 perfis familiares realistas
   - 18 cidades em 5 países
   - 1.224 comparações pareadas

5. **Validação Rigorosa**
   - Sanity checks automáticos
   - Análise de correlações
   - Identificação de outliers

---

## 💡 DECISÕES DE DESIGN

### Dependency Factor = 0.40
- **Base**: OECD equivalence scales (0.30-0.50)
- **Justificativa**: Valor médio para contexto brasileiro

### Moradia Própria = 50% do Aluguel
- **Estimativa**: IPTU + manutenção + condomínio
- **Fonte**: Mercado imobiliário brasileiro

### Escala de Consumo Infantil
| Item | % do Adulto |
|------|-------------|
| Alimentação | 60% |
| Utilities | +30% |
| Saúde | +40% |

**Fonte**: IBGE e DIEESE

---

## 🛠️ TECNOLOGIAS

- **Python 3.14+**
- **pandas** — manipulação de dados
- **numpy** — cálculos numéricos
- **scikit-learn** — clusterização e machine learning ⭐
- **pathlib** — manipulação de paths
- **CSV** — formato de armazenamento

---

## 📚 DOCUMENTAÇÃO COMPLETA

### 📊 Por Camada

| Documento | Descrição | Linhas |
|-----------|-----------|--------|
| [raw/README.md](raw/README.md) | Documentação camada RAW | 150+ |
| [enriched/README.md](enriched/README.md) | Documentação camada SILVER | 400+ |
| [gold/README.md](gold/README.md) | Documentação camada GOLD ⭐ | 500+ |

### 📋 Sumários Executivos

| Documento | Foco | Público |
|-----------|------|---------|
| [SILVER_SUMMARY.md](SILVER_SUMMARY.md) | Features & métricas | Analistas de dados |
| [GOLD_SUMMARY.md](GOLD_SUMMARY.md) | Decisões & insights ⭐ | Executivos, gestores |

### 🚀 Guias Práticos

| Documento | Objetivo | Uso |
|-----------|----------|-----|
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Referência rápida SILVER | Consulta diária |
| [GOLD_QUICK_REFERENCE.md](GOLD_QUICK_REFERENCE.md) | Referência rápida GOLD ⭐ | Consulta diária |
| [POWER_BI_INTEGRATION.md](POWER_BI_INTEGRATION.md) | Integração Power BI ⭐ | BI Developers |

### 🐍 Código

| Script | Função | Linhas |
|--------|--------|--------|
| [generate_raw_data.py](src/generate_raw_data.py) | Gera camada RAW | 200+ |
| [generate_enriched_data.py](src/generate_enriched_data.py) | Gera camada SILVER | 350+ |
| [generate_gold_data.py](src/generate_gold_data.py) | Gera camada GOLD ⭐ | 470+ |
| [validate_enriched_data.py](src/validate_enriched_data.py) | Validação SILVER | 100+ |
| [exemplos_uso_silver.py](src/exemplos_uso_silver.py) | Exemplos SILVER | 300+ |
| [exemplos_uso_gold.py](src/exemplos_uso_gold.py) | Exemplos GOLD ⭐ | 400+ |

**Total**: ~2.770+ linhas de código Python documentado

---

## 📈 ESTATÍSTICAS DO PROJETO

- **Linhas de código**: ~2.770+
- **Datasets gerados**: 17 (5 RAW + 6 SILVER + 6 GOLD)
- **Registros processados**: 40.000+ (inclui cenários)
- **Métricas calculadas**: 20+ principais
- **Países cobertos**: 5 (Brasil, EUA, Alemanha, França, Portugal)
- **Cidades**: 18

---

## 📝 CITAÇÃO

Se você usar este projeto, considere citar:

```bibtex
@software{pipeline_socioeconomico,
  title = {Pipeline Socioeconômico RAW-SILVER-GOLD},
  author = {Juan Melo},
  year = {2026},
  description = {Análise de dados socioeconômicos com feature engineering}
}
```

---

## 📄 LICENÇA

Este projeto é fornecido como está, para fins educacionais e de pesquisa.

---

## 🤝 CONTRIBUINDO

Sugestões de melhorias são bem-vindas:

1. Features avançadas (shock analysis, robustness)
2. Visualizações
3. Camada GOLD
4. Otimizações de performance
5. Documentação adicional

---

## 📧 CONTATO

Para dúvidas sobre a implementação:
- Consulte os READMEs em cada pasta
- Revise os scripts de exemplo
- Analise o SILVER_SUMMARY.md

---

## ✅ STATUS DO PROJETO

- ✅ **RAW Layer** — Completo
- ✅ **SILVER Layer** — Completo e validado
- ✅ **GOLD Layer** — Completo
- 🔄 **Power BI** — Guia pronto (ver POWER_BI_INTEGRATION.md)

---

**Última atualização**: 2026-01-19  
**Versão**: 1.2.0 (GOLD completo)
