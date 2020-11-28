# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 18:48:04 2020

@author: femdi
"""
'''
AFTER RUNNING THE FUNCTIONS FROM 
'''



#importing necessary libs
import pandas as pd
import time
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

#Path where the chromedriver is installed
PATH = 'C:\Program Files (x86)\chromedriver.exe'

#Opening Chrome
driver = webdriver.Chrome(PATH)
driver.maximize_window()

#Creating final table of properties
columns = ['Título','Endereço','Preço de Venda','Preço de Aluguel','Condomínio',
           'IPTU','Área','N° de Quarto','N° de Vagas','N° de Banheiros','Imobiliária',
           'Creci','Características','Descrição','Latitude','Longitude']
tabela_imoveis = pd.DataFrame(columns = columns)

#Selection variables to be used in the URL
localization="sp+sao-paulo+zona-sul+capao-redondo"
acao = 'aluguel'
tipo= 'imoveis'
inclui_proximos = 'nao'
bairros=["sp+sao-paulo+zona-sul+capao-redondo",'sp+sao-paulo+zona-sul+jd-sandra',
         'sp+sao-paulo+zona-sul+vl-das-belezas']

# For each neghborhood
for loc in bairros:
    quant_local=24
    # While quant_local=24, the program will run and skip to the page (Because the previous page was full of houses)
    while quant_local == 24: 
        #opening the URL
        quant_local = abrir_zap(loc,acao,tipo)
        
        #If quant_local > 0, there is houses, so the prgram will run
        if quant_local > 0:
            house_card = driver.find_elements_by_class_name('card-listing')[:quant_local]
            
            # Getting information for each card
            for i in range(len(house_card)):
                
                tabela_imoveis.loc[len(tabela_imoveis)] = extrair_informacoes(i)
            
            #If this page is full of houses, turn to the next page to get the rest
            if quant_local == 24:
                mudar_pagina()
        
        
         
