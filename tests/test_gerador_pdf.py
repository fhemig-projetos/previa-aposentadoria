from codigo.relatorios import PDFGenerator
from codigo.simulador import SimuladorAposentadoria


def test_gera_pdf(tmp_path, criar_servidor, criar_tempo):
    servidor = criar_servidor(idade=60)
    resultados = SimuladorAposentadoria().simular(
        servidor, criar_tempo(anos_exercicio=20)
    )

    caminho = PDFGenerator(pasta_saida=tmp_path).gerar(servidor, resultados)

    assert caminho.endswith("previa_aposentadoria_1234567.pdf")
    with open(caminho, "rb") as arquivo:
        assert arquivo.read(5) == b"%PDF-"
