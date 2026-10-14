# Ciência de Dados — Análise da Educação Superior no Brasil (Censo 2024 / INEP)

Repositório dedicado ao projeto de **Engenharia, Limpeza e Análise de Dados** da Educação Superior Brasileira, com base na **Sinopse Estatística da Educação Superior 2024** publicada pelo **INEP / MEC**.

---

## 🎯 Pilar de Engenharia de Dados: Cabeçalhos Hierárquicos Mesclados

O objetivo central deste projeto foi solucionar o desafio de tratar planilhas corporativas/governamentais formatadas para **leitura humana visual** e transformá-las em formato tabular estrito (**Tidy Data**), onde cada linha é uma observação atômica e cada coluna representa uma variável mensurável.

### Principais Desafios Superados:
- **Cabeçalhos Mesclados Multinível:** Eliminação de 97% de colunas `Unnamed` através da reconstrução da árvore hierárquica por concatenação contextual (` | `).
- **Propagação Segura (`ffill`):** Preenchimento horizontal condicionado à integridade dos nós pais superiores, impedindo vazamento de rótulos entre categorias adjacentes (ex.: *Pública* x *Privada*).
- **Tipagem Numérica e Símbolos:** Conversão de 1.423 traços estatísticos `"-"` (convenção de zero do INEP) em `0` e coerção para o tipo inteiro seguro `Int64`.
- **Desagregação Territorial:** Separação da 1ª coluna em três dimensões explícitas: `nivel` (Brasil, Região, UF, Município), `local` e `categoria`.

---

## 📊 Principais Descobertas e Insights do Censo 2024

- **Total Nacional:** O Brasil possui **2.561 Instituições de Ensino Superior (IES)** ativas em 2024.
- **Concentração Espacial:**
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
├── grupo2_educacao_superior.py       # Script Python completo com o pipeline de limpeza e análise
├── grupo2_educacao_superior.ipynb    # Jupyter Notebook original com todas as etapas interativas
├── relatorio_educacao_superior_grupo2.pdf # Relatório técnico executivo completo formatado em PDF
├── relatorio_educacao_superior_grupo2.md  # Relatório completo em Markdown
├── relatorio_educacao_superior_grupo2.html# Versão interativa web do relatório
├── sinopse_limpa.csv                  # Dataset final tratado e validado estatisticamente
├── .gitignore                         # Exclusão de arquivos pesados (> 100 MB do INEP)
└── README.md                          # Documentação geral do projeto
```

---

## 🚀 Como Executar

### 1. Pré-requisitos
Certifique-se de ter o Python 3.10+ instalado com as bibliotecas necessárias:
```bash
pip install pandas openpyxl requests
```

### 2. Executando o Script
Clone o repositório e execute diretamente:
```bash
python grupo2_educacao_superior.py
```

O script detectará automaticamente a base de dados local ou fará a extração do `.zip` da Sinopse 2024, gerando as validações na tela e salvando o arquivo `sinopse_limpa.csv`.
