img_pokemon = None
about = """
Instituto tecnológico de Costa Rica
Ingeniería en Computadores
Introducción a la programación
Fabricio Guillén Acevedo 2026005221
Profesor: Leornardo Araya
"""
stats = {
    "Venusaur": {"HP": 80, "Attack": 82, "Defense": 83, "Defendiendo": False},
    "Charizard": {"HP": 78, "Attack": 84, "Defense": 78, "Defendiendo": False},
    "Blastoise": {"HP": 79, "Attack": 83, "Defense": 100, "Defendiendo": False},
    "Pidgeot": {"HP": 83, "Attack": 80, "Defense": 75, "Defendiendo": False},
    "Rhydon": {"HP": 105, "Attack": 130, "Defense": 120, "Defendiendo": False},
    "Chansey": {"HP": 250, "Attack": 50, "Defense": 150, "Defendiendo": False},
    "Snorlax": {"HP": 160, "Attack": 110, "Defense": 65, "Defendiendo": False},
    "Pikachu": {"HP": 35, "Attack": 65, "Defense": 80, "Defendiendo": False},
    "Nidoking": {"HP": 81, "Attack": 102, "Defense": 77, "Defendiendo": False},
    "Machamp": {"HP": 90, "Attack": 130, "Defense": 80, "Defendiendo": False},
    "Mewtwo": {"HP": 106, "Attack": 150, "Defense": 90, "Defendiendo": False},
    "Moltres": {"HP": 90, "Attack": 110, "Defense": 90, "Defendiendo": False},
    "Rapidash": {"HP": 65, "Attack": 100, "Defense": 70, "Defendiendo": False},
    "Articuno": {"HP": 90, "Attack": 85, "Defense": 100, "Defendiendo": False},
    "Zapdos": {"HP": 90, "Attack": 100, "Defense": 85, "Defendiendo": False},
    "Dragonite": {"HP": 91, "Attack": 130, "Defense": 95, "Defendiendo": False},
    "Nidoqueen": {"HP": 90, "Attack": 87, "Defense": 87, "Defendiendo": False},
    "Slowbro": {"HP": 95, "Attack": 70, "Defense": 110, "Defendiendo": False},
}
sprites = {
    "Venusaur": "Spr b g1 003.png",
    "Charizard": "Spr b g1 006.png",
    "Blastoise": "Spr b g1 009.png",
    "Pidgeot": "Spr b g1 018.png",
    "Rhydon": "Spr b g1 112.png",
    "Chansey": "Spr b g1 113.png",
    "Snorlax": "Spr b g1 143.png",
    "Pikachu": "Spr b g1 025.png",
    "Nidoking": "Spr b g1 034.png",
    "Machamp": "Spr b g1 068.png",
    "Mewtwo": "Spr b g1 150.png",
    "Moltres": "Spr b g1 146.png",
    "Rapidash": "Spr b g1 078.png",
    "Articuno": "Spr b g1 144.png",
    "Zapdos": "Spr b g1 145.png",
    "Dragonite": "Spr b g1 149.png",
    "Nidoqueen": "Spr b g1 031.png",
    "Slowbro": "Spr b g1 080.png",
}
Mejores_puntajes = []
vent_personajes = "Elige tu personaje"
personaje_seleccionado = None # variable global para guardar el personaje seleccionado
global pokemones_jugador
pokemones_jugador = []
global pokemones_IA
pokemones_IA = ["Slowbro","Nidoqueen","Rapidash","Dragonite","Articuno","Zapdos","Moltres","Mewtwo"]
global nombre_jugador
nombre_jugador = None # variable global para guardar el nombre del jugador
pokemon_activo = None
turno_limite = 5

from tkinter import *
from os import path #para los archivos de audio e imágenes
from time import sleep 
import random 
import json


# Ruta base del script (útil para localizar el archivo de audio)
BASE_DIR = path.dirname(path.abspath(__file__))
PROJECT_ROOT = BASE_DIR  # si tus scripts están en la raíz
# Preferir las carpetas que creaste directamente en el proyecto: backgrounds, musica, sprites
ASSETS_DIR = path.join(PROJECT_ROOT, 'assets')  # mantenido como alternativa
SOUNDS_DIR = path.join(PROJECT_ROOT, 'musica')
BACKGROUNDS_DIR = path.join(PROJECT_ROOT, 'backgrounds')
SPRITES_DIR = path.join(PROJECT_ROOT, 'sprites')
PUNTAJES_FILE = path.join(PROJECT_ROOT, 'puntajes.json')  # archivo para guardar los puntajes

# Nombre del archivo de música dentro de la carpeta 'Smogon'. Cambia esto según tu archivo.
MUSIC_FILENAME = 'titulo.wav'  # usa WAV para reproducir con winsound (builtin en Windows)

import threading # para ejecutar la música en un hilo separado y evitar bloquear la interfaz
import platform # para detectar el sistema operativo y usar el backend de audio adecuado

def cargar_puntajes():
    try:
        with open(PUNTAJES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # si el archivo no existe, devolver una lista vacía

def guardar_puntaje(nombre, puntaje):
    puntajes = cargar_puntajes()
    puntajes.append({"nombre": nombre, "puntaje": puntaje})
    puntajes = sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)[:10]
    with open(PUNTAJES_FILE, "w") as f: json.dump(puntajes, f)

# helper para obtener rutas de assets
def asset_path(dir_path, filename):
    return path.join(dir_path, filename)

def musica_batalla(filename):
    candidates = [
        path.join(SOUNDS_DIR, filename),
        path.join(BASE_DIR, filename),
        path.join(BASE_DIR, 'Smogon', filename),
    ]
    music_path =  next((c for c in candidates if path.exists(c)), None)
    try:
        import winsound
        if music_path is None:
            print("Archivo de música no encontrado para cambiar música.")
        else:
            try:
                winsound.PlaySound(None, winsound.SND_PURGE)  # detener música actual
            except Exception:
                pass
            winsound.PlaySound(music_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
    except Exception as e:
        print("Error cambiando música con winsound:", e)
#fondo
def menu (nombre, max_size = (558,552)):
    candidates = [
        asset_path(BACKGROUNDS_DIR, nombre),
        path.join(BASE_DIR, nombre),
        path.join(ASSETS_DIR, 'backgrounds', nombre),
    ]
    ruta = next((c for c in candidates if path.exists(c)), None)
    if ruta is None:
        print('No se encontró', nombre, 'en ninguna de estas rutas:')
        for c in candidates:
            print('  -', c)
        # devolver una imagen vacía para evitar que la app se rompa; así no se lanza el error de Tk
        return PhotoImage(width=max_size[0], height=max_size[1])
    img = PhotoImage(file=ruta)
    return img

#Selección de personaje

def ventana_personajes():
    canvas_menu.delete("all")
    # eliminar widgets embebidos (Labels/Buttons creados con create_window)
    for w in canvas_menu.winfo_children():
        try:
            w.destroy()
        except Exception:
            pass
    
    #fondo 2
    fondo_personajes = asset_path(BACKGROUNDS_DIR, "pradera.png")
    canva_menu = PhotoImage(file=fondo_personajes)
    canvas_menu.create_image(0, 0, anchor=NW, image=canva_menu)
    canvas_menu.canva_personajes = canva_menu
    
    #avatar 1
    red_avatar = asset_path(SPRITES_DIR, "Spr_FRLG_Red.png")
    red_img_avatar = PhotoImage(file=red_avatar)
    red_item = canvas_menu.create_image(50, 400, anchor=W, image=red_img_avatar)
    canvas_menu.red_photo= red_img_avatar # mantener referencia para evitar garbage collection
    canvas_menu.red_item = red_item # mantener imagen para usar despues
    #avatar 2
    leaf_avatar = asset_path(SPRITES_DIR, "Spr_FRLG_Leaf.png")
    leaf_img_avatar = PhotoImage(file=leaf_avatar)
    leaf_item = canvas_menu.create_image(150, 400, anchor=W, image=leaf_img_avatar)
    canvas_menu.leaf_photo = leaf_img_avatar # mantener referencia para evitar garbage collection
    canvas_menu.leaf_item = leaf_item # mantener imagen para usar despues
    #avatar 3
    brendan_avatar = asset_path(SPRITES_DIR, "Spr_E_Brendan.png")
    brendan_img_avatar = PhotoImage(file=brendan_avatar)
    brendan_item = canvas_menu.create_image(250, 400, anchor=W, image=brendan_img_avatar)
    canvas_menu.brendan_photo = brendan_img_avatar # mantener referencia para evitar garbage collection
    canvas_menu.brendan_item = brendan_item # mantener imagen para usar despues
    #avatar 4
    may_avatar = asset_path(SPRITES_DIR, "Spr_E_May.png")
    may_img_avatar = PhotoImage(file=may_avatar)
    may_item = canvas_menu.create_image(350,400, anchor=W, image=may_img_avatar)
    canvas_menu.may_photo = may_img_avatar # mantener referencia para evitar garbage collection
    canvas_menu.may_item = may_item # mantener imagen para usar despues
    #avatar 5
    wally_avatar = asset_path(SPRITES_DIR, "Spr_RS_Wally.png")
    wally_img_avatar = PhotoImage(file=wally_avatar)
    wally_item = canvas_menu.create_image(450, 400, anchor=W, image=wally_img_avatar)
    canvas_menu.wally_photo = wally_img_avatar # mantener referencia para evitar garbage collection
    canvas_menu.wally_item = wally_item # mantener imagen para usar despues
    #texto
    label_vent_personajes = Label(canvas_menu, text=vent_personajes, font=('Arial', 12), bg='white')
    label_vent_personajes.place(x=10, y=10)
    
    #botones de selección de personaje, el botón guarda el personaje que usaste en una variable global para usarlo después
    def seleccion_personaje(personaje):
        global personaje_seleccionado
        personaje_seleccionado = personaje
        global red_item, leaf_item, brendan_item, may_item, wally_item
        red_item = canvas_menu.red_item
        leaf_item = canvas_menu.leaf_item
        brendan_item = canvas_menu.brendan_item
        may_item = canvas_menu.may_item
        wally_item = canvas_menu.wally_item
        print("Personaje seleccionado:", personaje_seleccionado)
    #boton red
    boton_red = Button(canvas_menu, text="Red", command=lambda: (seleccion_personaje("Red"), ventana_pokemon()))
    boton_red.place(x=50, y=500)
    #boton leaf
    boton_leaf = Button(canvas_menu, text="Leaf", command=lambda: (seleccion_personaje("Leaf"), ventana_pokemon()))
    boton_leaf.place(x=150, y=500)
    #boton brendan
    boton_brendan = Button(canvas_menu, text="Brendan", command=lambda: (seleccion_personaje("Brendan"), ventana_pokemon()))
    boton_brendan.place(x=250, y=500)
    #boton may
    boton_may = Button(canvas_menu, text="May", command=lambda: (seleccion_personaje("May"), ventana_pokemon()))
    boton_may.place(x=350, y=500)
    #boton wally
    boton_wally = Button(canvas_menu, text="Wally", command=lambda: (seleccion_personaje("Wally"), ventana_pokemon()))
    boton_wally.place(x=450, y=500)

def musica_personajes(filename):
    candidates = [
        path.join(SOUNDS_DIR, filename),
        path.join(BASE_DIR, filename),
        path.join(BASE_DIR, 'Smogon', filename),
    ]
    music_path =  next((c for c in candidates if path.exists(c)), None)
    try:
        import winsound
        # si no se encontró el archivo, salir sin intentar reproducir
        if music_path is None:
            print("Archivo de música no encontrado para cambiar música.")
        else:
            try:
                winsound.PlaySound(None, winsound.SND_PURGE)  # detener música actual
            except Exception:
                pass
            winsound.PlaySound(music_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
    except Exception as e:
        print("Error cambiando música con winsound:", e)

#función ventana selección de pokemones
def ventana_pokemon():
    for w in canvas_menu.winfo_children():
        try:
            w.destroy()
        except Exception:
            pass
    canvas_menu.delete("all")
    #Usaré el mismo fondo que la ventana de personajes
    fondo_personajes = asset_path(BACKGROUNDS_DIR, "pradera.png")
    fondo_img = PhotoImage(file=fondo_personajes)
    canvas_menu.create_image(0, 0, anchor=NW, image=fondo_img)
    canvas_menu.canvas_personajes = fondo_img
    #Venusaur
    venasaur = asset_path(SPRITES_DIR, "Spr_1g_003.png")
    venasaur_img = PhotoImage(file=venasaur)
    venasaur_item = canvas_menu.create_image(25, 100, anchor=W, image=venasaur_img)
    canvas_menu.venasaur_photo = venasaur_img # mantener referencia para evitar garbage
    canvas_menu.venasaur_item = venasaur_item # mantener imagen para usar despues
    boton_info_venasaur = Button(canvas_menu, text="Info", command=estadisticas_venasour)
    boton_info_venasaur.place(x=60, y=160)
    #Charizard
    charizard = asset_path(SPRITES_DIR, "Spr_1g_006.png")
    charizard_img = PhotoImage(file=charizard)
    charizard_item = canvas_menu.create_image(125, 100, anchor=W, image=charizard_img)
    canvas_menu.charizard_photo = charizard_img # mantener referencia para evitar garbage
    canvas_menu.charizard_item = charizard_item # mantener imagen para usar despues
    boton_info_charizard = Button(canvas_menu, text="Info", command=estadisticas_charizard)
    boton_info_charizard.place(x=160, y=160)
    #Blastoise
    blastoise = asset_path(SPRITES_DIR, "Blastoise.png")
    blastoise_img = PhotoImage(file=blastoise)
    blastoise_item = canvas_menu.create_image(225, 100, anchor=W, image=blastoise_img)
    canvas_menu.blastoise_photo = blastoise_img # mantener referencia para evitar garbage
    canvas_menu.blastoise_item = blastoise_item # mantener imagen para usar despues
    boton_info_blastoise = Button(canvas_menu, text="Info", command=estadisticas_blastoise)
    boton_info_blastoise.place(x=260, y=160)
    #Pidgeot
    pidgeot = asset_path(SPRITES_DIR, "Pidgeot.png")
    pidgeot_img = PhotoImage(file=pidgeot)
    pidgeot_item = canvas_menu.create_image(325, 100, anchor=W, image=pidgeot_img)
    canvas_menu.pidgeot_photo = pidgeot_img # mantener referencia para evitar garbage
    canvas_menu.pidgeot_item = pidgeot_item # mantener imagen para usar despues
    boton_info_pidgeot = Button(canvas_menu, text="Info", command=estadisticas_pidgeot)
    boton_info_pidgeot.place(x=360, y=160)
    #Rhydon
    rydhon = asset_path(SPRITES_DIR, "spr_1g_112.png")
    rydhon_img = PhotoImage(file=rydhon)
    rydhon_item = canvas_menu.create_image(425, 100, anchor=W, image=rydhon_img)
    canvas_menu.rydhon_photo = rydhon_img # mantener referencia para evitar garbage
    canvas_menu.rydhon_item = rydhon_item # mantener imagen para usar despues
    boton_info_rydhon = Button(canvas_menu, text="Info", command=estadisticas_rydhon)
    boton_info_rydhon.place(x=460, y=160)
    #Chansey
    chansey = asset_path(SPRITES_DIR, "Spr_1g_113.png")
    chansey_img = PhotoImage(file=chansey)
    chansey_item = canvas_menu.create_image(25, 250, anchor=W, image=chansey_img)
    canvas_menu.chansey_photo = chansey_img # mantener referencia para evitar garbage
    canvas_menu.chansey_item = chansey_item # mantener imagen para usar despues
    boton_info_chansey = Button(canvas_menu, text="Info", command=estadisticas_chansey)
    boton_info_chansey.place(x=60, y=310)
    #snorlax
    snorlax = asset_path(SPRITES_DIR, "Spr_1g_143.png")
    snorlax_img = PhotoImage(file=snorlax)
    snorlax_item = canvas_menu.create_image(125, 250, anchor=W, image=snorlax_img)
    canvas_menu.snorlax_photo = snorlax_img # mantener referencia para evitar garbage
    canvas_menu.snorlax_item = snorlax_item # mantener imagen para usar despues
    boton_info_snorlax = Button(canvas_menu, text="Info", command=estadisticas_snorlax)
    boton_info_snorlax.place(x=160, y=310)
    #Pikachu
    pikachu = asset_path(SPRITES_DIR, "Spr_1g_025.png")
    pikachu_img = PhotoImage(file=pikachu)
    pikachu_item = canvas_menu.create_image(225, 250, anchor=W, image=pikachu_img)
    canvas_menu.pikachu_photo = pikachu_img # mantener referencia para evitar garbage
    canvas_menu.pikachu_item = pikachu_item # mantener imagen para usar despues
    boton_info_pikachu = Button(canvas_menu, text="Info", command=estadisticas_pikachu)
    boton_info_pikachu.place(x=260, y=310)
    #Nidoking
    nidoking = asset_path(SPRITES_DIR, "Spr_1g_034.png")
    nidoking_img = PhotoImage(file=nidoking)
    nidoking_item = canvas_menu.create_image(325, 250, anchor=W, image=nidoking_img)
    canvas_menu.nidoking_photo = nidoking_img # mantener referencia para evitar garbage
    canvas_menu.nidoking_item = nidoking_item # mantener imagen para usar despues
    boton_info_nidoking = Button(canvas_menu, text="Info", command=estadisticas_nidoking)
    boton_info_nidoking.place(x=360, y=310)
    #machamp
    machamp = asset_path(SPRITES_DIR, "Spr_1g_068.png")
    machamp_img = PhotoImage(file=machamp)
    machamp_item = canvas_menu.create_image(425, 250, anchor=W, image=machamp_img)
    canvas_menu.machamp_photo = machamp_img # mantener referencia para evitar garbage
    canvas_menu.machamp_item = machamp_item # mantener imagen para usar despues
    boton_info_machamp = Button(canvas_menu, text="Info", command=estadisticas_machamp)
    boton_info_machamp.place(x=460, y=310)
    #boton para elegir el nombre
    boton_nombre = Button(canvas_menu, text="Elegir nombre", command=nombre)
    boton_nombre.place(x=10, y=500)
    boton_batalla = Button(canvas_menu, text="Comenzar batalla", command=lambda: (ventana_batalla(), musica_batalla("batalla.wav")))
    boton_batalla.place(x=150, y=500)

def estadisticas_venasour():
    def selección_venasour():
        global pokemones_jugador
        if len(pokemones_jugador) == 3:
            ventana_error_pokemon()
            ventana_venasour.destroy()
        else:
            pokemones_jugador.append("Venusaur")
        print("Pokemones seleccionado: ", pokemones_jugador)
    ventana_venasour = Toplevel()
    ventana_venasour.title("Estadísticas de Venusaur")
    ventana_venasour.geometry("300x400")
    label_venasour = Label(ventana_venasour, text="Estadísticas de Venusaur", font=('Arial', 12))
    label_venasour.pack(pady=10)
    label_stats = Label(ventana_venasour, text= f"HP: {stats['Venusaur']['HP']}\n Attack: {stats['Venusaur']['Attack']}\n Defense: {stats['Venusaur']['Defense']}", font=('Arial', 10))
    label_stats.pack(pady=10)
    boton_cerrar = Button(ventana_venasour, text="Cerrar", command=ventana_venasour.destroy)
    boton_cerrar.pack(pady=10)
    boton_seleccionar = Button(ventana_venasour, text="Seleccionar", command=lambda: (selección_venasour(), ventana_venasour.destroy()))
    boton_seleccionar.pack(pady=10)

def estadisticas_charizard():
    def selección_charizard():
        global pokemones_jugador
        if len(pokemones_jugador) == 3:
            ventana_error_pokemon()
            ventana_charizard.destroy()
        else:
            pokemones_jugador.append("Charizard")
        print("Pokemones seleccionado: ", pokemones_jugador)
    ventana_charizard = Toplevel()
    ventana_charizard.title("Estadísticas de Charizard")
    ventana_charizard.geometry("300x400")
    label_charizard = Label(ventana_charizard, text="Estadísticas de Charizard", font=('Arial', 12))
    label_charizard.pack(pady=10)
    label_stats = Label(ventana_charizard, text=f"HP: {stats['Charizard']['HP']}\n Attack: {stats['Charizard']['Attack']}\n Defense: {stats['Charizard']['Defense']}", font=('Arial', 10))
    label_stats.pack(pady=10)
    boton_cerrar = Button(ventana_charizard, text="Cerrar", command=ventana_charizard.destroy)
    boton_cerrar.pack(pady=10)
    boton_seleccionar = Button(ventana_charizard, text="Seleccionar", command=lambda: (selección_charizard(), ventana_charizard.destroy()))
    boton_seleccionar.pack(pady=10)

def estadisticas_blastoise():
    def selección_blastoise():
        global pokemones_jugador
        if len(pokemones_jugador) == 3:
            ventana_error_pokemon()
            ventana_blastoise.destroy()
        else:
            pokemones_jugador.append("Blastoise")
        print("Pokemones seleccionado: ", pokemones_jugador)
    ventana_blastoise = Toplevel()
    ventana_blastoise.title("Estadísticas de Blastoise")
    ventana_blastoise.geometry("300x400")
    label_blastoise = Label(ventana_blastoise, text="Estadísticas de Blastoise", font=('Arial', 12))
    label_blastoise.pack(pady=10)
    label_stats = Label(ventana_blastoise, text=f"HP: {stats['Blastoise']['HP']}\n Attack: {stats['Blastoise']['Attack']}\n Defense: {stats['Blastoise']['Defense']}", font=('Arial', 10))
    label_stats.pack(pady=10)
    boton_cerrar = Button(ventana_blastoise, text="Cerrar", command=ventana_blastoise.destroy)
    boton_cerrar.pack(pady=10)
    boton_seleccionar = Button(ventana_blastoise, text="Seleccionar", command=lambda: (selección_blastoise(), ventana_blastoise.destroy()))
    boton_seleccionar.pack(pady=10)

def estadisticas_pidgeot():
    def selección_pidgeot():
        global pokemones_jugador
        if len(pokemones_jugador) == 3:
            ventana_error_pokemon()
            ventana_pidgeot.destroy()
        else:
            pokemones_jugador.append("Pidgeot")
        print("Pokemones seleccionado: ", pokemones_jugador)
    ventana_pidgeot = Toplevel()
    ventana_pidgeot.title("Estadísticas de Pidgeot")
    ventana_pidgeot.geometry("300x400")
    label_pidgeot = Label(ventana_pidgeot, text="Estadísticas de Pidgeot", font=('Arial', 12))
    label_pidgeot.pack(pady=10)
    label_stats = Label(ventana_pidgeot, text=f"HP: {stats['Pidgeot']['HP']}\n Attack: {stats['Pidgeot']['Attack']}\n Defense: {stats['Pidgeot']['Defense']}", font=('Arial', 10))
    label_stats.pack(pady=10)
    boton_cerrar = Button(ventana_pidgeot, text="Cerrar", command=ventana_pidgeot.destroy)
    boton_cerrar.pack(pady=10)
    boton_seleccionar = Button(ventana_pidgeot, text="Seleccionar", command=lambda: (selección_pidgeot(), ventana_pidgeot.destroy()))
    boton_seleccionar.pack(pady=10)

def estadisticas_rydhon():
    def selección_rydhon():
        global pokemones_jugador
        if len(pokemones_jugador) == 3:
            ventana_error_pokemon()
            ventana_rydhon.destroy()
        else:
            pokemones_jugador.append("Rhydon")
        print("Pokemones seleccionado: ", pokemones_jugador)
    ventana_rydhon = Toplevel()
    ventana_rydhon.title("Estadísticas de Rhydon")
    ventana_rydhon.geometry("300x400")
    label_rydhon = Label(ventana_rydhon, text="Estadísticas de Rhydon", font=('Arial', 12))
    label_rydhon.pack(pady=10)
    label_stats = Label(ventana_rydhon, text=f"HP: {stats['Rhydon']['HP']}\n Attack: {stats['Rhydon']['Attack']}\n Defense: {stats['Rhydon']['Defense']}", font=('Arial', 10))
    label_stats.pack(pady=10)
    boton_cerrar = Button(ventana_rydhon, text="Cerrar", command=ventana_rydhon.destroy)
    boton_cerrar.pack(pady=10)
    boton_seleccionar = Button(ventana_rydhon, text="Seleccionar", command=lambda: (selección_rydhon(), ventana_rydhon.destroy()))
    boton_seleccionar.pack(pady=10)

def estadisticas_chansey():
    def selección_chansey():
        global pokemones_jugador
        if len(pokemones_jugador) == 3:
            ventana_error_pokemon()
            ventana_chansey.destroy()
        else:
            pokemones_jugador.append("Chansey")
        print("Pokemones seleccionado: ", pokemones_jugador)
    ventana_chansey = Toplevel()
    ventana_chansey.title("Estadísticas de Chansey")
    ventana_chansey.geometry("300x400")
    label_chansey = Label(ventana_chansey, text="Estadísticas de Chansey", font=('Arial', 12))
    label_chansey.pack(pady=10)
    label_stats = Label(ventana_chansey, text=f"HP: {stats['Chansey']['HP']}\n Attack: {stats['Chansey']['Attack']}\n Defense: {stats['Chansey']['Defense']}", font=('Arial', 10))
    label_stats.pack(pady=10)
    boton_cerrar = Button(ventana_chansey, text="Cerrar", command=ventana_chansey.destroy)
    boton_cerrar.pack(pady=10)
    boton_seleccionar = Button(ventana_chansey, text="Seleccionar", command=lambda: (selección_chansey(), ventana_chansey.destroy()))
    boton_seleccionar.pack(pady=10)

def estadisticas_snorlax():
    def selección_snorlax():
        global pokemones_jugador
        if len(pokemones_jugador) == 3:
            ventana_error_pokemon()
            ventana_snorlax.destroy()
        else:
            pokemones_jugador.append("Snorlax")
        print("Pokemones seleccionado: ", pokemones_jugador)
    ventana_snorlax = Toplevel()
    ventana_snorlax.title("Estadísticas de Snorlax")
    ventana_snorlax.geometry("300x400")
    label_snorlax = Label(ventana_snorlax, text="Estadísticas de Snorlax", font=('Arial', 12))
    label_snorlax.pack(pady=10)
    label_stats = Label(ventana_snorlax, text=f"HP: {stats['Snorlax']['HP']}\n Attack: {stats['Snorlax']['Attack']}\n Defense: {stats['Snorlax']['Defense']}", font=('Arial', 10))
    label_stats.pack(pady=10)
    boton_cerrar = Button(ventana_snorlax, text="Cerrar", command=ventana_snorlax.destroy)
    boton_cerrar.pack(pady=10)
    boton_seleccionar = Button(ventana_snorlax, text="Seleccionar", command=lambda: (selección_snorlax(), ventana_snorlax.destroy()))
    boton_seleccionar.pack(pady=10)

def estadisticas_pikachu():
    def selección_pikachu():
        global pokemones_jugador
        if len(pokemones_jugador) == 3:
            ventana_error_pokemon()
            ventana_pikachu.destroy()
        else:
            pokemones_jugador.append("Pikachu")
        print("Pokemones seleccionado: ", pokemones_jugador)
    ventana_pikachu = Toplevel()
    ventana_pikachu.title("Estadísticas de Pikachu")
    ventana_pikachu.geometry("300x400")
    label_pikachu = Label(ventana_pikachu, text="Estadísticas de Pikachu", font=('Arial', 12))
    label_pikachu.pack(pady=10)
    label_stats = Label(ventana_pikachu, text=f"HP: {stats['Pikachu']['HP']}\n Attack: {stats['Pikachu']['Attack']}\n Defense: {stats['Pikachu']['Defense']}", font=('Arial', 10))
    label_stats.pack(pady=10)
    boton_cerrar = Button(ventana_pikachu, text="Cerrar", command=ventana_pikachu.destroy)
    boton_cerrar.pack(pady=10)
    boton_seleccionar = Button(ventana_pikachu, text="Seleccionar", command=lambda: (selección_pikachu(), ventana_pikachu.destroy()))
    boton_seleccionar.pack(pady=10)

def estadisticas_nidoking():
    def selección_nidoking():
        global pokemones_jugador
        if len(pokemones_jugador) == 3:
            ventana_error_pokemon()
            ventana_nidoking.destroy()
        else:
            pokemones_jugador.append("Nidoking")
        print("Pokemones seleccionado: ", pokemones_jugador)
    ventana_nidoking = Toplevel()
    ventana_nidoking.title("Estadísticas de Nidoking")
    ventana_nidoking.geometry("300x400")
    label_nidoking = Label(ventana_nidoking, text="Estadísticas de Nidoking", font=('Arial', 12))
    label_nidoking.pack(pady=10)
    label_stats = Label(ventana_nidoking, text=f"HP: {stats['Nidoking']['HP']}\n Attack: {stats['Nidoking']['Attack']}\n Defense: {stats['Nidoking']['Defense']}", font=('Arial', 10))
    label_stats.pack(pady=10)
    boton_cerrar = Button(ventana_nidoking, text="Cerrar", command=ventana_nidoking.destroy)
    boton_cerrar.pack(pady=10)
    boton_seleccionar = Button(ventana_nidoking, text="Seleccionar", command=lambda: (selección_nidoking(), ventana_nidoking.destroy()))
    boton_seleccionar.pack(pady=10)

def estadisticas_machamp():
    def selección_machamp():
        global pokemones_jugador
        if len(pokemones_jugador) == 3:
            ventana_error_pokemon()
            ventana_machamp.destroy()
        else:
            pokemones_jugador.append("Machamp")
        print("Pokemones seleccionado: ", pokemones_jugador)
    ventana_machamp = Toplevel()
    ventana_machamp.title("Estadísticas de Machamp")
    ventana_machamp.geometry("300x400")
    label_machamp = Label(ventana_machamp, text="Estadísticas de Machamp", font=('Arial', 12))
    label_machamp.pack(pady=10)
    label_stats = Label(ventana_machamp, text=f"HP: {stats['Machamp']['HP']}\n Attack: {stats['Machamp']['Attack']}\n Defense: {stats['Machamp']['Defense']}", font=('Arial', 10))
    label_stats.pack(pady=10)
    boton_cerrar = Button(ventana_machamp, text="Cerrar", command=ventana_machamp.destroy)
    boton_cerrar.pack(pady=10)
    boton_seleccionar = Button(ventana_machamp, text="Seleccionar", command=lambda: (selección_machamp(), ventana_machamp.destroy()))
    boton_seleccionar.pack(pady=10)

def ventana_puntajes(): #muestra la ventana de puntajes, por ahora solo es un placeholder sin funcionalidad real
    ventana_puntaje = Toplevel()
    ventana_puntaje.title("Puntajes")
    ventana_puntaje.geometry("300x400")
    
    label_puntajes = Label(ventana_puntaje, text="Mejores Puntajes", font=('Arial', 14, 'bold'))
    label_puntajes.pack(pady=10)
    
    puntajes = cargar_puntajes()
    
    if len(puntajes) == 0:
        Label(ventana_puntaje, text="No hay puntajes aún", font=('Arial', 12)).pack(pady=5)
    else:
        for i, p in enumerate(puntajes):
            Label(ventana_puntaje,text=f"{i+1}. {p['nombre']} - {p['puntaje']}",font=('Arial', 12)).pack(pady=5)
    boton_cerrar = Button(ventana_puntaje, text="Cerrar", command=ventana_puntaje.destroy)
    boton_cerrar.pack(pady=10)

def ventana_error_pokemon():
    ventana_error = Toplevel()
    ventana_error.title("Error")
    ventana_error.geometry("300x200")
    label_error = Label(ventana_error, text="Ya seleccionaste 3 pokemones", font=('Arial', 12))
    label_error.pack(pady=10)

def nombre():
    def guardar_nombre():
        global nombre_jugador
        nombre_jugador = entry_nombre.get()
        print("Nombre del jugador:", nombre_jugador)
        ventana_nombre.destroy()
    ventana_nombre = Toplevel()
    ventana_nombre.title("Elegir nombre")
    ventana_nombre.geometry("300x200")
    label_nombre = Label(ventana_nombre, text="Ingresa tu nombre", font=('Arial', 12))
    label_nombre.pack(pady=10)
    entry_nombre = Entry(ventana_nombre)
    entry_nombre.pack(pady=10)
    boton_guardar = Button(ventana_nombre, text="Guardar", command=guardar_nombre)
    boton_guardar.pack(pady=10)

def ventana_batalla():
    if len(pokemones_jugador) < 3:
        ventana_error_batalla()
        return
    for w in canvas_menu.winfo_children():
        try:
            w.destroy()
        except Exception:
            pass
    canvas_menu.delete("all")
    fondo_batalla = asset_path(BACKGROUNDS_DIR, "fondo_batalla.png")
    fondo_batalla_img = PhotoImage(file=fondo_batalla)
    canvas_menu.create_image(0, 0, anchor=NW, image=fondo_batalla_img)
    canvas_menu.fondo_batalla = fondo_batalla_img
    steven = asset_path(SPRITES_DIR, "Spr_RS_Steven.png")
    steven_img = PhotoImage(file=steven)
    steven_canvas_id = canvas_menu.create_image(400, 100, anchor=NW, image=steven_img)
    canvas_menu.steven = steven_img
    canvas_menu.Steven_id = steven_canvas_id 
    if personaje_seleccionado == "Red":
        personaje_img = asset_path(SPRITES_DIR, "E_Red_Back.png")
    elif personaje_seleccionado == "Leaf":
        personaje_img = asset_path(SPRITES_DIR, "E_Leaf_Back.png")
    elif personaje_seleccionado == "Brendan":
        personaje_img = asset_path(SPRITES_DIR, "E_Brendan_Back.png")
    elif personaje_seleccionado == "May":
        personaje_img = asset_path(SPRITES_DIR, "E_May_Back.png")
    elif personaje_seleccionado == "Wally":
        personaje_img = asset_path(SPRITES_DIR, "RS_Wally_Back.png")
    personaje_img = PhotoImage(file=personaje_img)
    personaje_canvas_id = canvas_menu.create_image(100, 300, anchor=NW, image=personaje_img)
    canvas_menu.personaje = personaje_img
    canvas_menu.personaje_id = personaje_canvas_id 
    label_batalla = Label(canvas_menu, text="¡Prepárate para la batalla!", font=('Arial', 12), bg='white')
    label_batalla.place(x=10, y=10)
    def continuar_batalla():
        label_batalla.destroy()
        boton_continuar.destroy()
        label_seleccion = Label(canvas_menu, text="selecciona que pokemon quieres usar", font=('Arial', 12), bg='white')
        label_seleccion.place(x=10, y=400)
        boton_pokemon1 = Button(canvas_menu, text=pokemones_jugador[0], command=lambda: (batalla_continuar(pokemones_jugador[0]), print("Seleccionaste", pokemones_jugador[0])))
        boton_pokemon1.place(x=10, y=430)
        boton_pokemon2 = Button(canvas_menu, text=pokemones_jugador[1], command=lambda: (batalla_continuar(pokemones_jugador[1]), print("Seleccionaste", pokemones_jugador[1])))
        boton_pokemon2.place(x=10, y=460)
        boton_pokemon3 = Button(canvas_menu, text=pokemones_jugador[2], command=lambda: (batalla_continuar(pokemones_jugador[2]), print("Seleccionaste", pokemones_jugador[2])))
        boton_pokemon3.place(x=10, y=490)
        def batalla_continuar(pokemon_seleccionado):
            global pokemon_activo
            pokemon_activo = pokemon_seleccionado
            canvas_menu.delete(canvas_menu.personaje_id)
            boton_pokemon1.destroy()
            boton_pokemon2.destroy()
            boton_pokemon3.destroy()
            label_seleccion.destroy()
            def cargar_sprite_pokemon(pokemon_seleccionado):
                sprite = sprites.get(pokemon_seleccionado)
                if not sprite:
                    print(f"Error: No se encontró el sprite para {pokemon_seleccionado}")
                    return
                pokemon_img = PhotoImage(file=asset_path(SPRITES_DIR, sprite))
                id_pokemon = canvas_menu.create_image(100, 300, anchor=NW, image=pokemon_img)
                canvas_menu.pokemon = pokemon_img
                canvas_menu.pokemonid = id_pokemon
            cargar_sprite_pokemon(pokemon_seleccionado)
            boton_continuar2 = Button(canvas_menu, text="Continuar", command=lambda: (batalla_continuar2(), print("Continuar batalla")))
            boton_continuar2.place(x=10, y=500)
            def batalla_continuar2():
                canvas_menu.puntaje = 0
                canvas_menu.turno_actual = 0
                #Sistema de batalla
                def sistema_batalla(atacante, defensor):
                    daño = round(((50*stats[atacante]["Attack"]*2)/(stats[defensor]["Defense"])*random.randint(85, 100)/100),2)
                    print(stats[defensor]["Defendiendo"])
                    if stats[defensor]["Defendiendo"]:
                        daño = daño / 2
                        stats[defensor]["HP"] -= daño
                        stats[defensor]["Defendiendo"] = False
                    else:
                        stats[defensor]["HP"] -= daño
                    if stats[defensor]["HP"] <= 0:
                        stats[defensor]["HP"] = 0
                        print(defensor, "ha sido derrotado")
                        KO(defensor)
                        return
                    if stats[defensor]["HP"] <= 0:
                        print(defensor, "ha sido derrotado")
                    print(atacante, "ataca a", defensor, "y le hace", daño, "de daño. HP restante de", defensor, ":", stats[defensor]["HP"])
                    actualizar_vida()
                def actualizar_vida():
                    if len(pokemones_IA) == 0 or len(pokemones_jugador) == 0:
                        return  # si no quedan pokemones no intentes actualizar los labels
                    try:
                        label_vida_usuario.config(text=f"Tu {pokemon_activo} HP: {stats[pokemon_activo]['HP']}")
                        label_vida_steven.config(text=f"Steven {pokemones_IA[0]} HP: {stats[pokemones_IA[0]]['HP']}")
                    except Exception:
                        return
                def turno_usuario():
                    canvas_menu.turno_actual += 1
                    print(canvas_menu.turno_actual)
                    global turno_limite
                    num = random.randint(0,1)
                    if num < 0.5:
                        ia_defender = False
                        print("Steven decide atacar")
                    else:
                        ia_defender = True
                        print("Steven decide defender")
                        defender(pokemones_IA[0])
                    sistema_batalla(pokemon_activo, pokemones_IA[0])
                    print("Atacaste con", pokemon_activo)
                    if not ia_defender and stats[pokemones_IA[0]]["HP"] > 0:
                        canvas_menu.puntaje += 1
                        print(canvas_menu.puntaje)
                        sistema_batalla(pokemones_IA[0], pokemon_activo)
                    stats[pokemones_IA[0]]["Defendiendo"] = False
                    stats[pokemon_activo]["Defendiendo"] = False
                    if canvas_menu.turno_actual >= turno_limite:
                        canvas_menu.turno_actual = 0
                        canvas_menu.after(500, cambio_forzado)
                        return
                    actualizar_vida()
                def defensa_usuario():
                    canvas_menu.turno_actual += 1
                    canvas_menu.puntaje += 0.5
                    print(canvas_menu.puntaje)
                    print(canvas_menu.turno_actual)
                    if canvas_menu.turno_actual >= turno_limite:
                        canvas_menu.turno_actual = 0
                        canvas_menu.after(500, cambio_forzado)
                        return
                    defender(pokemon_activo)
                    print("Defendiste con", pokemon_activo)
                    sistema_batalla(pokemones_IA[0], pokemon_activo)
                    stats[pokemon_activo]["Defendiendo"] = False
                    stats[pokemones_IA[0]]["Defendiendo"] = False
                    canvas_menu.after(500)
                    actualizar_vida()
                def defender(pokemon):
                    stats[pokemon]["Defendiendo"] = True
                def KO(defensor):
                    canvas_menu.boton_defender.destroy()
                    canvas_menu.boton_atacar.destroy()
                    if defensor in pokemones_jugador:
                        canvas_menu.turno_actual = 0
                        pokemones_jugador.remove(defensor)
                        print(pokemones_jugador)
                        ko_usuario()
                    else:
                        canvas_menu.after(1000)
                        label_ko = Label(canvas_menu, text=f"{defensor} ha sido derrotado\n¿Quieres agregar a {defensor} a tu equipo?", font=('Arial', 12), bg='white')
                        label_ko.place(x=10, y=150)
                        canvas_menu.turno_actual = 0
                        def agregar_pokemon():
                            canvas_menu.puntaje += 1
                            print(canvas_menu.puntaje)
                            pokemones_jugador.append(defensor)
                            print(pokemones_jugador)
                            stats[defensor]["HP"] = 100
                            label_ko.destroy()
                            boton_agregar.destroy()
                            boton_no_agregar.destroy()
                            canvas_menu.delete(canvas_menu.pokemonia_id)
                            canvas_menu.pokemonia = None
                            cambios_pokemon_IA()
                            canvas_menu.after(500)
                            actualizar_vida()
                        def no_agregar():
                            canvas_menu.puntaje += 0.5
                            print(canvas_menu.puntaje)
                            label_ko.destroy()
                            boton_agregar.destroy()
                            boton_no_agregar.destroy()
                            canvas_menu.delete(canvas_menu.pokemonia_id)  # ✅ usa el ID
                            canvas_menu.pokemonia = None 
                            cambios_pokemon_IA()
                            canvas_menu.after(500)
                            actualizar_vida()
                        def cambios_pokemon_IA():
                            pokemones_IA.pop(0)
                            print(pokemones_IA)
                            if len(pokemones_IA) == 0:
                                victoria()
                                return
                            pokemon_ia()
                            mostrar_botones()
                        canvas_menu.after(500)
                        boton_agregar = Button(canvas_menu, text="Si", command=agregar_pokemon)
                        boton_agregar.place(x=10, y=180)
                        boton_no_agregar = Button(canvas_menu, text="No", command=no_agregar)
                        boton_no_agregar.place(x=60, y=180)
                def ko_usuario():
                    canvas_menu.puntaje -= 0.5
                    if len(pokemones_jugador) == 0:
                        derrota()
                        return
                    print(canvas_menu.puntaje)
                    label_ko_usuario = Label(canvas_menu, text="Tu Pokémon ha sido derrotado\nElige otro Pokémon", font=('Arial', 12), bg='white')
                    label_ko_usuario.place(x=10, y=150)
                    botones_pokemon = []
                    canvas_menu.after(500)
                    for i,pokemon in enumerate(pokemones_jugador):
                        boton = Button(canvas_menu, text=pokemon, command=lambda p=pokemon: (cambiar_pokemon(p, botones_pokemon, label_ko_usuario), print("Cambiaste a", p)))
                        boton.place(x=10, y=180 + i*30)
                        botones_pokemon.append(boton)
                    return botones_pokemon
                def cambiar_pokemon(p, botones, label_ko_usuario):
                    global pokemon_activo
                    pokemon_activo = p
                    label_ko_usuario.destroy()
                    canvas_menu.delete(canvas_menu.pokemonid)
                    for b in botones:
                        b.destroy()
                    cargar_sprite_pokemon(p)
                    mostrar_botones()
                    actualizar_vida()
                def destroy_botones_pokemon(botones):
                    canvas_menu.after(500)
                    canvas_menu.delete(canvas_menu.pokemonid)
                    for b in botones:
                        b.destroy()
                    mostrar_botones()
                    actualizar_vida()
                def cambio_forzado():
                    label_cambio = Label(canvas_menu, text="¡TIEMPO DE CAMBIO! Elige otro Pokémon", font=('Arial', 12), bg='white')
                    label_cambio.place(x=10, y=150)
                    if len(pokemones_IA) > 1:
                        pokemones_IA.append(pokemones_IA.pop(0))  # mueve el primer Pokémon al final de la lista
                    canvas_menu.after(500, lambda: (label_cambio.destroy(), elegir_pokemon_cambio()))
                def elegir_pokemon_cambio():
                    label_elegir = Label(canvas_menu, text="Elige tu nuevo Pokémon", font=('Arial', 12), bg='white')
                    label_elegir.place(x=10, y=180)
                    botones = []
                    canvas_menu.after(500)
                    for i,pokemon in enumerate(pokemones_jugador):
                        boton = Button(canvas_menu, text=pokemon, command=lambda p=pokemon: (confirmar_cambio(p,botones, label_elegir), print("Cambiaste a", p)))
                        boton.place(x=10, y=180 + i*30)
                        botones.append(boton)
                def confirmar_cambio(nuevo_pokemon, botones, label_elegir):
                    global pokemon_activo
                    pokemon_activo = nuevo_pokemon
                    for b in botones:
                        b.destroy()
                    label_elegir.destroy()
                    canvas_menu.delete(canvas_menu.pokemonid)
                    canvas_menu.delete(canvas_menu.pokemonia_id)
                    cargar_sprite_pokemon(nuevo_pokemon)
                    pokemon_ia()
                    actualizar_vida()
                #_________________________________
                #Interfaz de batalla
                def mostrar_botones():
                    boton_atacar = Button(canvas_menu, text="Atacar", command=lambda: (turno_usuario(), print("Atacaste con", pokemon_seleccionado)))
                    boton_atacar.place(x=10, y=110)
                    boton_defender = Button(canvas_menu, text="Defender", command=lambda: (defensa_usuario(), print("Defendiste con", pokemon_seleccionado)))
                    boton_defender.place(x=80, y=110)
                    canvas_menu.boton_atacar = boton_atacar
                    canvas_menu.boton_defender = boton_defender
                def pokemon_ia():
                    if len(pokemones_IA) == 0:  # si no quedan pokemones de la IA no actualices
                        return
                    pokemonia_img = pokemones_IA[0]
                    if pokemonia_img == "Slowbro":
                        pokemonia_img = asset_path(SPRITES_DIR, "Spr_1g_080.png")
                    elif pokemonia_img == "Nidoqueen":
                        pokemonia_img = asset_path(SPRITES_DIR, "Spr_1g_031.png")
                    elif pokemonia_img == "Rapidash":
                        pokemonia_img = asset_path(SPRITES_DIR, "Spr_1g_078.png")
                    elif pokemonia_img == "Dragonite":
                        pokemonia_img = asset_path(SPRITES_DIR, "Spr_1g_149.png")
                    elif pokemonia_img == "Articuno":
                        pokemonia_img = asset_path(SPRITES_DIR, "Spr_1g_144.png")
                    elif pokemonia_img == "Zapdos":
                        pokemonia_img = asset_path(SPRITES_DIR, "Spr_1g_145.png")
                    elif pokemonia_img == "Moltres":
                        pokemonia_img = asset_path(SPRITES_DIR, "Spr_1g_146.png")
                    elif pokemonia_img == "Mewtwo":
                        pokemonia_img = asset_path(SPRITES_DIR, "Spr_1g_150.png")
                    else:
                        print("Has derrotado a todos los pokemones de Steven, ¡Felicidades!")
                    pokemonia_img = PhotoImage(file=pokemonia_img)
                    pokemon_canvas_id = canvas_menu.create_image(400, 100, anchor=NW, image=pokemonia_img)
                    canvas_menu.pokemonia = pokemonia_img
                    canvas_menu.pokemonia_id = pokemon_canvas_id
                    if hasattr(canvas_menu, 'label_prebatalla') and canvas_menu.label_prebatalla.winfo_exists():
                        canvas_menu.label_prebatalla.config(text=f"Steven saca a {pokemones_IA[0]}")
                    else:
                        canvas_menu.label_prebatalla = Label(canvas_menu, text=f"Steven saca a {pokemones_IA[0]}", font=('Arial', 12), bg='white')
                        canvas_menu.label_prebatalla.place(x=10, y=10)
                boton_continuar2.destroy()
                canvas_menu.delete(canvas_menu.Steven_id)
                label_batalla.destroy()
                label_seleccion.destroy()
                pokemon_ia()
                label_vida_usuario = Label(canvas_menu, text=f"Tu {pokemon_seleccionado} HP: {stats[pokemon_seleccionado]['HP']}", font=('Arial', 12), bg='white')
                label_vida_usuario.place(x=10, y=50)
                label_vida_steven = Label(canvas_menu, text=f"Steven {pokemones_IA[0]} HP: {stats[pokemones_IA[0]]['HP']}", font=('Arial', 12), bg='white')
                label_vida_steven.place(x=10, y=80)
                canvas_menu.after(1000, mostrar_botones)  # espera 2 segundos antes de mostrar los botones de acción
    boton_continuar = Button(canvas_menu, text="Continuar", command=continuar_batalla)
    boton_continuar.place(x=10, y=500)

def victoria():
    for w in canvas_menu.winfo_children():
        try:
            w.destroy()
        except Exception:
            pass
    canvas_menu.delete("all")
    fondo_victoria = asset_path(BACKGROUNDS_DIR, "fondo puntaje.png")
    fondo_victoria_img = PhotoImage(file=fondo_victoria)
    canvas_menu.create_image(0, 0, anchor=NW, image=fondo_victoria_img)
    canvas_menu.fondo_victoria = fondo_victoria_img
    label_victoria = Label(canvas_menu, text=f"¡Victoria! Tu puntaje final es: {canvas_menu.puntaje}", font=('Arial', 12), bg='white')
    label_victoria.place(x=10, y=10)
    guardar_puntaje(nombre_jugador, canvas_menu.puntaje)

def derrota():
    for w in canvas_menu.winfo_children():
        try:
            w.destroy()
        except Exception:
            pass
    canvas_menu.delete("all")
    fondo_victoria = asset_path(BACKGROUNDS_DIR, "fondo puntaje.png")
    fondo_victoria_img = PhotoImage(file=fondo_victoria)
    canvas_menu.create_image(0, 0, anchor=NW, image=fondo_victoria_img)
    canvas_menu.fondo_victoria = fondo_victoria_img
    label_victoria = Label(canvas_menu, text=f"¡Derrota! :( Tu puntaje final es: {canvas_menu.puntaje}", font=('Arial', 12), bg='white')
    label_victoria.place(x=10, y=10)
    guardar_puntaje(nombre_jugador, canvas_menu.puntaje)

#función para reproducir música

def setup_music(window, filename=MUSIC_FILENAME): #Investigar el funcionamiento para usarlo en otras ventanas
    """Reproducir música de fondo usando únicamente winsound (builtin en Windows).

    Nota: winsound solo reproduce WAV. Si tienes un MP3, conviértelo a WAV
    (por ejemplo con herramientas como Audacity o ffmpeg) y colócalo en la carpeta 'Smogon'.
    """
    # buscar en varias ubicaciones comunes: en SOUNDS_DIR, BASE_DIR y en BASE_DIR/Smogon
    candidates = [
        path.join(SOUNDS_DIR, filename),
        path.join(BASE_DIR, filename),
        path.join(BASE_DIR, 'Smogon', filename),
    ]
    music_path = None
    for c in candidates:
        if path.exists(c):
            music_path = c
            break
    if music_path is None:
        print('Archivo de música no encontrado. Buscado en:')
        for c in candidates:
            print('  -', c)
        return
    else:
        print('Reproduciendo audio desde:', music_path)
    ext = music_path.lower().rsplit('.', 1)[-1]
    if ext != 'wav':
        print(f"Formato no compatible para el backend integrado: .{ext}. Convierte a WAV o instala pygame/playsound.")
        return
    # solo en Windows
    if platform.system() != 'Windows':
        print('winsound solo está disponible en Windows. En otros sistemas instala pygame o playsound.')
        return
    try:
        import winsound
        # iniciar reproducción en background en loop
        winsound.PlaySound(music_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
        # asegurar que al cerrar la ventana se detenga la reproducción
        def on_close():
            try:
                winsound.PlaySound(None, winsound.SND_PURGE)
            except Exception:
                pass
            window.destroy()
        window.protocol('WM_DELETE_WINDOW', on_close)
    except Exception as e:
        print('Error iniciando winsound:', e)

def ventana_error_batalla():
    ventana_error = Toplevel()
    ventana_error.title("Error")
    ventana_error.geometry("300x200")
    label_error = Label(ventana_error, text="Debes seleccionar 3 pokemones, un personaje y un nombre antes de comenzar la batalla", font=('Arial', 12), wraplength=280)
    label_error.pack(pady=10)

ventana = Tk()
ventana.title("Poketec")
ventana.geometry("558x552")
ventana.resizable(width=FALSE, height=FALSE)

#crea el canvas para el fondo
canvas_menu = Canvas(ventana, width=558, height=552, bg='white')
canvas_menu.place(x=0, y=0)

#label para el about
label_about = Label(canvas_menu, text=about, font=('Arial', 12), bg='white', anchor='nw', justify='left')
label_about.place(x=10, y=10)

#imagen de fondo
canvas_menu.fondo = menu("poketec.png", max_size = (558,552))
fondo_menu = canvas_menu.create_image(0, 0, anchor=NW, image=canvas_menu.fondo)

#boton para mostrar puntajes
btn_puntajes = Button(canvas_menu, text="Puntajes", command=ventana_puntajes)
btn_puntajes.place(x=10, y=500)

btn_personajes = Button(canvas_menu, text="Iniciar", command=lambda: (musica_personajes("personajes.wav"), ventana_personajes()))
btn_personajes.place(x=250, y=500)

setup_music(ventana)
ventana.mainloop()
