import pygame
from Constantes import *
from Funciones import *

pygame.init()
fuente = pygame.font.SysFont("Arial Narrow",28)
fuente_titulo = pygame.font.SysFont("Arial Narrow",40)
#BOTON VOLVER
boton_volver = crear_boton("boton_volver.png", TAMAÑO_BOTON_VOLVER)


#ORDENA DE MAYOR A MENOR
lista_ranking.sort(key=obtener_puntuacion, reverse=True)


def mostrar_rankings(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event]):
    retorno = "rankings"
  
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver["rectangulo"].collidepoint(evento.pos):
                print("VOLVER AL MENU")
                CLICK_SONIDO.play()
                retorno = "menu"
    
    fondo_ranking = pygame.image.load("champions.jpeg")
    fondo_ranking = pygame.transform.scale(fondo_ranking,VENTANA)
    pantalla.blit(fondo_ranking,(0,0))
    boton_volver["rectangulo"] = pantalla.blit(boton_volver["superficie"],(890,10))
    mostrar_texto(pantalla,"TOP 10",(10,60),fuente_titulo,COLOR_BLANCO)

#TOP 10
    numero_elementos = 10  
    contador = 0  
#ORDENO DE MAYOR A MENOR LOS PRIMEROS 10
    y = 100
    for dato in lista_ranking:
        texto = f"{contador + 1}. {dato['nombre']} - {dato['puntuacion']}pts - {dato['fecha']}"
        mostrar_texto(pantalla, texto, (10, y), fuente, COLOR_BLANCO)
        y += 40
        contador += 1
        if contador >= numero_elementos:
            break 

    return retorno
                