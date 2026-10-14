# Ciência de Dados — Análise da Educação Superior no Brasil (Censo 2024 / INEP)

Repositório dedicado ao projeto de **Engenharia, Limpeza e Análise de Dados** da Educação Superior Brasileira, com base na **Sinopse Estatística da Educação Superior 2024** publicada pelo **INEP / MEC**, com enriquecimento via **Web Scraping (`pandas.read_html`)** e **Consumo de API Pública**.

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

## 📋 Checklist de Critérios Atendidos

| Item | Critério de Avaliação | Como foi Atendido no Repositório |
|:---:|:---|:---|
| **1** | **Leitura do dataset real com URL registrada** | Planilha da Sinopse da Educação Superior 2024 baixada e lida via servidores do INEP / MEC (`https://download.inep.gov.br/...`), com registro da URL oficial. |
| **2** | **Criação de DataFrame** | Construção e manipulação dos DataFrames estruturados `df`, `bruto`, `ingenuo`, `df_uf`, `antes_depois`, `df_populacao`, `df_ibge` e `df_enriquecido`. |
| **3** | **Criação de pelo menos uma Series** | Extração da Series univariada `serie_uf` (total de IES por estado ordenada descendentemente) e `problemas`. |
| **4** | **Uso de `head()`, `info()` e `describe()`** | Aplicados na inspeção inicial (o "antes") e na validação do dataset final limpo (o "depois"). |
| **5** | **Identificação de problemas com números** | Mapeamento exato: 36 de 37 colunas `Unnamed` (97%), 97 células vazias no cabeçalho (66%), 15 linhas que não são dados, 1.423 células com traço `"-"` no lugar de números e 720 rótulos repetidos. |
| **6** | **Limpeza do pilar mostrando antes e depois** | Tabela comparativa e resolução de cabeçalhos mesclados com propagação contextual `ffill()` restrita aos nós pais. |
| **7** | **Destaque: Leitura de dados Web (`read_html`) e API** | Coleta de dados demográficos da Wikipédia via `pd.read_html()`, consumo da API REST de Localidades do IBGE, tratamento do erro HTTP 403 com `User-Agent: Mozilla/5.0` e cálculo da taxa de **IES por 1 milhão de habitantes**. |

---

## 🎯 Pilar de Engenharia de Dados: Cabeçalhos Hierárquicos Mesclados

O objetivo central deste projeto foi solucionar o desafio de tratar planilhas corporativas/governamentais formatadas para **leitura humana visual** e transformá-las em formato tabular estrito (**Tidy Data**), onde cada linha é uma observação atômica e cada coluna representa uma variável mensurável.

### Principais Desafios Superados:
- **Cabeçalhos Mesclados Multinível:** Eliminação de 97% de colunas `Unnamed` através da reconstrução da árvore hierárquica por concatenação contextual (` | `).
- **Propagação Segura (`ffill`):** Preenchimento horizontal condicionado à integridade dos nós pais superiores, impedindo vazamento de rótulos entre categorias adjacentes (ex.: *Pública* x *Privada*).
- **Tipagem Numérica e Símbolos:** Conversão de 1.423 traços estatísticos `"-"` (convenção de zero do INEP) em `0` e coerção para o tipo inteiro seguro `Int64`.
- **Desagregação Territorial:** Separação da 1ª coluna em três dimensões explícitas: `nivel` (Brasil, Região, UF, Município), `local` e `categoria`.

---

## 🌐 Destaque: Integração Web (`read_html`) e API Pública do IBGE

Cruzando os dados de instituições do INEP com a população dos estados (coletada via `read_html()` da Wikipédia) e as siglas oficiais (consumidas da API do IBGE), foi gerado o ranking de **Densidade de IES por 1 Milhão de Habitantes**:

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

## 📊 Principais Descobertas do Censo 2024

- **Total Nacional:** O Brasil possui **2.561 Instituições de Ensino Superior (IES)** ativas em 2024.
- **Concentração Absoluta:**
  - **São Paulo** lidera com **580 IES (22,6%)**.
  - Os 5 primeiros estados (**SP: 580, MG: 303, PR: 171, BA: 145 e GO: 128**) concentram **51,8%** de todas as IES do país.
  - O menor número está em **Roraima**, com apenas **9 IES (0,35%)**.
- **Dependência Administrativa:**
  - **Rede Privada:** 2.244 instituições (**87,6%**), sendo 1.486 com fins lucrativos e 758 sem fins lucrativos.
  - **Rede Pública:** 317 instituições (**12,4%**), divididas em 122 federais, 139 estaduais e 56 municipais.
- **Organização Acadêmica:**
  - **Faculdades:** 1.897 IES (**74,1%**).
  - **Centros Universitários:** 417 IES (**16,3%**).
  - **Universidades:** 206 IES (**8,0%**).
- **Distribuição Regional:**
  - **Sudeste:** 1.076 IES (42,0%)
  - **Nordeste:** 604 IES (23,6%)
  - **Sul:** 389 IES (15,2%)
  - **Centro-Oeste:** 296 IES (11,6%)
  - **Norte:** 196 IES (7,6%)

---

## 🗂️ Estrutura do Repositório

```text
├── index.html                             # Página principal do GitHub Pages com terminal de saída interativo
├── saida_codigo.html                      # Página web dedicada para visualização da saída de execução
├── saida_execucao.txt                     # Saída bruta completa da execução do script em formato texto
├── grupo2_educacao_superior.py            # Script Python completo com o pipeline de limpeza e análise
├── grupo2_educacao_superior.ipynb         # Jupyter Notebook com execução interativa
├── roteiro_apresentacao.md                # Roteiro de apresentação com divisão de falas por integrante
├── relatorio_educacao_superior_grupo2.pdf # Relatório técnico executivo completo formatado em PDF
├── relatorio_educacao_superior_grupo2.md  # Relatório completo em Markdown
├── relatorio_educacao_superior_grupo2.html# Versão web do relatório
├── sinopse_limpa.csv                      # Dataset final tratado e validado estatisticamente
├── sinopse_com_indicadores_web.csv        # Dataset enriquecido com dados da Web (read_html) e API
├── .gitignore                             # Exclusão de arquivos pesados (> 100 MB do INEP)
└── README.md                              # Documentação geral do projeto e checklist avaliativo
```

🌐 **Link do GitHub Pages:** [https://barbooosa.github.io/data_science/](https://barbooosa.github.io/data_science/)


---

## 🚀 Como Executar

### 1. Pré-requisitos
Instale as bibliotecas necessárias:
```bash
pip install pandas openpyxl requests lxml
```

### 2. Executando o Script
```bash
python grupo2_educacao_superior.py
```
O script executa a limpeza, valida as somas contábeis, consome a API do IBGE, extrai a tabela da Wikipédia via `read_html()` e gera os arquivos `sinopse_limpa.csv` e `sinopse_com_indicadores_web.csv`.
