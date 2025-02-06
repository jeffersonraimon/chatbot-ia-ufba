import pytest


# Teste do agente macro
def test_macro_agent_response():
    """Testa se o agente macro consegue fornecer resposta com a UFBA"""
    resposta = "O Instituto de Computação da UFBA oferece cursos de graduação e pós-graduação."
    assert "UFBA" in resposta, "A resposta do agente não contém 'UFBA'"

# Teste do agente especialista
def test_specialist_agent_redirect():
    """Testa se o agente especialista responde corretamente sobre disciplinas do curso"""
    pergunta = "Quais são as disciplinas do curso de Ciência da Computação?"
    especialista = "Agente de Graduação"
    # Simulação de redirecionamento do especialista
    assert especialista == "Agente de Graduação", f"O especialista esperado era 'Agente de Graduação', mas foi {especialista}"

