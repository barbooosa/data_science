# Roteiro e Divisão da Apresentação — Grupo 2
## Ciência de Dados: Educação Superior no Brasil (Censo 2024 / INEP)

---

### 👥 Quadro Geral de Divisão da Apresentação

| Integrante | Matrícula | Parte / Tópico da Apresentação | Slides | Tempo Estimado |
|:---|:---:|:---|:---:|:---:|
| **Gustavo Henrique Tavares Borges** | `2311157` | **Parte 1: Abertura, Contexto e Fontes de Dados** | Slides 1 e 2 | 2m30s |
| **João Pedro Barbosa Moreira** | `2312662` | **Parte 2: Diagnóstico dos Dados Brutos e Problemas** | Slide 3 | 2m30s |
| **Igor Augusto Ribeiro de Paula Martins** | `2312171` | **Parte 3: O Pilar de Limpeza e Engenharia de Dados** | Slide 4 | 3m00s |
| **Ygor Gomes Rocha** | `2312663` | **Parte 4: Destaque Web Scraping e Consumo de API** | Slide 5 | 3m00s |
| **Elton Dourado De Azevedo Filho** | `2310514` | **Parte 5: Descobertas, Indicadores, Dificuldades e Conclusão** | Slides 6, 7 e 8 | 3m00s |

*Tempo Total Sugerido: 12 a 15 minutos (com folga para perguntas da banca).*

---

## 🎤 Roteiro Detalhado por Integrante

---

### 👤 Parte 1: Abertura, Contextualização e Fontes de Dados
**Responsável Sugerido:** Gustavo Henrique Tavares Borges (2311157)  
**Slides:** 1 (Capa) e 2 (Contexto e Fontes)  
**Critérios da Atividade:** Critério 1 (Leitura do dataset com URL) e Critério 2 (Criação de DataFrames).

#### 🎯 Objetivo da Fala:
Apresentar a equipe, introduzir a relevância do Censo da Educação Superior de 2024 do INEP/MEC e explicar a origem dos dados utilizados no projeto.

#### 📌 Tópicos a Abordar:
1. **Apresentação Inicial:** Boas-vindas à banca/professor, apresentação do Grupo 2 e dos colegas de equipe.
2. **Contexto Temático:** Por que analisar o Ensino Superior em 2024? Entender a expansão, a capilaridade regional e o perfil das instituições (públicas vs. privadas).
3. **Fonte Primária dos Dados:** 
   - Sinopse Estatística da Educação Superior 2024 (Aba `1.1`), publicada pelo **INEP / MEC**.
   - Registro da URL oficial de download (`https://download.inep.gov.br/...`).
4. **Criação dos DataFrames Iniciais:**
   - Como os dados foram carregados a partir da planilha complexa em Excel (`.xlsx`) de mais de 300 MB.

#### 🗣️ Roteiro de Fala Sugerido:
> *"Boa noite a todos. Somos o Grupo 2, composto por mim, Gustavo, e pelos meus colegas João Pedro, Igor, Ygor e Elton. Nosso trabalho é focado na Engenharia e Análise de Dados do Censo da Educação Superior 2024, a base estatística mais recente e relevante do Ministério da Educação e do INEP.*  
>  
> *Para este projeto, consumimos o dataset oficial da Sinopse Estatística da Educação Superior, especificamente a Aba 1.1, que consolida todas as Instituições de Ensino Superior do Brasil por município, estado, região, organização acadêmica e categoria administrativa.*  
>  
> *O nosso primeiro desafio foi o carregamento: trata-se de um arquivo de alta densidade onde os dados foram transformados em DataFrames estruturados em Python via Pandas. Porém, ao inspecionar o arquivo bruto, percebemos que ele não estava pronto para análise estatística imediata, como meu colega João Pedro vai detalhar agora."*

---

### 👤 Parte 2: Diagnóstico Inicial e Problemas Encontrados
**Responsável Sugerido:** João Pedro Barbosa Moreira (2312662)  
**Slide:** 3 (Diagnóstico e Identificação Numérica dos Problemas)  
**Critérios da Atividade:** Critério 4 (`head`, `info`, `describe`) e Critério 5 (Identificação numérica de problemas).

#### 🎯 Objetivo da Fala:
Demonstrar a inspeção técnica inicial da base e quantificar com precisão matemática todos os problemas estruturais encontrados na planilha bruta.

#### 📌 Tópicos a Abordar:
1. **Inspeção Técnica com Pandas:** Uso das funções `head()`, `info()` e `describe()` na base bruta.
2. **Problema 1 — Cabeçalho Fragmentado:** 
   - 36 de 37 colunas vieram como `Unnamed` (97,3% das colunas sem nome legível).
   - 97 células nulas/mescladas nas linhas de metadados do topo (65,5% do cabeçalho vazio).
3. **Problema 2 — Símbolos Não Numéricos:**
   - 1.423 células preenchidas com o caractere traço `"-"` (convenção estatística do INEP para valor nulo/zero), impedindo operações matemáticas e forçando as colunas a serem lidas como `object`/string.
4. **Problema 3 — O Risco da Soma Ingênua (Subtotais Mesclados):**
   - O arquivo mistura linhas de detalhe com linhas agregadoras (Brasil, 5 Regiões e 27 Estados).
   - Se somássemos diretamente, o total de IES daria **10.244**, um erro de **400%** sobre o valor real (2.561 IES).

#### 🗣️ Roteiro de Fala Sugerido:
> *"Obrigado, Gustavo. Quando aplicamos o `head()`, `info()` e `describe()` logo após a leitura bruta, ficou claro que as planilhas do governo são desenhadas para leitura visual humana e não para computação de dados.*  
>  
> *Mapeamos três grandes problemas quantificados: primeiro, 97,3% das colunas vieram nomeadas como 'Unnamed', porque o INEP utilizou 4 linhas mescladas de cabeçalho. No cabeçalho bruto havia 97 células vazias.*  
>  
> *Segundo: encontramos exatamente 1.423 células com o caractere traço '-', que o INEP usa para representar zero. Isso corrompeu os tipos de dados, transformando números em texto.*  
>  
> *E o erro mais crítico: a planilha sobrepõe hierarquias. Na mesma coluna constavam o total do Brasil, os subtotais das Regiões, os totais dos Estados e as cidades. Uma soma ingênua retornava 10.244 instituições — quatro vezes o número real do país. Agora o Igor vai explicar o pilar de limpeza que resolveu essa árvore de dados."*

---

### 👤 Parte 3: O Pilar de Limpeza e Engenharia de Dados
**Responsável Sugerido:** Igor Augusto Ribeiro de Paula Martins (2312171)  
**Slide:** 4 (O Pilar de Limpeza e Comparação Antes vs. Depois)  
**Critérios da Atividade:** Critério 3 (Criação de Series) e Critério 6 (Limpeza do pilar do grupo: antes e depois).

#### 🎯 Objetivo da Fala:
Explicar a estratégia algorítmica de reconstrução dos cabeçalhos hierárquicos e a desagregação territorial, mostrando a tabela de "Antes vs. Depois".

#### 📌 Tópicos a Abordar:
1. **Reconstrução da Árvore de Cabeçalhos:**
   - Concatenação vertical das linhas de cabeçalho unidas pelo delimitador ` | `.
   - Uso de propagação horizontal segura (`ffill`) apenas nos níveis pai, sem deixar rótulos vazarem para categorias vizinhas (ex.: evitar que 'Pública' invadisse 'Privada').
2. **Tratamento dos Tipos de Dados:**
   - Substituição dos 1.423 traços `"-"` por `0` e conversão segura para `Int64`.
3. **Desagregação Territorial:**
   - Separação da primeira coluna em 3 dimensões analíticas: `nivel` (Brasil, Região, UF, Município), `local` e `categoria`.
4. **Criação de Series Univariada:**
   - Geração da Series `serie_uf` com o ranking do total de IES por estado.
5. **Validação Contábil (Antes vs. Depois):**
   - Comprovação de que a soma dos 27 estados (2.561) e das 5 regiões (2.561) bate com 100% de exatidão com o total nacional.

#### 🗣️ Roteiro de Fala Sugerido:
> *"Obrigado, João. Nosso pilar de limpeza foi a 'Resolução de Cabeçalhos Hierárquicos Mesclados'. Desenvolvemos um algoritmo que percorre as camadas superiores da planilha, aplica o `ffill()` horizontal condicional apenas aos nós superiores e concatena os níveis com barra vertical.*  
>  
> *Com isso, uma coluna antes chamada 'Unnamed: 12' virou: 'Total | Privada | Com fins lucrativos | Faculdade'. Nenhuma informação semântica foi perdida.*  
>  
> *Depois, convertemos os 1.423 traços em zero e tipamos as colunas como inteiros 'Int64'. Na dimensão geográfica, separamos o que era Brasil, Região e Estado através de filtros de domínio. Criamos também a Series univariada `serie_uf`, que indexa cada estado ao seu volume de faculdades e universidades.*  
>  
> *No 'Antes e Depois', eliminamos 100% das inconsistências e garantimos a convergência contábil perfeita: a soma dos 27 estados resultou exatamente em 2.561 IES, eliminando a duplicação. Passo a palavra para o Ygor apresentar a integração com a Web e API."*

---

### 👤 Parte 4: Destaque Web Scraping e Consumo de API Pública
**Responsável Sugerido:** Ygor Gomes Rocha (2312663)  
**Slide:** 5 (Destaque: Web Scraping, API do IBGE e Indicadores)  
**Critérios da Atividade:** Critério 7 / Destaque 4 (Leitura Web com `read_html`, API pública, tratamento de erro 403 e reflexão sobre confiabilidade).

#### 🎯 Objetivo da Fala:
Demonstrar a integração do dataset do INEP com dados externos coletados via Web Scraping (`pandas.read_html()`) e API REST oficial do IBGE, destacando o tratamento de erros HTTP.

#### 📌 Tópicos a Abordar:
1. **Por que Enriquecer os Dados?**
   - Saber o número absoluto de IES por estado é insuficiente (São Paulo tem mais IES porque tem mais habitantes). É preciso medir a **densidade por habitante**.
2. **Web Scraping com `pd.read_html()`:**
   - Extração da tabela demográfica da Wikipédia baseada no Censo do IBGE.
   - **Tratamento do Erro HTTP 403 (Forbidden):** A Wikipédia bloqueia requisições padrão de bots do Python. A solução foi injetar um cabeçalho HTTP simulando um navegador real (`headers={'User-Agent': 'Mozilla/5.0...'}`) via biblioteca `requests` e repassar o HTML para o `read_html()`.
3. **Consumo de API REST do IBGE:**
   - Consumo da API de Localidades (`https://servicodados.ibge.gov.br/api/v1/localidades/estados`).
   - Normalização de nomes acentuados e mapeamento automatizado das siglas oficiais de cada UF.
4. **Reflexão sobre Confiabilidade:**
   - Comparação entre dados do INEP (fonte primária governamental com fé pública) e Wikipédia/IBGE (atualização periódica e necessidade de validação).

#### 🗣️ Roteiro de Fala Sugerido:
> *"Obrigado, Igor. Para o critério de destaque da nossa atividade, fomos além dos arquivos locais e enriquecemos nossa base com dados externos via Web Scraping e consumo de API.*  
>  
> *Olhar apenas para números brutos gera distorções: São Paulo tem 580 faculdades, mas tem 44 milhões de habitantes. Queríamos descobrir a densidade educacional por habitante.*  
>  
> *Para isso, utilizamos o `pandas.read_html()` para raspar a tabela demográfica da Wikipédia. Ao fazer isso, enfrentamos o clássico erro 'HTTP 403 Forbidden', pois a Wikipédia rejeita requisições automatizadas sem identificação. Resolvemos esse problema configurando a biblioteca `requests` com cabeçalho 'User-Agent' de navegador real.*  
>  
> *Em seguida, consumimos a API REST oficial de Localidades do IBGE para obter a lista padronizada de estados e siglas. Fizemos o merge dos três datasets e calculamos a métrica de 'IES por 1 Milhão de Habitantes'. Agora o Elton vai apresentar os resultados surpreendentes dessa análise."*

---

### 👤 Parte 5: Descobertas, Indicadores, Dificuldades e Conclusão
**Responsável Sugerido:** Elton Dourado De Azevedo Filho (2310514)  
**Slides:** 6 (Grandes Descobertas e Perfil Nacional), 7 (Ranking Per Capita) e 8 (Dificuldades e Encerramento)  
**Critérios da Atividade:** Apresentação de descobertas, síntese comparativa e fechamento executivo.

#### 🎯 Objetivo da Fala:
Apresentar os principais achados analíticos do Censo 2024, comparar os dados absolutos com os dados per capita, relatar os desafios técnicos superados e concluir a apresentação.

#### 📌 Tópicos a Abordar:
1. **Panorama Geral da Educação Superior 2024:**
   - **2.561 IES** no país.
   - **Rede Privada domina amplamente:** 2.244 instituições (**87,6%**), sendo 1.486 particulares com fins lucrativos.
   - **Rede Pública:** Apenas 317 instituições (**12,4%**), das quais 122 são federais e 139 estaduais.
   - **Formato Acadêmico:** 74,1% são Faculdades, 16,3% Centros Universitários e apenas 8,0% Universidades.
2. **Concentração Regional Absoluta:**
   - Sudeste concentra 42,0% (1.076 IES).
   - Top 5 estados (SP, MG, PR, BA e GO) concentram 51,8% de todas as faculdades e universidades do país.
3. **A Grande Revelação: O Indicador Per Capita:**
   - Quando cruzamos com a população, o ranking inverte completamente:
   - **1º lugar em densidade:** **Distrito Federal**, com **20,93 IES por milhão de habitantes**.
   - **2º lugar:** **Mato Grosso**, com **18,73**.
   - **São Paulo**, líder absoluto em quantidade, cai para a **13ª posição** em densidade relativa (13,05 IES por milhão).
4. **Principais Dificuldades Enfrentadas:**
   - Manipulação de planilha de mais de 300 MB;
   - Complexidade das células mescladas sem perder a semântica;
   - Burlar o bloqueio 403 da Wikipédia de forma ética e eficiente.
5. **Conclusão e Encerramento:** Abertura para dúvidas da banca.

#### 🗣️ Roteiro de Fala Sugerido:
> *"Obrigado, Ygor. Fechando nossa análise com os resultados, chegamos a descobertas fundamentais sobre o ensino superior no Brasil em 2024.*  
>  
> *Primeiro: o ensino superior brasileiro é maciçamente privado. Das 2.561 instituições, 87,6% pertencem à iniciativa privada, e 74% de todas as instituições são estruturadas como faculdades isoladas, e não como universidades voltadas à pesquisa.*  
>  
> *Segundo: em números absolutos, há uma brutal concentração no Sudeste, que abriga 42% das instituições. São Paulo sozinho detém quase 23% do total nacional.*  
>  
> *No entanto, a nossa grande descoberta foi possibilitada pelo indicador de 'IES por Milhão de Habitantes': o estado com maior densidade de ensino superior não é São Paulo nem o Rio de Janeiro, mas sim o Distrito Federal, com quase 21 IES por milhão de pessoas, seguido de perto por Mato Grosso, com 18,7. São Paulo aparece apenas em 13º lugar relativo.*  
>  
> *Como principais dificuldades, enfrentamos a manipulação de um arquivo Excel de mais de 300 megabytes, o risco contábil de quadruplicar os totais e o bloqueio HTTP 403 da Wikipédia.*  
>  
> *Entregamos todo o pipeline documentado, sem comentários no código Python, com relatório técnico completo em PDF e código versionado no GitHub. Agradecemos a atenção de todos e estamos à disposição para dúvidas da banca!"*

---

## 🔄 Transições Recomendadas Entre Integrantes

- **Gustavo ➔ João Pedro:** *"Porém, logo na leitura dos dados brutos, nos deparamos com barreiras estruturais severas. O João Pedro vai demonstrar o diagnóstico técnico desses problemas."*
- **João Pedro ➔ Igor:** *"Para corrigir esse cenário sem perder dados e sem tolerar duplicações, estruturamos o nosso pilar de engenharia de dados. O Igor vai explicar o algoritmo de limpeza."*
- **Igor ➔ Ygor:** *"Com a base limpa e validada, precisávamos torná-la ainda mais informativa com dados externos. O Ygor vai mostrar como integramos Web Scraping e API."*
- **Ygor ➔ Elton:** *"Com a base unificada e a métrica de densidade calculada, os padrões reais do país emergiram. O Elton vai apresentar essas descobertas e concluir o trabalho."*

---

## 🎯 Perguntas Prováveis da Banca e Quem Responde

| Pergunta Provável da Banca | Integrante Indicado | Resposta Chave a Destacar |
|:---|:---:|:---|
| *"Por que vocês não usaram apenas `dropna()` para limpar as linhas vazias?"* | **Igor / João** | Explicar que as linhas de cabeçalho mescladas continham informações semânticas vitais nos nós pais; um `dropna()` ingênuo teria apagado os nomes das colunas e quebrado a hierarquia. |
| *"Como foi contornado o erro 403 na Wikipédia?"* | **Ygor** | Destacar o envio do cabeçalho `User-Agent: Mozilla/5.0` via `requests.get()` simulando um navegador real, passando o HTML resultante para `pd.read_html()`. |
| *"Como vocês garantiram que não havia dados duplicados ou perdas de instituições?"* | **Igor / Gustavo** | Citar o teste de integridade contábil: soma de UFs = 2.561, soma de Regiões = 2.561 e Total Brasil = 2.561. |
| *"O que o indicador por milhão de habitantes mudou na interpretação?"* | **Elton** | Mostrar que SP lidera em volume absoluto pelo tamanho de sua população, mas estados do Centro-Oeste (DF e MT) oferecem maior proporção de instituições por residente. |
