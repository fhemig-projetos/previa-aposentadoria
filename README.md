# Prévia de Aposentadoria

Aplicação web para simulação preliminar de aposentadoria de servidores públicos, desenvolvida com [Streamlit](https://streamlit.io/).

## Funcionalidades

- **Consulta de servidor** por MASP e ADM a partir de planilha Excel
- **Exibição de dados funcionais** do servidor (nome, cargo, idade, admissão etc.)
- **Captura de informações complementares**:
  - Dias trabalhados no serviço público (FIPA)
  - Dias de contribuição externa (INSS/privado)
  - Dias no cargo e na carreira
  - Sujeição ao teto do INSS
  - Interrupção de exercício no serviço público
- **Simulação de regras de aposentadoria**:
  - Regra de idade e tempo de contribuição
  - Direito adquirido — Art. 6º da EC 41/2003
  - Regra do teto do INSS
- **Geração de relatório em PDF** com o resultado da simulação

## Estrutura do projeto

```
previa-aposentadoria/
├── app.py                    # Interface Streamlit (ponto de entrada)
├── codigo/
│   ├── __init__.py           # Exportação dos módulos
│   ├── modelos.py            # Dataclasses: Servidor, DadosTempo, ResultadoRegra
│   ├── repositorio.py        # Leitura de dados do Excel
│   ├── regras.py             # Regras de aposentadoria
│   ├── simulador.py          # Orquestração das regras
│   ├── gerador_pdf.py        # Geração de relatório PDF
│   └── converter_json.py     # Utilitário de conversão
├── dados/
│   └── dados_cadastrais.xlsx # Base de dados dos servidores
├── output/
│   └── relatorios/           # PDFs gerados
├── requirements.txt
└── README.md
```

## Pré-requisitos

- Python 3.10 ou superior
- Pip (gerenciador de pacotes)

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/fhemig-projetos/previa-aposentadoria.git
cd previa-aposentadoria
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Coloque o arquivo `dados/dados_cadastrais.xlsx` com a base de servidores no local adequado.

## Execução

```bash
streamlit run app.py
```

A aplicação será aberta no navegador em `http://localhost:8501`.

## Uso

1. Informe o **MASP** e o **ADM** do servidor.
2. Preencha os dados complementares solicitados (dias trabalhados, contribuições externas etc.).
3. Clique em **"Calcular prévia"**.
4. Visualize os resultados de cada regra e faça o download do relatório em PDF.

## Dependências principais

- [Streamlit](https://streamlit.io/) — interface web
- [pandas](https://pandas.pydata.org/) — leitura da planilha Excel
- [reportlab](https://www.reportlab.com/) — geração de PDF
- [python-dateutil](https://dateutil.readthedocs.io/) — cálculos com datas

## Observações

- A simulação é **preliminar e ilustrativa**, não substituindo análise oficial do órgão competente.
- A base de dados deve estar no formato Excel com as colunas esperadas pelo `RepositorioServidores`.