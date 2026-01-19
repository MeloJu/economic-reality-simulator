# 🏆 GOLD LAYER — Quick Reference

## 🎯 Propósito
Camada de **decisão e insights** — transforma métricas SILVER em scores consolidados, clusters interpretativos e rankings acionáveis.

---

## 📦 Datasets

| Arquivo | Registros | Uso Principal |
|---------|-----------|---------------|
| `quality_of_life_score.csv` | 10.000 | Score QLES consolidado (0-100) |
| `socioeconomic_clusters.csv` | 10.000 | 6 clusters interpretativos |
| `country_rankings_by_profile.csv` | 72 | Rankings por perfil familiar |
| `vulnerability_and_risk.csv` | 10.000 | Flags de risco + classificação |
| `policy_scenarios.csv` | 20.000 | 2 cenários de política simulados |

---

## 🧮 QLES (Quality of Life Economic Score)

**Fórmula:**
```
QLES = 0.35*RDR_zscore + 0.25*(1-EPR) + 0.15*IAC_zscore + 0.15*IOE_zscore + 0.10*(1-social_support)
Escala: 0-100 (normalizado)
```

**Categorias:**
- Very Low: 0-20 (77.7%)
- Low: 20-40 (21.4%)
- Medium: 40-60 (0.8%)
- High: 60-80 (0.1%)
- Very High: 80-100 (0.0%)

**Média Geral:** 18.09

---

## 🔬 Clusters Socioeconômicos

| Cluster | % População | Características |
|---------|-------------|-----------------|
| **Vulnerabilidade Crítica** | 47% | Pressão muito alta, RDR baixa |
| **Classe Média Inferior** | 24% | Pressão alta, mobilidade limitada |
| **Classe Média Estável** | 15% | Pressão moderada, estabilidade relativa |
| **Sobrevivência Urbana** | 11% | Alta pressão, acesso mínimo |
| **Mobilidade Ascendente** | 3% | Baixa pressão, oportunidades amplas |
| **Alta Renda Consolidada** | 0.6% | Muito baixa pressão, acesso pleno |

**Técnica:** K-Means (k=6, silhouette=0.371)

---

## ⚠️ Vulnerabilidade

**Grupos de Risco:**
- Risco Alto: 65.1%
- Risco Baixo: 34.8%

**Flags:**
- `high_vulnerability`: EPR > 0.8 E RDR < R$ 500 → **65.1%**
- `extreme_pressure`: EPR > 0.9 → **62.8%**
- `negative_income`: RDR < 0 → **59.0%**
- `high_dependency`: social_support > 0.3 → **0.0%**

---

## 🎬 Cenários de Política

### Cenário 1: Aumento de aluguel +20%
- Impacto médio: **-4.93%** no QLES
- 10.3% com impacto severo (< -5%)
- Afeta especialmente Classe Média Inferior (-14.21%)

### Cenário 2: Corte de benefícios -15%
- Impacto médio: **-10.00%** no QLES
- 86.5% com impacto severo
- Uniforme entre clusters

---

## 🏆 Rankings (Exemplo: F4 - Profissional Solteiro)

| Posição | Cidade | QLES | RDR per capita |
|---------|--------|------|----------------|
| 1º | Faro, Portugal | 100.00 | $9,473 |
| 2º | Porto, Portugal | 99.04 | $9,382 |
| 3º | Lisbon, Portugal | 96.25 | $9,118 |

---

## 📊 Power BI — Modelo de Dados

```
quality_of_life_score [FATO]
    ├─ [1:1] socioeconomic_clusters
    ├─ [1:1] vulnerability_and_risk
    └─ [1:N] policy_scenarios

country_rankings_by_profile [FATO INDEPENDENTE]
```

---

## 📈 DAX Essenciais

```dax
// KPI Principal
QLES Médio = AVERAGE(quality_of_life_score[QLES])

// Vulnerabilidade
% Risco Alto = 
DIVIDE(
    COUNTROWS(FILTER(vulnerability_and_risk, [risk_group] = "Risco Alto")),
    COUNTROWS(vulnerability_and_risk)
)

// Cenários
Impacto Médio = AVERAGE(policy_scenarios[delta_percent])

// Cluster Dominante
Cluster Principal = 
CALCULATE(
    VALUES(socioeconomic_clusters[cluster_label]),
    TOPN(1, 
        VALUES(socioeconomic_clusters[cluster_label]),
        CALCULATE(COUNTROWS(socioeconomic_clusters))
    )
)
```

---

## 🚀 Execução

```bash
# Gerar GOLD
cd src
python generate_gold_data.py

# Analisar resultados
python exemplos_uso_gold.py
```

---

## 💡 Insights-Chave

1. **87% da população** com QLES Very Low/Low
2. **71%** em clusters de vulnerabilidade
3. **65%** em Risco Alto
4. **63%** com pressão econômica extrema (EPR > 0.9)
5. **Apenas 3.6%** com mobilidade ascendente ou alta renda

---

## 🎯 Próximos Passos

- [ ] Dashboard executivo no Power BI
- [ ] Drill-down por cluster e cidade
- [ ] Análise temporal (se dados históricos disponíveis)
- [ ] Benchmark internacional
- [ ] Modelo preditivo de vulnerabilidade

---

**Documentação completa:** [README.md](README.md)  
**Pipeline:** RAW → SILVER → **GOLD**  
**Status:** ✅ Produção
