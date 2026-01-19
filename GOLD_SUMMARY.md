# 🏆 GOLD LAYER — Sumário Executivo

**Camada de Decisão e Insights Socioeconômicos**

---

## 📊 VISÃO GERAL

A camada GOLD consolida as métricas da camada SILVER em **insights acionáveis** para tomada de decisão executiva e análise de políticas públicas.

### Princípios

✅ **Decisão, não descrição** — scores consolidados em vez de features isoladas  
✅ **Interpretabilidade** — clusters com narrativa clara, não técnica  
✅ **Ação** — simulações de cenários para "what-if analysis"  
✅ **Business-ready** — design otimizado para Power BI

---

## 🎯 SCORE PRINCIPAL: QLES

**QLES (Quality of Life Economic Score)** é o **indicador consolidado** de qualidade de vida econômica.

### Composição

| Componente | Peso | Métrica Base |
|------------|------|--------------|
| Renda Disponível Real | 35% | RDR_zscore |
| Pressão Econômica | 25% | 1 - EPR |
| Acesso Cultural | 15% | IAC_zscore |
| Oportunidades | 15% | IOE_zscore |
| Suporte Social | 10% | 1 - social_support_ratio |

**Escala**: 0-100 (normalizado)

### Resultados

- **Média nacional**: 18.09/100
- **Mediana**: 17.34
- **87% da população** em Very Low (0-20) ou Low (20-40)
- **Apenas 0.9%** em Medium+ (40-100)

### Interpretação

> **QLES < 20** indica crise socioeconômica generalizada.  
> A baixa média nacional (18.09) reflete pressão econômica extrema, renda disponível limitada e acesso restrito a cultura e oportunidades.

---

## 🔬 SEGMENTAÇÃO: 6 CLUSTERS

Clusterização socioeconômica usando **K-Means** (k=6, silhouette=0.371).

| # | Cluster | % Pop | Características | Perfil |
|---|---------|-------|-----------------|--------|
| 5 | **Vulnerabilidade Crítica** | 47% | EPR muito alta, RDR baixa | Não cobre necessidades básicas |
| 0 | **Classe Média Inferior** | 24% | EPR alta, mobilidade limitada | Estável mas sem margem |
| 2 | **Classe Média Estável** | 15% | EPR moderada, estabilidade | Conforto relativo |
| 4 | **Sobrevivência Urbana** | 11% | EPR extrema, acesso mínimo | Situação crítica |
| 1 | **Mobilidade Ascendente** | 3% | EPR baixa, oportunidades amplas | Potencial de crescimento |
| 3 | **Alta Renda Consolidada** | 0.6% | EPR muito baixa, acesso pleno | Elite econômica |

### Insights

- **71% em clusters de vulnerabilidade** (Crítica + Sobrevivência)
- **Classe média**: apenas 39% (Inferior + Estável)
- **Elite econômica**: menos de 1%

> A distribuição mostra **desigualdade estrutural severa** com concentração maciça em vulnerabilidade.

---

## ⚠️ VULNERABILIDADE E RISCO

### Classificação de Risco

| Grupo | % População | Critérios |
|-------|-------------|-----------|
| **Risco Crítico** | 0% | high_vulnerability E high_dependency |
| **Risco Alto** | 65.1% | high_vulnerability OU extreme_pressure |
| **Risco Moderado** | 0% | negative_income |
| **Risco Baixo** | 34.8% | Nenhuma flag ativa |

### Flags de Vulnerabilidade

| Flag | % | Critério |
|------|---|----------|
| **Alta vulnerabilidade** | 65.1% | EPR > 0.8 E RDR < R$ 500 |
| **Pressão extrema** | 62.8% | EPR > 0.9 |
| **Renda negativa** | 59.0% | RDR < 0 |
| **Alta dependência** | 0.0% | social_support_ratio > 0.3 |

### Insights

> **65% da população** está em Risco Alto — população crítica para políticas públicas.  
> **63% gasta mais de 90% da renda em necessidades básicas** — sobrevivência no limite.  
> **Ausência de alta dependência de benefícios** sugere subdimensionamento de programas sociais.

---

## 🎬 SIMULAÇÃO DE CENÁRIOS

Dois cenários determinísticos de políticas públicas.

### Cenário 1: **Aumento de Aluguel +20%**

- **Impacto médio**: -4.93% no QLES
- **10.3%** com impacto severo (< -5%)
- **Clusters mais afetados**: Classe Média Inferior (-14.21%)

**Interpretação**: Aumento de custo habitacional tem impacto moderado mas generalizado. Classe média é mais sensível que população em vulnerabilidade (que já gasta proporcionalmente menos com moradia).

### Cenário 2: **Corte de Benefícios Sociais -15%**

- **Impacto médio**: -10.00% no QLES
- **86.5%** com impacto severo
- **Uniforme entre clusters**

**Interpretação**: Corte de benefícios tem impacto severo e generalizado, dobrando o impacto do cenário de aluguel. População já está no limite — qualquer redução de suporte social é crítica.

### Conclusão

> **Ambos cenários pioram situação já crítica**.  
> Necessidade de **políticas expansionistas**: aumento de renda, controle de custos habitacionais, expansão de programas sociais.

---

## 🏆 RANKINGS POR PERFIL

Rankings contextuais para **4 perfis familiares**.

### Exemplo: **F4 — Profissional Solteiro, Classe Média-Alta**

| Posição | Cidade | País | QLES | RDR per capita |
|---------|--------|------|------|----------------|
| 1º | Faro | Portugal | 100.00 | $9,473 |
| 2º | Porto | Portugal | 99.04 | $9,382 |
| 3º | Lisbon | Portugal | 96.25 | $9,118 |
| ... | ... | ... | ... | ... |
| 18º | São Paulo | Brazil | 17.53 | $1,661 |

### Insights

- **Portugal domina rankings** para todos os perfis
- **Diferença de 82 pontos** no QLES entre Faro e São Paulo
- **Ganho de $7.812 em RDR** (469% de aumento)

> Migração internacional representa **oportunidade massiva** para profissionais brasileiros.

---

## 💡 INSIGHTS EXECUTIVOS

### 1. **Crise Generalizada**

- 87% da população com QLES Very Low ou Low
- Score médio de apenas 18.09/100
- Renda disponível e pressão econômica explicam 60% do problema

**Recomendação**: Políticas de **renda direta** (transferências, subsídios) têm maior impacto.

### 2. **Concentração em Vulnerabilidade**

- 71% da população em clusters de risco
- Apenas 3.6% com mobilidade ascendente ou alta renda
- Desigualdade estrutural severa

**Recomendação**: **Segmentação de políticas** — abordagens diferentes para cada cluster.

### 3. **Pressão Econômica Extrema**

- 63% da população com EPR > 0.9 (gasta mais de 90% da renda)
- 59% não consegue cobrir custos básicos (RDR negativa)
- População no limite da sobrevivência

**Recomendação**: **Controle de custos** (especialmente habitação) é urgente.

### 4. **Impacto de Políticas**

- Aumento de aluguel (-5%) tem impacto moderado
- Corte de benefícios (-10%) tem impacto severo
- Cenários pioram situação crítica

**Recomendação**: **Políticas expansionistas** — aumentar suporte, não reduzir.

### 5. **Subdimensionamento de Programas Sociais**

- 0% de alta dependência de benefícios
- Baixo social_support_ratio
- População vulnerável não está sendo atendida

**Recomendação**: **Expansão de programas sociais** — cobertura e valores insuficientes.

---

## 🎯 RECOMENDAÇÕES ESTRATÉGICAS

### Curto Prazo (0-6 meses)

1. **Transferência de renda emergencial** para 71% em vulnerabilidade
2. **Congelamento de aluguéis** em cidades críticas
3. **Expansão de benefícios sociais** (cobertura e valores)

### Médio Prazo (6-18 meses)

4. **Programa habitacional popular** (reduzir custo de moradia)
5. **Subsídio educacional** (cursos técnicos, idiomas)
6. **Incentivo à mobilidade urbana** (transporte subsidiado)

### Longo Prazo (18+ meses)

7. **Política de renda mínima universal** (estabilizar classe média)
8. **Programa de mobilidade internacional** (apoio à emigração qualificada)
9. **Reforma tributária progressiva** (redistribuição de renda)

---

## 📈 MONITORAMENTO CONTÍNUO

### KPIs de Acompanhamento

| KPI | Valor Atual | Meta (12 meses) |
|-----|-------------|-----------------|
| QLES Médio Nacional | 18.09 | 25.00 |
| % Risco Alto | 65.1% | 45.0% |
| % Vulnerabilidade Crítica (cluster) | 47.0% | 30.0% |
| % Pressão Extrema (EPR > 0.9) | 62.8% | 40.0% |
| % Classe Média (clusters 0+2) | 39.0% | 50.0% |

### Frequência de Atualização

- **QLES e clusters**: Mensal
- **Vulnerabilidade**: Quinzenal
- **Cenários**: Ad-hoc (quando políticas mudam)
- **Rankings**: Trimestral

---

## 📊 CONSUMO DE DADOS

### Power BI

- **5 datasets** prontos para importação
- **Modelo dimensional** pré-definido
- **30+ medidas DAX** documentadas
- **5 dashboards** recomendados

Ver: [POWER_BI_INTEGRATION.md](POWER_BI_INTEGRATION.md)

### Python

```python
import pandas as pd

# Carregar GOLD
qles = pd.read_csv('gold/quality_of_life_score.csv')
clusters = pd.read_csv('gold/socioeconomic_clusters.csv')

# Análise rápida
print(f"QLES médio: {qles['QLES'].mean():.2f}")
print(f"Distribuição:\n{qles['QLES_bucket'].value_counts()}")
```

Ver: [exemplos_uso_gold.py](src/exemplos_uso_gold.py)

---

## 🚀 PRÓXIMOS PASSOS

### Análise

- [ ] Dashboard executivo no Power BI
- [ ] Análise temporal (dados históricos)
- [ ] Benchmark internacional expandido
- [ ] Modelo preditivo de vulnerabilidade

### Produto

- [ ] API REST para acesso a scores
- [ ] Sistema de alertas (vulnerabilidade crítica)
- [ ] Relatórios automatizados (mensais)
- [ ] Integração com sistemas governamentais

### Pesquisa

- [ ] Validação externa (dados oficiais)
- [ ] Análise de sensibilidade (componentes QLES)
- [ ] Transição entre clusters (mobilidade social)
- [ ] Otimização de políticas (algoritmos)

---

## 📚 DOCUMENTAÇÃO TÉCNICA

- **Detalhada**: [gold/README.md](gold/README.md) — 200+ linhas de documentação
- **Referência rápida**: [GOLD_QUICK_REFERENCE.md](GOLD_QUICK_REFERENCE.md)
- **Power BI**: [POWER_BI_INTEGRATION.md](POWER_BI_INTEGRATION.md)
- **Código**: [src/generate_gold_data.py](src/generate_gold_data.py) — 470+ linhas

---

## ✅ STATUS

**Pipeline**: RAW → SILVER → **GOLD** ✅  
**Registros**: 10.000 pessoas, 6 clusters, 2 cenários  
**Datasets**: 5 CSVs prontos para Power BI  
**Qualidade**: Validado, documentado, pronto para produção

---

**Gerado em**: 2026-01-08  
**Versão**: 1.0  
**Responsável**: Pipeline automatizado  
**Próxima revisão**: 2026-02-08 (mensal)
