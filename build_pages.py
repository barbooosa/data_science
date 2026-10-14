import html
from pathlib import Path

PASTA = Path(__file__).resolve().parent
arquivo_saida = PASTA / 'saida_execucao.txt'
texto_saida = arquivo_saida.read_text(encoding='utf-8')

saida_escapada = html.escape(texto_saida)

html_template = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Grupo 2 — Execução do Pipeline e Análise de Dados (Censo 2024 / INEP)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --primary: #2563eb;
      --primary-dark: #1d4ed8;
      --primary-light: #60a5fa;
      --bg: #0b0f19;
      --card-bg: #111827;
      --card-border: #1f2937;
      --text: #f3f4f6;
      --text-muted: #9ca3af;
      --accent: #10b981;
      --accent-warning: #f59e0b;
      --terminal-bg: #030712;
      --terminal-header: #1f2937;
      --code-font: 'Fira Code', monospace;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding-bottom: 60px;
    }}
    header {{
      background: linear-gradient(180deg, rgba(37,99,235,0.15) 0%, rgba(11,15,25,0) 100%);
      border-bottom: 1px solid var(--card-border);
      padding: 40px 20px 30px;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 20px;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 600;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      background: rgba(37,99,235,0.2);
      color: var(--primary-light);
      border: 1px solid rgba(37,99,235,0.4);
      margin-bottom: 16px;
    }}
    .badge-success {{
      background: rgba(16,185,129,0.2);
      color: var(--accent);
      border-color: rgba(16,185,129,0.4);
    }}
    h1 {{
      font-size: 2.2rem;
      font-weight: 800;
      margin-bottom: 10px;
      background: linear-gradient(90deg, #ffffff, #93c5fd);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
      color: var(--text-muted);
      font-size: 1.1rem;
      margin-bottom: 24px;
      max-width: 850px;
    }}
    .nav-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 20px;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: var(--card-bg);
      color: var(--text);
      border: 1px solid var(--card-border);
      padding: 10px 18px;
      border-radius: 8px;
      font-size: 0.9rem;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s ease;
      cursor: pointer;
    }}
    .btn:hover {{
      background: #1f2937;
      border-color: var(--primary-light);
      transform: translateY(-2px);
    }}
    .btn-primary {{
      background: var(--primary);
      border-color: var(--primary);
      color: #fff;
    }}
    .btn-primary:hover {{
      background: var(--primary-dark);
      border-color: var(--primary-dark);
    }}
    .team-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin: 30px 0;
    }}
    .member-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      padding: 16px;
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      transition: border-color 0.2s;
    }}
    .member-card:hover {{
      border-color: rgba(59,130,246,0.5);
    }}
    .member-name {{
      font-weight: 600;
      font-size: 0.95rem;
      color: #fff;
    }}
    .member-id {{
      font-family: var(--code-font);
      font-size: 0.85rem;
      color: var(--primary-light);
    }}
    .stats-row {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 30px;
    }}
    .stat-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 20px;
      text-align: center;
    }}
    .stat-val {{
      font-size: 2rem;
      font-weight: 800;
      color: #fff;
      font-family: var(--code-font);
    }}
    .stat-lbl {{
      color: var(--text-muted);
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-top: 4px;
    }}
    .terminal-container {{
      background: var(--terminal-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 20px 40px rgba(0,0,0,0.5);
      margin-bottom: 40px;
    }}
    .terminal-header {{
      background: var(--terminal-header);
      padding: 12px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #374151;
    }}
    .terminal-dots {{
      display: flex;
      gap: 8px;
    }}
    .dot {{
      width: 12px;
      height: 12px;
      border-radius: 50%;
    }}
    .dot-red {{ background: #ef4444; }}
    .dot-yellow {{ background: #f59e0b; }}
    .dot-green {{ background: #10b981; }}
    .terminal-title {{
      font-family: var(--code-font);
      font-size: 0.85rem;
      color: #9ca3af;
    }}
    .terminal-actions {{
      display: flex;
      gap: 8px;
    }}
    .btn-sm {{
      padding: 4px 10px;
      font-size: 0.75rem;
      background: #374151;
      color: #e5e7eb;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-family: var(--code-font);
      transition: background 0.2s;
    }}
    .btn-sm:hover {{
      background: #4b5563;
    }}
    pre.terminal-body {{
      padding: 20px;
      color: #d1d5db;
      font-family: var(--code-font);
      font-size: 0.82rem;
      line-height: 1.5;
      overflow-x: auto;
      max-height: 700px;
      overflow-y: auto;
      white-space: pre;
    }}
    pre.terminal-body::-webkit-scrollbar {{
      width: 8px;
      height: 8px;
    }}
    pre.terminal-body::-webkit-scrollbar-thumb {{
      background: #374151;
      border-radius: 4px;
    }}
    .section-title {{
      font-size: 1.4rem;
      font-weight: 700;
      margin: 30px 0 16px;
      display: flex;
      align-items: center;
      gap: 10px;
      color: #fff;
    }}
    .table-container {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 30px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
      text-align: left;
    }}
    thead {{
      background: #1f2937;
    }}
    th, td {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--card-border);
    }}
    th {{
      color: #9ca3af;
      font-weight: 600;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    tr:last-child td {{
      border-bottom: none;
    }}
    tr:hover td {{
      background: rgba(255,255,255,0.02);
    }}
    .highlight {{
      font-weight: 700;
      color: var(--accent);
    }}
    footer {{
      text-align: center;
      color: #6b7280;
      font-size: 0.85rem;
      margin-top: 50px;
      padding-top: 20px;
      border-top: 1px solid var(--card-border);
    }}
  </style>
</head>
<body>

  <header>
    <div class="container">
      <div style="display:flex; gap:10px; flex-wrap:wrap;">
        <span class="badge">Ciência de Dados 2026</span>
        <span class="badge badge-success">Execução Concluída com Sucesso (Exit Code 0)</span>
      </div>
      <h1>Grupo 2 — Análise da Educação Superior no Brasil</h1>
      <p class="subtitle">
        Pipeline de Engenharia e Limpeza de Dados do Censo da Educação Superior 2024 (INEP/MEC), enriquecido com Web Scraping (<code style="color:var(--primary-light);">pd.read_html</code>) e consumo da API oficial de localidades do IBGE.
      </p>

      <div class="nav-links">
        <a href="#terminal" class="btn btn-primary">🖥️ Ver Saída do Console</a>
        <a href="relatorio_educacao_superior_grupo2.pdf" class="btn" target="_blank">📄 Baixar Relatório Técnico (PDF)</a>
        <a href="grupo2_educacao_superior.py" class="btn" target="_blank">🐍 Ver Código Python</a>
        <a href="roteiro_apresentacao.md" class="btn" target="_blank">🎤 Roteiro de Apresentação</a>
        <a href="https://github.com/barbooosa/data_science" class="btn" target="_blank">🐙 Repositório GitHub</a>
      </div>
    </div>
  </header>

  <main class="container" style="margin-top: 30px;">

    <h2 class="section-title">👥 Integrantes da Equipe (Grupo 2)</h2>
    <div class="team-grid">
      <div class="member-card">
        <span class="member-name">Gustavo Henrique Tavares Borges</span>
        <span class="member-id">Matrícula: 2311157</span>
      </div>
      <div class="member-card">
        <span class="member-name">João Pedro Barbosa Moreira</span>
        <span class="member-id">Matrícula: 2312662</span>
      </div>
      <div class="member-card">
        <span class="member-name">Igor Augusto Ribeiro de Paula Martins</span>
        <span class="member-id">Matrícula: 2312171</span>
      </div>
      <div class="member-card">
        <span class="member-name">Ygor Gomes Rocha</span>
        <span class="member-id">Matrícula: 2312663</span>
      </div>
      <div class="member-card">
        <span class="member-name">Elton Dourado De Azevedo Filho</span>
        <span class="member-id">Matrícula: 2310514</span>
      </div>
    </div>

    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-val">2.561</div>
        <div class="stat-lbl">Total IES no Brasil</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">87,6%</div>
        <div class="stat-lbl">Rede Privada (2.244)</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">12,4%</div>
        <div class="stat-lbl">Rede Pública (317)</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">20,93</div>
        <div class="stat-lbl">Top Densidade: DF (IES/M Hab)</div>
      </div>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Posição</th>
            <th>Sigla</th>
            <th>Estado (UF)</th>
            <th>Região</th>
            <th>Total IES (INEP)</th>
            <th>População (IBGE/Wiki)</th>
            <th>IES por 1M Habitantes</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>1º</strong></td>
            <td><code>DF</code></td>
            <td>Distrito Federal</td>
            <td>Centro-Oeste</td>
            <td>63</td>
            <td>3.009.996</td>
            <td class="highlight">20,93</td>
          </tr>
          <tr>
            <td><strong>2º</strong></td>
            <td><code>MT</code></td>
            <td>Mato Grosso</td>
            <td>Centro-Oeste</td>
            <td>74</td>
            <td>3.950.330</td>
            <td class="highlight">18,73</td>
          </tr>
          <tr>
            <td><strong>3º</strong></td>
            <td><code>AP</code></td>
            <td>Amapá</td>
            <td>Norte</td>
            <td>15</td>
            <td>809.953</td>
            <td class="highlight">18,52</td>
          </tr>
          <tr>
            <td><strong>4º</strong></td>
            <td><code>RO</code></td>
            <td>Rondônia</td>
            <td>Norte</td>
            <td>31</td>
            <td>1.757.338</td>
            <td class="highlight">17,64</td>
          </tr>
          <tr>
            <td><strong>5º</strong></td>
            <td><code>GO</code></td>
            <td>Goiás</td>
            <td>Centro-Oeste</td>
            <td>128</td>
            <td>7.495.033</td>
            <td class="highlight">17,08</td>
          </tr>
          <tr>
            <td><strong>6º</strong></td>
            <td><code>ES</code></td>
            <td>Espírito Santo</td>
            <td>Sudeste</td>
            <td>67</td>
            <td>4.150.692</td>
            <td>16,14</td>
          </tr>
          <tr>
            <td><strong>7º</strong></td>
            <td><code>TO</code></td>
            <td>Tocantins</td>
            <td>Norte</td>
            <td>23</td>
            <td>1.595.994</td>
            <td>14,41</td>
          </tr>
          <tr>
            <td><strong>8º</strong></td>
            <td><code>PR</code></td>
            <td>Paraná</td>
            <td>Sul</td>
            <td>171</td>
            <td>11.952.456</td>
            <td>14,31</td>
          </tr>
          <tr>
            <td><strong>9º</strong></td>
            <td><code>PI</code></td>
            <td>Piauí</td>
            <td>Nordeste</td>
            <td>48</td>
            <td>3.392.617</td>
            <td>14,15</td>
          </tr>
          <tr>
            <td><strong>10º</strong></td>
            <td><code>MG</code></td>
            <td>Minas Gerais</td>
            <td>Sudeste</td>
            <td>303</td>
            <td>21.460.311</td>
            <td>14,12</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div id="terminal" class="terminal-container">
      <div class="terminal-header">
        <div class="terminal-dots">
          <span class="dot dot-red"></span>
          <span class="dot dot-yellow"></span>
          <span class="dot dot-green"></span>
        </div>
        <div class="terminal-title">python grupo2_educacao_superior.py — Saída Completa de Execução</div>
        <div class="terminal-actions">
          <button class="btn-sm" onclick="copiarTerminal()">📋 Copiar Saída</button>
          <a class="btn-sm" style="text-decoration:none; display:inline-block;" href="saida_execucao.txt" download>⬇️ Baixar .txt</a>
        </div>
      </div>
      <pre id="terminalOutput" class="terminal-body">{saida_escapada}</pre>
    </div>

  </main>

  <footer>
    <div class="container">
      <p>Grupo 2 — Ciência de Dados • Repositório: <a href="https://github.com/barbooosa/data_science" style="color:var(--primary-light);">barbooosa/data_science</a> • Publicado via GitHub Pages</p>
    </div>
  </footer>

  <script>
    function copiarTerminal() {{
      const texto = document.getElementById('terminalOutput').innerText;
      navigator.clipboard.writeText(texto).then(() => {{
        alert('Saída completa copiada para a área de transferência!');
      }}).catch(err => {{
        console.error('Erro ao copiar: ', err);
      }});
    }}
  </script>
</body>
</html>
'''

(PASTA / 'index.html').write_text(html_template, encoding='utf-8')
(PASTA / 'saida_codigo.html').write_text(html_template, encoding='utf-8')
print("Arquivos index.html e saida_codigo.html gerados com sucesso!")
