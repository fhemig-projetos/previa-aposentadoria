# Prévia de Aposentadoria — FHEMIG

Aplicação web para simulação **preliminar** de aposentadoria dos servidores da Fundação Hospitalar do Estado de Minas Gerais (FHEMIG), desenvolvida pela Diretoria de Gestão de Pessoas (DIGEPE) com [Streamlit](https://streamlit.io/).

> ⚠️ A simulação é meramente informativa e **não substitui a análise oficial** do órgão competente.

## Funcionalidades

- **Login** de usuários, com credenciais nos *secrets* do Streamlit (senha em texto puro ou em hash).
- **Consulta do servidor** por MASP e nº de admissão (ADM), a partir de base cadastral em JSON.
- **Exibição dos dados funcionais**: nome, carreira, categoria profissional, data de nascimento, sexo, idade e data de admissão (editável na tela).
- **Captura de informações complementares**: dias de serviço público (FIPA), contribuição averbada do INSS, dias no cargo, demais dias averbados, teto do INSS, exercício sem interrupção (desde 1998, 2003 e 2020), férias-prêmio e dias de abono.
- **Simulação das regras de aposentadoria**:
  - Direito Adquirido / Pedágio — EC nº 104/2020;
  - Regra Geral — Constituição Estadual de MG, art. 36, alterado pela EC nº 104/2020;
  - Regra de Pontos — art. 146 do ADCT, EC nº 104/2020;
  - Aposentadoria Compulsória — aos 75 anos, CF/88, art. 40, §1º, III.
- **Para cada regra**: situação, requisitos × valores apurados, pendências, forma de cálculo dos proventos e **data prevista** de atendimento dos requisitos.
- **Relatório em PDF** com o resultado da simulação.

## Estrutura do projeto

```text
previa-aposentadoria/
├── app.py                        # Ponto de entrada (streamlit run app.py)
├── requirements.txt              # Dependências de execução
├── requirements-dev.txt          # + pytest
├── pytest.ini
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   ├── secrets.toml.example      # Modelo (o secrets.toml real NÃO é versionado)
│   └── secrets.toml
├── assets/                       # LogoFhemig.png, icone.png, cabecalho_pdf.png
├── dados/
│   ├── dados_cadastrais.xlsx     # Base original (opcional; não versionada)
│   ├── dados_cadastrais.json     # Base lida pelo app (não versionada)
│   └── dados_cadastrais.exemplo.json  # Exemplo fictício do formato
├── output/                       # PDFs gerados (não versionados)
├── docs/
│   ├── ANOTACOES.md              # Pendências e ideias
│   └── regras_legais.md          # Texto legal de proventos e reajustes
├── scripts/
│   ├── converter_json.py         # Excel -> JSON
│   ├── gerar_hash_senha.py       # Hash de senha para o secrets.toml
│   └── limpar_cache.py           # Remove __pycache__
├── tests/                        # Testes automatizados (pytest)
└── codigo/
    ├── __init__.py
    ├── config.py                 # Caminhos e constantes (BASE_DIR, DIAS_POR_ANO...)
    ├── modelos.py                # Servidor, DadosTempo, ResultadoRegra
    ├── repositorio.py            # Leitura e busca de servidores (JSON)
    ├── autenticacao.py           # Verificação de usuário/senha
    ├── projecao.py               # Projeção da data de atendimento dos requisitos
    ├── simulador.py              # Executa todas as regras
    ├── regras/
    │   ├── base.py               # RegraAposentadoria (classe abstrata)
    │   ├── pedagio.py            # Direito Adquirido / Pedágio
    │   ├── geral.py              # Regra Geral
    │   ├── pontos.py             # Regra de Pontos
    │   └── compulsoria.py        # Aposentadoria Compulsória
    ├── relatorios/
    │   └── gerador_pdf.py        # Relatório em PDF
    ├── utils/
    │   └── formatacao.py         # fmt_tempo, fmt_num, formatar_chave, formatar_valor
    └── ui/                       # Camada Streamlit
        ├── app_previa.py         # Orquestra a tela principal
        ├── cabecalho.py
        ├── login.py
        ├── formulario.py         # Dados funcionais e informações complementares
        └── resultados.py
```

O pacote `codigo/` (exceto `codigo/ui/`) não depende do Streamlit, o que permite testá-lo isoladamente.

## Pré-requisitos

- Python 3.10 ou superior
- pip

## Instalação

```bash
git clone https://github.com/fhemig-projetos/previa-aposentadoria.git
cd previa-aposentadoria

python -m venv venv
# Windows (PowerShell):
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

## Configuração

### 1. Imagens

Coloque em `assets/`: `LogoFhemig.png`, `icone.png` e `cabecalho_pdf.png`. Se algum não existir, o app continua funcionando sem ele.

### 2. Base de dados

O app lê `dados/dados_cadastrais.json`. Se a base estiver em Excel, salve-a como `dados/dados_cadastrais.xlsx` e converta:

```bash
python scripts/converter_json.py
```

Colunas esperadas (veja `dados/dados_cadastrais.exemplo.json`):

| Coluna | Uso |
|---|---|
| `MASP` | Matrícula do servidor |
| `Nº Admissão` | Número de admissão |
| `Masp/Admissão` | Chave de busca (MASP + ADM concatenados) |
| `Nome Servidor` | Nome |
| `Data Completa` | Data de nascimento |
| `Cod Sexo` | Sexo (`F` ou `M`) |
| `Cod Carreira` | Carreira/cargo |
| `Categoria Profissional/Ocupação` | Categoria profissional |
| `Data Exercício` | Data de admissão |

### 3. Usuários (login)

Copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml` (local) ou preencha os *Secrets* no Streamlit Cloud:

```toml
[usuarios]
maria = "pbkdf2_sha256$260000$...$..."   # hash (recomendado)
joao  = "senha-em-texto"                  # texto puro (também aceito)
```

Para gerar o hash de uma senha:

```bash
python scripts/gerar_hash_senha.py
```

## Execução

```bash
streamlit run app.py
```

## Uso

1. Faça login com usuário e senha.
2. Informe o **MASP** e o **ADM** do servidor.
3. Confira os dados funcionais (e a data de admissão, se necessário).
4. Preencha as informações complementares.
5. Clique em **"Calcular prévia"**.
6. Consulte o resultado de cada regra e baixe o **PDF** da prévia.

## Testes

```bash
pip install -r requirements-dev.txt
pytest
```

## Como adicionar uma nova regra

1. Crie `codigo/regras/<nome>.py` com uma classe que herde de `RegraAposentadoria` e implemente `avaliar(servidor, dados_tempo) -> ResultadoRegra`.
2. Exporte a classe em `codigo/regras/__init__.py` (e em `codigo/__init__.py`, se desejar).
3. Inclua uma instância na lista `self.regras` de `SimuladorAposentadoria` (`codigo/simulador.py`).
4. Se surgirem novas chaves de requisitos/valores, traduza-as em `TRADUCOES_CHAVES` (`codigo/utils/formatacao.py`).
5. Escreva um teste em `tests/test_regras.py`.

## Dependências principais

- [Streamlit](https://streamlit.io/) — interface web
- [pandas](https://pandas.pydata.org/) — leitura da base de dados
- [openpyxl](https://openpyxl.readthedocs.io/) — leitura do Excel na conversão para JSON
- [ReportLab](https://www.reportlab.com/) — geração de PDF
- [python-dateutil](https://dateutil.readthedocs.io/) — cálculos com datas

## Limitações conhecidas

- A projeção da data de atendimento considera acúmulo contínuo de 1 dia de tempo para cada dia corrido, sem novos períodos de interrupção (limite de 100 anos).
- Os campos *demais dias averbados*, *férias-prêmio*, *dias de abono*, *teto do INSS* e as interrupções desde 2003/2020 são coletados na tela, mas ainda **não entram nos cálculos** das regras atuais.
- Admissão em 01/08/1990 pode indicar ingresso por implantação do regime estatutário e exige conferência manual.

## Dados pessoais (LGPD)

A base cadastral e os PDFs gerados contêm dados pessoais de servidores. O `.gitignore` já exclui `dados/*.json`, `dados/*.xlsx`, `output/` e `.streamlit/secrets.toml`: não os versione.
