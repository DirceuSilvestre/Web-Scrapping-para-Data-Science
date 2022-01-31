from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
########### Acima #################
#Importa as bibliotecas necessárias

########### Abaixo ################

#Escolhe o site da americanas
#abre o navegador firefox
#e conecta ao site da americanas

url = 'https://www.americanas.com.br/'

drive = webdriver.Firefox()
drive.get(url)

#Aguarda o carregamento total da página
#e coloca em tela cheia o navegador

sleep(1)

drive.maximize_window()

#Procura no HTML o primeiro elemento input
#clica nele
#escreve no input o nome do produto que deseja buscar
#procura no HTML o primeiro botão que é um elemento button
#e clica nele para que busque o termo escrito anteriormente
#após aguardar o carregamento dos resultados fecha o navegador, encerrando o processo

busca = drive.find_element_by_tag_name('input')
busca.click()
busca.send_keys('lápis hb')
busca = drive.find_element_by_tag_name('button')
busca.click()

sleep(3)

drive.quit()