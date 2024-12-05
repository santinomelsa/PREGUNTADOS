import pygame
from Constantes import *
from Funciones import *

pygame.init()

#FUENTE
fuente_volumen = pygame.font.SysFont("Karmatic Arcade",120)

#CREAR BOTONES
boton_suma = crear_boton("imagenes/boton_mas.png", TAMAÑO_BOTON_VOLUMEN)
boton_resta = crear_boton("imagenes/boton_menos.png", TAMAÑO_BOTON_VOLUMEN)
boton_volver = crear_boton("imagenes/boton_volver.png", TAMAÑO_BOTON_VOLVER)
boton_mutear = crear_boton("imagenes/boton_mute.png", TAMAÑO_BOTON_VOLVER)


def mostrar_configuracion(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    retorno = "configuraciones"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_suma["rectangulo"].collidepoint(evento.pos):
                print("SUMA VOLUMEN")
                if datos_juego["volumen_musica"] < 100:
                    datos_juego["volumen_musica"] += 5
                CLICK_SONIDO.play()
            elif boton_resta["rectangulo"].collidepoint(evento.pos):
                print("RESTA VOLUMEN")
                if datos_juego["volumen_musica"] > 0:
                    datos_juego["volumen_musica"] -= 5
                CLICK_SONIDO.play()
            elif boton_mutear["rectangulo"].collidepoint(evento.pos):
                print("MUTEAR/DESMUTEAR")
                if datos_juego["volumen_musica"] == 0:
                    # Si el volumen está muteado (0), desmuteamos al 50%
                    datos_juego["volumen_musica"] = 50
                else:
                    # Si el volumen no está muteado, lo mutamos (lo ponemos a 0)
                    datos_juego["volumen_musica"] = 0
                CLICK_SONIDO.play()
            elif boton_volver["rectangulo"].collidepoint(evento.pos):
                print("VOLVER AL MENU")
                CLICK_SONIDO.play()
                retorno = "menu"
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RIGHT:  # Flecha hacia arriba
                print("AUMENTAR VOLUMEN")
                if datos_juego["volumen_musica"] < 100:
                    datos_juego["volumen_musica"] += 5
            elif evento.key == pygame.K_LEFT:  # Flecha hacia abajo
                print("DISMINUIR VOLUMEN")
                if datos_juego["volumen_musica"] > 0:
                    datos_juego["volumen_musica"] -= 5

    #CREAR FONDO      
    fondo_confi = cargar_imagen("imagenes/fondo_confi.jpg", VENTANA)      
    pantalla.blit(fondo_confi,(0,0))
    #UBICACION BOTONES
    boton_suma["rectangulo"] = pantalla.blit(boton_suma['superficie'],(800,300))
    boton_resta["rectangulo"] = pantalla.blit(boton_resta['superficie'],(100,300))
    boton_volver["rectangulo"] = pantalla.blit(boton_volver['superficie'],(920,10))
    boton_mutear["rectangulo"] = pantalla.blit(boton_mutear['superficie'],(10,10))
    
    #MOSTRAR PORCENTAJE
    mostrar_texto(pantalla,f"{datos_juego["volumen_musica"]} %",(380,270),fuente_volumen,COLOR_NEGRO)

    return retorno
                
