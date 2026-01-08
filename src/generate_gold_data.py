"""
GOLD LAYER — DECISION & INSIGHTS
Camada final: scores consolidados, clusters, rankings e cenários
Design otimizado para Power BI
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

INPUT_DIR = '../enriched/'
OUTPUT_DIR = '../gold/'

# Pesos para o QLES (Quality of Life Economic Score)
QLES_WEIGHTS = {
    'rdr_zscore': 0.35,
    'epr_inverse': 0.25,
    'iac_zscore': 0.15,
    'ioe_zscore': 0.15,
    'social_support_inverse': 0.10
}

# ============================================================================
# 1️⃣ CARREGAR DADOS SILVER
# ============================================================================

def load_silver_data():
    """Carrega todos os datasets SILVER necessários"""
    print("📥 Carregando dados SILVER...")
    
    people = pd.read_csv(f'{INPUT_DIR}people_enriched.csv')
    household = pd.read_csv(f'{INPUT_DIR}household_costs_enriched.csv')
    cultural = pd.read_csv(f'{INPUT_DIR}cultural_access_enriched.csv')
    opportunity = pd.read_csv(f'{INPUT_DIR}opportunity_access_enriched.csv')
    simulation = pd.read_csv(f'{INPUT_DIR}cross_country_family_simulation.csv')
    comparison = pd.read_csv(f'{INPUT_DIR}cross_country_family_comparison.csv')
    
    # Consolidar features relevantes
    base = people[['person_id', 'age', 'gender', 'city_br', 'education_level', 
                   'job_category', 'gross_salary_brl', 'dependents', 'receives_social_benefit',
                   'renda_disponivel_real', 'economic_pressure_ratio', 'cost_per_capita',
                   'social_support_ratio', 'renda_disponivel_real_zscore']].copy()
    
    # Adicionar features culturais
    base = base.merge(
        cultural[['person_id', 'iac_raw_zscore']],
        on='person_id',
        how='left'
    )
    
    # Adicionar features de oportunidade
    base = base.merge(
        opportunity[['person_id', 'ioe_raw_zscore']],
        on='person_id',
        how='left'
    )
    
    base['country'] = 'Brazil'
    base.rename(columns={'city_br': 'city'}, inplace=True)
    
    print(f"✅ Dados consolidados: {len(base)} registros")
    print(f"   Colunas: {', '.join(base.columns)}\n")
    
    return base, simulation, comparison

# ============================================================================
# 2️⃣ QUALITY OF LIFE ECONOMIC SCORE (QLES)
# ============================================================================

def calculate_qles(df):
    """
    Calcula o QLES (Quality of Life Economic Score)
    
    QLES = 0.35*RDR_zscore + 0.25*(1-EPR) + 0.15*IAC_zscore + 
           0.15*IOE_zscore + 0.10*(1-social_support_ratio)
    
    Normalizado para escala 0-100
    """
    print("🧮 Calculando QLES (Quality of Life Economic Score)...")
    
    qles_df = df[['person_id', 'country', 'city']].copy()
    
    # Componentes intermediários (para explicabilidade)
    qles_df['component_rdr'] = df['renda_disponivel_real_zscore'] * QLES_WEIGHTS['rdr_zscore']
    qles_df['component_epr'] = (1 - df['economic_pressure_ratio']) * QLES_WEIGHTS['epr_inverse']
    qles_df['component_iac'] = df['iac_raw_zscore'] * QLES_WEIGHTS['iac_zscore']
    qles_df['component_ioe'] = df['ioe_raw_zscore'] * QLES_WEIGHTS['ioe_zscore']
    qles_df['component_social'] = (1 - df['social_support_ratio']) * QLES_WEIGHTS['social_support_inverse']
    
    # Score bruto
    qles_df['QLES_raw'] = (
        qles_df['component_rdr'] +
        qles_df['component_epr'] +
        qles_df['component_iac'] +
        qles_df['component_ioe'] +
        qles_df['component_social']
    )
    
    # Normalizar para escala 0-100
    qles_min = qles_df['QLES_raw'].min()
    qles_max = qles_df['QLES_raw'].max()
    qles_df['QLES'] = ((qles_df['QLES_raw'] - qles_min) / (qles_max - qles_min)) * 100
    
    # Criar buckets interpretativos
    qles_df['QLES_bucket'] = pd.cut(
        qles_df['QLES'],
        bins=[0, 20, 40, 60, 80, 100],
        labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'],
        include_lowest=True
    )
    
    # Selecionar colunas finais
    output = qles_df[['person_id', 'country', 'city', 'QLES', 'QLES_bucket',
                      'component_rdr', 'component_epr', 'component_iac', 
                      'component_ioe', 'component_social']]
    
    print(f"✅ QLES calculado")
    print(f"   Range: {output['QLES'].min():.2f} - {output['QLES'].max():.2f}")
    print(f"   Média: {output['QLES'].mean():.2f}")
    print(f"   Distribuição por bucket:")
    print(output['QLES_bucket'].value_counts().sort_index())
    print()
    
    return output

# ============================================================================
# 3️⃣ CLUSTERIZAÇÃO SOCIOECONÔMICA
# ============================================================================

def create_clusters(df):
    """
    Clusterização interpretável usando K-Means
    Features: RDR_zscore, EPR, IAC_zscore, IOE_zscore, cost_per_capita
    """
    print("🔬 Executando clusterização socioeconômica...")
    
    # Features para clustering
    features = ['renda_disponivel_real_zscore', 'economic_pressure_ratio', 
                'iac_raw_zscore', 'ioe_raw_zscore', 'cost_per_capita']
    
    X = df[features].copy()
    
    # Tratar valores infinitos e NaN
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median())
    
    # Padronizar features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Testar k entre 4 e 6 (elbow + silhouette)
    # Para performance, testar com amostra menor
    sample_size = min(2000, len(X_scaled))
    sample_indices = np.random.choice(len(X_scaled), sample_size, replace=False)
    X_sample = X_scaled[sample_indices]
    
    best_k = 4
    best_score = -1
    
    for k in range(4, 7):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=100)
        labels = kmeans.fit_predict(X_sample)
        score = silhouette_score(X_sample, labels)
        print(f"   k={k}: silhouette={score:.3f}")
        
        if score > best_score:
            best_score = score
            best_k = k
    
    print(f"✅ Melhor k={best_k} (silhouette={best_score:.3f})")
    
    # Clustering final com todos os dados
    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10, max_iter=100)
    df['cluster_id'] = kmeans.fit_predict(X_scaled)
    
    # Calcular métricas médias por cluster
    cluster_stats = df.groupby('cluster_id').agg({
        'renda_disponivel_real': 'mean',
        'economic_pressure_ratio': 'mean',
        'iac_raw_zscore': 'mean',
        'ioe_raw_zscore': 'mean',
        'cost_per_capita': 'mean',
        'gross_salary_brl': 'mean',
        'person_id': 'count'
    }).round(2)
    cluster_stats.rename(columns={'person_id': 'count'}, inplace=True)
    
    # Atribuir labels interpretativos
    cluster_labels = assign_cluster_labels(cluster_stats, best_k)
    
    # Preparar output
    cluster_df = df[['person_id', 'cluster_id']].copy()
    cluster_df['cluster_label'] = cluster_df['cluster_id'].map(lambda x: cluster_labels[x]['label'])
    cluster_df['cluster_description'] = cluster_df['cluster_id'].map(lambda x: cluster_labels[x]['description'])
    
    # Adicionar estatísticas do cluster
    for col in ['avg_rdr', 'avg_epr', 'avg_iac', 'avg_ioe', 'avg_cost_per_capita']:
        cluster_df[col] = cluster_df['cluster_id'].map(
            cluster_stats[col.replace('avg_', '')] if col.replace('avg_', '') in cluster_stats.columns 
            else cluster_stats['renda_disponivel_real']
        )
    
    print(f"\n📊 Distribuição dos clusters:")
    print(cluster_df['cluster_label'].value_counts())
    print()
    
    return cluster_df, cluster_stats

def assign_cluster_labels(stats, k):
    """Atribui labels interpretativos aos clusters baseado nas características"""
    
    # Ordenar clusters por renda disponível média
    sorted_clusters = stats.sort_values('renda_disponivel_real')
    
    labels = {}
    
    if k == 4:
        cluster_names = [
            ('Sobrevivência Urbana', 'Alta pressão econômica, renda disponível muito baixa, acesso limitado'),
            ('Classe Média Pressionada', 'Pressão moderada-alta, renda disponível média-baixa, mobilidade limitada'),
            ('Mobilidade Potencial', 'Pressão moderada, renda disponível média-alta, oportunidades emergentes'),
            ('Alta Renda Consolidada', 'Baixa pressão econômica, alta renda disponível, amplo acesso')
        ]
    elif k == 5:
        cluster_names = [
            ('Sobrevivência Urbana', 'Alta pressão econômica, renda disponível muito baixa, acesso limitado'),
            ('Vulnerabilidade Econômica', 'Pressão alta, renda disponível baixa, acesso restrito'),
            ('Classe Média Pressionada', 'Pressão moderada, renda disponível média, mobilidade limitada'),
            ('Estabilidade Emergente', 'Pressão moderada-baixa, renda disponível média-alta, crescimento potencial'),
            ('Alta Renda Consolidada', 'Baixa pressão, alta renda disponível, amplo acesso')
        ]
    else:  # k == 6
        cluster_names = [
            ('Sobrevivência Urbana', 'Alta pressão econômica, renda disponível muito baixa, acesso mínimo'),
            ('Vulnerabilidade Crítica', 'Pressão muito alta, renda disponível baixa, suporte necessário'),
            ('Classe Média Inferior', 'Pressão alta, renda disponível média-baixa, mobilidade limitada'),
            ('Classe Média Estável', 'Pressão moderada, renda disponível média, estabilidade relativa'),
            ('Mobilidade Ascendente', 'Pressão baixa-moderada, renda disponível alta, oportunidades amplas'),
            ('Alta Renda Consolidada', 'Baixa pressão, renda disponível muito alta, acesso pleno')
        ]
    
    for i, cluster_id in enumerate(sorted_clusters.index):
        labels[cluster_id] = {
            'label': cluster_names[i][0],
            'description': cluster_names[i][1]
        }
    
    return labels

# ============================================================================
# 4️⃣ RANKINGS POR PERFIL
# ============================================================================

def create_profile_rankings(simulation_df):
    """Cria rankings contextuais baseados em perfis familiares"""
    print("📊 Criando rankings por perfil familiar...")
    
    # Calcular QLES simplificado para simulação (baseado apenas em RDR per capita)
    # Como não temos todas as features, usamos proxy
    simulation_df['QLES_proxy'] = (
        simulation_df['per_capita_rdr'] / simulation_df['per_capita_rdr'].max()
    ) * 100
    
    # Criar ranking por perfil
    simulation_df['rank_position'] = simulation_df.groupby('profile_id')['QLES_proxy'].rank(
        method='dense', ascending=False
    ).astype(int)
    
    # Agregar por perfil + país/cidade
    rankings = simulation_df.groupby(['profile_id', 'description', 'country', 'city']).agg({
        'QLES_proxy': 'mean',
        'per_capita_rdr': 'mean',
        'rank_position': 'first'
    }).reset_index()
    
    rankings.rename(columns={
        'QLES_proxy': 'QLES_avg',
        'per_capita_rdr': 'avg_per_capita_rdr'
    }, inplace=True)
    
    rankings = rankings.sort_values(['profile_id', 'rank_position'])
    
    print(f"✅ Rankings criados para {rankings['profile_id'].nunique()} perfis")
    print(f"   Localizações ranqueadas: {len(rankings)}")
    print()
    
    return rankings

# ============================================================================
# 5️⃣ VULNERABILIDADE E RISCO
# ============================================================================

def create_vulnerability_flags(df):
    """Cria flags simples e interpretáveis de vulnerabilidade"""
    print("⚠️  Analisando vulnerabilidade e risco...")
    
    vuln_df = df[['person_id']].copy()
    
    # Flag 1: Alta vulnerabilidade (alta pressão E renda disponível negativa/baixa)
    vuln_df['high_vulnerability'] = (
        (df['economic_pressure_ratio'] > 0.8) & 
        (df['renda_disponivel_real'] < 500)
    )
    
    # Flag 2: Alta dependência de suporte social
    vuln_df['high_dependency'] = (df['social_support_ratio'] > 0.3)
    
    # Flag 3: Pressão extrema
    vuln_df['extreme_pressure'] = (df['economic_pressure_ratio'] > 0.9)
    
    # Flag 4: Renda negativa (não consegue cobrir custos básicos)
    vuln_df['negative_income'] = (df['renda_disponivel_real'] < 0)
    
    # Classificação de grupo de risco
    def classify_risk(row):
        if row['high_vulnerability'] and row['high_dependency']:
            return 'Risco Crítico'
        elif row['high_vulnerability'] or row['extreme_pressure']:
            return 'Risco Alto'
        elif row['negative_income']:
            return 'Risco Moderado'
        else:
            return 'Risco Baixo'
    
    vuln_df['risk_group'] = vuln_df.apply(classify_risk, axis=1)
    
    print(f"📊 Distribuição de risco:")
    print(vuln_df['risk_group'].value_counts())
    print(f"\n   Alta vulnerabilidade: {vuln_df['high_vulnerability'].sum()} pessoas")
    print(f"   Alta dependência: {vuln_df['high_dependency'].sum()} pessoas")
    print(f"   Pressão extrema: {vuln_df['extreme_pressure'].sum()} pessoas")
    print()
    
    return vuln_df

# ============================================================================
# 6️⃣ SIMULAÇÃO DE CENÁRIOS
# ============================================================================

def simulate_policy_scenarios(df, qles_df):
    """Simula cenários determinísticos de políticas"""
    print("🎬 Simulando cenários de política...")
    
    scenarios = []
    
    # Cenário base
    base = df[['person_id', 'renda_disponivel_real', 'economic_pressure_ratio', 
               'cost_per_capita', 'renda_disponivel_real_zscore']].copy()
    base = base.merge(qles_df[['person_id', 'QLES']], on='person_id', how='left')
    base.rename(columns={'QLES': 'QLES_base'}, inplace=True)
    
    # CENÁRIO 1: Aumento de aluguel em +20%
    print("   Cenário 1: Aumento de aluguel +20%")
    scenario1 = base.copy()
    scenario1['housing_cost_increase'] = 0.20 * df['cost_per_capita'] * 0.35  # Assumindo habitação = 35% do custo
    scenario1['rdr_after'] = scenario1['renda_disponivel_real'] - scenario1['housing_cost_increase']
    scenario1['epr_after'] = np.minimum(
        (df['cost_per_capita'] + scenario1['housing_cost_increase']) / df['gross_salary_brl'],
        1.0
    )
    
    # Recalcular QLES simplificado
    scenario1['QLES_after'] = scenario1['QLES_base'] * (
        0.65 +  # Base 65%
        0.35 * (scenario1['rdr_after'] / (scenario1['renda_disponivel_real'] + 1))  # Ajuste proporcional
    )
    scenario1['delta_percent'] = (
        (scenario1['QLES_after'] - scenario1['QLES_base']) / scenario1['QLES_base']
    ) * 100
    scenario1['scenario_name'] = 'Aluguel +20%'
    
    scenarios.append(scenario1[['person_id', 'scenario_name', 'QLES_base', 'QLES_after', 'delta_percent']])
    
    # CENÁRIO 2: Corte de benefícios em -15%
    print("   Cenário 2: Corte de benefícios sociais -15%")
    scenario2 = base.copy()
    benefit_users = df['receives_social_benefit'] == True
    scenario2['benefit_cut'] = 0.0
    scenario2.loc[benefit_users, 'benefit_cut'] = (
        df.loc[benefit_users, 'renda_disponivel_real'] * 
        df.loc[benefit_users, 'social_support_ratio'] * 0.15
    )
    scenario2['rdr_after'] = scenario2['renda_disponivel_real'] - scenario2['benefit_cut']
    scenario2['QLES_after'] = scenario2['QLES_base'] * (
        0.90 -  # Penalização direta -10%
        0.10 * (scenario2['benefit_cut'] / (scenario2['renda_disponivel_real'] + 1))
    )
    scenario2['delta_percent'] = (
        (scenario2['QLES_after'] - scenario2['QLES_base']) / scenario2['QLES_base']
    ) * 100
    scenario2['scenario_name'] = 'Benefícios -15%'
    
    scenarios.append(scenario2[['person_id', 'scenario_name', 'QLES_base', 'QLES_after', 'delta_percent']])
    
    # Consolidar
    scenarios_df = pd.concat(scenarios, ignore_index=True)
    scenarios_df.rename(columns={'QLES_base': 'QLES_before'}, inplace=True)
    
    print(f"✅ Cenários simulados: {scenarios_df['scenario_name'].nunique()}")
    print(f"   Impacto médio Cenário 1: {scenario1['delta_percent'].mean():.2f}%")
    print(f"   Impacto médio Cenário 2: {scenario2['delta_percent'].mean():.2f}%")
    print()
    
    return scenarios_df

# ============================================================================
# 7️⃣ PIPELINE PRINCIPAL
# ============================================================================

def main():
    print("=" * 80)
    print("🏆 GOLD LAYER — DECISION & INSIGHTS")
    print("=" * 80)
    print()
    
    # Criar diretório de saída
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Carregar dados
    base_df, simulation_df, comparison_df = load_silver_data()
    
    # 2. Calcular QLES
    qles_df = calculate_qles(base_df)
    qles_df.to_csv(f'{OUTPUT_DIR}quality_of_life_score.csv', index=False)
    print(f"💾 Salvo: quality_of_life_score.csv\n")
    
    # 3. Clusterização
    clusters_df, cluster_stats = create_clusters(base_df)
    clusters_df.to_csv(f'{OUTPUT_DIR}socioeconomic_clusters.csv', index=False)
    cluster_stats.to_csv(f'{OUTPUT_DIR}cluster_statistics.csv')
    print(f"💾 Salvo: socioeconomic_clusters.csv\n")
    
    # 4. Rankings por perfil
    rankings_df = create_profile_rankings(simulation_df)
    rankings_df.to_csv(f'{OUTPUT_DIR}country_rankings_by_profile.csv', index=False)
    print(f"💾 Salvo: country_rankings_by_profile.csv\n")
    
    # 5. Vulnerabilidade
    vuln_df = create_vulnerability_flags(base_df)
    vuln_df.to_csv(f'{OUTPUT_DIR}vulnerability_and_risk.csv', index=False)
    print(f"💾 Salvo: vulnerability_and_risk.csv\n")
    
    # 6. Cenários
    scenarios_df = simulate_policy_scenarios(base_df, qles_df)
    scenarios_df.to_csv(f'{OUTPUT_DIR}policy_scenarios.csv', index=False)
    print(f"💾 Salvo: policy_scenarios.csv\n")
    
    # Resumo final
    print("=" * 80)
    print("✅ GOLD LAYER COMPLETA")
    print("=" * 80)
    print(f"""
Datasets gerados:
1. quality_of_life_score.csv       → {len(qles_df)} registros
2. socioeconomic_clusters.csv      → {len(clusters_df)} registros, {clusters_df['cluster_id'].nunique()} clusters
3. country_rankings_by_profile.csv → {len(rankings_df)} rankings
4. vulnerability_and_risk.csv      → {len(vuln_df)} registros
5. policy_scenarios.csv            → {len(scenarios_df)} cenários

Todos os arquivos estão prontos para consumo direto no Power BI.
Datasets denormalizados, categóricos explícitos, sem JSON aninhado.
    """)

if __name__ == '__main__':
    main()
