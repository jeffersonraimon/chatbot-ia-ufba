import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    """Configura o WebDriver do Chrome e abre o chatbot"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa sem abrir o navegador (opcional)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280,800")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(3)  # Espera implícita para todos os elementos

    driver.get("http://localhost:3000")  # Substituir pelo endereço do chatbot
    yield driver
    driver.quit()

@pytest.mark.skip(reason="Chatbot ainda não foi implementado")
def test_preencher_campo_e_enviar(driver):
    """Testa se é possível digitar uma pergunta no chatbot e enviá-la"""
    input_box = driver.find_element(By.ID, "chat-input")  # Verifique o ID correto
    send_button = driver.find_element(By.ID, "send-button")  # Verifique o ID correto

    input_box.send_keys("Qual é a capital do Brasil?")
    send_button.click()
    
    time.sleep(1)  # Tempo para a resposta carregar
    resposta = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "chat-response"))
    ).text

    print(f"Resposta recebida: {resposta}")  # Debug
    assert "Brasília" in resposta or "capital do Brasil" in resposta

@pytest.mark.skip(reason="Chatbot ainda não foi implementado")
def test_enviar_com_enter(driver):
    """Testa se é possível enviar uma pergunta pressionando ENTER"""
    input_box = driver.find_element(By.ID, "chat-input")

    input_box.send_keys("Como funciona a matrícula?")
    input_box.send_keys(Keys.RETURN)  # Pressiona ENTER

    time.sleep(1)
    resposta = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "chat-response"))
    ).text

    print(f"Resposta recebida: {resposta}")  # Debug
    assert "sistema de matrícula" in resposta or "matrícula" in resposta

@pytest.mark.skip(reason="Chatbot ainda não foi implementado")
def test_placeholder_presente(driver):
    """Verifica se o campo de entrada tem um placeholder apropriado"""
    input_box = driver.find_element(By.ID, "chat-input")
    placeholder = input_box.get_attribute("placeholder")

    print(f"Placeholder encontrado: {placeholder}")  # Debug
    assert placeholder == "Digite sua pergunta..."

@pytest.mark.skip(reason="Chatbot ainda não foi implementado")
def test_mensagem_muito_longa(driver):
    """Testa envio de uma mensagem muito longa para verificar comportamento do layout"""
    input_box = driver.find_element(By.ID, "chat-input")
    send_button = driver.find_element(By.ID, "send-button")

    mensagem_longa = "A" * 500  # 500 caracteres
    input_box.send_keys(mensagem_longa)
    send_button.click()

    time.sleep(1)
    mensagem_enviada = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "user-message"))
    ).text

    print(f"Mensagem longa enviada: {mensagem_enviada}")
    assert len(mensagem_enviada) >= 500  # Garantir que a mensagem não foi cortada
