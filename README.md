# ZAP-imoveis-Web-Scraping

This script aims to help people extract property data from Zap Imóveis website (www.zapimoveis.com.br) using Python and Selenium.

In the file 'Scraping_functions.py' there is 3 functions that I created, 'abrir_zap', 'extrair_informacoes' and 'mudar_pagina'. In the file 'Exemple_Usage.py' there is one example of real world usage. 

The idea of the exemple script is: opening the Chrome Web Driver, opening the page with the given URL and searching for all the 'house cards' in the page. The function 'extrair_informacoes' clicks and opens one card's page and get the informations inside of it. For getting all the information of a page, I use a for loop with this function. There is also a function for going to the next result page, 'mudar_pagina', if that is necessary.

The function 'abrir_zap' require the parameters: localization (the neighborhood URL substring, can be found by entering the website, typing the neighborhood in the search bar, and then copying it from the url), acao ('aluguel' or 'venda', to search for renting or selling houses), tipo ('imoveis' or 'casas' or 'apartamentos', to search for all properties, only apartments or only houses). There is also optional parameters, inclui_proximos ('nao' or 'sim', to search for only property in the neighborhood, or also properties close to it, 'nao' as default) and url_zap (the website generic URL, default as "https://www.zapimoveis.com.br/%(acao)s/%(tipo)s/%(localization)s/"). It returns 'quant_local', the number of house cards to be used in that page.

The function 'extrair_informacoes' require the parameters:
It returns 'row': a list containing house information, title, address, selling price, renting price, condominium price, IPTU (housing tax), area, number of rooms, parking spots, bathrooms, real state agency, Creci (agenci number), caracteristics, description, latitude and longitude: 
[titulo,endereco,preco_venda,preco_aluguel,condominio,IPTU,area,quartos,vagas,banheiros,imobiliaria,Creci,caracteristicas,descricao,latitude,longitude]


Thanks for https://github.com/GeovRodri , for the inspiration and some of the insights!
