import pygame
from Constantes import *
from Funciones import *

pygame.init()


fuente = pygame.font.SysFont("Arial Narrow",40)

imagen_cuadro = cargar_imagen("imagenes/cuadro_terminado.jpeg", CUADRO_TEXTO)
cuadro = {}
cuadro["superficie"] = imagen_cuadro
cuadro["rectangulo"] = cuadro["superficie"].get_rect()
nombre = ""

def mostrar_fin_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    global nombre
    retorno = "terminado"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif evento.type == pygame.KEYDOWN:
            bloc_mayus = pygame.key.get_mods() and pygame.KMOD_CAPS
            letra_presionada = pygame.key.name(evento.key)
            
            if letra_presionada == "backspace" and len(nombre) > 0:
                nombre = nombre[0:-1]#Elimino el ultimo
                cuadro["superficie"] = imagen_cuadro.copy()
            
            if letra_presionada == "space" and len(nombre) < 15:
                nombre += " "
            
            if len(letra_presionada) == 1 and len(nombre) < 15:  
                if bloc_mayus != 0:
                    nombre += letra_presionada.upper()
                else:
                    nombre += letra_presionada
            if letra_presionada == "return" and len(nombre) > 0:
                #GUARDO NOMBRE Y PUNTUACION AL PRESIONAR ENTER
                guardar_puntuacion("puntuaciones.json", nombre, datos_juego["puntuacion"])
                retorno = "menu"
                nombre=""
                reiniciar_estadisticas(datos_juego)

    fondo_terminado = cargar_imagen("imagenes/llorando.jpg", VENTANA)             
    pantalla.blit(fondo_terminado,(0,0))   
    pantalla.blit(cuadro["superficie"], (10, 10))
    
    mostrar_texto(pantalla, nombre, (20, 150), fuente, COLOR_AZUL)
    mostrar_texto(pantalla,f"Usted obtuvo: {datos_juego["puntuacion"]} puntos",(20,40),fuente,COLOR_NEGRO)
    mostrar_texto(pantalla, "INGRESE SU NOMBRE:", (20, 100), fuente, COLOR_NEGRO)
    mostrar_texto(pantalla, "Presione Enter para guardar", (20, 250), fuente, COLOR_NEGRO)
    return retorno

