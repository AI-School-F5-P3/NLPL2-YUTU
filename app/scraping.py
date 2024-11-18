from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_comments_selenium(video_url, max_comments=100):
    # Configuración del navegador (asegúrate de tener 'chromedriver' en tu sistema)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Ejecutar en modo headless (sin ventana)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    driver.get(video_url)
    time.sleep(3)  # Esperar a que la página cargue

    # Desplazarse hacia abajo para cargar más comentarios
    for _ in range(5):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)

    # Extraer comentarios
    comments = []
    comment_elements = driver.find_elements(By.XPATH, '//*[@id="content-text"]')

    for comment in comment_elements:
        comments.append(comment.text)
        if len(comments) >= max_comments:
            break

    driver.quit()
    return comments