# ⚡ GUIA RÁPIDO DE COMANDOS

## 📦 Setup Inicial

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install pandas numpy
```

## 🚀 Execução

### Gerar Camada SILVER (Principal)
```bash
python src/generate_enriched_data.py
```

### Validar Dados
```bash
python src/validate_enriched_data.py
```

### Ver Exemplos de Análise
```bash
python src/exemplos_uso_silver.py
```

### (Re)Gerar Dados RAW
```bash
python src/generate_raw_data.py
```

## 📊 Exploração Rápida

### Python
```python
import pandas as pd

# Carregar dados principais
people = pd.read_csv('enriched/people_enriched.csv')

# Ver primeiras linhas
print(people.head())

# Estatísticas
print(people['renda_disponivel_real'].describe())

# Filtrar vulneráveis
vuln = people[
    (people['renda_disponivel_real'] < 0) & 
    (people['dependents'] >= 2)
]
print(f"Vulneráveis: {len(vuln)}")
```

### Excel/Power BI
```
Abrir diretamente:
- enriched/people_enriched.csv
- enriched/cross_country_family_comparison.csv
```

## 🔍 Validações Rápidas

### Verificar Completude
```bash
python -c "import pandas as pd; df=pd.read_csv('enriched/people_enriched.csv'); print(df.isnull().sum())"
```

### Ver Estatísticas RDR
```bash
python -c "import pandas as pd; df=pd.read_csv('enriched/people_enriched.csv'); print(df['renda_disponivel_real'].describe())"
```

### Contar Déficits
```bash
python -c "import pandas as pd; df=pd.read_csv('enriched/people_enriched.csv'); print(f'Déficit: {(df[\"renda_disponivel_real\"]<0).sum()}')"
```

## 📁 Estrutura de Arquivos

```bash
# Listar arquivos RAW
ls raw/*.csv

# Listar arquivos SILVER
ls enriched/*.csv

# Verificar tamanhos
du -h enriched/*.csv  # Linux/Mac
dir enriched\*.csv    # Windows
```

## 🐍 Análises Personalizadas

### Template Básico
```python
import pandas as pd
from pathlib import Path

# Carregar
df = pd.read_csv('enriched/people_enriched.csv')

# Sua análise aqui
# ...

# Salvar resultado
resultado.to_csv('minha_analise.csv', index=False)
```

### Filtros Úteis
```python
# Déficit
deficit = df[df['renda_disponivel_real'] < 0]

# Alta pressão econômica
pressao_alta = df[df['economic_pressure_ratio'] > 1.5]

# Com dependentes
com_filhos = df[df['dependents'] > 0]

# Região específica
nordeste = df[df['region_br'] == 'NE']

# Educação superior
superior = df[df['education_level'] == 'superior']
```

## 📊 Análises por Grupo

```python
# Por região
df.groupby('region_br')['renda_disponivel_real'].mean()

# Por educação
df.groupby('education_level')['economic_pressure_ratio'].median()

# Por dependentes
df.groupby('dependents')['total_household_cost'].mean()
```

## 🌍 Cross-Country

```python
# Carregar comparações
comp = pd.read_csv('enriched/cross_country_family_comparison.csv')

# Melhor destino para cada perfil
comp.loc[comp['from_country']=='Brazil'].groupby('profile_id')['fpp_delta_usd'].max()

# Top 10 melhores mudanças
comp.nlargest(10, 'fpp_delta_usd')[['profile_id', 'from_city', 'to_city', 'fpp_delta_usd']]
```

## 🔧 Troubleshooting

### Erro: "pandas not found"
```bash
pip install pandas numpy
```

### Erro: "File not found"
```bash
# Verificar diretório atual
pwd  # Linux/Mac
cd   # Windows

# Navegar para project-root
cd c:\Users\juan_\OneDrive\Desktop\project-root
```

### Dados Vazios
```bash
# Regerar RAW
python src/generate_raw_data.py

# Regerar SILVER
python src/generate_enriched_data.py
```

### Performance Lenta
```python
# Usar amostra
df = pd.read_csv('enriched/people_enriched.csv', nrows=1000)

# Ou especificar colunas
df = pd.read_csv('enriched/people_enriched.csv', usecols=['person_id', 'renda_disponivel_real'])
```

## 📖 Documentação

```
README.md                  → Visão geral
SILVER_SUMMARY.md          → Resumo executivo
enriched/README.md         → Detalhes técnicos SILVER
raw/README.md              → Documentação RAW
```

## 💡 Dicas

1. **Sempre ative o ambiente virtual** antes de executar
2. **Valide após gerar** dados com `validate_enriched_data.py`
3. **Use exemplos_uso_silver.py** como referência
4. **Salve análises** em arquivos separados
5. **Documente** mudanças em comments

## 🎯 Workflow Típico

```bash
# 1. Setup (uma vez)
python -m venv .venv
.venv\Scripts\activate
pip install pandas numpy

# 2. Gerar dados (quando necessário)
python src/generate_enriched_data.py

# 3. Validar
python src/validate_enriched_data.py

# 4. Analisar
python src/exemplos_uso_silver.py

# 5. Análise customizada
python minha_analise.py
```

---

**Criado**: 2026-01-06  
**Para**: Pipeline Socioeconômico SILVER
