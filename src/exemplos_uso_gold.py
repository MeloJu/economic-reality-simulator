"""
GOLD LAYER — Exemplos de Uso
Demonstrações práticas de análise com os dados GOLD
"""

import pandas as pd
import numpy as np

# ============================================================================
# CARREGAR DADOS GOLD
# ============================================================================

print("=" * 80)
print("📊 EXEMPLOS DE USO — GOLD LAYER")
print("=" * 80)
print()

# Carregar datasets
qles = pd.read_csv('../gold/quality_of_life_score.csv')
clusters = pd.read_csv('../gold/socioeconomic_clusters.csv')
rankings = pd.read_csv('../gold/country_rankings_by_profile.csv')
vulnerability = pd.read_csv('../gold/vulnerability_and_risk.csv')
scenarios = pd.read_csv('../gold/policy_scenarios.csv')

# ============================================================================
# EXEMPLO 1: ANÁLISE DO QLES
# ============================================================================

print("📈 EXEMPLO 1: Análise do QLES (Quality of Life Economic Score)")
print("-" * 80)

print(f"\n🔹 Estatísticas Gerais:")
print(f"   QLES Médio: {qles['QLES'].mean():.2f}")
print(f"   QLES Mediano: {qles['QLES'].median():.2f}")
print(f"   Desvio Padrão: {qles['QLES'].std():.2f}")
print(f"   Min: {qles['QLES'].min():.2f} | Max: {qles['QLES'].max():.2f}")

print(f"\n🔹 Distribuição por Categoria:")
print(qles['QLES_bucket'].value_counts(normalize=True).mul(100).round(1))

print(f"\n🔹 Top 5 Cidades com Maior QLES Médio:")
top_cities = qles.groupby('city')['QLES'].mean().sort_values(ascending=False).head()
for city, score in top_cities.items():
    print(f"   {city}: {score:.2f}")

print(f"\n🔹 Contribuição Média dos Componentes do QLES:")
components = ['component_rdr', 'component_epr', 'component_iac', 
              'component_ioe', 'component_social']
for comp in components:
    avg = qles[comp].mean()
    pct = (avg / qles[[c for c in components]].sum(axis=1).mean()) * 100
    print(f"   {comp.replace('component_', '').upper()}: {avg:.4f} ({pct:.1f}%)")

# ============================================================================
# EXEMPLO 2: ANÁLISE DE CLUSTERS
# ============================================================================

print("\n" + "=" * 80)
print("🔬 EXEMPLO 2: Análise de Clusters Socioeconômicos")
print("-" * 80)

print(f"\n🔹 Distribuição da População:")
cluster_dist = clusters['cluster_label'].value_counts()
for label, count in cluster_dist.items():
    pct = (count / len(clusters)) * 100
    print(f"   {label}: {count:,} pessoas ({pct:.1f}%)")

# Análise por cidade
print(f"\n🔹 Distribuição de Clusters por Cidade (Top 5):")
city_cluster = pd.crosstab(
    clusters.merge(qles[['person_id', 'city']], on='person_id')['city'],
    clusters['cluster_label'],
    normalize='index'
).mul(100).round(1)

top_cities_for_cluster = city_cluster.sum(axis=1).sort_values(ascending=False).head()
for city in top_cities_for_cluster.index:
    print(f"\n   {city}:")
    for cluster in city_cluster.columns:
        pct = city_cluster.loc[city, cluster]
        if pct > 0:
            print(f"      - {cluster}: {pct:.1f}%")

# ============================================================================
# EXEMPLO 3: VULNERABILIDADE E RISCO
# ============================================================================

print("\n" + "=" * 80)
print("⚠️  EXEMPLO 3: Análise de Vulnerabilidade e Risco")
print("-" * 80)

print(f"\n🔹 Distribuição por Grupo de Risco:")
risk_dist = vulnerability['risk_group'].value_counts()
for risk, count in risk_dist.items():
    pct = (count / len(vulnerability)) * 100
    print(f"   {risk}: {count:,} pessoas ({pct:.1f}%)")

print(f"\n🔹 Flags de Vulnerabilidade:")
flags = ['high_vulnerability', 'high_dependency', 'extreme_pressure', 'negative_income']
for flag in flags:
    count = vulnerability[flag].sum()
    pct = (count / len(vulnerability)) * 100
    print(f"   {flag.replace('_', ' ').title()}: {count:,} ({pct:.1f}%)")

# Cruzar vulnerabilidade com clusters
vuln_cluster = vulnerability.merge(clusters[['person_id', 'cluster_label']], on='person_id')
print(f"\n🔹 Risco Alto por Cluster:")
risk_by_cluster = vuln_cluster[vuln_cluster['risk_group'] == 'Risco Alto'].groupby('cluster_label').size()
risk_by_cluster = risk_by_cluster.sort_values(ascending=False)
for cluster, count in risk_by_cluster.items():
    total_in_cluster = (vuln_cluster['cluster_label'] == cluster).sum()
    pct = (count / total_in_cluster) * 100
    print(f"   {cluster}: {count:,} ({pct:.1f}% do cluster)")

# ============================================================================
# EXEMPLO 4: RANKINGS POR PERFIL
# ============================================================================

print("\n" + "=" * 80)
print("🏆 EXEMPLO 4: Rankings por Perfil Familiar")
print("-" * 80)

profiles = rankings['profile_id'].unique()

for profile in profiles:
    profile_data = rankings[rankings['profile_id'] == profile].sort_values('rank_position')
    desc = profile_data.iloc[0]['description']
    
    print(f"\n🔹 {profile} — {desc}")
    print(f"   Top 3 Localizações:")
    
    for idx, row in profile_data.head(3).iterrows():
        print(f"      {int(row['rank_position'])}º. {row['city']}, {row['country']}")
        print(f"          QLES: {row['QLES_avg']:.2f} | RDR per capita: ${row['avg_per_capita_rdr']:.2f}")

# ============================================================================
# EXEMPLO 5: ANÁLISE DE CENÁRIOS
# ============================================================================

print("\n" + "=" * 80)
print("🎬 EXEMPLO 5: Simulação de Cenários de Política")
print("-" * 80)

scenario_names = scenarios['scenario_name'].unique()

for scenario in scenario_names:
    scenario_data = scenarios[scenarios['scenario_name'] == scenario]
    
    print(f"\n🔹 {scenario}")
    print(f"   Impacto médio: {scenario_data['delta_percent'].mean():.2f}%")
    print(f"   Impacto mediano: {scenario_data['delta_percent'].median():.2f}%")
    print(f"   Pior impacto: {scenario_data['delta_percent'].min():.2f}%")
    print(f"   Melhor impacto: {scenario_data['delta_percent'].max():.2f}%")
    
    # Distribuição de impacto
    negative_impact = (scenario_data['delta_percent'] < -5).sum()
    moderate_impact = ((scenario_data['delta_percent'] >= -5) & (scenario_data['delta_percent'] < 0)).sum()
    positive_impact = (scenario_data['delta_percent'] >= 0).sum()
    
    total = len(scenario_data)
    print(f"\n   Distribuição de impacto:")
    print(f"      Negativo severo (< -5%): {negative_impact:,} ({negative_impact/total*100:.1f}%)")
    print(f"      Negativo moderado (-5% a 0%): {moderate_impact:,} ({moderate_impact/total*100:.1f}%)")
    print(f"      Positivo/neutro (≥ 0%): {positive_impact:,} ({positive_impact/total*100:.1f}%)")

# Cenários por cluster
print(f"\n🔹 Impacto dos Cenários por Cluster:")
scenario_cluster = scenarios.merge(clusters[['person_id', 'cluster_label']], on='person_id')

for cluster in scenario_cluster['cluster_label'].unique():
    cluster_data = scenario_cluster[scenario_cluster['cluster_label'] == cluster]
    print(f"\n   {cluster}:")
    
    for scenario in scenario_names:
        scenario_impact = cluster_data[cluster_data['scenario_name'] == scenario]['delta_percent'].mean()
        print(f"      {scenario}: {scenario_impact:.2f}%")

# ============================================================================
# EXEMPLO 6: ANÁLISE INTEGRADA
# ============================================================================

print("\n" + "=" * 80)
print("🔗 EXEMPLO 6: Análise Integrada (QLES + Cluster + Vulnerabilidade)")
print("-" * 80)

# Merge de todos os datasets
integrated = qles[['person_id', 'city', 'QLES', 'QLES_bucket']].merge(
    clusters[['person_id', 'cluster_label']], on='person_id'
).merge(
    vulnerability[['person_id', 'risk_group']], on='person_id'
)

print(f"\n🔹 QLES Médio por Cluster e Risco:")
pivot = integrated.groupby(['cluster_label', 'risk_group'])['QLES'].agg(['mean', 'count'])
pivot = pivot.round(2)

for cluster in integrated['cluster_label'].unique():
    print(f"\n   {cluster}:")
    cluster_data = pivot.loc[cluster]
    for risk in cluster_data.index:
        mean_qles = cluster_data.loc[risk, 'mean']
        count = int(cluster_data.loc[risk, 'count'])
        print(f"      {risk}: QLES={mean_qles:.2f} (n={count:,})")

# ============================================================================
# INSIGHTS FINAIS
# ============================================================================

print("\n" + "=" * 80)
print("💡 INSIGHTS-CHAVE")
print("=" * 80)

print("""
1. CRISE GENERALIZADA
   - 87% da população com QLES Very Low ou Low
   - Score médio de apenas 18.09/100
   - Renda disponível (RDR) e pressão econômica (EPR) explicam 60% do problema

2. CONCENTRAÇÃO EM VULNERABILIDADE
   - 71% da população está em clusters de risco (Vulnerabilidade Crítica + Sobrevivência)
   - 65% classificados como Risco Alto
   - Apenas 3.6% possui mobilidade ascendente ou alta renda

3. PRESSÃO ECONÔMICA EXTREMA
   - 63% da população com EPR > 0.9 (gasta mais de 90% da renda em custos básicos)
   - 65% em alta vulnerabilidade (EPR > 0.8 E RDR < R$ 500)
   - População está no limite da sobrevivência econômica

4. IMPACTO DE POLÍTICAS
   - Aumento de aluguel (-5%) afeta moderadamente toda população
   - Corte de benefícios (-10%) tem impacto severo em população já vulnerável
   - Ambos cenários pioram situação crítica — necessidade de políticas expansionistas

5. DESIGUALDADE ESTRUTURAL
   - Clusters mostram segmentação clara da sociedade
   - 47% em Vulnerabilidade Crítica vs 0.6% em Alta Renda
   - Mobilidade social limitada (apenas 3% em cluster de mobilidade ascendente)

RECOMENDAÇÕES EXECUTIVAS:
→ Priorizar políticas de renda direta para 71% em vulnerabilidade
→ Controle de custos habitacionais (maior impacto no QLES)
→ Expansão de programas sociais (baixa dependência atual = subdimensionamento)
→ Foco em classe média inferior (24%) para prevenir queda para vulnerabilidade
→ Monitoramento contínuo do QLES como indicador de saúde socioeconômica
""")

print("=" * 80)
print("✅ Análise completa. Dados prontos para Power BI.")
print("=" * 80)
