import random
from Constantes import *
import pygame
import os
import csv
import json
import datetime

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def mezclar_lista(preguntas:list) -> None:
    random.shuffle(preguntas)

def actualizar_estadisticas(pregunta, correcta):
    pregunta["veces_preguntada"] += 1
    if correcta:
        pregunta["aciertos"] += 1
    else:
        pregunta["fallos"] += 1
    # Calcular porcentaje de aciertos
    if pregunta["veces_preguntada"] > 0:
        pregunta["porcentaje_aciertos"] = (pregunta["aciertos"] / pregunta["veces_preguntada"]) * 100
    
def verificar_respuesta(datos_juego:dict,pregunta_actual:dict,respuesta:int) -> bool:
    correcta = respuesta == pregunta_actual["respuesta_correcta"]
    
    # Actualizar estadísticas de la pregunta
    actualizar_estadisticas(pregunta_actual, correcta)
    guardar_preguntas("preguntas.csv", preguntas)
    
    #BOTON X2
    if correcta:
        puntos = datos_juego["puntos_acierto"] * datos_juego["multiplicador"]  #Aplica el multiplicador
        datos_juego["puntuacion"] += puntos
        datos_juego["multiplicador"] = 1  #SE REINICIA
        datos_juego["respuestas_correctas_consecutivas"]+=1
        
        #SI SE RESPONDIO 5 VECES SEGUIDAS
        if datos_juego["respuestas_correctas_consecutivas"] == 5:
            datos_juego["vidas"] += 1  #DA UNA VIDA
            datos_juego["respuestas_correctas_consecutivas"] = 0  #SE REINICIA CONTADOR
        retorno = True
    else:
        datos_juego["respuestas_correctas_consecutivas"] = 0
        #SIN PUNTOS NEGATIVOS
        if datos_juego["puntuacion"] > datos_juego["puntos_error"]:
            datos_juego["puntuacion"] -= datos_juego["puntos_error"]
        
        datos_juego["vidas"] -= 1
        retorno = False
    return retorno
    
def reiniciar_estadisticas(datos_juego:dict):
    datos_juego["puntuacion"] = 0
    datos_juego["vidas"] = CANTIDAD_VIDAS

#CSV A DICCIONARIO

def cargar_preguntas(ruta):
    global preguntas
    print(os.path.abspath(ruta))
    preguntas = []
    with open(ruta, "r", encoding="utf-8", errors="replace") as archivo:
        lector_csv = csv.DictReader(archivo)
        for fila in lector_csv:
            pregunta = {
                "pregunta": fila["pregunta"],
                "respuesta_1": fila["respuesta_1"],
                "respuesta_2": fila["respuesta_2"],
                "respuesta_3": fila["respuesta_3"],
                "respuesta_4": fila["respuesta_4"],
                "respuesta_correcta": int(fila["respuesta_correcta"]),
                "aciertos": int(fila["aciertos"]),
                "fallos": int(fila["fallos"]),
                "veces_preguntada": int(fila["veces_preguntada"]),
                "porcentaje_aciertos": float(fila["porcentaje_aciertos"])
            }
            preguntas.append(pregunta)
    return preguntas
cargar_preguntas("preguntas.csv")

def crear_cabecera(diccionario: dict, separador: str) -> str:
    # Genera la cabecera a partir de las claves del diccionario
    lista_claves = list(diccionario.keys())
    cabecera = separador.join(lista_claves)
    return cabecera

def crear_dato_csv(diccionario: dict, separador: str) -> str:
    # Genera una línea de datos a partir de los valores del diccionario
    lista_valores = list(diccionario.values())
    # Convierto todo a str para evitar que rompa al escribir
    for i in range(len(lista_valores)):
        lista_valores[i] = str(lista_valores[i])
    dato = separador.join(lista_valores)
    return dato

def guardar_preguntas(nombre_archivo: str, lista: list) -> bool:
    if type(lista) == list and len(lista) > 0:
        # Crear cabecera utilizando el primer diccionario de la lista
        cabecera = crear_cabecera(lista[0], ",")
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(cabecera + "\n")
            for diccionario in lista:
                linea = crear_dato_csv(diccionario, ",")
                archivo.write(linea + "\n")
        retorno = True
    else:
        retorno = False
    return retorno

# Ejemplo de guardar las preguntas en un nuevo archivo


def guardar_puntuacion(nombre_archivo: str, nombre: str, puntuacion: int) -> bool:
    
    datos = []
    fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")
    #Si el archivo ya existe, cargamos los datos existentes
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)   
    #Agregar los nuevos datos
    datos.append({"nombre": nombre, "puntuacion": puntuacion, "fecha": fecha_actual})
    #Guardar los datos actualizados en el archivo JSON
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)
    return True


#RANKING
def leer_json(nombre_archivo: str, lista: list) -> bool:
    """
    Lee el archivo JSON y carga sus datos en una lista.
    Retorna True si la lectura fue exitosa, False si hubo un error o si el archivo no existe.
    """
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            lista.clear()  #Limpiar la lista antes de cargar nuevos datos
            lista.extend(json.load(archivo))  #Cargar los datos en la lista
        return True
    return False

lista_ranking=[]
leer_json("puntuaciones.json", lista_ranking)

def obtener_puntuacion(diccionario):
    return diccionario['puntuacion']


def cargar_imagen(ruta, tamaño):
    imagen = pygame.image.load(ruta)
    return pygame.transform.scale(imagen, tamaño)

def crear_boton(imagen, tamaño):   
    #CARGO IMAGEN
    boton_imagen = pygame.image.load(imagen)
    #TAMAÑO IMAGEN
    boton_imagen = pygame.transform.scale(boton_imagen, tamaño)
    #CREO DICCIONARIO
    boton = {}
    boton["superficie"] = boton_imagen
    boton["rectangulo"] = boton["superficie"].get_rect()    
    return boton