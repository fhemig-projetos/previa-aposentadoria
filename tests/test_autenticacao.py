from codigo.autenticacao import gerar_hash_senha, verificar_credenciais


def test_senha_em_texto_puro():
    usuarios = {"ana": "segredo"}
    assert verificar_credenciais("ana", "segredo", usuarios)
    assert not verificar_credenciais("ana", "errada", usuarios)
    assert not verificar_credenciais("outro", "segredo", usuarios)


def test_senha_com_hash():
    usuarios = {"ana": gerar_hash_senha("segredo")}
    assert verificar_credenciais("ana", "segredo", usuarios)
    assert not verificar_credenciais("ana", "errada", usuarios)


def test_hash_malformado_nao_autentica():
    assert not verificar_credenciais("ana", "x", {"ana": "pbkdf2_sha256$abc"})


def test_hashes_diferentes_para_mesma_senha():
    assert gerar_hash_senha("a") != gerar_hash_senha("a")
