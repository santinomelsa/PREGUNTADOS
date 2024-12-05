import pygame
from Constantes import *
from Funciones import *

pygame.init()

#IMAGEN DE FONDO
fondo_opciones = cargar_imagen("fondo_opciones.jpg", VENTANA)
# fondo_opciones = pygame.image.load("fondo_opciones.jpg")
# fondo_opciones = pygame.transform.scale(fondo_opciones, VENTANA) 

#FUENTE
fuente_opciones = pygame.font.SysFont("Arial Narrow", 40)

#IMAGEN MENOS
cuadro_menos = pygame.image.load("boton_menos.png") 
cuadro_menos = pygame.transform.scale(cuadro_menos, TAMAÑO_BOTON_VOLUMEN)
#IMAGEN MAS
cuadro_mas = pygame.image.load("boton_mas.png") 
cuadro_mas = pygame.transform.scale(cuadro_mas, TAMAÑO_BOTON_VOLUMEN)

#BOTONES
boton_sumar_puntos = crear_boton("boton_mas.png", TAMAÑO_BOTON_VOLUMEN)
boton_restar_puntos = crear_boton("boton_menos.png", TAMAÑO_BOTON_VOLUMEN)
boton_sumar_errores = crear_boton("boton_mas.png", TAMAÑO_BOTON_VOLUMEN)
boton_restar_errores = crear_boton("boton_menos.png", TAMAÑO_BOTON_VOLUMEN)
boton_sumar_vidas = crear_boton("boton_mas.png", TAMAÑO_BOTON_VOLUMEN)
boton_restar_vidas = crear_boton("boton_menos.png", TAMAÑO_BOTON_VOLUMEN)
boton_sumar_tiempo = crear_boton("boton_mas.png", TAMAÑO_BOTON_VOLUMEN)
boton_restar_tiempo = crear_boton("boton_menos.png", TAMAÑO_BOTON_VOLUMEN)
boton_volver = crear_boton("boton_volver.png", TAMAÑO_BOTON_VOLVER)




def mostrar_opciones(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    retorno = "opciones"
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_sumar_puntos["rectangulo"].collidepoint(evento.pos):
                datos_juego["puntos_acierto"] += 1
            elif boton_restar_puntos["rectangulo"].collidepoint(evento.pos) and datos_juego["puntos_acierto"] > 0:
                datos_juego["puntos_acierto"] -= 1
            elif boton_sumar_errores["rectangulo"].collidepoint(evento.pos):
                datos_juego["puntos_error"] += 1
            elif boton_restar_errores["rectangulo"].collidepoint(evento.pos) and datos_juego["puntos_error"] > 0:
                datos_juego["puntos_error"] -= 1
            elif boton_sumar_vidas["rectangulo"].collidepoint(evento.pos) and datos_juego["vidas"] < 10:
                datos_juego["vidas"] += 1
            elif boton_restar_vidas["rectangulo"].collidepoint(evento.pos) and datos_juego["vidas"] > 1:
                datos_juego["vidas"] -= 1
            elif boton_sumar_tiempo["rectangulo"].collidepoint(evento.pos):
                datos_juego["tiempo"] += 5
            elif boton_restar_tiempo["rectangulo"].collidepoint(evento.pos) and datos_juego["tiempo"] > 5:
                datos_juego["tiempo"] -= 5
            elif boton_volver["rectangulo"].collidepoint(evento.pos):
                CLICK_SONIDO.play()
                retorno = "menu"
    
    #DIBUJO EL FONDO
    pantalla.blit(fondo_opciones, (0, 0))  

    #DIBUJO Y POSICIONO BOTONES
    boton_sumar_puntos["rectangulo"] = pantalla.blit(boton_sumar_puntos["superficie"], (650, 100))
    boton_restar_puntos["rectangulo"] = pantalla.blit(boton_restar_puntos["superficie"], (200, 100))
    boton_sumar_errores["rectangulo"] = pantalla.blit(boton_sumar_errores["superficie"], (650, 200))
    boton_restar_errores["rectangulo"] = pantalla.blit(boton_restar_errores["superficie"], (200, 200))
    boton_sumar_vidas["rectangulo"] = pantalla.blit(boton_sumar_vidas["superficie"], (650, 300))
    boton_restar_vidas["rectangulo"] = pantalla.blit(boton_restar_vidas["superficie"], (200, 300))
    boton_sumar_tiempo["rectangulo"] = pantalla.blit(boton_sumar_tiempo["superficie"], (650, 400))
    boton_restar_tiempo["rectangulo"] = pantalla.blit(boton_restar_tiempo["superficie"], (200, 400))
    boton_volver["rectangulo"] = pantalla.blit(boton_volver["superficie"], (920,10))


    #MUESTRO LOS VALORES ACTUALES
    mostrar_texto(pantalla, f"PTS POR ACIERTO: {datos_juego['puntos_acierto']}", (320, 130), fuente_opciones, COLOR_BLANCO)
    mostrar_texto(pantalla, f"PTS POR ERROR: {datos_juego['puntos_error']}", (320, 230), fuente_opciones, COLOR_BLANCO)
    mostrar_texto(pantalla, f"VIDAS: {datos_juego['vidas']}", (320, 330), fuente_opciones, COLOR_BLANCO)
    mostrar_texto(pantalla, f"TIEMPO: {datos_juego['tiempo']} SEG", (320, 430), fuente_opciones, COLOR_BLANCO)

    return retorno