import time
import mysql.connector
import pyperclip
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Definir opções para o Google Chrome
options = Options()
options.add_argument("--user-data-dir=C:\\Users\\zapzap\\AppData\\Local\\Google\\Chrome\\User Data\\Default")

# Configuração do navegador Chrome
driver = webdriver.Chrome(options=options)

# Abre o WhatsApp Web
driver.get('https://web.whatsapp.com/')

# Espera até que o QR Code seja escaneado
wait = WebDriverWait(driver, 600)
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@title="Caixa de texto de pesquisa"]')))

# Loop principal
while True:
    # Configuração do banco de dados
    db = mysql.connector.connect(
        host="***.***.*.***",
        user="******",
        password="******",
        database="**********",
        ssl_disabled = True
    )
     # Espera 5 segundos antes de verificar novamente
    time.sleep(5)
    #print("ping")

    # Executa a query no banco de dados
    cursor = db.cursor()
    query = "SELECT * FROM mensagens WHERE ENVIADA = 0 ORDER BY ID ASC LIMIT 1"
    cursor.execute(query)
    rows = cursor.fetchall()
    #print(rows)
    
    # Se encontrou alguma linha, envia a mensagem via WhatsApp Web
    if rows:
        for row in rows:
            id = row[0]
            mensagem = row[1]
            numero = row[2]
            #print("message sent")

            pyperclip.copy(mensagem)
                  
            # Localiza o campo de pesquisa e insere o número do destinatário
            search_box = driver.find_element(By.XPATH, '//div[@title="Caixa de texto de pesquisa"]')
            search_box.click()
            search_box.send_keys(numero)
            search_box.send_keys(Keys.ENTER)

            # Localiza o campo de mensagem e insere o texto
            message_box = driver.find_element(By.XPATH,'//div[@title="Mensagem"]')
            message_box.click()
            message_box.send_keys(Keys.CONTROL + 'v')
            message_box.send_keys(Keys.ENTER)

            # Marca a mensagem como enviada no banco de dados
            update_cursor = db.cursor()
            update_cursor.execute("UPDATE mensagens SET Enviada = 1 WHERE Id = %s", (id,))
            db.commit()
        
    #fechar conexão com banco de dados
    db.close()

       


            
