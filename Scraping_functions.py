
#importing necessary libs
import pandas as pd
import time
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def abrir_zap(localization, acao, tipo, inclui_proximos = 'nao', url_zap = "https://www.zapimoveis.com.br/%(acao)s/%(tipo)s/%(localization)s/"):
      '''
    

    Parameters
    ----------
    localization : str
        The neighborhood URL substring, can be found by entering the website
        typing the neighborhood in the search bar, and then copying it from the url.
    acao : str
        'aluguel' or 'venda', to search for renting or selling houses.
    tipo : str
        'imoveis' or 'casas' or 'apartamentos', to search for all properties, only apartments or only houses.
    inclui_proximos : str, optional
        'nao' or 'sim', to search for only property in the neighborhood, or also properties close to it. The default is 'nao'.
    url_zap : str, optional
        The website generic URL. The default is "https://www.zapimoveis.com.br/%(acao)s/%(tipo)s/%(localization)s/".

    Returns
    -------
    quant_local: int
        The number of house cards to be used in that page.

    '''
  
    # Opening URL in Driver
    driver.get(url_zap % vars())
    
    #Checking if the page exist
    try:
        driver.find_element_by_class_name('display-small')
        quant_local = 0
        print("Page doesn't exist")
        return quant_local
    except:
        print('Loading page...')
    
    #Waiting until the website loads complety (I chose to wait for the houses images because they are the last things to load)
    wait = WebDriverWait(driver,15).until(
         EC.presence_of_element_located((By.CLASS_NAME, "img")))
    
    #Selecting the house 'card', where is possible to click to see the full description
    house_card = driver.find_elements_by_class_name('card-listing')

    #Calculating the number of houses EXACTLY in the neighborhood, not 'close to'
    if inclui_proximos == 'nao':
        
        #Calculating the number all houses: in + close to the neighborhood
        quant_tudo = driver.find_element_by_class_name('js-summary-title').text
        quant_tudo1 = int(quant_tudo.split(' ')[0].replace('.',''))
        
        #Calculating the number of houses CLOSE TO  the neighborhood
        try:
            quant_prox = driver.find_element_by_class_name('nearby-title').text
            quant_prox1 = int(quant_prox.split(' ')[2].replace('.',''))
        except:
            quant_prox1 = 0
            
        #Calculating the number of houses EXACTLY in the neighboorhood
        quant_local = quant_tudo1 - quant_prox1
    
    
        # 24 is the limit per page, 'quant_local will be used to decide if the program should change page or not
        if quant_local > 24:
            quant_local = 24
        
    elif inclui_proximos == 'sim':
        quant_local = 24
    
    else:
        return print('inclui_proximos should be "nao" or "yes"')

    return quant_local



def extrair_informacoes(i):
     '''
    
    Parameters
    ----------
    i : int
        The number of the house card to get information from.

    Returns
    -------
    row : list
        A list containing house information, title, address, selling price, 
        renting price, condominium price, IPTU (housing tax), area, number of rooms,
        parking spots, bathrooms, real state agency, Creci (agenci number), 
        caracteristics, description, latitude and longitude.

    '''
    #Getting the house cards ans selcting only the wanted ones
    house_card = driver.find_elements_by_class_name('card-listing')[:quant_local]
    
    #moving page to the card
    actions = ActionChains(driver).move_to_element(house_card[i]).perform()
    
    #Saving the number of pages in a variable 
    handles_before = driver.window_handles
    
    try:
        #waiting until card is clickable
        wait_1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "card-listing")))
        
        #getting house cards again(because the reference becomes stale after some time)
        house_card = driver.find_elements_by_class_name('card-listing')[:quant_local]
        
        #clicking in the house card
        house_card[i].click()
        
        #Checking with a new page was opened or not
        WebDriverWait(driver, 10).until(
                lambda driver: len(handles_before) != len(driver.window_handles))
    
    #If error, waiting 5 seconds and trying again, usually works
    except: 
        wait_1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "card-listing")))
        
        time.sleep(5)
        
        house_card = driver.find_elements_by_class_name('card-listing')[:quant_local]
    
        house_card[i].click()
        
        #Checking with a new page was opened or not
        WebDriverWait(driver, 10).until(
                lambda driver: len(handles_before) != len(driver.window_handles))
    
    # Switching to the new window
    driver.switch_to_window(driver.window_handles[1])
    
    # Waiting until the title loads
    wait2 = WebDriverWait(driver,15).until(
     EC.presence_of_element_located((By.CLASS_NAME, "main__info")))

    #Getting the title text
    title = driver.find_element_by_class_name('main__info').text
    
    #Splitting the title by '\n', so we can get the information by position
    lista = title.split("\n")
    
    #The next few lines are used to find the important elements and assign them to varibles
    try:
        titulo = lista[0]
    except:
        titulo = 'Não Consta'
        
    try:
        endereco = lista[2]
    except:
        endereco = 'Não Consta'
        
    try:
        preco_venda = int([i for i in lista[1:] if 'Venda' in i][0].split(' ')[2].replace('.',''))
    except:
        preco_venda = 'Não Consta'
        
    try:
        preco_aluguel = int([i for i in lista[1:] if '/mês' in i][0].split('R$ ')[1].replace('.','').split(' ')[0])
    except:
        preco_aluguel = 'Não Consta'
    
    try:
        condominio = int([i for i in lista[1:] if 'condomínio' in i][0].split(' IPTU R$ ')[0][10:])
    except:
        condominio = 'Não Consta'
    
    try:
        IPTU = int([i for i in lista[1:] if 'IPTU' in i][0].split(' IPTU R$ ')[1])
    except:
        IPTU = 'Não Consta'
    
    try:
        area = [i for i in lista[1:] if 'm²' in i][0].split(' ')[0]
    except:
        area = 'Não Consta'
    
    try:
        quartos = [i for i in lista[1:] if 'quarto' in i][0].split(' ')[0]
    except:
        quartos = 'Não Consta'
        
    try:
        vagas = [i for i in lista[1:] if 'vaga' in i][0].split(' ')[0]
    except:
        vagas = 'Não Consta'
    
    try:
        banheiros = [i for i in lista[1:] if 'banheiro' in i][0].split(' ')[0]
    except:
        banheiros = 'Não Consta'
        
    try:
        imobiliaria = driver.find_element_by_class_name('publisher__title').text
    except:
        imobiliaria = 'Não Consta'
        
    try:
        Creci = driver.find_element_by_class_name('publisher__license').text[6:]
    except:
        Creci = 'Não Consta'
        
    try:
        caracteristicas = driver.find_element_by_class_name('collapse').text.replace('\n',' ')
    except:
        caracteristicas = 'Não Consta'

    try:
        descricao = driver.find_element_by_class_name('amenities__description').text
    except:
        descricao = 'Não Consta'
    
    
    #This part gets the map information (latitude and longitude)
    
    #waiting for the map to load
    wait3 = WebDriverWait(driver,15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "map__cta")) )
    
    #scrolling to the map
    mapa = driver.find_element_by_class_name('map__cta')
    actions = ActionChains(driver).move_to_element(mapa).perform()
    
    #Clicking in the map to open it
    mapa = driver.find_element_by_class_name('map__cta')
    mapa.click()
    
    
    try:
        wait4 = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "embed__iframe")))
        
    #sometimes the map doens't load, so it must click again
    except:
        mapa = driver.find_element_by_class_name('map__cta')
        mapa.click()
        wait4_1 = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "embed__iframe")))
        
    #Finding the link to the google maps in the 'embed__iframe' element
    x = driver.find_element_by_class_name('embed__iframe')
    x.get_attribute("src")
    maps = x.get_attribute("src")
    
    #If the link contains the coordinates (float), assigning them to varables
    try:
        latitude = float(maps[31:41])
        longitude = float(maps[42:52])
        
    #If error, opening the Google Maps page
    except:
        link = maps[:-28] + maps[-15:]
        
        #Opening link
        driver.get(link)
        
        #Waiting for 5 seconds, because the URL take some time to change
        time.sleep(5)
        
        #The changed URL always contains teh coordinates, assigning them to variables
        current = driver.current_url
        current = current.split('/')
        current2 = current[6].split(',')
        latitude = float(current2[0][1:])
        longitude = float(current2[1])
    
    # Creating the Main object, a list with all important caracteristics
    row = [titulo,endereco,preco_venda,preco_aluguel,condominio,IPTU,
           area,quartos,vagas,banheiros,imobiliaria,Creci,caracteristicas,
           descricao,latitude,longitude]
    
    #Closing the house tab
    driver.close()
    
    #Switching back to the main search page
    driver.switch_to_window(driver.window_handles[0])
    
    
    return row
    

def mudar_pagina():
    #Waiting for getting back to the main page
    time.sleep(5)
    #Finding the 'next page' button
    prox_pag = driver.find_element_by_class_name('pagination__button')
    
    #Scrolling to the button
    ActionChains(driver).move_to_element(prox_pag).perform()
    
    #clicking the button
    prox_pag = driver.find_element_by_class_name('pagination__button')
    prox_pag.click()


