# 🏗️ Pipeline Socioeconômico — RAW → SILVER → GOLD

**Análise de Dados Socioeconômicos com Feature Engineering**

[![Status](https://img.shields.io/badge/Status-Camada%20SILVER%20Completa-success)]()
[![Python](https://img.shields.io/badge/Python-3.14+-blue)]()
[![Data](https://img.shields.io/badge/Registros-10%2C000-orange)]()

---

## 📋 VISÃO GERAL

Este projeto implementa um **pipeline completo de engenharia de dados** para análise socioeconômica, seguindo a arquitetura **Medallion** (Bronze → Silver → Gold).

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
├── src/                              # 🐍 Scripts Python
│   ├── generate_raw_data.py          # Gera camada RAW
│   ├── generate_enriched_data.py     # Gera camada SILVER ⭐
│   ├── validate_enriched_data.py     # Valida SILVER
│   └── exemplos_uso_silver.py        # Exemplos de análise
│
├── SILVER_SUMMARY.md                 # 📊 Resumo executivo
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
pip install pandas numpy
```

### 2️⃣ Gerar Dados

```bash
# Camada RAW (se ainda não existir)
python src/generate_raw_data.py

# Camada SILVER ⭐
python src/generate_enriched_data.py
```

### 3️⃣ Validar

```bash
python src/validate_enriched_data.py
```

### 4️⃣ Explorar

```bash
python src/exemplos_uso_silver.py
```

---

## 🔢 MÉTRICAS IMPLEMENTADAS (SILVER)

### 💰 **Econômicas**
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

### Situação Econômica Brasileira
- **RDR médio**: R$ 1.557,31
- **58,98%** da população com **déficit** (custo > renda)
- **EPR mediano**: 1,28 (custos = 128% da renda)

### Composição de Custos
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

---

## 📚 DOCUMENTAÇÃO

### Principais Documentos
- 📖 **[SILVER_SUMMARY.md](SILVER_SUMMARY.md)** — Resumo executivo completo
- 📁 **[enriched/README.md](enriched/README.md)** — Documentação detalhada da camada SILVER
- 📁 **[raw/README.md](raw/README.md)** — Documentação da camada RAW

### Scripts
- 🐍 **generate_enriched_data.py** — Pipeline principal (350+ linhas)
- 🔍 **validate_enriched_data.py** — Validação e sanity checks
- 📊 **exemplos_uso_silver.py** — 6 exemplos práticos de análise

---

## 🎯 PRÓXIMOS PASSOS

### 1️⃣ **EDA Avançada**
- [ ] Distribuições por região/cidade
- [ ] Análise de outliers
- [ ] Visualizações (matplotlib/seaborn)
- [ ] Análise temporal (simulada)

### 2️⃣ **Camada GOLD**
- [ ] Score composto de vulnerabilidade
- [ ] Sistema de elegibilidade para benefícios
- [ ] Ranking de oportunidades
- [ ] Recomendações de políticas públicas
- [ ] Segmentação de perfis

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
- **pathlib** — manipulação de paths
- **CSV** — formato de armazenamento

---

## 📈 ESTATÍSTICAS DO PROJETO

- **Linhas de código**: ~1.200
- **Datasets gerados**: 11 (5 RAW + 6 SILVER)
- **Registros processados**: 10.000+
- **Métricas calculadas**: 14 principais
- **Países cobertos**: 5 (Brasil, EUA, Alemanha, França, Portugal)
- **Cidades**: 18

---

## 📝 CITAÇÃO

Se você usar este projeto, considere citar:

```bibtex
@software{pipeline_socioeconomico,
  title = {Pipeline Socioeconômico RAW-SILVER-GOLD},
  author = {Seu Nome},
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
- ⏳ **GOLD Layer** — Planejado
- ⏳ **Dashboards** — Planejado

---

**Última atualização**: 2026-01-06  
**Versão**: 1.0 (SILVER completo)
