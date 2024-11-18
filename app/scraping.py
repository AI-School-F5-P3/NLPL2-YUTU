from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def iniciar_driver():
    """
    Inicializa y devuelve el objeto del controlador de Chrome.
    Asegúrate de que chromedriver esté en tu PATH o especifica la ruta completa en 'executable_path'.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Ejecutar en modo headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # Desactivar uso de GPU para evitar errores
    options.add_argument('--window-size=1920,1080')  # Opcional: establecer tamaño de ventana
    
    
    try:
        driver = webdriver.Chrome(options=options)
        print("Navegador iniciado con éxito")
        return driver
    except Exception as e:
        print(f"Error al iniciar el navegador: {e}")
        return None

def get_comments_selenium(video_url, max_comments=100):
    """
    Extrae comentarios de un video de YouTube utilizando Selenium.
    """
    driver = iniciar_driver()
    if driver is None:
        return []

    comments = []
    
    try:
        # Cargar la página del video
        driver.get(video_url)
        
        # Esperar a que los comentarios se carguen
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        
        time.sleep(3)  # Esperar un poco más para asegurarse de que la página cargue

        # Desplazarse hacia abajo para cargar más comentarios
        scroll_pause_time = 2
        last_height = driver.execute_script("return document.documentElement.scrollHeight")

        while len(comments) < max_comments:
            # Desplazarse al final de la página para cargar más comentarios
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(scroll_pause_time)
            
            # Verificar si los comentarios se han cargado
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="content-text"]'))
                )
            except TimeoutException:
                print("No se pudieron cargar más comentarios")
                break
            
            # Extraer comentarios visibles actualmente
            comment_elements = driver.find_elements(By.XPATH, '//*[@id="content-text"]')
            for comment in comment_elements:
                comment_text = comment.text.strip()
                if comment_text not in comments:  # Evitar duplicados
                    comments.append(comment_text)
                if len(comments) >= max_comments:
                    break

            # Revisar si hay más comentarios que cargar
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                print("No hay más comentarios para cargar")
                break
            last_height = new_height

    except NoSuchElementException as e:
        print(f"Elemento no encontrado: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        driver.quit()
        print("Navegador cerrado")
    
    return comments

# Ejemplo de uso
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=iNZnnMGypjY"  # Cambia este enlace por el video que quieras analizar
    comentarios = get_comments_selenium(video_url, max_comments=10)
    
    if comentarios:
        print(f"Se obtuvieron {len(comentarios)} comentarios:")
        for i, comentario in enumerate(comentarios, 1):
            print(f"{i}. {comentario}")
    else:
        print("No se obtuvieron comentarios.")




