import pygame
from Constantes import *
from Funciones import mostrar_texto

pygame.init()
fuente_menu = pygame.font.SysFont("Karmatic Arcade",40)
fuente_menu2 = pygame.font.SysFont("Karmatic Arcade",30)
lista_botones = []

imagen_boton = pygame.image.load("imagenes/menu.jpeg")
imagen_boton = pygame.transform.scale(imagen_boton, TAMAÑO_BOTON)

for i in range(5):
    boton = {}
    boton["superficie"] = imagen_boton.copy()
    boton["rectangulo"] = boton["superficie"].get_rect()
    lista_botones.append(boton)

fondo = pygame.image.load("imagenes/fondo2.jpg")
fondo = pygame.transform.scale(fondo,VENTANA)

def mostrar_menu(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event])-> str:
    #Gestionar eventos:
    retorno = "menu"
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(lista_botones)): 
                if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    if i == BOTON_SALIR:
                        retorno = "salir"  
                    elif i == BOTON_JUGAR:
                        retorno = "juego"  
                    elif i == BOTON_PUNTUACIONES:
                        retorno = "rankings"
                    elif i == BOTON_CONFIG:
                        retorno = "configuraciones"  
                    elif i == BOTON_OPCIONES:  # Nuevo botón para agregar pregunta
                        retorno = "opciones"      
        elif evento.type == pygame.QUIT:
            retorno = "salir"
                
    #Actualizar el juego:
    
    #Dibujar pantalla y las otras superficies
    #pantalla.fill(COLOR_BLANCO)
    pantalla.blit(fondo,(0,0))
    
    lista_botones[0]["rectangulo"] = pantalla.blit(lista_botones[0]["superficie"],(120,115))
    lista_botones[1]["rectangulo"] = pantalla.blit(lista_botones[1]["superficie"],(530,115))
    lista_botones[2]["rectangulo"] = pantalla.blit(lista_botones[2]["superficie"],(120,250))
    lista_botones[3]["rectangulo"] = pantalla.blit(lista_botones[3]["superficie"],(330, 385))
    lista_botones[4]["rectangulo"] = pantalla.blit(lista_botones[4]["superficie"], (530,250))
    mostrar_texto(lista_botones[0]["superficie"],"JUGAR",(75,25),fuente_menu,COLOR_BLANCO)
    mostrar_texto(lista_botones[1]["superficie"],"CONFIGURACION",(20,30),fuente_menu2,COLOR_BLANCO)
    mostrar_texto(lista_botones[2]["superficie"],"PUNTUACIONES",(23,32),fuente_menu2,COLOR_BLANCO)
    mostrar_texto(lista_botones[3]["superficie"],"SALIR",(80,25),fuente_menu,COLOR_BLANCO)
    mostrar_texto(lista_botones[4]["superficie"], "OPCIONES", (40, 25), fuente_menu, COLOR_BLANCO)
    
    return retorno