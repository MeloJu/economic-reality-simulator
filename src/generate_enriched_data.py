
import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

RAW_DIR = Path("../raw")
ENRICHED_DIR = Path("../enriched")
ENRICHED_DIR.mkdir(exist_ok=True)

# Fator de ajuste por dependente (literatura sugere 30-50%)
DEPENDENCY_FACTOR = 0.40

# Mapeamento de cidades brasileiras para contexto econômico
CITY_MAPPING = {
    # Grandes metrópoles -> São Paulo (mais caro)
    'São Paulo': 'São Paulo',
    'Campinas': 'São Paulo',
    'Santo André': 'São Paulo',
    'Guarulhos': 'São Paulo',
    
    # Rio de Janeiro
    'Rio de Janeiro': 'Rio de Janeiro',
    'Niterói': 'Rio de Janeiro',
    
    # Belo Horizonte
    'Belo Horizonte': 'Belo Horizonte',
    'Contagem': 'Belo Horizonte',
    
    # Curitiba
    'Curitiba': 'Curitiba',
    
    # Salvador
    'Salvador': 'Salvador',
    'Feira de Santana': 'Salvador',
    
    # Demais cidades por região/custo de vida
    # Sul (similar a Curitiba)
    'Porto Alegre': 'Curitiba',
    'Florianópolis': 'Curitiba',
    
    # Nordeste (similar a Salvador - mais barato)
    'Fortaleza': 'Salvador',
    'Recife': 'Salvador',
    'Natal': 'Salvador',
    'Maceió': 'Salvador',
    'João Pessoa': 'Salvador',
    'Aracaju': 'Salvador',
    'São Luís': 'Salvador',
    
    # Centro-Oeste (custo médio - Belo Horizonte)
    'Brasília': 'Belo Horizonte',
    'Goiânia': 'Belo Horizonte',
    'Campo Grande': 'Belo Horizonte',
    'Cuiabá': 'Belo Horizonte',
    
    # Norte (custo mais alto que NE - Belo Horizonte)
    'Manaus': 'Belo Horizonte',
    'Belém': 'Belo Horizonte',
    'Porto Velho': 'Belo Horizonte',
    'Boa Vista': 'Belo Horizonte',
    'Rio Branco': 'Salvador',
    'Macapá': 'Salvador',
    'Palmas': 'Salvador',
    
    # Sudeste interior (Belo Horizonte)
    'Vitória': 'Belo Horizonte',
    'Vila Velha': 'Belo Horizonte',
}


# ============================================================================
# 1. CARREGAMENTO DOS DADOS RAW
# ============================================================================

def load_raw_data():
    """Carrega todos os arquivos RAW"""
    people = pd.read_csv(RAW_DIR / "people_raw.csv")
    economic = pd.read_csv(RAW_DIR / "economic_context_raw.csv")
    cultural = pd.read_csv(RAW_DIR / "cultural_costs_raw.csv")
    opportunity = pd.read_csv(RAW_DIR / "opportunity_costs_raw.csv")
    social = pd.read_csv(RAW_DIR / "social_benefits_raw.csv")
    
    return people, economic, cultural, opportunity, social


# ============================================================================
# 2. MÉTRICAS DE CUSTOS E RENDA
# ============================================================================

def calculate_household_costs(people_df, economic_df):
    """
    Calcula Total Household Cost e Renda Disponível Real (RDR)
    """
    # Mapear cidades para contexto econômico
    people_df['city_mapped'] = people_df['city_br'].map(CITY_MAPPING)
    
    # Se cidade não mapeada, usar Belo Horizonte como padrão (custo médio)
    people_df['city_mapped'] = people_df['city_mapped'].fillna('Belo Horizonte')
    
    # Merge com contexto econômico
    df = people_df.merge(
        economic_df,
        left_on=['city_mapped'],
        right_on=['city'],
        how='left'
    )
    
    # Custos de habitação baseado em rent_status
    df['housing_cost'] = np.where(
        df['dependents'] == 0,
        df['avg_rent_single'],
        df['avg_rent_family']
    )
    
    # Ajuste para moradia própria ou cedida (50% do aluguel em manutenção/IPTU)
    df.loc[df['rent_status'].isin(['próprio', 'cedido']), 'housing_cost'] *= 0.5
    
    # Ajuste de custos por dependente (escala de consumo)
    df['dependent_adjustment'] = df['dependents'] * (
        df['basic_food_cost'] * 0.6 +  # Criança consome ~60% do adulto em comida
        df['utilities_cost'] * 0.3 +    # 30% adicional em utilities
        df['healthcare_cost'] * 0.4     # 40% adicional em saúde
    )
    
    # Total Household Cost
    df['total_household_cost'] = (
        df['housing_cost'] +
        df['basic_food_cost'] +
        df['transport_cost'] +
        df['utilities_cost'] +
        df['healthcare_cost'] +
        df['dependent_adjustment']
    )
    
    # Benefícios sociais calculados (simplificado - assumindo elegibilidade)
    df['total_social_benefits'] = 0.0
    
    # Renda Disponível Real (RDR)
    df['renda_disponivel_real'] = (
        df['net_salary_brl'] +
        df['total_social_benefits'] -
        df['total_household_cost']
    )
    
    return df


def calculate_economic_metrics(df):
    """
    Calcula métricas de pressão econômica e estrutura familiar
    """
    # Economic Pressure Ratio (EPR)
    df['economic_pressure_ratio'] = df['total_household_cost'] / df['net_salary_brl']
    
    # EPR Clean - versão limpa para análises (remove inf e valores inválidos)
    # Mantém apenas valores economicamente interpretáveis (0 < EPR < 2)
    df['epr_clean'] = df['economic_pressure_ratio'].where(
        (df['economic_pressure_ratio'] > 0) &
        (df['economic_pressure_ratio'] < 2.0) &
        (np.isfinite(df['economic_pressure_ratio'])),
        np.nan
    )
    
    # Custo por Dependente (CPD)
    df['cost_per_capita'] = df['total_household_cost'] / (df['dependents'] + 1)
    
    # Salário Mínimo Ajustado
    df['adjusted_min_wage'] = df['local_min_wage'] * (1 + df['dependents'] * DEPENDENCY_FACTOR)
    
    # Distância do Salário Mínimo Ajustado (DSMA)
    df['dist_salario_minimo_ajustado'] = (
        (df['net_salary_brl'] - df['adjusted_min_wage']) / df['adjusted_min_wage']
    )
    
    # Gap de Subsistência
    df['subsistence_gap'] = df['net_salary_brl'] - df['total_household_cost']
    
    # Social Support Ratio (SSR)
    df['social_support_ratio'] = df['total_social_benefits'] / df['net_salary_brl']
    
    return df


# ============================================================================
# 3. ACESSO CULTURAL
# ============================================================================

def calculate_cultural_access(df, cultural_df):
    """
    Calcula Índice de Acesso Cultural (bruto e normalizado)
    """
    # Adicionar país baseado na cidade
    df['country'] = 'Brazil'  # Todos os dados são BR por enquanto
    
    # Merge com custos culturais
    df = df.merge(cultural_df, on='country', how='left')
    
    # Cultural Basic Cost
    df['cultural_basic_cost'] = (
        df['streaming_cost'] +
        df['internet_cost'] +
        df['cinema_ticket'] +
        df['cultural_events'] +
        df['music_subscription']
    )
    
    # Índice de Acesso Cultural (bruto)
    # Evita divisão por zero
    df['iac_raw'] = df['renda_disponivel_real'] / df['cultural_basic_cost'].replace(0, np.nan)
    
    return df


# ============================================================================
# 4. OPORTUNIDADES ECONÔMICAS
# ============================================================================

def calculate_opportunity_access(df, opportunity_df):
    """
    Calcula Índice de Oportunidades Econômicas (bruto)
    """
    # Merge com custos de oportunidades
    df = df.merge(opportunity_df, on='country', how='left')
    
    # IOE - soma dos acessos individuais
    # Quanto maior o RDR relativo ao custo, maior o acesso
    df['ioe_technical'] = df['renda_disponivel_real'] / df['technical_course'].replace(0, np.nan)
    df['ioe_college'] = df['renda_disponivel_real'] / df['college_private'].replace(0, np.nan)
    df['ioe_language'] = df['renda_disponivel_real'] / df['language_course'].replace(0, np.nan)
    df['ioe_savings'] = df['renda_disponivel_real'] / df['emergency_savings_target'].replace(0, np.nan)
    df['ioe_mobility'] = df['renda_disponivel_real'] / df['mobility_cost'].replace(0, np.nan)
    
    # Índice agregado (soma)
    df['ioe_raw'] = (
        df['ioe_technical'].fillna(0) +
        df['ioe_college'].fillna(0) +
        df['ioe_language'].fillna(0) +
        df['ioe_savings'].fillna(0) +
        df['ioe_mobility'].fillna(0)
    )
    
    return df


# ============================================================================
# 5. NORMALIZAÇÃO
# ============================================================================

def normalize_metrics(df):
    """
    Aplica normalização Z-score por país e Min-Max global
    """
    # Z-score por país para RDR, IAC, IOE
    for metric in ['renda_disponivel_real', 'iac_raw', 'ioe_raw']:
        if metric in df.columns:
            df[f'{metric}_zscore'] = df.groupby('country')[metric].transform(
                lambda x: (x - x.mean()) / x.std() if x.std() > 0 else 0
            )
    
    # Min-Max (0-1) para métricas de dashboard
    for metric in ['renda_disponivel_real', 'iac_raw', 'ioe_raw', 'economic_pressure_ratio']:
        if metric in df.columns:
            min_val = df[metric].min()
            max_val = df[metric].max()
            if max_val > min_val:
                df[f'{metric}_minmax'] = (df[metric] - min_val) / (max_val - min_val)
            else:
                df[f'{metric}_minmax'] = 0.0
    
    return df


# ============================================================================
# 6. DATASETS ENRICHED
# ============================================================================

def generate_people_enriched(df):
    """
    Gera people_enriched.csv
    Contém todas as métricas individuais
    """
    cols_to_keep = [
        'person_id', 'age', 'gender', 'region_br', 'city_br', 'education_level',
        'job_category', 'employment_type', 'gross_salary_brl', 'net_salary_brl',
        'dependents', 'rent_status', 'receives_social_benefit',
        # Custos
        'total_household_cost', 'housing_cost', 'dependent_adjustment',
        # Benefícios
        'total_social_benefits',
        # Métricas principais
        'renda_disponivel_real',
        'economic_pressure_ratio',
        'epr_clean',  # EPR limpo para análises
        'cost_per_capita',
        'adjusted_min_wage',
        'dist_salario_minimo_ajustado',
        'subsistence_gap',
        'social_support_ratio',
        # Normalizações
        'renda_disponivel_real_zscore',
        'renda_disponivel_real_minmax',
        'economic_pressure_ratio_minmax'
    ]
    
    return df[[col for col in cols_to_keep if col in df.columns]]


def generate_household_costs_enriched(df):
    """
    Gera household_costs_enriched.csv
    Detalha composição de custos por pessoa
    """
    cols = [
        'person_id', 'city_br', 'dependents', 'rent_status',
        'housing_cost',
        'basic_food_cost',
        'transport_cost',
        'utilities_cost',
        'healthcare_cost',
        'dependent_adjustment',
        'total_household_cost',
        'cost_per_capita',
        'economic_pressure_ratio',
        'epr_clean'  # EPR limpo para análises
    ]
    
    return df[[col for col in cols if col in df.columns]]


def generate_cultural_access_enriched(df):
    """
    Gera cultural_access_enriched.csv
    """
    cols = [
        'person_id', 'country', 'city_br',
        'renda_disponivel_real',
        'streaming_cost', 'internet_cost', 'cinema_ticket',
        'cultural_events', 'music_subscription',
        'cultural_basic_cost',
        'iac_raw',
        'iac_raw_zscore',
        'iac_raw_minmax'
    ]
    
    return df[[col for col in cols if col in df.columns]]


def generate_opportunity_access_enriched(df):
    """
    Gera opportunity_access_enriched.csv
    """
    cols = [
        'person_id', 'country', 'city_br',
        'renda_disponivel_real',
        'technical_course', 'college_private', 'language_course',
        'emergency_savings_target', 'mobility_cost',
        'ioe_technical', 'ioe_college', 'ioe_language',
        'ioe_savings', 'ioe_mobility',
        'ioe_raw',
        'ioe_raw_zscore',
        'ioe_raw_minmax'
    ]
    
    return df[[col for col in cols if col in df.columns]]


# ============================================================================
# 7. COMPARAÇÃO CROSS-COUNTRY
# ============================================================================

def generate_cross_country_comparison(people_df, economic_df):
    """
    Simula a mesma família em diferentes países/cidades
    
    Cria perfis familiares típicos e calcula:
    - Family Purchasing Power Delta (FPPΔ)
    - Relative Family Power Gap (RFPG)
    - Per Capita Family Delta
    """
    
    # Perfis familiares típicos
    family_profiles = [
        {
            'profile_id': 'F1',
            'description': 'Casal sem filhos, classe média',
            'net_salary': 6000,
            'dependents': 0,
            'rent_status': 'aluguel'
        },
        {
            'profile_id': 'F2',
            'description': 'Família com 2 filhos, classe média',
            'net_salary': 8000,
            'dependents': 2,
            'rent_status': 'aluguel'
        },
        {
            'profile_id': 'F3',
            'description': 'Família com 3 filhos, classe média-baixa',
            'net_salary': 5000,
            'dependents': 3,
            'rent_status': 'aluguel'
        },
        {
            'profile_id': 'F4',
            'description': 'Profissional solteiro, classe média-alta',
            'net_salary': 10000,
            'dependents': 0,
            'rent_status': 'aluguel'
        },
    ]
    
    results = []
    
    for profile in family_profiles:
        for _, city_data in economic_df.iterrows():
            # Calcula custos para este perfil nesta cidade
            if profile['dependents'] == 0:
                housing_cost = city_data['avg_rent_single']
            else:
                housing_cost = city_data['avg_rent_family']
            
            if profile['rent_status'] in ['próprio', 'cedido']:
                housing_cost *= 0.5
            
            dependent_adjustment = profile['dependents'] * (
                city_data['basic_food_cost'] * 0.6 +
                city_data['utilities_cost'] * 0.3 +
                city_data['healthcare_cost'] * 0.4
            )
            
            total_cost = (
                housing_cost +
                city_data['basic_food_cost'] +
                city_data['transport_cost'] +
                city_data['utilities_cost'] +
                city_data['healthcare_cost'] +
                dependent_adjustment
            )
            
            # Ajusta salário pela taxa de câmbio (para comparação internacional)
            # Converte BRL para USD para comparação
            salary_adjusted = profile['net_salary'] / city_data['usd_rate']
            
            # RDR
            rdr = salary_adjusted - total_cost / city_data['usd_rate']
            
            results.append({
                'profile_id': profile['profile_id'],
                'description': profile['description'],
                'country': city_data['country'],
                'city': city_data['city'],
                'dependents': profile['dependents'],
                'net_salary_local': profile['net_salary'],
                'net_salary_usd': salary_adjusted,
                'total_household_cost_local': total_cost,
                'total_household_cost_usd': total_cost / city_data['usd_rate'],
                'renda_disponivel_real_usd': rdr,
                'per_capita_rdr': rdr / (profile['dependents'] + 1)
            })
    
    df_cross = pd.DataFrame(results)
    
    # Calcula deltas entre países para cada perfil
    comparisons = []
    
    for profile_id in df_cross['profile_id'].unique():
        profile_data = df_cross[df_cross['profile_id'] == profile_id].copy()
        
        # Compara cada cidade com todas as outras
        for i, row_a in profile_data.iterrows():
            for j, row_b in profile_data.iterrows():
                if i != j:
                    # Family Purchasing Power Delta
                    fpp_delta = row_b['renda_disponivel_real_usd'] - row_a['renda_disponivel_real_usd']
                    
                    # Relative Family Power Gap
                    if row_a['renda_disponivel_real_usd'] != 0:
                        rfpg = fpp_delta / abs(row_a['renda_disponivel_real_usd'])
                    else:
                        rfpg = np.nan
                    
                    # Per Capita Delta
                    pc_delta = fpp_delta / (row_a['dependents'] + 1)
                    
                    comparisons.append({
                        'profile_id': profile_id,
                        'from_country': row_a['country'],
                        'from_city': row_a['city'],
                        'to_country': row_b['country'],
                        'to_city': row_b['city'],
                        'fpp_delta_usd': fpp_delta,
                        'rfpg_percent': rfpg * 100 if not np.isnan(rfpg) else np.nan,
                        'pc_fpp_delta_usd': pc_delta
                    })
    
    df_comparisons = pd.DataFrame(comparisons)
    
    return df_cross, df_comparisons


# ============================================================================
# 8. PIPELINE PRINCIPAL
# ============================================================================

def main():
    """
    Executa todo o pipeline de enriquecimento
    """
    print("=" * 70)
    print("SILVER LAYER - FEATURE ENGINEERING")
    print("=" * 70)
    print()
    
    # 1. Carregamento
    print("📥 Carregando dados RAW...")
    people, economic, cultural, opportunity, social = load_raw_data()
    print(f"   ✓ {len(people):,} pessoas carregadas")
    print(f"   ✓ {len(economic)} contextos econômicos")
    print()
    
    # 2. Custos e Renda
    print("💰 Calculando custos e renda disponível...")
    df = calculate_household_costs(people, economic)
    print(f"   ✓ Total Household Cost calculado")
    print(f"   ✓ RDR médio: R$ {df['renda_disponivel_real'].mean():,.2f}")
    print()
    
    # 3. Métricas Econômicas
    print("📊 Calculando métricas econômicas...")
    df = calculate_economic_metrics(df)
    print(f"   ✓ EPR médio: {df['economic_pressure_ratio'].mean():.2f}")
    print(f"   ✓ Custo per capita médio: R$ {df['cost_per_capita'].mean():,.2f}")
    print()
    
    # 4. Acesso Cultural
    print("🎭 Calculando acesso cultural...")
    df = calculate_cultural_access(df, cultural)
    print(f"   ✓ IAC médio: {df['iac_raw'].mean():.2f}")
    print()
    
    # 5. Oportunidades Econômicas
    print("🎯 Calculando oportunidades econômicas...")
    df = calculate_opportunity_access(df, opportunity)
    print(f"   ✓ IOE médio: {df['ioe_raw'].mean():.2f}")
    print()
    
    # 6. Normalização
    print("📐 Aplicando normalizações...")
    df = normalize_metrics(df)
    print(f"   ✓ Z-scores calculados por país")
    print(f"   ✓ Min-Max aplicado para dashboard")
    print()
    
    # 7. Gerar outputs
    print("💾 Gerando datasets enriched...")
    
    people_enriched = generate_people_enriched(df)
    people_enriched.to_csv(ENRICHED_DIR / "people_enriched.csv", index=False)
    print(f"   ✓ people_enriched.csv ({len(people_enriched):,} linhas)")
    
    household_enriched = generate_household_costs_enriched(df)
    household_enriched.to_csv(ENRICHED_DIR / "household_costs_enriched.csv", index=False)
    print(f"   ✓ household_costs_enriched.csv ({len(household_enriched):,} linhas)")
    
    cultural_enriched = generate_cultural_access_enriched(df)
    cultural_enriched.to_csv(ENRICHED_DIR / "cultural_access_enriched.csv", index=False)
    print(f"   ✓ cultural_access_enriched.csv ({len(cultural_enriched):,} linhas)")
    
    opportunity_enriched = generate_opportunity_access_enriched(df)
    opportunity_enriched.to_csv(ENRICHED_DIR / "opportunity_access_enriched.csv", index=False)
    print(f"   ✓ opportunity_access_enriched.csv ({len(opportunity_enriched):,} linhas)")
    
    # 8. Comparação cross-country
    print()
    print("🌍 Gerando comparações cross-country...")
    df_cross, df_comparisons = generate_cross_country_comparison(people, economic)
    df_cross.to_csv(ENRICHED_DIR / "cross_country_family_simulation.csv", index=False)
    df_comparisons.to_csv(ENRICHED_DIR / "cross_country_family_comparison.csv", index=False)
    print(f"   ✓ cross_country_family_simulation.csv ({len(df_cross):,} linhas)")
    print(f"   ✓ cross_country_family_comparison.csv ({len(df_comparisons):,} linhas)")
    
    print()
    print("=" * 70)
    print("✅ CAMADA SILVER CONCLUÍDA")
    print("=" * 70)
    print()
    print("📁 Arquivos gerados em: enriched/")
    print()
    print("Próximos passos:")
    print("  1. EDA avançada nos dados enriched")
    print("  2. Validação de métricas")
    print("  3. Camada GOLD (decisões e rankings)")
    print()


if __name__ == "__main__":
    main()
