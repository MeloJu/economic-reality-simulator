# 🥈 SILVER LAYER — Feature Engineering

**Status**: ✅ Completo  
**Gerado em**: 2026-01-06  
**Registros**: 10.000 indivíduos + 1.224 comparações cross-country

---

## 📋 VISÃO GERAL

A camada SILVER (enriched) é a **camada de features derivadas** do pipeline de dados socioeconômico.

### Filosofia da Camada

✅ **O QUE CONTÉM**:
- Métricas socioeconômicas calculadas
- Features derivadas dos dados RAW
- Normalizações e transformações
- Comparabilidade internacional
- Preparação para análise

❌ **O QUE NÃO CONTÉM**:
- Scores finais ou compostos
- Rankings ou classificações
- Decisões ou recomendações
- Clustering ou segmentação
- Visualizações

---

## 📂 ARQUIVOS GERADOS

### 1. `people_enriched.csv` (10.000 linhas)
**Descrição**: Dataset principal com todas as métricas individuais

**Colunas principais**:
- **Identificação**: `person_id`, `age`, `gender`, `region_br`, `city_br`
- **Econômicas**: `net_salary_brl`, `gross_salary_brl`
- **Custos**: `total_household_cost`, `housing_cost`, `dependent_adjustment`
- **Métricas**:
  - `renda_disponivel_real` (RDR)
  - `economic_pressure_ratio` (EPR)
  - `cost_per_capita`
  - `dist_salario_minimo_ajustado` (DSMA)
  - `subsistence_gap`
  - `social_support_ratio`
- **Normalizações**: `*_zscore`, `*_minmax`

### 2. `household_costs_enriched.csv` (10.000 linhas)
**Descrição**: Composição detalhada de custos domésticos

**Colunas**:
- `housing_cost`: Custo de moradia
- `basic_food_cost`: Alimentação básica
- `transport_cost`: Transporte
- `utilities_cost`: Contas (água, luz, etc.)
- `healthcare_cost`: Saúde
- `dependent_adjustment`: Ajuste por dependentes
- `total_household_cost`: Custo total
- `cost_per_capita`: Custo por pessoa

### 3. `cultural_access_enriched.csv` (10.000 linhas)
**Descrição**: Acesso à cultura e entretenimento

**Colunas**:
- Custos individuais: `streaming_cost`, `internet_cost`, `cinema_ticket`, etc.
- `cultural_basic_cost`: Soma dos custos culturais
- `iac_raw`: Índice de Acesso Cultural (bruto)
- `iac_raw_zscore`: IAC normalizado (Z-score por país)
- `iac_raw_minmax`: IAC normalizado (0-1)

### 4. `opportunity_access_enriched.csv` (10.000 linhas)
**Descrição**: Acesso a oportunidades de crescimento

**Colunas**:
- Custos: `technical_course`, `college_private`, `language_course`, `emergency_savings_target`, `mobility_cost`
- Índices individuais: `ioe_technical`, `ioe_college`, `ioe_language`, `ioe_savings`, `ioe_mobility`
- `ioe_raw`: Índice de Oportunidades Econômicas (soma)
- Normalizações: `ioe_raw_zscore`, `ioe_raw_minmax`

### 5. `cross_country_family_simulation.csv` (72 linhas)
**Descrição**: Simulação de 4 perfis familiares em 18 cidades/países

**Perfis**:
- **F1**: Casal sem filhos, classe média (net_salary: $6.000)
- **F2**: Família com 2 filhos, classe média (net_salary: $8.000)
- **F3**: Família com 3 filhos, classe média-baixa (net_salary: $5.000)
- **F4**: Profissional solteiro, classe média-alta (net_salary: $10.000)

**Colunas**:
- `profile_id`, `description`, `country`, `city`
- `net_salary_usd`: Salário convertido para USD
- `total_household_cost_usd`: Custo total em USD
- `renda_disponivel_real_usd`: RDR em USD
- `per_capita_rdr`: RDR per capita

### 6. `cross_country_family_comparison.csv` (1.224 linhas)
**Descrição**: Comparações pareadas entre países/cidades

**Colunas**:
- `profile_id`: Perfil familiar
- `from_country`, `from_city`: Origem
- `to_country`, `to_city`: Destino
- `fpp_delta_usd`: **Family Purchasing Power Delta** (FPPΔ) — diferença absoluta em USD
- `rfpg_percent`: **Relative Family Power Gap** (RFPG) — diferença percentual
- `pc_fpp_delta_usd`: **Per Capita Family Delta** — delta por pessoa

---

## 🔢 MÉTRICAS IMPLEMENTADAS

### 1️⃣ Custos e Renda

#### **Total Household Cost**
```
total_household_cost = 
    housing_cost + 
    basic_food_cost + 
    transport_cost + 
    utilities_cost + 
    healthcare_cost + 
    dependent_adjustment
```

**Ajustes**:
- Moradia própria/cedida: 50% do aluguel (manutenção/IPTU)
- Dependentes: escala de consumo (60% comida, 30% utilities, 40% saúde)

#### **Renda Disponível Real (RDR)**
```
RDR = net_salary + total_social_benefits - total_household_cost
```

**Interpretação**:
- RDR > 0: Sobra dinheiro após custos essenciais
- RDR < 0: Déficit orçamentário
- RDR alto: Maior capacidade de poupança/investimento

---

### 2️⃣ Pressão Econômica

#### **Economic Pressure Ratio (EPR)**
```
EPR = total_household_cost / net_salary
```

**Interpretação**:
- EPR < 0.5: Baixa pressão (sobra >50% da renda)
- EPR 0.5-0.7: Pressão moderada
- EPR > 0.7: Alta pressão (>70% da renda em custos básicos)
- EPR > 1.0: Insustentável (custos > renda)

---

### 3️⃣ Estrutura Familiar

#### **Custo por Dependente (CPD)**
```
CPD = total_household_cost / (dependents + 1)
```

**Uso**: Comparar eficiência econômica entre famílias de tamanhos diferentes

---

### 4️⃣ Relação com Mínimos Econômicos

#### **Salário Mínimo Ajustado**
```
adjusted_min_wage = local_min_wage * (1 + dependents * 0.40)
```

**Fator**: 0.40 = literatura sugere 30-50% adicional por dependente

#### **Distância do Salário Mínimo Ajustado (DSMA)**
```
DSMA = (net_salary - adjusted_min_wage) / adjusted_min_wage
```

**Interpretação**:
- DSMA > 1.0: Ganha mais de 2x o mínimo ajustado
- DSMA = 0: Ganha exatamente o mínimo ajustado
- DSMA < 0: Ganha menos que o mínimo ajustado

#### **Gap de Subsistência**
```
Subsistence_Gap = net_salary - total_household_cost
```

**Uso**: Valor absoluto disponível após custos essenciais (= RDR sem benefícios)

---

### 5️⃣ Benefícios Sociais

#### **Social Support Ratio (SSR)**
```
SSR = total_social_benefits / net_salary
```

**Interpretação**: Proporção da renda que vem de benefícios governamentais

---

### 6️⃣ Acesso Cultural

#### **Cultural Basic Cost**
```
cultural_basic_cost = 
    streaming + 
    internet + 
    cinema + 
    cultural_events + 
    music_subscription
```

#### **Índice de Acesso Cultural (IAC)**
```
IAC_raw = RDR / cultural_basic_cost
```

**Interpretação**:
- IAC > 10: Alto acesso (pode pagar cultura 10x)
- IAC 3-10: Acesso moderado
- IAC < 3: Acesso limitado

---

### 7️⃣ Oportunidades Econômicas

#### **Índice de Oportunidades Econômicas (IOE)**
```
IOE_raw = Σ (RDR / opportunity_cost_i)

Onde i ∈ {technical_course, college_private, language_course, 
           emergency_savings, mobility_cost}
```

**Interpretação**:
- IOE alto: Maior capacidade de investir em educação/mobilidade
- IOE baixo: Dificuldade de acessar oportunidades

---

### 8️⃣ Comparação Internacional

#### **Family Purchasing Power Delta (FPPΔ)**
```
FPPΔ(A → B) = RDR_B - RDR_A
```

**Interpretação**: Quanto a família ganha/perde mudando de A para B (em USD)

#### **Relative Family Power Gap (RFPG)**
```
RFPG(A → B) = (RDR_B - RDR_A) / |RDR_A|
```

**Interpretação**: Mudança percentual no poder de compra

#### **Per Capita Family Delta**
```
PC_FPPΔ = FPPΔ / (dependents + 1)
```

**Interpretação**: Impacto por pessoa da família

---

## 📐 NORMALIZAÇÃO

### **Z-Score (por país)**
Aplicado em: `renda_disponivel_real`, `iac_raw`, `ioe_raw`

```
normalized_value = (value - country_mean) / country_std
```

**Interpretação**:
- Z-score = 0: Na média do país
- Z-score = 1: 1 desvio-padrão acima da média
- Z-score = -1: 1 desvio-padrão abaixo da média

### **Min-Max (0-1)**
Aplicado para dashboards e comparações visuais

```
normalized_value = (value - min) / (max - min)
```

**Interpretação**:
- 0 = pior valor do dataset
- 1 = melhor valor do dataset

### **Não Normalizados**
Mantidos em valores absolutos:
- Salários
- Custos totais
- EPR (já é uma razão)
- Benefícios

---

## 🗺️ MAPEAMENTO DE CIDADES

Cidades brasileiras mapeadas para contexto econômico:

| Cidade Real | Contexto Econômico | Justificativa |
|-------------|-------------------|---------------|
| São Paulo, Campinas, Guarulhos | São Paulo | Metrópole, custo alto |
| Rio de Janeiro, Niterói | Rio de Janeiro | Grande metrópole |
| Belo Horizonte, Contagem, Vitória | Belo Horizonte | Custo médio |
| Curitiba, Porto Alegre, Florianópolis | Curitiba | Sul, custo médio-alto |
| Salvador, Fortaleza, Recife, etc. | Salvador | Nordeste, custo mais baixo |
| Brasília, Goiânia, Manaus, etc. | Belo Horizonte | Centro-Oeste/Norte, custo médio |

**Padrão**: Cidades não mapeadas → **Belo Horizonte** (custo médio nacional)

---

## 📊 ESTATÍSTICAS GERAIS

### Métricas Médias (Brasil)
- **RDR médio**: R$ 1.557,31
- **EPR médio**: 0,70 (70% da renda em custos básicos)
- **Custo per capita**: R$ 1.866,51
- **IAC médio**: 5,54 (acesso moderado)
- **IOE médio**: 16,92 (acesso moderado a oportunidades)

---

## 🚀 PRÓXIMOS PASSOS

### 1. **EDA Avançada**
- Distribuições de métricas
- Correlações
- Análise por região/cidade
- Identificação de outliers

### 2. **Validação**
- Checagem de consistência
- Valores negativos inesperados
- Normalidade das distribuições

### 3. **Camada GOLD**
- Scores compostos
- Rankings
- Decisões de elegibilidade
- Segmentação
- Dashboards

---

## 🔥 FEATURES AVANÇADAS (BÔNUS)

### Implementações Futuras

#### 1️⃣ **Sensibilidade a Choque Econômico**
```python
Shock_Impact = ΔRDR / ΔCost
```
**Uso**: Identificar quem é mais vulnerável a aumentos de custo

#### 2️⃣ **Robustez Financeira**
Simular variações de ±5% renda, ±10% custo:
```python
RDR_volatility = std(RDR_simulations)
```
**Uso**: Medir resiliência familiar

#### 3️⃣ **Linha de Pobreza Endógena**
```python
poverty_threshold = 0.6 * median(RDR_country)
```
**Uso**: Definição dinâmica baseada na realidade do país

---

## 📝 NOTAS TÉCNICAS

### Limitações
- Benefícios sociais simplificados (não verifica elegibilidade real)
- Câmbio fixo (não considera volatilidade)
- Cidades mapeadas por proxy (não contexto exato)

### Decisões de Design
- **DEPENDENCY_FACTOR = 0.40**: Literatura sugere 30-50%, escolhido valor médio
- **Moradia própria = 50% aluguel**: Estimativa de custos de manutenção/IPTU
- **Escala de consumo infantil**: 60% comida, 30% utilities, 40% saúde

---

## 📚 REFERÊNCIAS

- **Dependency Factor**: OECD equivalence scales
- **EPR thresholds**: Índice de comprometimento de renda (IBGE)
- **Poverty lines**: EUROSTAT relative poverty (60% of median)

---

**Gerado por**: `generate_enriched_data.py`  
**Versão**: 1.0  
**Última atualização**: 2026-01-06
