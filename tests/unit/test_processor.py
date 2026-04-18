import pytest
from src.app.core.processor import TextProcessor

class TestTextProcessor:
    
    @pytest.mark.parametrize("input_text, expected", [
        ("INSTALAÇÃO DE LUMINÁRIA LED", "Instalação de Luminária LED"),
        ("limpeza de caixa de ralo", "Limpeza de Caixa de Ralo"),
        ("MANUTENÇÃO NO RIO DE JANEIRO RJ", "Manutenção no Rio de Janeiro RJ"),
        ("D'AREIA E PCD", "D'Areia e PCD"),
        ("sistema bhls e ip", "Sistema BHLS e IP"),
        ("", ""),
        (None, ""),
    ])
    def test_corrigir_capitalizacao(self, input_text, expected):
        assert TextProcessor.corrigir_capitalizacao(input_text) == expected

    def test_formatar_resumo_simples(self):
        servicos = ["Pintura", "LIMPEZA"]
        resultado = TextProcessor.formatar_resumo(servicos)
        # sorted: Limpeza, Pintura
        assert resultado == "Limpeza e Pintura"

    def test_formatar_resumo_multiplos(self):
        servicos = ["instalação de led", "manutenção", "limpeza"]
        resultado = TextProcessor.formatar_resumo(servicos)
        # sorted: Instalação de LED, Limpeza, Manutenção
        assert resultado == "Instalação de LED, Limpeza e Manutenção"

    def test_formatar_resumo_vazio(self):
        assert TextProcessor.formatar_resumo([]) == ""
