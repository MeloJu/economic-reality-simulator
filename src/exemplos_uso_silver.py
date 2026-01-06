"""
Exemplos de Uso — Camada SILVER
=================================
Demonstra como usar os dados enriched para análises
"""

import pandas as pd
import numpy as np
from pathlib import Path


ENRICHED_DIR = Path("enriched")


def exemplo_1_analise_regional():
    """
    Exemplo 1: Análise Regional do Brasil
    Compara métricas entre regiões
    """
    print("=" * 70)
    print("EXEMPLO 1: ANÁLISE REGIONAL")
    print("=" * 70)
    print()
    
    # Carregar dados
    df = pd.read_csv(ENRICHED_DIR / "people_enriched.csv")
    
    # Agrupar por região
    regional = df.groupby('region_br').agg({
        'renda_disponivel_real': ['mean', 'median', 'std'],
        'economic_pressure_ratio': 'median',
        'cost_per_capita': 'mean',
        'person_id': 'count'
    }).round(2)
    
    regional.columns = ['RDR_Média', 'RDR_Mediana', 'RDR_StdDev', 'EPR_Mediana', 'Custo_PC', 'N']
    
    print("Métricas por Região:")
    print(regional)
    print()
    
    # Região com melhor situação
    best_region = regional['RDR_Média'].idxmax()
    print(f"✅ Melhor região (maior RDR médio): {best_region}")
    print(f"   RDR: R$ {regional.loc[best_region, 'RDR_Média']:,.2f}")
    print()


def exemplo_2_impacto_educacao():
    """
    Exemplo 2: Impacto da Educação
    Analisa como educação afeta oportunidades
    """
    print("=" * 70)
    print("EXEMPLO 2: IMPACTO DA EDUCAÇÃO NAS OPORTUNIDADES")
    print("=" * 70)
    print()
    
    # Carregar dados
    df = pd.read_csv(ENRICHED_DIR / "opportunity_access_enriched.csv")
    people = pd.read_csv(ENRICHED_DIR / "people_enriched.csv")
    
    # Merge para ter educação
    df = df.merge(people[['person_id', 'education_level']], on='person_id')
    
    # Agrupar por educação
    by_edu = df.groupby('education_level').agg({
        'ioe_raw': ['mean', 'median'],
        'person_id': 'count'
    }).round(2)
    
    by_edu.columns = ['IOE_Média', 'IOE_Mediana', 'N']
    
    # Ordenar por IOE médio
    by_edu = by_edu.sort_values('IOE_Média', ascending=False)
    
    print("Índice de Oportunidades Econômicas por Nível de Educação:")
    print(by_edu)
    print()
    
    # Calcular gap entre superior e sem ensino médio
    if 'superior' in by_edu.index and 'sem ensino médio' in by_edu.index:
        gap = by_edu.loc['superior', 'IOE_Média'] - by_edu.loc['sem ensino médio', 'IOE_Média']
        print(f"📊 Gap entre superior e sem ensino médio: {gap:.2f} pontos de IOE")
        print()


def exemplo_3_perfil_vulneravel():
    """
    Exemplo 3: Identificar Perfil Mais Vulnerável
    Combina múltiplas métricas
    """
    print("=" * 70)
    print("EXEMPLO 3: PERFIL DE MAIOR VULNERABILIDADE")
    print("=" * 70)
    print()
    
    # Carregar dados
    df = pd.read_csv(ENRICHED_DIR / "people_enriched.csv")
    
    # Filtrar pessoas vulneráveis (múltiplos critérios)
    vulnerable = df[
        (df['renda_disponivel_real'] < 0) &  # RDR negativo
        (df['economic_pressure_ratio'] > 1.5) &  # Alta pressão
        (df['dependents'] >= 2)  # Tem dependentes
    ]
    
    print(f"Total de pessoas vulneráveis: {len(vulnerable):,} ({len(vulnerable)/len(df)*100:.1f}%)")
    print()
    
    if len(vulnerable) > 0:
        # Perfil típico
        print("Características do grupo vulnerável:")
        print(f"  Idade média: {vulnerable['age'].mean():.1f} anos")
        print(f"  Salário médio: R$ {vulnerable['net_salary_brl'].mean():,.2f}")
        print(f"  Custo médio: R$ {vulnerable['total_household_cost'].mean():,.2f}")
        print(f"  RDR médio: R$ {vulnerable['renda_disponivel_real'].mean():,.2f}")
        print(f"  Dependentes médios: {vulnerable['dependents'].mean():.1f}")
        print()
        
        # Educação
        print("Nível de educação:")
        edu_dist = vulnerable['education_level'].value_counts()
        for edu, count in edu_dist.head().items():
            print(f"  {edu}: {count:,} ({count/len(vulnerable)*100:.1f}%)")
        print()
        
        # Região
        print("Região:")
        region_dist = vulnerable['region_br'].value_counts()
        for region, count in region_dist.items():
            print(f"  {region}: {count:,} ({count/len(vulnerable)*100:.1f}%)")
        print()


def exemplo_4_melhor_cidade_para_migracao():
    """
    Exemplo 4: Melhor Cidade para Migração
    Usa comparação cross-country
    """
    print("=" * 70)
    print("EXEMPLO 4: MELHORES CIDADES PARA MIGRAÇÃO")
    print("=" * 70)
    print()
    
    # Carregar comparações
    df = pd.read_csv(ENRICHED_DIR / "cross_country_family_comparison.csv")
    
    # Filtrar apenas saindo do Brasil
    from_brazil = df[df['from_country'] == 'Brazil'].copy()
    
    # Para cada perfil, encontrar melhor destino
    for profile in ['F1', 'F2', 'F3', 'F4']:
        profile_data = from_brazil[from_brazil['profile_id'] == profile]
        
        # Melhor cidade (maior ganho médio saindo de qualquer cidade BR)
        best_by_city = profile_data.groupby('to_city').agg({
            'fpp_delta_usd': 'mean',
            'rfpg_percent': 'mean'
        }).sort_values('fpp_delta_usd', ascending=False)
        
        if len(best_by_city) > 0:
            best_city = best_by_city.index[0]
            best_gain = best_by_city.loc[best_city, 'fpp_delta_usd']
            best_pct = best_by_city.loc[best_city, 'rfpg_percent']
            
            print(f"Perfil {profile}:")
            print(f"  ✅ Melhor destino: {best_city}")
            print(f"     Ganho médio: ${best_gain:,.2f} USD")
            print(f"     Aumento: {best_pct:.1f}%")
            print()


def exemplo_5_acesso_cultural_por_cidade():
    """
    Exemplo 5: Ranking de Acesso Cultural
    """
    print("=" * 70)
    print("EXEMPLO 5: ANÁLISE DE ACESSO CULTURAL")
    print("=" * 70)
    print()
    
    # Carregar dados
    df = pd.read_csv(ENRICHED_DIR / "cultural_access_enriched.csv")
    
    # Estatísticas gerais
    print("Distribuição de Acesso Cultural (IAC):")
    print(f"  Média: {df['iac_raw'].mean():.2f}")
    print(f"  Mediana: {df['iac_raw'].median():.2f}")
    print()
    
    # Filtrar apenas IAC positivo
    df_positive = df[df['iac_raw'] > 0]
    
    print(f"Pessoas com IAC positivo: {len(df_positive):,} ({len(df_positive)/len(df)*100:.1f}%)")
    print()
    
    # Top 10 pessoas com melhor acesso
    top_10 = df_positive.nlargest(10, 'iac_raw')[['person_id', 'iac_raw', 'renda_disponivel_real', 'cultural_basic_cost']]
    print("Top 10 Indivíduos com Melhor Acesso Cultural:")
    print(top_10.to_string(index=False))
    print()


def exemplo_6_correlacao_avancada():
    """
    Exemplo 6: Análise de Correlação
    Identifica fatores que mais impactam RDR
    """
    print("=" * 70)
    print("EXEMPLO 6: FATORES QUE MAIS IMPACTAM A RENDA DISPONÍVEL")
    print("=" * 70)
    print()
    
    # Carregar dados
    df = pd.read_csv(ENRICHED_DIR / "people_enriched.csv")
    
    # Variáveis de interesse
    vars_of_interest = [
        'net_salary_brl',
        'dependents',
        'total_household_cost',
        'housing_cost',
        'economic_pressure_ratio',
        'renda_disponivel_real'
    ]
    
    # Correlação com RDR
    correlations = df[vars_of_interest].corr()['renda_disponivel_real'].sort_values(ascending=False)
    
    print("Correlação com Renda Disponível Real:")
    for var, corr in correlations.items():
        if var != 'renda_disponivel_real':
            print(f"  {var:30s}: {corr:6.3f}")
    print()


def main():
    """
    Executa todos os exemplos
    """
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "EXEMPLOS DE USO" + " " * 33 + "║")
    print("║" + " " * 22 + "CAMADA SILVER" + " " * 33 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")
    
    exemplo_1_analise_regional()
    print("\n")
    
    exemplo_2_impacto_educacao()
    print("\n")
    
    exemplo_3_perfil_vulneravel()
    print("\n")
    
    exemplo_4_melhor_cidade_para_migracao()
    print("\n")
    
    exemplo_5_acesso_cultural_por_cidade()
    print("\n")
    
    exemplo_6_correlacao_avancada()
    
    print("\n")
    print("=" * 70)
    print("✅ TODOS OS EXEMPLOS EXECUTADOS")
    print("=" * 70)
    print("\n📝 Estes exemplos demonstram como usar os dados enriched")
    print("   para análises reais. Adapte-os para suas necessidades!")
    print()


if __name__ == "__main__":
    main()
