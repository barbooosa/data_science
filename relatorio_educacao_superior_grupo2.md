# Relatório de Engenharia e Análise de Dados: Ensino Superior 2024
**Grupo 2 — Educação: Ensino Superior**  
**Fontes dos Dados:** 
1. **INEP / MEC** — Sinopse Estatística da Educação Superior 2024 (Aba `1.1`)
2. **Wikipédia (read_html)** — População das UFs do Brasil (Censo Demográfico IBGE)
3. **API do IBGE** — API de Serviços de Dados / Localidades do Brasil  
**Pilar de Limpeza:** Resolução de cabeçalhos hierárquicos mesclados e desagregação territorial  
**Destaque:** Coleta de dados da Web com `pd.read_html()` e consumo de API pública oficial

---

### 👥 Integrantes da Equipe (Grupo 2)

| Nome do Aluno | Matrícula |
|:---|:---:|
| **Gustavo Henrique Tavares Borges** | `2311157` |
| **João Pedro Barbosa Moreira** | `2312662` |
| **Igor Augusto Ribeiro de Paula Martins** | `2312171` |
| **Ygor Gomes Rocha** | `2312663` |
| **Elton Dourado De Azevedo Filho** | `2310514` |

---

## 📋 Checklist de Atendimento aos Critérios da Atividade

- [x] **1. Leitura do dataset real do tema com registro de URL:** Planilha oficial da Sinopse da Educação Superior 2024 baixada e lida a partir dos servidores do INEP / MEC (`https://download.inep.gov.br/...`).
- [x] **2. Criação de DataFrame:** Construção de DataFrames estruturados (`df`, `bruto`, `ingenuo`, `df_uf`, `antes_depois`, `df_populacao`, `df_ibge`, `df_enriquecido`).
- [x] **3. Criação de pelo menos uma Series:** Criação da Series univariada `serie_uf` indexada pelos estados, além de `problemas`.
- [x] **4. Uso de `head()`, `info()` e `describe()`:** Aplicados tanto na inspeção inicial (o "antes") quanto na validação do dataset final limpo (o "depois").
- [x] **5. Identificação de problemas nos dados, com números:**
  - 36 de 37 colunas sem nome (`Unnamed: 1` a `Unnamed: 36`);
  - 97 de 148 células vazias no cabeçalho (66%);
  - 15 linhas que não são dados (títulos, espaçamentos e rodapés);
  - 34 de 36 colunas de valores lidas como texto (`object`);
  - 1.423 células com símbolos no lugar de números (traço `"-"`);
  - 720 rótulos repetidos na 1ª coluna por mistura de níveis geográficos.
- [x] **6. Aplicação da limpeza do pilar do grupo, mostrando antes e depois:** Tabela comparativa detalhada de 7 critérios e explicação aprofundada de cada transformação.
- [x] **7. Destaque: Leitura de dados da web (`read_html`) e consumo de API pública:**
  - Utilização de `pandas.read_html()` a partir da Wikipédia (`https://pt.wikipedia.org/wiki/Lista_de_unidades_federativas_do_Brasil_por_popula%C3%A7%C3%A3o`);
  - Consumo da API REST pública de Localidades do IBGE (`https://servicodados.ibge.gov.br/api/v1/localidades/estados`);
  - Tratamento de erro HTTP 403 através de injeção de `User-Agent: Mozilla/5.0`;
  - Cruzamento de dados e cálculo da taxa de **IES por 1 milhão de habitantes**;
  - Reflexão crítica sobre a confiabilidade de cada fonte.

---

## 1. Contexto e Objetivos do Estudo

A **Sinopse Estatística da Educação Superior** é o relatório anual consolidado divulgado pelo INEP com os dados oficiais do Censo da Educação Superior no Brasil. 

Historicamente, esse arquivo é diagramado no formato Microsoft Excel visando prioritariamente a **apresentação visual e a leitura humana** (relatórios de gabinete, consultas manuais e impressão). Por conta disso, a planilha apresenta características problemáticas para a análise de dados automatizada:
- Múltiplas linhas de cabeçalho mescladas horizontal e verticalmente;
- Células mescladas que chegam vazias (`NaN`) na leitura de bibliotecas padrão como o Pandas;
- Concomitância de totais nacionais, regionais, estaduais e municipais dentro de uma mesma coluna;
- Uso de caracteres tipográficos (como o traço `"-"`) para denotar frequência zero, contaminando os tipos numéricos com o tipo genérico `object`.

O objetivo central deste trabalho de engenharia de dados foi desenvolver uma rotina em Python capaz de transformar essa planilha não-estruturada em um dataset limpo no formato **Tidy Data** (onde cada linha representa uma unidade de observação estrita e cada coluna representa uma variável atômica), habilitando análises estatísticas rigorosas e reprodutíveis.

---

## 2. Descrição das Fontes de Dados e Confiabilidade

1. **INEP / MEC (Sinopse da Educação Superior 2024):**
   - *Quem publica:* Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (autarquia do MEC).
   - *Atualização:* Anual, baseada no Censo da Educação Superior com preenchimento obrigatório por lei para todas as IES.
   - *Limitações:* Dados pré-agregados; não permite cruzamento de microdados individuais de estudantes não tabulados.
2. **Wikipédia (read_html — Censo Demográfico IBGE):**
   - *Quem publica:* Comunidade aberta da Wikipédia, transcrevendo os dados oficiais apurados pelo Censo Demográfico do IBGE.
   - *Tratamento:* Acesso protegido contra bloqueio HTTP 403 com cabeçalho `User-Agent: Mozilla/5.0`.
   - *Limitações:* Necessidade de validação programática de integridade das tabelas HTML.
3. **API do IBGE (Serviço de Dados):**
   - *Quem publica:* Instituto Brasileiro de Geografia e Estatística (órgão oficial do Estado brasileiro).
   - *Atualização:* Contínua via API REST imutável com códigos geográficos oficiais.

---

## 3. Tabela Comparativa de Auditoria: Antes x Depois

| Métrica de Auditoria | Antes (Leitura Padrão do Excel) | Depois (Dataset Limpo) | Racional & Técnica de Limpeza |
|:---|:---:|:---:|:---|
| **Formato (Linhas x Colunas)** | `746 x 37` | `731 x 40` | Descarte de títulos/rodapés e inclusão das colunas dimensionais (`nivel`, `local`, `categoria`). |
| **Colunas sem nome ('Unnamed')** | `36 de 37 (97%)` | `0 (0%)` | Reconstrução dos nomes através da concatenação hierárquica dos 4 níveis do cabeçalho original. |
| **Células vazias no cabeçalho** | `97 de 148 (66%)` | `0 (0%)` | Preenchimento progressivo horizontal (`ffill`) restrito estritamente dentro de cada nó pai superior. |
| **Linhas que não são dados** | `15 linhas` | `0 linhas` | Mapeamento automático dos limites de início e fim dos dados via densidade numérica de cada linha. |
| **Colunas de valores como texto** | `34 de 36 colunas` | `0 colunas` | Coerção numérica e conversão integral para o tipo inteiro seguro `Int64`. |
| **Símbolos no lugar de números** | `1.423 células` | `0 células` | Substituição do traço tipográfico `"-"` (convenção de zero do INEP) pelo número `0`. |
| **Estrutura da primeira coluna** | Aglutinada e heterogênea | Desmembrada em 3 colunas | Classificação territorial precisa em `Brasil`, `Região`, `UF` e `Município`. |

---

## 4. Explicação Detalhada de Cada Comparação

### 4.1 Formato Geral da Matriz (`746x37` para `731x40`)
Na leitura crua (`header=None`), a planilha trazia 746 linhas. Dessas, as primeiras 4 linhas eram títulos e códigos de controle; as 4 seguintes compunham o cabeçalho multinível; a linha 9 era um espaçamento em branco; e as linhas 742 a 745 continham notas de rodapé institucionais do INEP. A limpeza isolou cirurgicamente as **731 linhas de dados reais** e expandiu a matriz de 37 para 40 colunas para acomodar a hierarquia explícita.

### 4.2 Eliminação de Colunas `Unnamed` (de 97% para 0%)
Ao executar `pd.read_excel()` sem parâmetros especiais, o Pandas assume que a primeira linha do arquivo é o cabeçalho. Como na linha 0 apenas a primeira célula possui texto ("Voltar ao Sumário"), todas as demais 36 colunas receberam o nome genérico `Unnamed: 1`, `Unnamed: 2`, etc. A rotina `achatar_cabecalho()` montou a árvore hierárquica completa unindo os níveis com ` | ` (ex.: *"Organização Acadêmica | Faculdade | Privada | Com Fins Lucrativos"*).

### 4.3 Preenchimento das Células Vazias no Cabeçalho (de 66% para 0%)
As células mescladas guardam informação apenas na primeira célula da esquerda/topo, deixando as demais vazias. Para reconstruir os nomes corretos sem que um rótulo "vazasse" para o bloco ao lado (por exemplo, propagar o rótulo "Pública" para dentro das colunas "Privada"), a técnica agrupou as colunas pela tupla de ancestrais superiores antes de aplicar o `ffill()`.

### 4.4 Tratamento de Tipos e Conversão de Símbolos (1.423 traços eliminados)
A convenção estatística do INEP utiliza o traço `"-"` para sinalizar ausência de instituições naquela combinação de variáveis. Um único traço em uma coluna com 700 números faz o Pandas inferir toda a coluna como string (`object`). Trocando `"-"` por `0` e convertendo para `Int64`, restaurou-se a capacidade de somar, calcular médias e gerar gráficos.

### 4.5 Desmembramento da Primeira Coluna
Na planilha bruta, a primeira coluna continha uma mistura de totais nacionais, nomes de regiões, nomes de estados e municípios. A função `determinar_nivel()` criou três dimensões canônicas:
- **`nivel`**: `Brasil` (1 linha), `Região` (5 linhas), `UF` (27 linhas) e `Município` (698 linhas).
- **`local`**: Nome padronizado da localidade (ex.: "São Paulo", "Nordeste", "Brasil").
- **`categoria`**: Identificador da desagregação.

---

## 5. Validação Matemática e Hierárquica

A integridade do pipeline foi comprovada por validação contábil:
- **Total Brasil na Planilha:** **2.561** instituições
- **Soma dos 27 Estados (UFs):** **2.561** instituições (**Convergência exata: 100%**)
- **Soma das 5 Regiões Geográficas:** **2.561** instituições (**Convergência exata: 100%**)
- **Conformidade de Colunas:** **33 de 33 colunas numéricas** bateram com precisão absoluta.

> [!CAUTION]
> **O Perigo da Análise sem Limpeza:**
> Se alguém aplicasse a função `.sum()` diretamente sobre a coluna de total antes do tratamento, o resultado seria **10.244 instituições** — um erro crasso de **400% (4 vezes maior)** gerado pela soma acumulada de municípios, estados, regiões e total nacional.

---

## 6. Destaque: Leitura de Dados da Web (`read_html`) e Consumo de API

Para enriquecer o estudo, foi realizada a coleta web e integração com API governamental:
- **Web Scraping com `pd.read_html()`:** Extração da tabela demográfica da Wikipédia tratando o erro HTTP 403 com `User-Agent`.
- **API Pública do IBGE:** Consumo do endpoint de estados para mapeamento das siglas (UFs) e regiões.
- **Métrica Per Capita Calculada (IES por 1 Milhão de Habitantes):**

| Sigla | Estado (UF) | Região | Total de IES (INEP) | População (IBGE / Wiki) | IES por 1 Milhão de Hab. |
|:---:|:---|:---:|:---:|:---:|:---:|
| **DF** | Distrito Federal | Centro-Oeste | 63 | 3.009.996 | **20,93** (1º lugar) |
| **MT** | Mato Grosso | Centro-Oeste | 74 | 3.950.330 | **18,73** (2º lugar) |
| **AP** | Amapá | Norte | 15 | 809.953 | **18,52** (3º lugar) |
| **RO** | Rondônia | Norte | 31 | 1.757.338 | **17,64** (4º lugar) |
| **GO** | Goiás | Centro-Oeste | 128 | 7.495.033 | **17,08** (5º lugar) |
| **ES** | Espírito Santo | Sudeste | 67 | 4.150.692 | **16,14** |
| **TO** | Tocantins | Norte | 23 | 1.595.994 | **14,41** |
| **PR** | Paraná | Sul | 171 | 11.952.456 | **14,31** |
| **PI** | Piauí | Nordeste | 48 | 3.392.617 | **14,15** |
| **MG** | Minas Gerais | Sudeste | 303 | 21.460.311 | **14,12** |

---

## 7. Descobertas e Insights do Censo 2024

1. **Volume Total:** O Brasil encerrou o ano de 2024 com **2.561 instituições de educação superior** ativas em sua sede administrativa.
2. **Alta Concentração Espacial vs. Densidade Per Capita:**
   - **São Paulo lidera em números absolutos** com 580 instituições (22,6% do país). Os 5 maiores estados (SP, MG, PR, BA e GO) somam 51,8% de todas as IES.
   - **Centro-Oeste lidera na densidade per capita:** DF (20,93), MT (18,73) e GO (17,08) possuem a maior concentração de instituições em relação à população residente.
   - O menor número absoluto está em **Roraima**, com apenas **9 instituições** (0,35% do total nacional).
3. **Predomínio da Rede Privada:**
   - **Rede Privada:** 2.244 IES (**87,6%** do total), sendo 1.486 com fins lucrativos e 758 sem fins lucrativos.
   - **Rede Pública:** 317 IES (**12,4%** do total), divididas em 122 federais, 139 estaduais e 56 municipais.
4. **Organização Acadêmica das Instituições:**
   - **Faculdades:** 1.897 IES (**74,1%**)
   - **Centros Universitários:** 417 IES (**16,3%**)
   - **Universidades:** 206 IES (**8,0%**)
   - **IFs e CEFETs:** 41 instituições federais registradas.
5. **Divisão por Grandes Regiões:**
   - **Sudeste:** 1.076 IES (42,0%)
   - **Nordeste:** 604 IES (23,6%)
   - **Sul:** 389 IES (15,2%)
   - **Centro-Oeste:** 296 IES (11,6%)
   - **Norte:** 196 IES (7,6%)

---

## 8. Possíveis Dificuldades Encontradas e Soluções

1. **Escala e Peso dos Arquivos Excel:** O arquivo compactado do INEP ultrapassa 397 MB e quase 1 GB descompactado. A solução exigiu leitura sob demanda exclusivamente da aba necessária (`1.1`).
2. **Falhas do Mecanismo Nativo do Pandas:** O suporte padrão do Pandas para múltiplos cabeçalhos (`header=[5,6,7,8]`) gera um MultiIndex que não resolve adequadamente células mescladas verticais. Foi essencial desenvolver o algoritmo de propagação orientada por árvore de dependência.
3. **Bloqueio HTTP 403 em Requisições Web:** A Wikipédia rejeita conexões de bots sem cabeçalho; foi contornado com a inclusão de `headers={"User-Agent": "Mozilla/5.0"}`.
