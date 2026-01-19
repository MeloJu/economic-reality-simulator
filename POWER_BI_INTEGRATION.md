# 📊 Power BI — Guia de Integração

## 🎯 Objetivo

Este guia mostra como conectar os datasets da camada GOLD ao Power BI e criar um dashboard executivo socioeconômico.

---

## 📦 Datasets para Importar

### Caminho dos Arquivos
```
project-root/gold/
├── quality_of_life_score.csv       ← FATO PRINCIPAL
├── socioeconomic_clusters.csv      ← DIMENSÃO
├── vulnerability_and_risk.csv      ← DIMENSÃO
├── policy_scenarios.csv            ← FATO CENÁRIOS
└── country_rankings_by_profile.csv ← FATO RANKINGS
```

---

## 🔗 Modelo de Dados

### Relacionamentos

```
quality_of_life_score (FATO)
    │
    ├─── [person_id] ──► socioeconomic_clusters [person_id]
    │                     Tipo: 1:1
    │                     Direção: Ambas
    │
    ├─── [person_id] ──► vulnerability_and_risk [person_id]
    │                     Tipo: 1:1
    │                     Direção: Ambas
    │
    └─── [person_id] ──► policy_scenarios [person_id]
                          Tipo: 1:N
                          Direção: Ambas

country_rankings_by_profile (FATO INDEPENDENTE)
    Sem relacionamentos
```

### Configuração Manual

1. **Carregar Dados**
   - Home > Get Data > Text/CSV
   - Selecionar cada arquivo CSV da pasta `gold/`
   - Transform Data: verificar tipos de dados

2. **Criar Relacionamentos**
   - Model view > Arrastar `person_id` entre tabelas
   - quality_of_life_score ←→ socioeconomic_clusters (1:1)
   - quality_of_life_score ←→ vulnerability_and_risk (1:1)
   - quality_of_life_score ←→ policy_scenarios (1:N)

3. **Configurar Tipos de Dados**
   - `QLES`: Decimal Number
   - `delta_percent`: Decimal Number
   - `high_vulnerability`: True/False
   - `cluster_id`: Whole Number

---

## 📈 Medidas DAX Essenciais

### KPIs Principais

```dax
// ============================================================================
// MEDIDAS — QLES
// ============================================================================

QLES Médio = 
AVERAGE(quality_of_life_score[QLES])

QLES Mediano = 
MEDIAN(quality_of_life_score[QLES])

QLES Min = 
MIN(quality_of_life_score[QLES])

QLES Max = 
MAX(quality_of_life_score[QLES])

// ============================================================================
// MEDIDAS — VULNERABILIDADE
// ============================================================================

Total Pessoas = 
COUNTROWS(vulnerability_and_risk)

Pessoas em Risco Alto = 
CALCULATE(
    COUNTROWS(vulnerability_and_risk),
    vulnerability_and_risk[risk_group] = "Risco Alto"
)

% Risco Alto = 
DIVIDE(
    [Pessoas em Risco Alto],
    [Total Pessoas],
    0
)

Pessoas Vulneráveis = 
CALCULATE(
    COUNTROWS(vulnerability_and_risk),
    vulnerability_and_risk[high_vulnerability] = TRUE
)

% Vulnerabilidade = 
DIVIDE(
    [Pessoas Vulneráveis],
    [Total Pessoas],
    0
)

Pessoas Pressão Extrema = 
CALCULATE(
    COUNTROWS(vulnerability_and_risk),
    vulnerability_and_risk[extreme_pressure] = TRUE
)

% Pressão Extrema = 
DIVIDE(
    [Pessoas Pressão Extrema],
    [Total Pessoas],
    0
)

// ============================================================================
// MEDIDAS — CLUSTERS
// ============================================================================

Total Clusters = 
DISTINCTCOUNT(socioeconomic_clusters[cluster_id])

Cluster Dominante = 
CALCULATE(
    SELECTEDVALUE(socioeconomic_clusters[cluster_label]),
    TOPN(1, 
        VALUES(socioeconomic_clusters[cluster_label]),
        CALCULATE(COUNTROWS(socioeconomic_clusters)),
        DESC
    )
)

Distribuição Cluster = 
VAR TotalPessoas = [Total Pessoas]
VAR ClusterCount = COUNTROWS(socioeconomic_clusters)
RETURN
DIVIDE(ClusterCount, TotalPessoas, 0)

// ============================================================================
// MEDIDAS — CENÁRIOS
// ============================================================================

Impacto Médio Cenários = 
AVERAGE(policy_scenarios[delta_percent])

Impacto por Cenário = 
CALCULATE(
    AVERAGE(policy_scenarios[delta_percent]),
    ALLEXCEPT(policy_scenarios, policy_scenarios[scenario_name])
)

Pessoas Impacto Negativo = 
CALCULATE(
    COUNTROWS(policy_scenarios),
    policy_scenarios[delta_percent] < 0
)

% Impacto Negativo = 
DIVIDE(
    [Pessoas Impacto Negativo],
    COUNTROWS(policy_scenarios),
    0
)

// ============================================================================
// MEDIDAS — RANKINGS
// ============================================================================

Melhor Cidade = 
CALCULATE(
    SELECTEDVALUE(country_rankings_by_profile[city]),
    TOPN(1,
        VALUES(country_rankings_by_profile[city]),
        country_rankings_by_profile[rank_position],
        ASC
    )
)

QLES Médio Ranking = 
AVERAGE(country_rankings_by_profile[QLES_avg])

// ============================================================================
// MEDIDAS — COMPARATIVAS
// ============================================================================

QLES vs Média Nacional = 
VAR MediaNacional = 
    CALCULATE(
        [QLES Médio],
        ALL(quality_of_life_score[city])
    )
RETURN
[QLES Médio] - MediaNacional

% Acima da Média = 
VAR MediaNacional = 
    CALCULATE(
        [QLES Médio],
        ALL(quality_of_life_score[city])
    )
RETURN
DIVIDE(
    CALCULATE(
        COUNTROWS(quality_of_life_score),
        quality_of_life_score[QLES] > MediaNacional
    ),
    [Total Pessoas],
    0
)
```

---

## 📊 Visualizações Recomendadas

### Dashboard 1: **Visão Executiva**

**Objetivo**: KPIs de alto nível para tomada de decisão

| Visual | Tipo | Dados |
|--------|------|-------|
| QLES Médio Nacional | Card | [QLES Médio] |
| % em Risco Alto | Gauge (0-100%) | [% Risco Alto] |
| % Vulnerabilidade | Gauge | [% Vulnerabilidade] |
| Total Pessoas | Card | [Total Pessoas] |
| QLES por Categoria | Donut Chart | QLES_bucket (Values: Count) |
| QLES por Cidade | Bar Chart | city (Axis) + QLES Médio (Values) |
| Evolução QLES | Line Chart (simulada) | *Requer dados temporais* |
| Mapa de Vulnerabilidade | Map | city (Location) + % Risco Alto (Size) |

**Slicers:**
- city (Dropdown)
- QLES_bucket (List)
- risk_group (Buttons)

---

### Dashboard 2: **Análise de Clusters**

**Objetivo**: Segmentação socioeconômica detalhada

| Visual | Tipo | Dados |
|--------|------|-------|
| População por Cluster | Stacked Bar Chart | cluster_label (Axis) + Count (Values) |
| QLES por Cluster | Column Chart | cluster_label (Axis) + QLES Médio (Values) |
| Vulnerabilidade por Cluster | 100% Stacked Bar | cluster_label (Axis) + risk_group (Legend) |
| Scatter: RDR vs EPR | Scatter Chart | avg_rdr (X) + avg_epr (Y) + cluster_label (Legend) |
| Tabela de Estatísticas | Table | cluster_label, avg_rdr, avg_epr, avg_iac, avg_ioe |
| Distribuição Geográfica | Treemap | city (Group) + cluster_label (Category) |

**Slicers:**
- cluster_label (List com ícones)
- city (Dropdown)

---

### Dashboard 3: **Vulnerabilidade e Risco**

**Objetivo**: Identificar populações críticas

| Visual | Tipo | Dados |
|--------|------|-------|
| % Risco por Grupo | Funnel Chart | risk_group (Group) + Count (Values) |
| Flags de Vulnerabilidade | Multi-row Card | high_vulnerability, extreme_pressure, negative_income (TRUE count) |
| Risco por Cluster | Matrix | cluster_label (Rows) + risk_group (Columns) + Count (Values) |
| QLES: Risco Alto vs Baixo | Clustered Column | risk_group (Axis) + QLES Médio (Values) |
| Heatmap: Cidade x Risco | Matrix | city (Rows) + risk_group (Columns) + % (Values) + Color Scale |
| Progressão de Vulnerabilidade | Waterfall Chart | Flags (Category) + Count (Values) |

**Slicers:**
- risk_group (Buttons com ícones ⚠️)
- cluster_label (Dropdown)

---

### Dashboard 4: **Simulação de Cenários**

**Objetivo**: Análise de impacto de políticas

| Visual | Tipo | Dados |
|--------|------|-------|
| Impacto Médio por Cenário | Clustered Bar Chart | scenario_name (Axis) + delta_percent (Values) |
| Distribuição de Impacto | Histogram | delta_percent (Axis) + Count (Values) |
| Antes vs Depois | Line & Stacked Column | person_id (Axis) + QLES_before, QLES_after (Values) |
| Impacto por Cluster | Matrix | cluster_label (Rows) + scenario_name (Columns) + delta_percent (Values) |
| Box Plot de Impacto | Box & Whisker (via Python visual) | scenario_name (Category) + delta_percent (Values) |
| Impacto Severo (< -5%) | Card | [Pessoas Impacto Negativo] |

**Slicers:**
- scenario_name (Buttons)
- cluster_label (Dropdown)
- delta_percent (Range slider: -100% a +100%)

---

### Dashboard 5: **Rankings e Comparações**

**Objetivo**: Análise comparativa por perfil familiar

| Visual | Tipo | Dados |
|--------|------|-------|
| Top 10 Cidades por Perfil | Table | rank_position, city, country, QLES_avg, avg_per_capita_rdr |
| QLES por Localização | Map | city (Location) + QLES_avg (Size) + profile_id (Legend) |
| Comparação de Perfis | Clustered Bar Chart | profile_id (Legend) + city (Axis) + QLES_avg (Values) |
| Ganho de RDR | Waterfall Chart | city (Category) + avg_per_capita_rdr (Values) |
| Radar Chart: Perfis | Radar Chart (custom) | profile_id (Axis) + QLES_avg (Values) |

**Slicers:**
- profile_id (Buttons com descrição)
- country (Dropdown)

---

## 🎨 Design System

### Paleta de Cores

```
🟢 Baixo Risco / High QLES:   #27AE60 (Verde)
🟡 Médio Risco / Medium QLES:  #F39C12 (Laranja)
🔴 Alto Risco / Low QLES:      #E74C3C (Vermelho)
⚫ Risco Crítico:               #2C3E50 (Cinza escuro)
🔵 Neutro / Info:              #3498DB (Azul)
🟣 Clusters:                   Gradiente Roxo → Rosa
```

### Formatação de Valores

```dax
// Formato de Porcentagem
FORMAT([% Risco Alto], "0.0%")

// Formato de QLES
FORMAT([QLES Médio], "0.00")

// Formato de Delta
FORMAT([Impacto Médio Cenários], "+0.0%;-0.0%;0.0%")

// Formato de Moeda
FORMAT([avg_per_capita_rdr], "$#,##0.00")
```

---

## 🔄 Refresh e Atualização

### Refresh Manual

1. Home > Refresh
2. Dados atualizados do CSV

### Refresh Automático (Power BI Service)

1. Publicar relatório no Power BI Service
2. Settings > Datasets > Scheduled refresh
3. Configurar gateway se arquivos locais

### Refresh via Python (Automatizado)

```python
# Script para regenerar GOLD e atualizar Power BI
import subprocess

# Gerar nova camada GOLD
subprocess.run(["python", "src/generate_gold_data.py"])

# Atualizar Power BI (se configurado)
# Usar Power BI REST API ou Power BI Cmdlets
```

---

## 📝 Checklist de Implementação

### Fase 1: Setup Básico
- [ ] Importar 5 CSVs da pasta `gold/`
- [ ] Verificar tipos de dados
- [ ] Criar relacionamentos
- [ ] Configurar formato de data/números

### Fase 2: Medidas DAX
- [ ] Copiar medidas essenciais (KPIs)
- [ ] Testar cálculos básicos
- [ ] Criar medidas customizadas

### Fase 3: Dashboards
- [ ] Dashboard 1: Visão Executiva
- [ ] Dashboard 2: Clusters
- [ ] Dashboard 3: Vulnerabilidade
- [ ] Dashboard 4: Cenários
- [ ] Dashboard 5: Rankings

### Fase 4: Design e UX
- [ ] Aplicar paleta de cores
- [ ] Configurar tooltips customizados
- [ ] Adicionar botões de navegação
- [ ] Testar responsividade (mobile)

### Fase 5: Deploy
- [ ] Publicar no Power BI Service
- [ ] Configurar permissões
- [ ] Agendar refresh (se aplicável)
- [ ] Documentar para usuários finais

---

## 💡 Dicas Avançadas

### Performance

1. **Reduzir Cardinalidade**
   - Evitar colunas de alta cardinalidade (person_id) em visuais
   - Usar agregações (AVG, SUM) em vez de detalhes

2. **Query Folding**
   - Aplicar filtros no Power Query antes de carregar
   - Reduzir colunas desnecessárias

3. **Agregações**
   - Criar tabela agregada de QLES por cluster/cidade
   - Usar para visuais de alto nível

### Storytelling

1. **Narrativa Progressiva**
   - Dashboard 1: "O que está acontecendo?"
   - Dashboard 2: "Quem está afetado?"
   - Dashboard 3: "Onde está o risco?"
   - Dashboard 4: "E se...?"
   - Dashboard 5: "Onde ir?"

2. **Call to Action**
   - Adicionar insights textuais
   - Destacar KPIs críticos
   - Sugerir próximos passos

---

## 🚀 Exemplo de Dashboard Executivo

```
╔═══════════════════════════════════════════════════════════╗
║  📊 DASHBOARD SOCIOECONÔMICO — VISÃO EXECUTIVA            ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      ║
║  │ QLES Médio  │  │ Risco Alto  │  │ Vulneráveis │      ║
║  │   18.09     │  │    65.1%    │  │    65.1%    │      ║
║  └─────────────┘  └─────────────┘  └─────────────┘      ║
║                                                           ║
║  ┌─────────────────────────────────────────────────┐     ║
║  │ QLES por Categoria (Donut)                      │     ║
║  │   ● Very Low (77.7%)                            │     ║
║  │   ● Low (21.4%)                                 │     ║
║  │   ○ Medium+ (0.9%)                              │     ║
║  └─────────────────────────────────────────────────┘     ║
║                                                           ║
║  ┌─────────────────────────────────────────────────┐     ║
║  │ Top 5 Cidades por QLES (Bar Chart)              │     ║
║  │   Goiânia         ████████████ 19.55            │     ║
║  │   Londrina        ███████████ 19.01             │     ║
║  │   Porto Alegre    ███████████ 18.97             │     ║
║  └─────────────────────────────────────────────────┘     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 📚 Recursos Adicionais

- **Power BI Docs**: https://docs.microsoft.com/power-bi/
- **DAX Guide**: https://dax.guide/
- **Community**: https://community.powerbi.com/
- **Templates**: https://appsource.microsoft.com/marketplace/apps?product=power-bi

---

**Status**: ✅ Pronto para integração  
**Última atualização**: 2026-01-08  
**Arquivos**: 5 CSVs (10K+ registros)  
**Compatibilidade**: Power BI Desktop + Service
