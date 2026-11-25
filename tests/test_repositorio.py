import json

import pytest

from codigo.repositorio import RepositorioServidores

REGISTRO = {
    "Masp/Admissão": "00012341",
    "MASP": "0001234",
    "Nº Admissão": "1",
    "Nome Servidor": "FULANO DE TAL",
    "Data Completa": "1975-06-15T00:00:00.000",
    "Cod Sexo": "M",
    "Cod Carreira": "CARREIRA",
    "Categoria Profissional/Ocupação": "CATEGORIA",
    "Data Exercício": "2001-03-01T00:00:00.000",
}


@pytest.fixture
def caminho_json(tmp_path):
    caminho = tmp_path / "base.json"
    caminho.write_text(json.dumps([REGISTRO], ensure_ascii=False), encoding="utf-8")
    return caminho


def test_busca_preserva_zeros_a_esquerda(caminho_json):
    servidor = RepositorioServidores(caminho_json).buscar_por_masp_adm("0001234", "1")
    assert servidor is not None
    assert servidor.masp == "0001234"
    assert servidor.nome == "FULANO DE TAL"
    assert servidor.data_nascimento.isoformat() == "1975-06-15"
    assert servidor.data_admissao.isoformat() == "2001-03-01"


def test_busca_ignora_espacos(caminho_json):
    assert RepositorioServidores(caminho_json).buscar_por_masp_adm(" 0001234 ", " 1 ")


def test_busca_inexistente_retorna_none(caminho_json):
    assert RepositorioServidores(caminho_json).buscar_por_masp_adm("999", "9") is None


def test_fallback_sem_coluna_masp_adm(tmp_path):
    registro = {k: v for k, v in REGISTRO.items() if k != "Masp/Admissão"}
    caminho = tmp_path / "base.json"
    caminho.write_text(json.dumps([registro], ensure_ascii=False), encoding="utf-8")

    servidor = RepositorioServidores(caminho).buscar_por_masp_adm("0001234", "1")
    assert servidor is not None
