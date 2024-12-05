import pygame
from Constantes import *
from Funciones import *

pygame.init()

#CUADRO PREGUNTA
imagen_cuadro_pregunta = cargar_imagen("imagenes/marco_pregunta.jpeg", TAMAÑO_PREGUNTA)
cuadro_pregunta = {}
cuadro_pregunta["superficie"] = imagen_cuadro_pregunta
cuadro_pregunta["rectangulo"] = cuadro_pregunta["superficie"].get_rect()
#CUADRO RESPUESTA
imagen_cuadro_respuesta = cargar_imagen("imagenes/marco_respuesta.png", TAMAÑO_RESPUESTA)
#RESPUESTA CORRRECTA
cuadro_respuesta_correcta = cargar_imagen("imagenes/marco_respuesta_correcta.png", TAMAÑO_RESPUESTA)
#RESPUESTA INCORRECTA
cuadro_respuesta_incorrecta = cargar_imagen("imagenes/marco_respuesta_incorrecta.png", TAMAÑO_RESPUESTA)
#BOTON VOLVER
boton_volver = crear_boton("imagenes/boton_volver.png", TAMAÑO_BOTON_VOLVER)
#BOTON SALTAR PREGUNTA
boton_saltar = crear_boton("imagenes/cambio_de_pregunta.png", TAMAÑO_BOTON_VOLVER)
#BOTON X2
boton_x2 = crear_boton("imagenes/duplicar_puntos.png", TAMAÑO_BOTON_VOLVER)
#FONDO
fondo_juego = cargar_imagen("imagenes/fondo_futbol.jpg", VENTANA)
#RELOJ
clock = pygame.time.Clock()
evento_tiempo_1s = pygame.USEREVENT
pygame.time.set_timer(evento_tiempo_1s, 1000)
#CUADRO RESPUESTA
cartas_respuestas = []
for i in range(4):
    cuadro_respuesta = {}
    cuadro_respuesta["superficie"] = imagen_cuadro_respuesta
    cuadro_respuesta["rectangulo"] = cuadro_respuesta["superficie"].get_rect()
    cartas_respuestas.append(cuadro_respuesta)
#FUENTES
fuente_pregunta = pygame.font.SysFont("Arial Narrow",42)
fuente_respuesta = pygame.font.SysFont("Arial Narrow",30)
fuente_texto = pygame.font.SysFont("Arial Narrow",25)
fuente_boton = pygame.font.SysFont("Arial Narrow",23)

mezclar_lista(preguntas)
indice = 0 
bandera_respuesta = False 
bandera_eliminado = True
bandera_x2 = True


def mostrar_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    global indice
    global bandera_respuesta
    global CANTIDAD_VIDAS
    global VIDAS_INICIALES
    global bandera_eliminado
    global bandera_x2
    retorno = "juego"
    
    #LIMPIA LA PREGUNTA ANTERIOR
    cuadro_pregunta["superficie"] = imagen_cuadro_pregunta.copy()
    for carta in cartas_respuestas:
        carta["superficie"] = imagen_cuadro_respuesta.copy()
        
    if bandera_respuesta:
        pygame.time.delay(500)
        bandera_respuesta = False
        datos_juego["tiempo"] = TIEMPO_PREGUNTA
        
    pregunta_actual = preguntas[indice]

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == evento_tiempo_1s:#TEMPORIZADOR
            datos_juego["tiempo"] -= 1
            if datos_juego["tiempo"] <= 0:
                ERROR_SONIDO.play()
                CANTIDAD_VIDAS -= 1
                datos_juego["vidas"] -= 1
                datos_juego["tiempo"] = TIEMPO_PREGUNTA 
                if datos_juego["vidas"] <= 0:
                    retorno = "terminado"
                    bandera_eliminado = True
                    bandera_x2 = True 
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(cartas_respuestas)):
                if cartas_respuestas[i]['rectangulo'].collidepoint(evento.pos):
                    respuesta_usuario = (i + 1)   
                    if verificar_respuesta(datos_juego,pregunta_actual,respuesta_usuario):
                        ACIERTO_SONIDO.play()
                        cartas_respuestas[i]['superficie']=cuadro_respuesta_correcta.copy()
                        print("RESPUESTA CORRECTA")
                    else:
                        ERROR_SONIDO.play()
                        cartas_respuestas[i]['superficie']=cuadro_respuesta_incorrecta.copy()
                        CANTIDAD_VIDAS-=1
                        print("RESPUESTA INCORRECTA")
                        if datos_juego["vidas"] <= 0:
                            retorno = "terminado"
                            bandera_eliminado = True
                            bandera_x2 = True
                         
                    print(f"SE HIZO CLICK EN UNA RESPUESTA {respuesta_usuario}")
                    bandera_respuesta = True
                    #SI TERMINO EL INDICE, SE VUELVE DE 0
                    if indice == len(preguntas):
                        indice = 0
                        mezclar_lista(preguntas)
                    indice += 1

                #BOTON VOLVER
                #SI PRESIONO EL BOTON SE REINICIA TOD0
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    pygame.mixer.music.stop()
                    CLICK_SONIDO.play()
                    CANTIDAD_VIDAS = VIDAS_INICIALES
                    datos_juego["vidas"] = CANTIDAD_VIDAS  # Valor inicial de las vidas
                    datos_juego["puntuacion"] = 0                  # Reiniciar la puntuación
                    datos_juego["multiplicador"] = 1               # Resetear multiplicador
                    mezclar_lista(preguntas)                       # Reordenar las preguntas
                    indice = 0                                     # Reiniciar el índice de preguntas
                    datos_juego["tiempo"] = TIEMPO_PREGUNTA        # Reiniciar el temporizador
                    bandera_eliminado = True                       # Restablecer banderas
                    bandera_x2 = True
                    retorno = "menu"
                #BOTON SALTAR PREGUNTA
                if boton_saltar["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    bandera_respuesta = True
                    bandera_eliminado = False
                    if indice == len(preguntas):
                        indice = 0
                        mezclar_lista(preguntas)
                    else:
                        indice += 1
                #BOTON X2   
                if boton_x2["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    datos_juego["multiplicador"] = 2  #ACTIVA MULTIPLICADOR
                    bandera_x2 = False


    #TEXTO
    for i in range(4):
        mostrar_texto(cartas_respuestas[i]["superficie"], f"{pregunta_actual[f'respuesta_{i + 1}']}", (20, 20), fuente_respuesta, COLOR_BLANCO)
    mostrar_texto(cuadro_pregunta["superficie"],f"{pregunta_actual["pregunta"]}",(20,20),fuente_pregunta,COLOR_BLANCO)
    # mostrar_texto(cartas_respuestas[0]["superficie"],f"{pregunta_actual["respuesta_1"]}",(20,20),fuente_respuesta,COLOR_BLANCO)
    # mostrar_texto(cartas_respuestas[1]["superficie"],f"{pregunta_actual["respuesta_2"]}",(20,20),fuente_respuesta,COLOR_BLANCO)
    # mostrar_texto(cartas_respuestas[2]["superficie"],f"{pregunta_actual["respuesta_3"]}",(20,20),fuente_respuesta,COLOR_BLANCO)
    # mostrar_texto(cartas_respuestas[3]["superficie"],f"{pregunta_actual["respuesta_4"]}",(20,20),fuente_respuesta,COLOR_BLANCO)
    # mostrar_texto(boton_volver["superficie"],"VOLVER",(10,10),fuente_boton,COLOR_BLANCO)

    #DIBUJO FONDO
    pantalla.blit(fondo_juego,(0,0))

    
    #DIBUJO CUADROS Y BOTONES Y LOS UBICO
    cartas_respuestas[0]['rectangulo'] = pantalla.blit(cartas_respuestas[0]['superficie'],(340,270))
    cartas_respuestas[1]['rectangulo'] = pantalla.blit(cartas_respuestas[1]['superficie'],(340,350))
    cartas_respuestas[2]['rectangulo'] = pantalla.blit(cartas_respuestas[2]['superficie'],(340,430))
    cartas_respuestas[3]['rectangulo'] = pantalla.blit(cartas_respuestas[3]['superficie'],(340,510))
    pantalla.blit(cuadro_pregunta["superficie"],(300,80))
    boton_volver["rectangulo"] = pantalla.blit(boton_volver['superficie'],(890,10))
    if bandera_eliminado:
        boton_saltar["rectangulo"] = pantalla.blit(boton_saltar['superficie'],(890,520))
    if bandera_x2:
        boton_x2["rectangulo"] = pantalla.blit(boton_x2['superficie'], (890, 600))

    
    mostrar_texto(pantalla,f"PUNTUACION: {datos_juego['puntuacion']}",(10,10),fuente_texto,COLOR_BLANCO)
    mostrar_texto(pantalla,f"VIDAS: {datos_juego['vidas']}",(10,40),fuente_texto,COLOR_BLANCO)
    mostrar_texto(pantalla, f"TIEMPO: {datos_juego["tiempo"]}s", (10, 70), fuente_texto, COLOR_BLANCO)
    
    return retorno