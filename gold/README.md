# 🏆 GOLD LAYER — Documentação Técnica

## 📋 VISÃO GERAL

A camada GOLD é a **camada de decisão** do pipeline de dados. Ela transforma as métricas calculadas na camada SILVER em **insights acionáveis, scores consolidados e rankings interpretativos** prontos para consumo executivo e visualização em Power BI.

**Princípios de Design:**
- ✅ Datasets denormalizados para facilitar consumo no Power BI
- ✅ Scores consolidados e interpretáveis
- ✅ Segmentações (clusters) com narrativa clara
- ✅ Sem cálculos complexos — apenas síntese e interpretação
- ✅ Nomes de colunas legíveis para negócio

---

## 📦 DATASETS GERADOS

### 1️⃣ `quality_of_life_score.csv` (10.000 registros)

**Score principal do pipeline: QLES (Quality of Life Economic Score)**

#### Fórmula:
```
QLES = 0.35 * RDR_zscore +
       0.25 * (1 - EPR) +
       0.15 * IAC_zscore +
       0.15 * IOE_zscore +
       0.10 * (1 - social_support_ratio)

Normalizado para escala 0-100
```

#### Estrutura:
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `person_id` | String | Identificador único |
| `country` | String | País (Brazil) |
| `city` | String | Cidade |
| `QLES` | Float | Score consolidado (0-100) |
| `QLES_bucket` | String | Categoria: Very Low, Low, Medium, High, Very High |
| `component_rdr` | Float | Contribuição da renda disponível (35%) |
| `component_epr` | Float | Contribuição da pressão econômica (25%) |
| `component_iac` | Float | Contribuição do acesso cultural (15%) |
| `component_ioe` | Float | Contribuição das oportunidades (15%) |
| `component_social` | Float | Contribuição do suporte social (10%) |

#### Insights:
- **Média QLES**: 18.09 (baixa qualidade de vida econômica geral)
- **Distribuição**: 67% Very Low, 19% Low, 0.7% Medium+
- **Explicabilidade**: Componentes intermediários mostram quais fatores impactam o score

---

### 2️⃣ `socioeconomic_clusters.csv` (10.000 registros)

**Segmentação socioeconômica interpretável (K-Means, k=6)**

#### Técnica:
- **Algoritmo**: K-Means com k=6 (melhor silhouette: 0.371)
- **Features**: RDR_zscore, EPR, IAC_zscore, IOE_zscore, cost_per_capita
- **Validação**: Elbow + Silhouette Score em amostra de 2.000 casos

#### Estrutura:
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `person_id` | String | Identificador único |
| `cluster_id` | Int | ID do cluster (0-5) |
| `cluster_label` | String | Nome interpretativo |
| `cluster_description` | String | Descrição narrativa |
| `avg_rdr` | Float | Renda disponível média do cluster |
| `avg_epr` | Float | Pressão econômica média do cluster |
| `avg_iac` | Float | Acesso cultural médio do cluster |
| `avg_ioe` | Float | Oportunidades médias do cluster |
| `avg_cost_per_capita` | Float | Custo per capita médio do cluster |

#### Clusters Identificados:

| Cluster | Label | Descrição | % População |
|---------|-------|-----------|-------------|
| 5 | **Vulnerabilidade Crítica** | Pressão muito alta, renda disponível baixa, suporte necessário | 47% |
| 0 | **Classe Média Inferior** | Pressão alta, renda disponível média-baixa, mobilidade limitada | 24% |
| 2 | **Classe Média Estável** | Pressão moderada, renda disponível média, estabilidade relativa | 15% |
| 4 | **Sobrevivência Urbana** | Alta pressão econômica, renda disponível muito baixa, acesso mínimo | 11% |
| 1 | **Mobilidade Ascendente** | Pressão baixa-moderada, renda disponível alta, oportunidades amplas | 3% |
| 3 | **Alta Renda Consolidada** | Baixa pressão, renda disponível muito alta, acesso pleno | 0.6% |

#### Insights:
- **71% da população** está em clusters de vulnerabilidade (Crítica + Sobrevivência)
- **24%** está na classe média com mobilidade limitada
- **Apenas 3.6%** possui mobilidade ascendente ou alta renda consolidada

---

### 3️⃣ `country_rankings_by_profile.csv` (72 registros)

**Rankings contextuais por perfil familiar**

#### Metodologia:
- Rankings baseados em QLES proxy (per capita RDR normalizado)
- Perfis familiares da simulação cross-country
- Rankings relativos dentro de cada perfil

#### Estrutura:
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `profile_id` | String | Código do perfil (F1, F2, F3, F4) |
| `description` | String | Descrição do perfil familiar |
| `country` | String | País |
| `city` | String | Cidade |
| `QLES_avg` | Float | Score médio para o perfil |
| `avg_per_capita_rdr` | Float | Renda disponível per capita |
| `rank_position` | Int | Posição no ranking (1 = melhor) |

#### Perfis:
- **F1**: Casal sem filhos, classe média
- **F2**: Família com 2 filhos
- **F3**: Profissional sênior, família grande
- **F4**: Jovem profissional, solteiro

#### Uso no Power BI:
- Filtrar por `profile_id` para ver ranking específico
- Comparar cidades com mesmo perfil familiar
- Identificar melhores localizações para cada contexto

---

### 4️⃣ `vulnerability_and_risk.csv` (10.000 registros)

**Flags de vulnerabilidade e classificação de risco**

#### Estrutura:
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `person_id` | String | Identificador único |
| `high_vulnerability` | Bool | EPR > 0.8 E RDR < 500 |
| `high_dependency` | Bool | social_support_ratio > 0.3 |
| `extreme_pressure` | Bool | EPR > 0.9 |
| `negative_income` | Bool | RDR < 0 |
| `risk_group` | String | Risco Crítico, Alto, Moderado, Baixo |

#### Lógica de Classificação:
```
Risco Crítico  → high_vulnerability E high_dependency
Risco Alto     → high_vulnerability OU extreme_pressure
Risco Moderado → negative_income
Risco Baixo    → nenhuma flag ativa
```

#### Insights:
- **65% da população** está em Risco Alto (6.515 pessoas)
- **65%** possui alta vulnerabilidade
- **63%** enfrenta pressão extrema (EPR > 0.9)
- **0%** possui alta dependência de benefícios (social_support_ratio > 0.3)

---

### 5️⃣ `policy_scenarios.csv` (20.000 registros)

**Simulações determinísticas de cenários de política**

#### Cenários Simulados:

##### Cenário 1: **Aumento de aluguel +20%**
- Aumenta custo habitacional em 20%
- Recalcula RDR e QLES
- **Impacto médio**: -4.93% no QLES

##### Cenário 2: **Corte de benefícios sociais -15%**
- Reduz benefícios sociais em 15%
- Impacta apenas quem recebe benefícios
- **Impacto médio**: -10.00% no QLES

#### Estrutura:
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `person_id` | String | Identificador único |
| `scenario_name` | String | Nome do cenário |
| `QLES_before` | Float | Score antes da política |
| `QLES_after` | Float | Score após a política |
| `delta_percent` | Float | Variação percentual |

#### Uso no Power BI:
- Comparar impacto dos cenários por cluster
- Identificar populações mais vulneráveis a cada política
- Visualizar distribuição de impacto (histogramas)

---

## 📊 GUIA DE CONSUMO NO POWER BI

### Modelo de Dados Recomendado

```
quality_of_life_score (FATO PRINCIPAL)
    ├─ person_id [1:1] socioeconomic_clusters
    ├─ person_id [1:1] vulnerability_and_risk
    └─ person_id [1:N] policy_scenarios

country_rankings_by_profile (FATO INDEPENDENTE)
```

### Medidas Recomendadas (DAX)

```dax
QLES Médio = AVERAGE(quality_of_life_score[QLES])

% Vulnerabilidade = 
DIVIDE(
    COUNTROWS(FILTER(vulnerability_and_risk, [high_vulnerability] = TRUE)),
    COUNTROWS(vulnerability_and_risk)
)

Impacto Cenário = 
AVERAGE(policy_scenarios[delta_percent])
```

### Visualizações Sugeridas

1. **Dashboard Executivo**
   - KPI: QLES médio
   - Gráfico de pizza: Distribuição por QLES_bucket
   - Mapa de calor: QLES por cidade

2. **Análise de Clusters**
   - Gráfico de barras: População por cluster
   - Scatter plot: RDR vs EPR colorido por cluster
   - Tabela: Estatísticas descritivas por cluster

3. **Vulnerabilidade**
   - Gauge: % em Risco Alto/Crítico
   - Treemap: risk_group por cluster
   - Funnel: Progressão de flags de risco

4. **Cenários**
   - Gráfico de barras: Impacto médio por cenário
   - Box plot: Distribuição de delta_percent
   - Slicer: Filtro por cluster para análise direcionada

---

## 🔍 INSIGHTS-CHAVE

### Qualidade de Vida Econômica
- **Score médio muito baixo** (18.09/100) indica crise socioeconômica generalizada
- **87% da população** está em Very Low ou Low
- **Componentes críticos**: RDR e EPR explicam 60% do score

### Segmentação Socioeconômica
- **Concentração em vulnerabilidade**: 71% em clusters de risco
- **Classe média**: apenas 24%, com mobilidade limitada
- **Elite econômica**: menos de 4% da população

### Vulnerabilidade e Risco
- **65% em risco alto** — população crítica para políticas públicas
- **63% com pressão extrema** (EPR > 0.9) — gastam mais do que ganham
- **Baixa dependência de benefícios** sugere subdimensionamento de programas sociais

### Impacto de Políticas
- **Aumento de aluguel** tem impacto moderado (-5%), mas afeta todos
- **Corte de benefícios** tem impacto severo (-10%) em população já vulnerável
- **Cenários pioram situação** já crítica — necessidade de políticas expansionistas

---

## 🚀 PRÓXIMOS PASSOS

### Melhorias Técnicas
1. **Adicionar dimensão temporal** (se houver dados históricos)
2. **Incluir mais cenários**: aumento de salário mínimo, programas habitacionais
3. **Geolocalização**: coordenadas para mapas interativos
4. **Benchmark internacional**: comparar Brasil com outros países

### Análises Avançadas
1. **Análise de sensibilidade**: quais componentes do QLES têm maior impacto
2. **Transição entre clusters**: modelar mobilidade socioeconômica
3. **Predição de vulnerabilidade**: modelo preditivo usando features SILVER
4. **Otimização de políticas**: quais intervenções maximizam QLES

### Integração Power BI
1. **Dashboard executivo** com KPIs principais
2. **Relatório de clusters** com drill-down por cidade
3. **Análise comparativa de cenários** com slicers dinâmicos
4. **Mapa de vulnerabilidade** com heatmap geográfico

---

## 📚 REFERÊNCIAS

- **Camada SILVER**: [../enriched/README.md](../enriched/README.md)
- **Script de geração**: [../src/generate_gold_data.py](../src/generate_gold_data.py)
- **Metodologia de clustering**: K-Means com validação por Silhouette Score
- **Design Power BI**: Kimball dimensional modeling (fact + dimensions)

---

## ⚙️ EXECUÇÃO

```bash
# Gerar camada GOLD
cd src
python generate_gold_data.py

# Output:
# - gold/quality_of_life_score.csv
# - gold/socioeconomic_clusters.csv
# - gold/country_rankings_by_profile.csv
# - gold/vulnerability_and_risk.csv
# - gold/policy_scenarios.csv
# - gold/cluster_statistics.csv (auxiliar)
```

---

**Status**: ✅ Produção  
**Última atualização**: 2026-01-08  
**Responsável**: Pipeline automatizado  
**Versão**: 1.0
