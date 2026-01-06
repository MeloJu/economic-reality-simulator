
import pandas as pd
import numpy as np
from pathlib import Path

ENRICHED_DIR = Path("enriched")

def load_enriched_data():
    """Carrega todos os datasets enriched"""
    people = pd.read_csv(ENRICHED_DIR / "people_enriched.csv")
    household = pd.read_csv(ENRICHED_DIR / "household_costs_enriched.csv")
    cultural = pd.read_csv(ENRICHED_DIR / "cultural_access_enriched.csv")
    opportunity = pd.read_csv(ENRICHED_DIR / "opportunity_access_enriched.csv")
    cross_country = pd.read_csv(ENRICHED_DIR / "cross_country_family_comparison.csv")
    
    return people, household, cultural, opportunity, cross_country


def validate_people_enriched(df):
    """Valida people_enriched.csv"""
    print("=" * 70)
    print("VALIDAÇÃO: people_enriched.csv")
    print("=" * 70)
    
    # 1. Completude
    print("\n📊 COMPLETUDE DOS DADOS")
    print("-" * 70)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        'Missing': missing[missing > 0],
        'Percent': missing_pct[missing > 0]
    })
    if len(missing_df) > 0:
        print(missing_df)
    else:
        print("✅ Nenhum valor faltante")
    
    # 2. Distribuições
    print("\n📈 DISTRIBUIÇÕES")
    print("-" * 70)
    
    metrics = [
        'renda_disponivel_real',
        'economic_pressure_ratio',
        'dist_salario_minimo_ajustado'
    ]
    
    for metric in metrics:
        if metric in df.columns:
            print(f"\n{metric}:")
            print(f"  Média: {df[metric].mean():,.2f}")
            print(f"  Mediana: {df[metric].median():,.2f}")
            print(f"  Std Dev: {df[metric].std():,.2f}")
            print(f"  Min: {df[metric].min():,.2f}")
            print(f"  Max: {df[metric].max():,.2f}")
            
            # Percentis
            p25, p75 = df[metric].quantile([0.25, 0.75])
            print(f"  Q1 (25%): {p25:,.2f}")
            print(f"  Q3 (75%): {p75:,.2f}")
    
    # 3. Sanity Checks
    print("\n🔍 SANITY CHECKS")
    print("-" * 70)
    
    # EPR não pode ser negativo
    if 'economic_pressure_ratio' in df.columns:
        negative_epr = (df['economic_pressure_ratio'] < 0).sum()
        print(f"EPR negativos: {negative_epr} ({negative_epr/len(df)*100:.2f}%)")
        if negative_epr > 0:
            print("  ⚠️  EPR não deveria ser negativo")
    
    # Salário vs Custo
    if 'net_salary_brl' in df.columns and 'total_household_cost' in df.columns:
        deficit = (df['net_salary_brl'] < df['total_household_cost']).sum()
        print(f"Pessoas com déficit (custo > renda): {deficit} ({deficit/len(df)*100:.2f}%)")
    
    # RDR
    if 'renda_disponivel_real' in df.columns:
        negative_rdr = (df['renda_disponivel_real'] < 0).sum()
        print(f"RDR negativo: {negative_rdr} ({negative_rdr/len(df)*100:.2f}%)")
        print(f"RDR positivo: {(df['renda_disponivel_real'] > 0).sum()} ({(df['renda_disponivel_real'] > 0).sum()/len(df)*100:.2f}%)")
    
    # 4. Correlações
    print("\n🔗 CORRELAÇÕES PRINCIPAIS")
    print("-" * 70)
    
    corr_vars = [
        'net_salary_brl',
        'total_household_cost',
        'renda_disponivel_real',
        'economic_pressure_ratio'
    ]
    
    available_vars = [v for v in corr_vars if v in df.columns]
    if len(available_vars) >= 2:
        corr_matrix = df[available_vars].corr()
        print(corr_matrix.round(3))


def validate_household_costs(df):
    """Valida household_costs_enriched.csv"""
    print("\n\n")
    print("=" * 70)
    print("VALIDAÇÃO: household_costs_enriched.csv")
    print("=" * 70)
    
    # Composição média de custos
    print("\n💰 COMPOSIÇÃO MÉDIA DE CUSTOS")
    print("-" * 70)
    
    cost_cols = [
        'housing_cost',
        'basic_food_cost',
        'transport_cost',
        'utilities_cost',
        'healthcare_cost',
        'dependent_adjustment'
    ]
    
    available_costs = [c for c in cost_cols if c in df.columns]
    
    total_avg = df['total_household_cost'].mean() if 'total_household_cost' in df.columns else 0
    
    for cost in available_costs:
        avg = df[cost].mean()
        pct = (avg / total_avg * 100) if total_avg > 0 else 0
        print(f"{cost:25s}: R$ {avg:8,.2f} ({pct:5.2f}%)")
    
    if 'total_household_cost' in df.columns:
        print(f"{'TOTAL':25s}: R$ {total_avg:8,.2f}")
    
    # Por dependentes
    if 'dependents' in df.columns and 'total_household_cost' in df.columns:
        print("\n📊 CUSTO POR NÚMERO DE DEPENDENTES")
        print("-" * 70)
        by_deps = df.groupby('dependents')['total_household_cost'].agg(['count', 'mean', 'median'])
        print(by_deps)


def validate_cultural_access(df):
    """Valida cultural_access_enriched.csv"""
    print("\n\n")
    print("=" * 70)
    print("VALIDAÇÃO: cultural_access_enriched.csv")
    print("=" * 70)
    
    if 'iac_raw' in df.columns:
        print("\n🎭 ÍNDICE DE ACESSO CULTURAL (IAC)")
        print("-" * 70)
        
        # Distribuição
        print(f"Média: {df['iac_raw'].mean():.2f}")
        print(f"Mediana: {df['iac_raw'].median():.2f}")
        print(f"Min: {df['iac_raw'].min():.2f}")
        print(f"Max: {df['iac_raw'].max():.2f}")
        
        # Categorias
        print("\nCategorias de acesso:")
        high = (df['iac_raw'] > 10).sum()
        medium = ((df['iac_raw'] >= 3) & (df['iac_raw'] <= 10)).sum()
        low = (df['iac_raw'] < 3).sum()
        
        print(f"  Alto (>10):     {high:6,} ({high/len(df)*100:5.2f}%)")
        print(f"  Médio (3-10):   {medium:6,} ({medium/len(df)*100:5.2f}%)")
        print(f"  Baixo (<3):     {low:6,} ({low/len(df)*100:5.2f}%)")


def validate_opportunity_access(df):
    """Valida opportunity_access_enriched.csv"""
    print("\n\n")
    print("=" * 70)
    print("VALIDAÇÃO: opportunity_access_enriched.csv")
    print("=" * 70)
    
    if 'ioe_raw' in df.columns:
        print("\n🎯 ÍNDICE DE OPORTUNIDADES ECONÔMICAS (IOE)")
        print("-" * 70)
        
        print(f"Média: {df['ioe_raw'].mean():.2f}")
        print(f"Mediana: {df['ioe_raw'].median():.2f}")
        print(f"Min: {df['ioe_raw'].min():.2f}")
        print(f"Max: {df['ioe_raw'].max():.2f}")
        
        # Componentes
        print("\nComponentes médios:")
        components = [
            'ioe_technical',
            'ioe_college',
            'ioe_language',
            'ioe_savings',
            'ioe_mobility'
        ]
        
        for comp in components:
            if comp in df.columns:
                print(f"  {comp:20s}: {df[comp].mean():6.2f}")


def validate_cross_country(df):
    """Valida cross_country_family_comparison.csv"""
    print("\n\n")
    print("=" * 70)
    print("VALIDAÇÃO: cross_country_family_comparison.csv")
    print("=" * 70)
    
    # Top 10 melhores mudanças
    print("\n🌍 TOP 10 MELHORES MUDANÇAS (maior ganho em USD)")
    print("-" * 70)
    top_gains = df.nlargest(10, 'fpp_delta_usd')[
        ['profile_id', 'from_city', 'to_city', 'fpp_delta_usd', 'rfpg_percent']
    ]
    print(top_gains.to_string(index=False))
    
    # Top 10 piores mudanças
    print("\n🌍 TOP 10 PIORES MUDANÇAS (maior perda em USD)")
    print("-" * 70)
    top_losses = df.nsmallest(10, 'fpp_delta_usd')[
        ['profile_id', 'from_city', 'to_city', 'fpp_delta_usd', 'rfpg_percent']
    ]
    print(top_losses.to_string(index=False))
    
    # Por perfil
    print("\n📊 ESTATÍSTICAS POR PERFIL FAMILIAR")
    print("-" * 70)
    by_profile = df.groupby('profile_id')['fpp_delta_usd'].agg(['mean', 'std', 'min', 'max'])
    print(by_profile)


def main():
    """Executa todas as validações"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "VALIDAÇÃO DA CAMADA SILVER" + " " * 27 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Carregar dados
    print("📥 Carregando datasets...")
    people, household, cultural, opportunity, cross_country = load_enriched_data()
    print(f"   ✓ {len(people):,} pessoas")
    print(f"   ✓ {len(cross_country):,} comparações cross-country")
    
    # Validações
    validate_people_enriched(people)
    validate_household_costs(household)
    validate_cultural_access(cultural)
    validate_opportunity_access(opportunity)
    validate_cross_country(cross_country)
    
    # Resumo
    print("\n\n")
    print("=" * 70)
    print("✅ VALIDAÇÃO CONCLUÍDA")
    print("=" * 70)
    print("\n📝 Próximos passos:")
    print("  1. Revisar outliers identificados")
    print("  2. Verificar valores inesperados")
    print("  3. Prosseguir para EDA detalhada")
    print()


if __name__ == "__main__":
    main()
