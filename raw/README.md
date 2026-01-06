# Projeto de Simulação Socioeconômica Internacional

## 1. Visão Geral

Este projeto tem como objetivo modelar, de forma **quantitativa e comparável**, o poder de compra, a pressão econômica e as oportunidades de mobilidade social de indivíduos brasileiros sob diferentes contextos econômicos internacionais.

A proposta não é apenas converter salários entre moedas, mas **simular como uma mesma pessoa se comportaria economicamente** quando inserida em países distintos, considerando:

* custo de vida real
* estrutura tributária
* benefícios sociais
* custos culturais e digitais
* oportunidades de investimento no futuro

O projeto utiliza **dados sintéticos**, calibrados com **estatísticas reais**, para permitir análises reprodutíveis, éticas e escaláveis.

---

## 2. Princípios do Projeto

Este projeto segue cinco princípios fundamentais:

1. **Realismo Estatístico**
   Os dados não representam indivíduos reais, mas respeitam distribuições e proporções observadas em fontes oficiais.

2. **Separação de Camadas**
   A pipeline é organizada em camadas (RAW → SILVER → GOLD), evitando mistura de dados brutos com métricas derivadas.

3. **Decisão, não apenas Visualização**
   O foco está em responder perguntas socioeconômicas reais, e não apenas gerar gráficos.

4. **Comparabilidade Internacional**
   Todas as simulações utilizam métricas ajustadas por contexto local.

5. **Transparência de Suposições**
   Todas as simplificações e escolhas econômicas são explicitadas neste documento.

---

## 3. Fontes de Referência Estatística

Os valores utilizados como base foram inspirados em médias públicas, incluindo:

* IBGE (Brasil)
* Numbeo (custo de vida por cidade)
* World Bank
* OECD
* Eurostat
* BLS (Bureau of Labor Statistics – EUA)

Os valores **não são cópias exatas**, mas aproximações coerentes para fins de simulação.

---

## 4. Estrutura do Dataset (Camada RAW)

A camada RAW contém apenas dados brutos, sem normalizações ou métricas calculadas.

### 4.1 `people_raw.csv`

Representa indivíduos brasileiros economicamente ativos.

Principais suposições:

* Distribuição salarial assimétrica (cauda longa)
* Educação influencia renda média
* Informalidade concentrada em faixas de menor renda
* Nem todos os elegíveis acessam benefícios sociais
* Desempregados possuem renda zero

Campos relevantes:

* salário bruto e líquido
* tipo de vínculo (CLT, PJ, informal)
* dependentes
* região e cidade

---

### 4.2 `economic_context_raw.csv`

Contexto econômico por país e cidade.

Inclui:

* salário mínimo local
* custos médios de moradia (indivíduo e família)
* alimentação básica
* transporte
* utilidades
* saúde
* carga tributária efetiva

### Observação importante

Em grandes centros urbanos, o custo de vida familiar pode se aproximar ou exceder o salário mínimo. Isso é **intencional** e reflete a realidade econômica observada.

---

### 4.3 `cultural_costs_raw.csv`

Custos mensais de acesso cultural e digital, utilizados como **proxy de inclusão social**.

Inclui:

* streaming
* internet
* cinema
* eventos culturais
* música

Esses custos não são essenciais à sobrevivência, mas indicam **capacidade de participação social**.

---

### 4.4 `opportunity_costs_raw.csv`

Custos associados à mobilidade social e investimento no futuro.

Inclui:

* cursos técnicos
* faculdade privada
* cursos de idioma
* meta de reserva de emergência
* custo de mobilidade

Esses valores serão usados posteriormente para medir **quantas oportunidades uma pessoa consegue acessar**.

---

### 4.5 `social_benefits_raw.csv`

Benefícios sociais e regras de elegibilidade.

Observações importantes:

* Limiares de elegibilidade podem ser per capita ou por domicílio
* Nem toda pessoa elegível recebe benefícios
* Benefícios variam por número de dependentes

Essas simplificações são intencionais e permitem simulações realistas de políticas públicas.

---

## 5. Simplificações Assumidas

Para manter o modelo compreensível e escalável, foram adotadas algumas simplificações:

* Impostos modelados como taxa efetiva média
* Custos de saúde médios (cenários mais detalhados podem ser simulados depois)
* Custos médios por cidade (sem variância intraurbana)
* Benefícios sociais não cobrem 100% dos elegíveis

Essas decisões não invalidam o modelo — elas são documentadas e ajustáveis.

---

## 6. O Que NÃO Existe na Camada RAW

Explicitamente ausente nesta etapa:

* métricas normalizadas
* índices compostos
* scores de qualidade de vida
* classificações socioeconômicas
* análises ou gráficos

Esses elementos pertencem às camadas SILVER e GOLD.

---

## 7. Próximas Etapas

1. **Análise exploratória dos dados (EDA)**
   Validação estatística das distribuições.

2. **Feature Engineering (Camada SILVER)**
   Criação de métricas como renda disponível, pressão econômica e acesso cultural.

3. **Modelagem e Simulação (Camada GOLD)**
   Clusterização, cenários e sistema de recomendação socioeconômica.

---

## 8. Considerações Finais

Este projeto busca demonstrar domínio técnico em:

* modelagem de dados
* economia aplicada
* análise socioeconômica
* engenharia de dados
* tomada de decisão baseada em dados

Mais do que responder quanto uma pessoa ganharia em outro país, o projeto responde:

> **como as condições estruturais moldam o bem-estar econômico real.**


