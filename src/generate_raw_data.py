"""
Gerador de dados sintéticos realistas para camada RAW
Pipeline de análise socioeconômica internacional
"""

import pandas as pd
import numpy as np
from uuid import uuid4
from datetime import datetime

# Seed para reprodutibilidade
np.random.seed(42)

print("🚀 Iniciando geração de dados RAW...")

# ============================================================================
# ARQUIVO 1: people_raw.csv (10.000 registros)
# ============================================================================

print("\n📊 Gerando people_raw.csv...")

n_people = 10000

# Distribuições realistas baseadas em dados do IBGE/PNAD
regions = ['SE', 'NE', 'S', 'N', 'CO']
region_weights = [0.42, 0.27, 0.14, 0.09, 0.08]  # Distribuição populacional aproximada

cities_by_region = {
    'SE': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Vitória', 'Campinas'],
    'NE': ['Salvador', 'Fortaleza', 'Recife', 'Natal', 'São Luís'],
    'S': ['Curitiba', 'Porto Alegre', 'Florianópolis', 'Joinville', 'Londrina'],
    'N': ['Manaus', 'Belém', 'Porto Velho', 'Rio Branco', 'Macapá'],
    'CO': ['Brasília', 'Goiânia', 'Campo Grande', 'Cuiabá', 'Palmas']
}

education_levels = ['sem ensino médio', 'médio', 'técnico', 'superior', 'pós']
education_weights = [0.28, 0.35, 0.12, 0.18, 0.07]  # Aproximado PNAD

job_categories = ['serviços', 'indústria', 'tecnologia', 'comércio', 'informal', 'desempregado']
job_weights = [0.28, 0.15, 0.08, 0.20, 0.18, 0.11]

employment_types = ['CLT', 'PJ', 'informal', 'desempregado']

rent_statuses = ['aluguel', 'próprio', 'cedido']
rent_weights = [0.35, 0.50, 0.15]

# Gerando dados
people_data = []

for i in range(n_people):
    person_id = str(uuid4())
    age = np.random.randint(18, 66)
    gender = np.random.choice(['M', 'F'])
    region_br = np.random.choice(regions, p=region_weights)
    city_br = np.random.choice(cities_by_region[region_br])
    
    # Educação (mais jovens tendem a ter mais educação)
    if age < 30:
        edu_weights_adj = [0.20, 0.35, 0.15, 0.22, 0.08]
    elif age < 45:
        edu_weights_adj = [0.28, 0.35, 0.12, 0.18, 0.07]
    else:
        edu_weights_adj = [0.38, 0.32, 0.10, 0.15, 0.05]
    
    education_level = np.random.choice(education_levels, p=edu_weights_adj)
    
    # Job category (influenciado por educação)
    if education_level == 'pós':
        job_category = np.random.choice(['tecnologia', 'serviços', 'indústria'], p=[0.5, 0.4, 0.1])
    elif education_level == 'superior':
        job_category = np.random.choice(['tecnologia', 'serviços', 'comércio', 'indústria'], p=[0.3, 0.4, 0.2, 0.1])
    elif education_level == 'técnico':
        job_category = np.random.choice(['indústria', 'tecnologia', 'serviços', 'comércio'], p=[0.35, 0.25, 0.25, 0.15])
    elif education_level == 'médio':
        job_category = np.random.choice(['comércio', 'serviços', 'informal', 'desempregado'], p=[0.35, 0.30, 0.20, 0.15])
    else:
        job_category = np.random.choice(['informal', 'desempregado', 'serviços', 'comércio'], p=[0.40, 0.25, 0.20, 0.15])
    
    # Employment type
    if job_category == 'desempregado':
        employment_type = 'desempregado'
    elif job_category == 'informal':
        employment_type = 'informal'
    elif job_category == 'tecnologia':
        employment_type = np.random.choice(['CLT', 'PJ'], p=[0.4, 0.6])
    else:
        employment_type = np.random.choice(['CLT', 'PJ', 'informal'], p=[0.6, 0.25, 0.15])
    
    # Salário (distribuição log-normal realista)
    base_salary = 1412  # Salário mínimo 2024
    
    if job_category == 'desempregado':
        gross_salary_brl = 0
    else:
        # Multiplicadores por educação
        edu_multipliers = {
            'sem ensino médio': np.random.lognormal(0.2, 0.4),
            'médio': np.random.lognormal(0.5, 0.5),
            'técnico': np.random.lognormal(1.0, 0.6),
            'superior': np.random.lognormal(1.5, 0.7),
            'pós': np.random.lognormal(2.0, 0.8)
        }
        
        # Multiplicadores por categoria
        job_multipliers = {
            'informal': 0.7,
            'serviços': 1.0,
            'comércio': 0.9,
            'indústria': 1.2,
            'tecnologia': 2.5
        }
        
        # Multiplicador regional
        region_multipliers = {
            'SE': 1.3,
            'S': 1.2,
            'CO': 1.15,
            'NE': 0.85,
            'N': 0.9
        }
        
        gross_salary_brl = (
            base_salary * 
            edu_multipliers[education_level] * 
            job_multipliers[job_category] * 
            region_multipliers[region_br]
        )
        
        # Arredondamento realista
        gross_salary_brl = round(gross_salary_brl / 100) * 100
    
    # Net salary (descontos de INSS + IR simplificados)
    if gross_salary_brl == 0:
        net_salary_brl = 0
    elif gross_salary_brl <= 2000:
        net_salary_brl = gross_salary_brl * 0.92  # ~8% INSS
    elif gross_salary_brl <= 4000:
        net_salary_brl = gross_salary_brl * 0.86  # ~14% INSS + IR
    elif gross_salary_brl <= 8000:
        net_salary_brl = gross_salary_brl * 0.80  # ~20% total
    else:
        net_salary_brl = gross_salary_brl * 0.72  # ~28% total
    
    net_salary_brl = round(net_salary_brl, 2)
    
    # Dependentes (mais provável em pessoas mais velhas)
    if age < 25:
        dependents = np.random.choice([0, 1], p=[0.85, 0.15])
    elif age < 35:
        dependents = np.random.choice([0, 1, 2], p=[0.50, 0.35, 0.15])
    elif age < 50:
        dependents = np.random.choice([0, 1, 2, 3], p=[0.30, 0.30, 0.30, 0.10])
    else:
        dependents = np.random.choice([0, 1, 2], p=[0.60, 0.25, 0.15])
    
    # Rent status
    rent_status = np.random.choice(rent_statuses, p=rent_weights)
    
    # Benefício social (renda baixa tem mais chance)
    if net_salary_brl == 0:
        receives_social_benefit = np.random.choice([True, False], p=[0.7, 0.3])
    elif net_salary_brl <= 2000:
        receives_social_benefit = np.random.choice([True, False], p=[0.4, 0.6])
    elif net_salary_brl <= 3000:
        receives_social_benefit = np.random.choice([True, False], p=[0.15, 0.85])
    else:
        receives_social_benefit = False
    
    people_data.append({
        'person_id': person_id,
        'age': age,
        'gender': gender,
        'region_br': region_br,
        'city_br': city_br,
        'education_level': education_level,
        'job_category': job_category,
        'employment_type': employment_type,
        'gross_salary_brl': gross_salary_brl,
        'net_salary_brl': net_salary_brl,
        'dependents': dependents,
        'rent_status': rent_status,
        'receives_social_benefit': receives_social_benefit
    })

df_people = pd.DataFrame(people_data)
df_people.to_csv('people_raw.csv', index=False, encoding='utf-8')
print(f"✅ people_raw.csv gerado: {len(df_people)} registros")

# ============================================================================
# ARQUIVO 2: economic_context_raw.csv
# ============================================================================

print("\n🌍 Gerando economic_context_raw.csv...")

economic_context_data = [
    # Brasil - principais cidades
    {
        'country': 'Brazil', 'city': 'São Paulo', 'currency': 'BRL',
        'usd_rate': 5.00, 'eur_rate': 5.40,
        'local_min_wage': 1412, 'avg_rent_single': 1800, 'avg_rent_family': 3200,
        'basic_food_cost': 800, 'transport_cost': 250, 'utilities_cost': 300,
        'healthcare_cost': 200, 'effective_tax_rate': 0.27
    },
    {
        'country': 'Brazil', 'city': 'Rio de Janeiro', 'currency': 'BRL',
        'usd_rate': 5.00, 'eur_rate': 5.40,
        'local_min_wage': 1412, 'avg_rent_single': 1600, 'avg_rent_family': 3000,
        'basic_food_cost': 750, 'transport_cost': 230, 'utilities_cost': 350,
        'healthcare_cost': 180, 'effective_tax_rate': 0.27
    },
    {
        'country': 'Brazil', 'city': 'Belo Horizonte', 'currency': 'BRL',
        'usd_rate': 5.00, 'eur_rate': 5.40,
        'local_min_wage': 1412, 'avg_rent_single': 1200, 'avg_rent_family': 2200,
        'basic_food_cost': 650, 'transport_cost': 200, 'utilities_cost': 280,
        'healthcare_cost': 150, 'effective_tax_rate': 0.27
    },
    {
        'country': 'Brazil', 'city': 'Salvador', 'currency': 'BRL',
        'usd_rate': 5.00, 'eur_rate': 5.40,
        'local_min_wage': 1412, 'avg_rent_single': 1000, 'avg_rent_family': 1800,
        'basic_food_cost': 600, 'transport_cost': 180, 'utilities_cost': 250,
        'healthcare_cost': 120, 'effective_tax_rate': 0.27
    },
    {
        'country': 'Brazil', 'city': 'Curitiba', 'currency': 'BRL',
        'usd_rate': 5.00, 'eur_rate': 5.40,
        'local_min_wage': 1412, 'avg_rent_single': 1300, 'avg_rent_family': 2400,
        'basic_food_cost': 680, 'transport_cost': 210, 'utilities_cost': 320,
        'healthcare_cost': 160, 'effective_tax_rate': 0.27
    },
    
    # EUA - principais cidades
    {
        'country': 'USA', 'city': 'New York', 'currency': 'USD',
        'usd_rate': 1.00, 'eur_rate': 1.08,
        'local_min_wage': 2900, 'avg_rent_single': 2800, 'avg_rent_family': 4200,
        'basic_food_cost': 600, 'transport_cost': 150, 'utilities_cost': 200,
        'healthcare_cost': 450, 'effective_tax_rate': 0.35
    },
    {
        'country': 'USA', 'city': 'San Francisco', 'currency': 'USD',
        'usd_rate': 1.00, 'eur_rate': 1.08,
        'local_min_wage': 3200, 'avg_rent_single': 3200, 'avg_rent_family': 5000,
        'basic_food_cost': 650, 'transport_cost': 180, 'utilities_cost': 180,
        'healthcare_cost': 480, 'effective_tax_rate': 0.37
    },
    {
        'country': 'USA', 'city': 'Austin', 'currency': 'USD',
        'usd_rate': 1.00, 'eur_rate': 1.08,
        'local_min_wage': 2500, 'avg_rent_single': 1800, 'avg_rent_family': 3000,
        'basic_food_cost': 550, 'transport_cost': 200, 'utilities_cost': 160,
        'healthcare_cost': 420, 'effective_tax_rate': 0.32
    },
    {
        'country': 'USA', 'city': 'Miami', 'currency': 'USD',
        'usd_rate': 1.00, 'eur_rate': 1.08,
        'local_min_wage': 2600, 'avg_rent_single': 2200, 'avg_rent_family': 3600,
        'basic_food_cost': 580, 'transport_cost': 180, 'utilities_cost': 190,
        'healthcare_cost': 440, 'effective_tax_rate': 0.30
    },
    
    # Alemanha - principais cidades
    {
        'country': 'Germany', 'city': 'Berlin', 'currency': 'EUR',
        'usd_rate': 0.93, 'eur_rate': 1.00,
        'local_min_wage': 2100, 'avg_rent_single': 1200, 'avg_rent_family': 2200,
        'basic_food_cost': 400, 'transport_cost': 80, 'utilities_cost': 250,
        'healthcare_cost': 300, 'effective_tax_rate': 0.40
    },
    {
        'country': 'Germany', 'city': 'Munich', 'currency': 'EUR',
        'usd_rate': 0.93, 'eur_rate': 1.00,
        'local_min_wage': 2100, 'avg_rent_single': 1600, 'avg_rent_family': 2800,
        'basic_food_cost': 450, 'transport_cost': 90, 'utilities_cost': 270,
        'healthcare_cost': 320, 'effective_tax_rate': 0.42
    },
    {
        'country': 'Germany', 'city': 'Frankfurt', 'currency': 'EUR',
        'usd_rate': 0.93, 'eur_rate': 1.00,
        'local_min_wage': 2100, 'avg_rent_single': 1400, 'avg_rent_family': 2500,
        'basic_food_cost': 420, 'transport_cost': 85, 'utilities_cost': 260,
        'healthcare_cost': 310, 'effective_tax_rate': 0.41
    },
    
    # França - principais cidades
    {
        'country': 'France', 'city': 'Paris', 'currency': 'EUR',
        'usd_rate': 0.93, 'eur_rate': 1.00,
        'local_min_wage': 1800, 'avg_rent_single': 1400, 'avg_rent_family': 2600,
        'basic_food_cost': 450, 'transport_cost': 75, 'utilities_cost': 180,
        'healthcare_cost': 250, 'effective_tax_rate': 0.43
    },
    {
        'country': 'France', 'city': 'Lyon', 'currency': 'EUR',
        'usd_rate': 0.93, 'eur_rate': 1.00,
        'local_min_wage': 1800, 'avg_rent_single': 900, 'avg_rent_family': 1800,
        'basic_food_cost': 400, 'transport_cost': 65, 'utilities_cost': 160,
        'healthcare_cost': 230, 'effective_tax_rate': 0.43
    },
    {
        'country': 'France', 'city': 'Marseille', 'currency': 'EUR',
        'usd_rate': 0.93, 'eur_rate': 1.00,
        'local_min_wage': 1800, 'avg_rent_single': 850, 'avg_rent_family': 1650,
        'basic_food_cost': 380, 'transport_cost': 60, 'utilities_cost': 150,
        'healthcare_cost': 220, 'effective_tax_rate': 0.43
    },
    
    # Portugal - principais cidades
    {
        'country': 'Portugal', 'city': 'Lisbon', 'currency': 'EUR',
        'usd_rate': 0.93, 'eur_rate': 1.00,
        'local_min_wage': 820, 'avg_rent_single': 900, 'avg_rent_family': 1600,
        'basic_food_cost': 300, 'transport_cost': 50, 'utilities_cost': 120,
        'healthcare_cost': 150, 'effective_tax_rate': 0.35
    },
    {
        'country': 'Portugal', 'city': 'Porto', 'currency': 'EUR',
        'usd_rate': 0.93, 'eur_rate': 1.00,
        'local_min_wage': 820, 'avg_rent_single': 700, 'avg_rent_family': 1300,
        'basic_food_cost': 280, 'transport_cost': 45, 'utilities_cost': 110,
        'healthcare_cost': 140, 'effective_tax_rate': 0.35
    },
    {
        'country': 'Portugal', 'city': 'Faro', 'currency': 'EUR',
        'usd_rate': 0.93, 'eur_rate': 1.00,
        'local_min_wage': 820, 'avg_rent_single': 650, 'avg_rent_family': 1200,
        'basic_food_cost': 270, 'transport_cost': 40, 'utilities_cost': 100,
        'healthcare_cost': 130, 'effective_tax_rate': 0.35
    }
]

df_economic_context = pd.DataFrame(economic_context_data)
df_economic_context.to_csv('economic_context_raw.csv', index=False, encoding='utf-8')
print(f"✅ economic_context_raw.csv gerado: {len(df_economic_context)} registros")

# ============================================================================
# ARQUIVO 3: cultural_costs_raw.csv
# ============================================================================

print("\n🎭 Gerando cultural_costs_raw.csv...")

cultural_costs_data = [
    {
        'country': 'Brazil',
        'streaming_cost': 45.0,  # Netflix + Spotify
        'internet_cost': 100.0,
        'cinema_ticket': 35.0,
        'cultural_events': 80.0,  # média mensal
        'music_subscription': 21.0
    },
    {
        'country': 'USA',
        'streaming_cost': 35.0,
        'internet_cost': 80.0,
        'cinema_ticket': 15.0,
        'cultural_events': 100.0,
        'music_subscription': 11.0
    },
    {
        'country': 'Germany',
        'streaming_cost': 30.0,
        'internet_cost': 40.0,
        'cinema_ticket': 12.0,
        'cultural_events': 80.0,
        'music_subscription': 10.0
    },
    {
        'country': 'France',
        'streaming_cost': 28.0,
        'internet_cost': 35.0,
        'cinema_ticket': 11.0,
        'cultural_events': 75.0,
        'music_subscription': 10.0
    },
    {
        'country': 'Portugal',
        'streaming_cost': 25.0,
        'internet_cost': 30.0,
        'cinema_ticket': 8.0,
        'cultural_events': 60.0,
        'music_subscription': 9.0
    }
]

df_cultural_costs = pd.DataFrame(cultural_costs_data)
df_cultural_costs.to_csv('cultural_costs_raw.csv', index=False, encoding='utf-8')
print(f"✅ cultural_costs_raw.csv gerado: {len(df_cultural_costs)} registros")

# ============================================================================
# ARQUIVO 4: opportunity_costs_raw.csv
# ============================================================================

print("\n🎓 Gerando opportunity_costs_raw.csv...")

opportunity_costs_data = [
    {
        'country': 'Brazil',
        'technical_course': 400.0,  # mensal
        'college_private': 1200.0,  # mensal
        'language_course': 300.0,  # mensal
        'emergency_savings_target': 5000.0,  # recomendado
        'mobility_cost': 250.0  # transporte extra para oportunidades
    },
    {
        'country': 'USA',
        'technical_course': 800.0,
        'college_private': 2500.0,
        'language_course': 400.0,
        'emergency_savings_target': 10000.0,
        'mobility_cost': 300.0
    },
    {
        'country': 'Germany',
        'technical_course': 200.0,  # muito subsidiado
        'college_private': 500.0,  # educação pública forte
        'language_course': 250.0,
        'emergency_savings_target': 8000.0,
        'mobility_cost': 150.0
    },
    {
        'country': 'France',
        'technical_course': 180.0,
        'college_private': 450.0,
        'language_course': 230.0,
        'emergency_savings_target': 7500.0,
        'mobility_cost': 140.0
    },
    {
        'country': 'Portugal',
        'technical_course': 150.0,
        'college_private': 400.0,
        'language_course': 180.0,
        'emergency_savings_target': 5000.0,
        'mobility_cost': 100.0
    }
]

df_opportunity_costs = pd.DataFrame(opportunity_costs_data)
df_opportunity_costs.to_csv('opportunity_costs_raw.csv', index=False, encoding='utf-8')
print(f"✅ opportunity_costs_raw.csv gerado: {len(df_opportunity_costs)} registros")

# ============================================================================
# ARQUIVO 5: social_benefits_raw.csv
# ============================================================================

print("\n🏛️ Gerando social_benefits_raw.csv...")

social_benefits_data = [
    # Brasil
    {
        'country': 'Brazil',
        'benefit_name': 'Bolsa Família',
        'monthly_value': 600.0,
        'eligibility_income_threshold': 218.0,  # per capita
        'per_dependent_bonus': 150.0,
        'max_dependents': 5
    },
    {
        'country': 'Brazil',
        'benefit_name': 'BPC - Benefício Continuado',
        'monthly_value': 1412.0,
        'eligibility_income_threshold': 353.0,  # 1/4 SM per capita
        'per_dependent_bonus': 0.0,
        'max_dependents': 0
    },
    {
        'country': 'Brazil',
        'benefit_name': 'Auxílio Gás',
        'monthly_value': 102.0,
        'eligibility_income_threshold': 218.0,
        'per_dependent_bonus': 0.0,
        'max_dependents': 0
    },
    
    # EUA
    {
        'country': 'USA',
        'benefit_name': 'SNAP (Food Stamps)',
        'monthly_value': 250.0,
        'eligibility_income_threshold': 2500.0,
        'per_dependent_bonus': 150.0,
        'max_dependents': 8
    },
    {
        'country': 'USA',
        'benefit_name': 'EITC (Tax Credit)',
        'monthly_value': 450.0,  # média mensal
        'eligibility_income_threshold': 4500.0,
        'per_dependent_bonus': 200.0,
        'max_dependents': 3
    },
    {
        'country': 'USA',
        'benefit_name': 'Medicaid',
        'monthly_value': 400.0,  # valor equivalente cobertura
        'eligibility_income_threshold': 3000.0,
        'per_dependent_bonus': 0.0,
        'max_dependents': 0
    },
    
    # Alemanha
    {
        'country': 'Germany',
        'benefit_name': 'Bürgergeld',
        'monthly_value': 563.0,
        'eligibility_income_threshold': 1500.0,
        'per_dependent_bonus': 350.0,
        'max_dependents': 6
    },
    {
        'country': 'Germany',
        'benefit_name': 'Kindergeld',
        'monthly_value': 250.0,
        'eligibility_income_threshold': 5000.0,
        'per_dependent_bonus': 250.0,
        'max_dependents': 10
    },
    {
        'country': 'Germany',
        'benefit_name': 'Wohngeld',
        'monthly_value': 350.0,
        'eligibility_income_threshold': 2000.0,
        'per_dependent_bonus': 100.0,
        'max_dependents': 5
    },
    
    # França
    {
        'country': 'France',
        'benefit_name': 'RSA',
        'monthly_value': 607.0,
        'eligibility_income_threshold': 1200.0,
        'per_dependent_bonus': 180.0,
        'max_dependents': 6
    },
    {
        'country': 'France',
        'benefit_name': 'Allocations Familiales',
        'monthly_value': 140.0,
        'eligibility_income_threshold': 4500.0,
        'per_dependent_bonus': 140.0,
        'max_dependents': 8
    },
    {
        'country': 'France',
        'benefit_name': 'APL (Housing)',
        'monthly_value': 300.0,
        'eligibility_income_threshold': 1800.0,
        'per_dependent_bonus': 50.0,
        'max_dependents': 5
    },
    
    # Portugal
    {
        'country': 'Portugal',
        'benefit_name': 'RSI',
        'monthly_value': 230.0,
        'eligibility_income_threshold': 600.0,
        'per_dependent_bonus': 115.0,
        'max_dependents': 6
    },
    {
        'country': 'Portugal',
        'benefit_name': 'Abono de Família',
        'monthly_value': 50.0,
        'eligibility_income_threshold': 2000.0,
        'per_dependent_bonus': 50.0,
        'max_dependents': 8
    },
    {
        'country': 'Portugal',
        'benefit_name': 'Apoio ao Arrendamento',
        'monthly_value': 200.0,
        'eligibility_income_threshold': 1200.0,
        'per_dependent_bonus': 30.0,
        'max_dependents': 4
    }
]

df_social_benefits = pd.DataFrame(social_benefits_data)
df_social_benefits.to_csv('social_benefits_raw.csv', index=False, encoding='utf-8')
print(f"✅ social_benefits_raw.csv gerado: {len(df_social_benefits)} registros")

# ============================================================================
# RESUMO FINAL
# ============================================================================

print("\n" + "="*80)
print("✅ GERAÇÃO COMPLETA!")
print("="*80)

print("\n📊 Estatísticas people_raw.csv:")
print(f"   Total de pessoas: {len(df_people):,}")
print(f"   Salário médio bruto: R$ {df_people['gross_salary_brl'].mean():,.2f}")
print(f"   Salário mediano: R$ {df_people['gross_salary_brl'].median():,.2f}")
print(f"   Taxa de desemprego: {(df_people['employment_type']=='desempregado').sum()/len(df_people)*100:.1f}%")
print(f"   Taxa de informalidade: {(df_people['employment_type']=='informal').sum()/len(df_people)*100:.1f}%")
print(f"   Recebem benefício social: {df_people['receives_social_benefit'].sum():,} ({df_people['receives_social_benefit'].sum()/len(df_people)*100:.1f}%)")

print("\n📋 Distribuição por região:")
print(df_people['region_br'].value_counts().sort_index())

print("\n🎓 Distribuição por educação:")
print(df_people['education_level'].value_counts())

print("\n💼 Distribuição por categoria de trabalho:")
print(df_people['job_category'].value_counts())

print("\n🌍 Arquivos gerados:")
print("   ✅ people_raw.csv")
print("   ✅ economic_context_raw.csv")
print("   ✅ cultural_costs_raw.csv")
print("   ✅ opportunity_costs_raw.csv")
print("   ✅ social_benefits_raw.csv")

print("\n💡 Próximos passos sugeridos:")
print("   1. Validar consistência dos dados")
print("   2. Criar camada BRONZE (limpeza básica)")
print("   3. Criar camada SILVER (normalização)")
print("   4. Criar camada GOLD (métricas agregadas)")

print("\n" + "="*80)
