import io
import unicodedata
import zipfile
from pathlib import Path
import pandas as pd
import requests
try:
    display
except NameError:
    display = print
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 200)
PASTA = Path(__file__).resolve().parent
print('Pasta de trabalho:', PASTA)
ABA = '1.1'
LINHAS_CABECALHO = None
PAGINA_INEP = 'https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/sinopses-estatisticas/educacao-superior-graduacao'
BASE = 'https://download.inep.gov.br/'
URLS = [BASE + 'dados_abertos/sinopses_estatisticas/sinopses_estatisticas_censo_da_educacao_superior_2024.zip', BASE + 'dados_abertos/sinopses_estatisticas/sinopses_estatisticas_censo_da_educacao_superior_2023.zip', BASE + 'informacoes_estatisticas/sinopses_estatisticas/sinopses_educacao_superior/sinopse_educacao_superior_2022.zip']
try:
    from google.colab import files as colab_files
except ImportError:
    colab_files = None

def extrair_zip(conteudo_zip, pasta_destino=None):
    destino = pasta_destino or PASTA
    with zipfile.ZipFile(io.BytesIO(conteudo_zip)) as z:
        for nome in z.namelist():
            if nome.lower().endswith('.xlsx') and (not Path(nome).name.startswith('~$')):
                caminho_saida = destino / Path(nome).name
                caminho_saida.write_bytes(z.read(nome))

def escolher_xlsx():
    melhor, nota_melhor = (None, 0)
    for p in sorted(PASTA.rglob('*.xlsx')):
        if p.name.startswith('~$'):
            continue
        try:
            abas = pd.ExcelFile(p).sheet_names
        except Exception as erro:
            print(f'  {p.name}: não abriu ({type(erro).__name__})')
            continue
        print(f'  {p.name}: {len(abas)} aba(s)', abas[:5])
        nota = 2 if ABA in [a.strip() for a in abas] else 1 if any((ABA in a for a in abas)) else 0
        if nota > nota_melhor:
            melhor, nota_melhor = (p, nota)
    return melhor

def obter_arquivo():
    achado = escolher_xlsx()
    if achado:
        return (achado, f'arquivo local em {achado.parent} ({achado.name})')
    for p in sorted(PASTA.rglob('*.zip')):
        try:
            extrair_zip(p.read_bytes())
            print('Zip extraído:', p.name)
        except zipfile.BadZipFile:
            print('Zip incompleto ou corrompido, ignorado:', p.name)
    achado = escolher_xlsx()
    if achado:
        return (achado, f'arquivo local extraído do zip ({achado.name})')
    for url in URLS:
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=(15, 180))
            r.raise_for_status()
            extrair_zip(r.content)
        except (requests.RequestException, zipfile.BadZipFile) as erro:
            print('Não deu certo:', url)
            print('   motivo:', type(erro).__name__, '-', str(erro)[:120])
            continue
        achado = escolher_xlsx()
        if achado:
            return (achado, url)
    if colab_files:
        print()
        print('Baixe a Sinopse mais recente em', PAGINA_INEP)
        print('e escolha o .zip ou .xlsx no botão abaixo:')
        for nome, conteudo in colab_files.upload().items():
            if nome.lower().endswith('.zip'):
                extrair_zip(conteudo)
        achado = escolher_xlsx()
        if achado:
            return (achado, 'arquivo baixado de ' + PAGINA_INEP + ' e enviado como ' + achado.name)
    raise FileNotFoundError(f'Nenhum Excel com a aba {ABA!r} em {PASTA}. Certifique-se de que o arquivo sinopse_educacao_superior_2024.zip ou os arquivos .xlsx descompactados estão na pasta.')
ARQUIVO, ORIGEM = obter_arquivo()
print('\nArquivo selecionado:', ARQUIVO)
print('Origem             :', ORIGEM)
print('Página oficial     :', PAGINA_INEP)
planilha = pd.ExcelFile(ARQUIVO)
abas = planilha.sheet_names
print(f'\n{len(abas)} abas no arquivo. Primeiras:', abas[:12])
if ABA not in abas:
    parecidas = [a for a in abas if ABA in a]
    if parecidas:
        ABA = parecidas[0]
    elif len(abas) == 1:
        ABA = abas[0]
        print(f"Aviso: Aba '{ABA}' selecionada automaticamente por ser a única disponível.")
    else:
        raise ValueError(f'A aba {ABA!r} não existe. Troque a variável ABA por uma destas: {abas}')
print('Aba escolhida:', repr(ABA))
ingenuo = planilha.parse(ABA)
print('\n--- Leitura Ingênua (padrão) ---')
print('Formato:', ingenuo.shape)
print('Nomes das primeiras 6 colunas na leitura padrão:')
print(list(ingenuo.columns[:6]))
display(ingenuo.head(8))
bruto = planilha.parse(ABA, header=None)
print('\n--- Leitura Bruta (header=None) ---')
print('shape:', bruto.shape)
colunas_vazias = int(bruto.isna().all().sum())
bruto = bruto.dropna(axis=1, how='all')
bruto.columns = range(bruto.shape[1])
print('Colunas totalmente vazias descartadas:', colunas_vazias)
display(bruto.head(12))
print('\n--- Informações do DataFrame Bruto ---')
bruto.info()
print('\n--- Resumo Estatístico Inicial ---')
display(bruto.describe(include='all').T.head(15))

def mapear_planilha(bruto, linhas_cabecalho=None):
    qtd_numeros = bruto.iloc[:, 1:].apply(pd.to_numeric, errors='coerce').notna().sum(axis=1)
    linha_de_dados = bruto[0].notna() & (qtd_numeros >= qtd_numeros.max() / 2)
    inicio = int(linha_de_dados.idxmax())
    fim = int(linha_de_dados[::-1].idxmax())
    if linhas_cabecalho is None:
        tem_rotulo = bruto.iloc[:inicio, 1:].notna().any(axis=1)
        linhas_cabecalho = []
        for i in range(inicio - 1, -1, -1):
            if tem_rotulo[i]:
                linhas_cabecalho.insert(0, i)
            elif linhas_cabecalho:
                break
    return {'titulo': [i for i in range(min(linhas_cabecalho)) if bruto.loc[i].notna().any()], 'cabecalho': list(linhas_cabecalho), 'inicio_dados': inicio, 'fim_dados': fim, 'rodape': [i for i in range(fim + 1, len(bruto)) if bruto.loc[i].notna().any()]}
mapa = mapear_planilha(bruto, LINHAS_CABECALHO)
print('\n--- Mapeamento Estrutural da Planilha ---')
print('Linhas de título   :', mapa['titulo'])
print('Linhas de cabeçalho:', mapa['cabecalho'])
print('Dados              : da linha', mapa['inicio_dados'], 'até a', mapa['fim_dados'])
print('Linhas de rodapé   :', mapa['rodape'])
print()
titulo_tabela = ' '.join((str(v) for i in mapa['titulo'] for v in bruto.loc[i].dropna()))
print('Título da tabela:', titulo_tabela)
cab_bruto = bruto.loc[mapa['cabecalho']]
print('\nCabeçalho como está no Excel (NaN = célula que fazia parte de uma mesclagem):')
display(cab_bruto)
bloco = bruto.loc[mapa['inicio_dados']:mapa['fim_dados']]
valores_brutos = bloco.iloc[:, 1:]
eh_texto = valores_brutos.apply(lambda col: col.map(lambda v: isinstance(v, str)))
rotulos_brutos = bloco[0].dropna().astype(str)
problemas = pd.Series({"Colunas 'Unnamed' na leitura padrão": f'{sum((str(c).startswith('Unnamed') for c in ingenuo.columns))} de {ingenuo.shape[1]}', 'Linhas de cabeçalho (níveis mesclados)': len(mapa['cabecalho']), 'Células vazias dentro do cabeçalho': f'{int(cab_bruto.isna().sum().sum())} de {cab_bruto.size} ({cab_bruto.isna().sum().sum() / cab_bruto.size:.0%})', 'Linhas que não são dados (título, cabeçalho, rodapé, vazias)': f'{len(bruto) - len(bloco.dropna(how='all'))} de {len(bruto)}', 'Colunas totalmente vazias': colunas_vazias, 'Colunas de valores lidas como texto (object)': f'{int((valores_brutos.dtypes == object).sum())} de {valores_brutos.shape[1]}', "Células com símbolo no lugar de número (ex.: '-')": int(eh_texto.sum().sum()), 'Rótulos com espaços sobrando (recuo)': int((rotulos_brutos != rotulos_brutos.str.strip()).sum()), 'Rótulos repetidos na 1ª coluna': int(rotulos_brutos.str.strip().duplicated().sum())})
print('\n--- PROBLEMAS ENCONTRADOS ---')
display(problemas.to_frame('quantidade'))
if eh_texto.sum().sum():
    print('\nSímbolos encontrados nas colunas de valores:')
    print(pd.Series(valores_brutos.values[eh_texto.values]).value_counts().head())

def achatar_cabecalho(cab):
    niveis = []
    for i in range(len(cab)):
        linha = cab.iloc[i]
        if not niveis:
            linha = linha.ffill()
        else:
            pai = pd.Series(list(zip(*[n.fillna('') for n in niveis])), index=linha.index)
            linha = linha.groupby(pai).ffill()
        niveis.append(linha)
    niveis = pd.DataFrame(niveis)
    nomes = []
    for col in niveis.columns:
        partes = [' '.join(str(p).split()) for p in niveis[col].dropna()]
        partes = [p for k, p in enumerate(partes) if k == 0 or p != partes[k - 1]]
        nomes.append(' | '.join(partes))
    return (nomes, niveis)
colunas_validas = bloco.columns[bloco.notna().any()]
nomes, cab_preenchido = achatar_cabecalho(cab_bruto[colunas_validas])
print('\nCabeçalho DEPOIS de preencher as mesclagens:')
display(cab_preenchido)
primeiras = {n.split(' | ')[0] for n in nomes[1:]}
if len(primeiras) == 1 and all((' | ' in n for n in nomes[1:])):
    geral = primeiras.pop()
    nomes = [nomes[0]] + [n.split(' | ', 1)[1] for n in nomes[1:]]
    print('\nRótulo geral removido de todas as colunas:', repr(geral))
rotulo_original = nomes[0]
nomes[0] = 'rotulo'
assert len(set(nomes)) == len(nomes), 'Há nomes de coluna repetidos: confira LINHAS_CABECALHO'
df = bloco[colunas_validas].copy()
df.columns = nomes
df = df.dropna(how='all').reset_index(drop=True)
print('\n1ª coluna no Excel:', repr(rotulo_original))
print('\nNomes das colunas depois da limpeza:')
for n in df.columns:
    print('  -', n)
try:
    multi = planilha.parse(ABA, header=mapa['cabecalho'])
    sobras = sum(('Unnamed' in str(parte) for col in multi.columns for parte in col))
    print(f"\nCom header={mapa['cabecalho']} -> {multi.columns.nlevels} níveis e {sobras} rótulos 'Unnamed' ainda sobrando")
    print('Exemplo das primeiras 4 colunas nativas:', list(multi.columns[:4]))
except Exception as erro:
    print('header=[...] não funcionou nesta aba:', type(erro).__name__, erro)
colunas_valor = list(df.columns[4:])
tipos_antes = df[colunas_valor].dtypes.astype(str).value_counts()
for c in colunas_valor:
    texto = df[c].astype(str).str.strip().replace({'-': '0'})
    df[c] = pd.to_numeric(texto, errors='coerce')
    if (df[c].dropna() % 1 == 0).all():
        df[c] = df[c].astype('Int64')
print('\nTipos ANTES :', dict(tipos_antes))
print('Tipos DEPOIS:', dict(df[colunas_valor].dtypes.astype(str).value_counts()))
print('Valores ausentes depois da conversão:', int(df[colunas_valor].isna().sum().sum()))

def normalizar(texto):
    return unicodedata.normalize('NFKD', str(texto)).encode('ascii', 'ignore').decode().strip().lower()
df['Região Geográfica'] = df['rotulo'].astype(str).str.strip()

def determinar_nivel(row):
    reg = str(row['Região Geográfica']).strip()
    uf = str(row.get('Unidade da Federação', '')).strip()
    mun = str(row.get('Município', '')).strip()
    if 'Brasil' in reg:
        return ('Brasil', 'Brasil')
    elif 'Total' in reg or pd.isna(row.get('Unidade da Federação')) or uf in ('<NA>', 'nan', 'NaN', 'None', ''):
        return ('Região', reg.replace('Total', '').strip())
    elif 'Total' in uf or pd.isna(row.get('Município')) or mun in ('<NA>', 'nan', 'NaN', 'None', ''):
        return ('UF', uf.replace('Total', '').strip())
    else:
        return ('Município', mun)
df[['nivel', 'local']] = df.apply(determinar_nivel, axis=1, result_type='expand')
df['categoria'] = 'Total'
cols_hierarquia = ['nivel', 'local', 'categoria', 'Região Geográfica', 'Unidade da Federação', 'Município', 'Código do Município']
df = df[cols_hierarquia + colunas_valor]
print('\n--- Distribuição por Nível ---')
print(df['nivel'].value_counts())
print('\nCategorias encontradas:', list(df['categoria'].unique()))
COL_TOTAL_candidates = [c for c in colunas_valor if c.endswith('| Total')]
COL_TOTAL = COL_TOTAL_candidates[0] if COL_TOTAL_candidates else colunas_valor[0]
df_uf = df[(df['nivel'] == 'UF') & (df['categoria'] == 'Total')].reset_index(drop=True)
antes_depois = pd.DataFrame({'Antes (leitura do Excel)': [f'{bruto.shape[0]} x {bruto.shape[1]}', sum((str(c).startswith('Unnamed') for c in ingenuo.columns)), int(cab_bruto.isna().sum().sum()), len(bruto) - len(bloco.dropna(how='all')), int((valores_brutos.dtypes == object).sum()), int(eh_texto.sum().sum()), '1 coluna com local e categoria misturados'], 'Depois (limpo)': [f'{df.shape[0]} x {df.shape[1]}', sum((str(c).startswith('Unnamed') for c in df.columns)), 0, 0, int((df[colunas_valor].dtypes == object).sum()), 0, '3 colunas: nivel, local, categoria']}, index=['Formato (linhas x colunas)', "Colunas sem nome ('Unnamed')", 'Células vazias no cabeçalho', 'Linhas que não são dados', 'Colunas de valores como texto', 'Símbolos no lugar de números', 'Primeira coluna'])
print('\n--- TABELA COMPARATIVA (Antes x Depois) ---')
display(antes_depois)
print('\nPrimeiras 10 linhas do DataFrame Limpo:')
display(df.head(10))
print('\nInformações do DataFrame Limpo:')
df.info()
print('\nEstatísticas das UFs:')
display(df_uf[colunas_valor].describe().T)
serie_uf = df_uf.set_index('local')[COL_TOTAL].sort_values(ascending=False)
serie_uf.name = 'instituicoes'
print('\n--- Series: Instituições por UF ---')
print(type(serie_uf))
print(f'Tamanho: {serie_uf.size} | Maior: {serie_uf.idxmax()} ({serie_uf.max()}) | Menor: {serie_uf.idxmin()} ({serie_uf.min()})')
print(f'Média por UF: {round(serie_uf.mean(), 1)} | Mediana: {serie_uf.median()}')
print('\nTop 10 UFs:')
display(serie_uf.head(10))
brasil = df[(df['nivel'] == 'Brasil') & (df['categoria'] == 'Total')]
regioes = df[(df['nivel'] == 'Região') & (df['categoria'] == 'Total')]
print('\n--- Validação Estatística e Hierárquica ---')
print('Estados (UF) encontrados:', len(df_uf), '(esperado: 27)')
print('Regiões encontradas     :', len(regioes), '(esperado: 5)')
if len(brasil) == 1:
    total_brasil = int(brasil[COL_TOTAL].iloc[0])
    soma_ufs = int(df_uf[COL_TOTAL].sum())
    soma_regioes = int(regioes[COL_TOTAL].sum())
    colunas_ok = int((df_uf[colunas_valor].sum() == brasil[colunas_valor].iloc[0]).sum())
    soma_sem_limpar = int(df[COL_TOTAL].sum())
    print(f'Total Brasil na planilha: {total_brasil}')
    print(f'Soma dos estados        : {soma_ufs}  ->', 'OK' if soma_ufs == total_brasil else 'DIFERENTE')
    print(f'Soma das regiões        : {soma_regioes}  ->', 'OK' if soma_regioes == total_brasil else 'DIFERENTE')
    print(f'Colunas em que a soma dos estados bate com o Brasil: {colunas_ok} de {len(colunas_valor)}')
    print(f'Somando a coluna sem limpar daria {soma_sem_limpar}, {soma_sem_limpar / total_brasil:.1f} vezes o valor real (totais contados várias vezes).')
else:
    print("Não achei uma linha única 'Brasil' nesta aba; confira o conteúdo de df['local'].")
print('\n--- DESCOBERTAS E INSIGHTS ANALÍTICOS ---')
print('Tabela analisada:', titulo_tabela)
print()
total = int(serie_uf.sum())
print(f'1) O país tem {total} instituições de educação superior nesta tabela.')
top5 = serie_uf.head(5)
print(f'2) {serie_uf.idxmax()} lidera com {int(serie_uf.max())} ({serie_uf.max() / total:.1%} do total). Os 5 primeiros estados somam {top5.sum() / total:.1%}.')
print(f'   Menor número: {serie_uf.idxmin()}, com {int(serie_uf.min())}.')
print('\nTop 5 estados:')
display(top5.to_frame())
col_pub = [c for c in colunas_valor if 'publica | total' in normalizar(c)]
col_pri = [c for c in colunas_valor if 'privada | total' in normalizar(c)]
if col_pub and col_pri and (len(brasil) == 1):
    v_pub = int(brasil[col_pub[0]].iloc[0])
    v_pri = int(brasil[col_pri[0]].iloc[0])
    print(f'3) Rede privada: {v_pri} instituições ({v_pri / total:.1%}); rede pública: {v_pub} ({v_pub / total:.1%}).')
else:
    br = df[df['nivel'] == 'Brasil'].set_index('categoria')[COL_TOTAL]
    pub = [c for c in br.index if normalizar(c) == 'publica']
    pri = [c for c in br.index if normalizar(c) == 'privada']
    if pub and pri:
        print(f'3) Rede privada: {int(br[pri[0]])} instituições ({br[pri[0]] / br['Total']:.1%}); rede pública: {int(br[pub[0]])} ({br[pub[0]] / br['Total']:.1%}).')
cap = [c for c in colunas_valor if normalizar(c.split(' | ')[-1]) == 'capital']
inte = [c for c in colunas_valor if normalizar(c.split(' | ')[-1]) == 'interior']
if cap and inte and (len(brasil) == 1):
    v_cap, v_int = (int(brasil[cap[0]].iloc[0]), int(brasil[inte[0]].iloc[0]))
    print(f'4) Localização: {v_cap} em capitais ({v_cap / (v_cap + v_int):.1%}) e {v_int} no interior ({v_int / (v_cap + v_int):.1%}).')
if len(regioes):
    por_regiao = regioes.set_index('local')[COL_TOTAL].sort_values(ascending=False)
    print('\n5) Instituições por região:')
    display(por_regiao.to_frame())
col_univ = [c for c in colunas_valor if 'universidade | total' in normalizar(c)]
col_cent = [c for c in colunas_valor if 'centro universitario | total' in normalizar(c)]
col_fac = [c for c in colunas_valor if 'faculdade | total' in normalizar(c)]
if col_univ and col_cent and col_fac and (len(brasil) == 1):
    v_univ = int(brasil[col_univ[0]].iloc[0])
    v_cent = int(brasil[col_cent[0]].iloc[0])
    v_fac = int(brasil[col_fac[0]].iloc[0])
    df_tipos = pd.DataFrame({'instituicoes': [v_fac, v_cent, v_univ], 'percentual': [f'{v_fac / total:.1%}', f'{v_cent / total:.1%}', f'{v_univ / total:.1%}']}, index=['Faculdade', 'Centro Universitário', 'Universidade'])
    print('\n6) Instituições por organização acadêmica (Brasil):')
    display(df_tipos)
else:
    tipos = [c for c in colunas_valor[1:] if normalizar(c.split(' | ')[-1]) == 'total']
    if tipos and len(brasil) == 1:
        por_tipo = brasil[tipos].iloc[0].sort_values(ascending=False)
        por_tipo.index = [c.split(' | ')[0] for c in por_tipo.index]
        print('\n6) Instituições por organização acadêmica (Brasil):')
        display(por_tipo.to_frame('instituicoes'))
print('\n--- INTEGRAÇÃO DE DADOS DA WEB E API ---')
URL_WIKI_POP = 'https://pt.wikipedia.org/wiki/Lista_de_unidades_federativas_do_Brasil_por_popula%C3%A7%C3%A3o'
headers_web = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
print(f'1) Coletando dados demográficos da Web via read_html():\n   URL: {URL_WIKI_POP}')
try:
    resposta_wiki = requests.get(URL_WIKI_POP, headers=headers_web, timeout=15)
    resposta_wiki.raise_for_status()
    tabelas_wiki = pd.read_html(io.StringIO(resposta_wiki.text))
    tabela_pop_raw = tabelas_wiki[1]
    col_estado = tabela_pop_raw.iloc[:, 0].astype(str)
    col_habitantes = tabela_pop_raw.iloc[:, 1].astype(str).str.replace('\\D', '', regex=True)
    df_populacao = pd.DataFrame({'local': col_estado, 'populacao': pd.to_numeric(col_habitantes, errors='coerce')}).dropna()
    df_populacao['local_norm'] = df_populacao['local'].apply(normalizar)
    print(f'   -> Sucesso! {len(df_populacao)} estados lidos da Wikipédia via read_html().')
except requests.exceptions.HTTPError as e:
    print(f'   Aviso: Falha HTTP ({e.response.status_code}) ao acessar a Wikipédia.')
    df_populacao = pd.DataFrame()
except Exception as e:
    print(f'   Aviso: Não foi possível processar a tabela da Wikipédia: {e}')
    df_populacao = pd.DataFrame()
URL_API_IBGE = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
print(f'\n2) Consumindo API pública oficial de Localidades do IBGE:\n   URL: {URL_API_IBGE}')
try:
    resp_ibge = requests.get(URL_API_IBGE, headers=headers_web, timeout=15)
    resp_ibge.raise_for_status()
    dados_ibge = resp_ibge.json()
    df_ibge = pd.DataFrame([{'id_uf_ibge': item['id'], 'sigla_uf': item['sigla'], 'nome_uf': item['nome'], 'regiao_ibge': item['regiao']['nome']} for item in dados_ibge])
    df_ibge['local_norm'] = df_ibge['nome_uf'].apply(normalizar)
    print(f'   -> Sucesso! {len(df_ibge)} estados integrados via API do IBGE.')
except Exception as e:
    print(f'   Aviso: Não foi possível consumir a API do IBGE: {e}')
    df_ibge = pd.DataFrame()
if not df_populacao.empty and (not df_ibge.empty):
    df_analise_uf = df_uf[['local', COL_TOTAL]].copy()
    df_analise_uf['local_norm'] = df_analise_uf['local'].apply(normalizar)
    df_enriquecido = pd.merge(df_analise_uf, df_ibge[['local_norm', 'sigla_uf', 'id_uf_ibge', 'regiao_ibge']], on='local_norm', how='left')
    df_enriquecido = pd.merge(df_enriquecido, df_populacao[['local_norm', 'populacao']], on='local_norm', how='left')
    df_enriquecido.rename(columns={COL_TOTAL: 'total_ies'}, inplace=True)
    df_enriquecido['ies_por_milhao_hab'] = (df_enriquecido['total_ies'] / (df_enriquecido['populacao'] / 1000000)).round(2)
    df_enriquecido = df_enriquecido.sort_values(by='ies_por_milhao_hab', ascending=False).reset_index(drop=True)
    colunas_exibir = ['sigla_uf', 'local', 'regiao_ibge', 'total_ies', 'populacao', 'ies_por_milhao_hab']
    print('\n--- Ranking de Densidade de IES por 1 Milhão de Habitantes (Top 10) ---')
    display(df_enriquecido[colunas_exibir].head(10))
    saida_enriquecida = PASTA / 'sinopse_com_indicadores_web.csv'
    df_enriquecido[colunas_exibir].to_csv(saida_enriquecida, sep=';', index=False, encoding='utf-8-sig')
    print('\nDataset enriquecido com dados da Web/API salvo em:', saida_enriquecida)
saida = PASTA / 'sinopse_limpa.csv'
df.to_csv(saida, sep=';', index=False, encoding='utf-8-sig')
print('\nArquivo limpo salvo em:', saida)
if __name__ == '__main__':
    print('\nExecução finalizada com sucesso!')