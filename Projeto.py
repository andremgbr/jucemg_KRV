from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from db import set_data_viabilidade, find_data_viabilidade
from emailBot import send_email
import time, os, sys, traceback



# from selenium.webdriver.firefox.options import Options
# profile = webdriver.FirefoxProfile()
# profile.set_preference("browser.download.folderList",2)
# profile.set_preference("browser.download.manager.showWhenStarting",False)
# profile.set_preference("browser.download.dir","C:\\Users\\Andre\\Documents\\Python\\Rodrigo_Project\\Downloads")
# profile.set_preference("browser.helperApps.neverAsk.saveToDisk","application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, application/ ,text/html, text/plain, application/zip, application/x-zip, application, application/x-zip-compressed, application/download, application/octet-stream , , ")
# profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
# profile.set_preference("browser.download.manager.focusWhenStarting", False)
# profile.set_preference("browser.helperApps.alwaysAsk.force", False)
# profile.set_preference("browser.download.manager.useWindow", False)
# driver = webdriver.Firefox(firefox_profile=profile)

def init_config():
	options = Options()
	options.add_experimental_option("prefs", {
	"download.default_directory": r"C:\Automacao_KRV\Downloads",
	"download.prompt_for_download": False,
	"download.directory_upgrade": True,
	"safebrowsing.enabled": True,
	"plugins.always_open_pdf_externally": True,
	"plugins.always_open_jsf_externally": True,
	})

	driver = webdriver.Chrome("chromedriver_win32\\chromedriver",chrome_options=options)
	driver.set_window_position(-2000, 0);
	wait = WebDriverWait(driver,300)
	return driver,wait

def entra_login(driver, wait):

	driver.get("http://portalservicos.jucemg.mg.gov.br/Portal/pages/principal.jsf")
	print('---------------------------------------------------\n')
	print('... Esperando carregamento do site!!!')

	try:
		element = wait.until(EC.presence_of_element_located((By.XPATH ,"//*[@id='username']")))
	except:
		sys.tracebacklimit = 0
		print('... ERROR --- Site não está carregando, tente novamete mais tarde!!!!\n')
		print('---------------------------------------------------\n')
	finally:
		login_form = driver.find_element_by_id('username')
		senha_form = driver.find_element_by_id('password')
		entra_form = driver.find_element_by_id('kc-login')
		login_form.send_keys('????***.***.***-**?????')
		senha_form.send_keys('????****????')
		entra_form.click()
		print('... Conta Logada!!!')


def entra_viabilidade(driver, wait):
	try:
		element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='card__content__link' and @title='Viabilidade']")))
	finally:
		viabilidade_entry = driver.find_element_by_xpath("//a[@class='card__content__link' and @title='Viabilidade']" )
		viabilidade_entry.click()


def entra_consultuar_viabilidade(driver, wait):

	try:
		element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Consultar Viabilidade']")))
	finally:
		consultar_viabilidade_entry = driver.find_element_by_xpath("//*[text()='Consultar Viabilidade']//ancestor::p")
		try:
			element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Consultar Viabilidade']//ancestor::p")))
		finally:
			consultar_viabilidade_entry.click()

def entra_consultar_viabilidade_2(driver,wait):
	driver.get('http://portalservicos.jucemg.mg.gov.br/viabilidade/pages/consultaViabilidade.jsf')



def leitura_de_paginas(driver, wait):
	print('\n... Fazendo Leituras de novos Protocolos!!!')
	protocolo_1 = ''
	bool_pass = True
	for i in range(5):
		for page in range(104,119,3):
			while bool_pass:
				try:
					element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/form/span/table/tbody/tr[1]/td[1]')))
				finally:
					if protocolo_1 != str(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/span/table/tbody/tr[1]/td[1]').get_attribute('innerHTML').splitlines()[0]):
						bool_pass = False
					else:
						time.sleep(.1)
			bool_pass = True	
			for i in range(1,6):
				protocolo = str(driver.find_element_by_xpath(('/html/body/div[2]/div/div[2]/form/span/table/tbody/tr[{}]/td[1]').format(i)).get_attribute('innerHTML').splitlines()[0])
				if  find_data_viabilidade(protocolo):
					print('... Busca de novos protocolos encerrado!')
					print('---------------------------------------------------------\n\n')
					return
				else:
					print("... Novo protocolo encontrado --",protocolo," --!!!!")
				try:
					nome_op = str(driver.find_element_by_xpath(('/html/body/div[2]/div/div[2]/form/span/table/tbody/tr[{}]/td[2]').format(i)).get_attribute('innerHTML').splitlines()[0])
				except:
					nome_op = ''	
				situacao = str(driver.find_element_by_xpath(('/html/body/div[2]/div/div[2]/form/span/table/tbody/tr[{}]/td[3]').format(i)).get_attribute('innerHTML').splitlines()[0])
				data_cadastro = str(driver.find_element_by_xpath(('/html/body/div[2]/div/div[2]/form/span/table/tbody/tr[{}]/td[4]').format(i)).get_attribute('innerHTML').splitlines()[0])
				set_data_viabilidade(protocolo,nome_op,situacao,data_cadastro)
			protocolo_1 = str(driver.find_element_by_xpath(('/html/body/div[2]/div/div[2]/form/span/table/tbody/tr[1]/td[1]')).get_attribute('innerHTML').splitlines()[0])	
			select_page = driver.find_element_by_xpath(('//*[@id="j_idt85:j_idt{}"]').format(page))
			select_page.click()
			time.sleep(1)

def TESTE_DOWNLOAD(driver,wait):
#	try:
#		element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_idt55:1:j_idt82"]')))
#	finally:
#		selecionar_element = driver.find_element_by_xpath( '//*[@id="j_idt55:1:j_idt82"]')
#	selecionar_element.click()
#	time.sleep(2)
	print('... Fazendo Download do Protocolo!!!')
	try:
		element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/form/div[3]/div[1]/div[2]/a')))
		
	finally:
		ver_relatorio_element = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/div[3]/div[1]/div[2]/a')
		ver_relatorio_element.click()
		time.sleep(10)

	driver.switch_to.window(driver.window_handles[-1])
	#Initial_path = '\\Downloads\\'
	#filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
	#print('...Protocolo baixado como -- ',filename,' -- !!!')

	#print(filename)
	#send_email(filename)


def Consulta_Protocol_Viabilidade(driver,wait):
	try:
		element = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div[2]/form/div[2]/div/div[1]/input')))
	finally:
		campo = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/div[2]/div/div[1]/input')
		pesquisar = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/div[2]/div/div[2]/a')
		campo.send_keys('mgp2000654378')
		pesquisar.click()

	try:
		element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/form/div[3]/div[1]/div[2]/a')))
		
	finally:
		ver_relatorio_element = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/div[3]/div[1]/div[2]/a')
	ver_relatorio_element.click()
	print(ver_relatorio_element)
	time.sleep(10)


def check_protocolo(driver,wait,protocolo):
	print('\n--------------------------------------------------------------------------------------')
	print('... Verificando a Situação do Protocolo - ',protocolo,' - !!!')
	try:
		element = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div[2]/form/div[2]/div/div[1]/input')))
	finally:
		campo = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/div[2]/div/div[1]/input')
		pesquisar = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/div[2]/div/div[2]/a')
		campo.clear()
		time.sleep(4)
		campo.send_keys(protocolo)
		pesquisar.click()



