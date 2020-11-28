# ZAP-imoveis-Web-Scraping

This program aims to help people extract Zap Imóveis website. Using Selenium, it opens the Chrome Web Driver, opens the page with the given URL and search for all the houses 'cards' in the page. The function 'extrair_informacoes' clicks and opens one card and get the informations inside of its page. For getting all the information of a page, I use a for loop with this function. There is also a function for going to the next result page, 'mudar_pagina'.

The function 'extrair_informacoes' returns 'row': a list containing house information, title, address, selling price, renting price, condominium price, IPTU (housing tax), area, number of rooms, parking spots, bathrooms, real state agency, Creci (agenci number), caracteristics, description, latitude and longitude: 
[titulo,endereco,preco_venda,preco_aluguel,condominio,IPTU,area,quartos,vagas,banheiros,imobiliaria,Creci,caracteristicas,descricao,latitude,longitude]
