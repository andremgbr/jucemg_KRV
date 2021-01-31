from Projeto import TESTE_DOWNLOAD,check_protocolo,entra_login,entra_consultar_viabilidade_2,leitura_de_paginas,init_config,Consulta_Protocol_Viabilidade
from db import consultar_data, update_data
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os




driver, wait = init_config()
entra_login(driver, wait)
entra_consultar_viabilidade_2(driver, wait)
leitura_de_paginas(driver, wait)
#leitura_de_paginas(driver,wait)
#entra_consultar_viabilidade_2(driver, wait)
#Consulta_Protocol_Viabilidade(driver,wait)
entra_consultar_viabilidade_2(driver, wait)
data = consultar_data()
print('\n..........Lista de Protocolos para serem analisados.............' )
for i in data:
	print(i)
print('\n........................................................\n\n')
for i in data:
	check_protocolo(driver,wait,i)
	time.sleep(5)
	try:
		element = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="situacaoViabilidade"]')))
	finally:
		status = driver.find_element_by_xpath('//*[@id="situacaoViabilidade"]')
		status= str(status.get_attribute('innerHTML'))
		status = status[1:]
	if status == "Deferida":
		print('... Protocolo Acima está Deferida!!!')
		TESTE_DOWNLOAD(driver,wait)
		update_data(i,status)
	elif status == "Indeferida":
		print('... Protocolo Acima está Indeferida!!!')
		TESTE_DOWNLOAD(driver,wait)
		update_data(i,status)
	elif status == "Cancelada Pelo Usuário":
		print('... Protocolo Acima Foi cancelada pelo Usuário!!!')
		update_data(i,status)
	elif status == "Protocolada'":
		print('... Protocolo Acima continua Protocolada!!!')
	print("-------------------------------------------------------\n\n")
driver.close()
print("\n...Encerrada a Verificação!!!\n-------------------------------------------------------\n\n")




