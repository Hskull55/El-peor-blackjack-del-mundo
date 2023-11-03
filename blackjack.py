import os 
import tkinter as tk
from tkinter import messagebox
from tkinter.colorchooser import askcolor
import random

valores_cartas = {
    'As': 11, 'Dos': 2, 'Tres': 3, 'Cuatro': 4, 'Cinco': 5, 'Seis': 6,
    'Siete': 7, 'Ocho': 8, 'Nueve': 9, 'Diez': 10, 'Jota': 10, 'Reina': 10, 'Rey': 10
}

ultima_carta = None  # Variable global para la última carta

if not os.path.isfile('stats.txt'):
    with open('stats.txt', 'w') as stats_file:
        stats_file.write('Victorias: 0\nDerrotas: 0\nEmpates: 0')

import random

class Baraja:
    def __init__(self, num_barajas=4):
        self.num_barajas = num_barajas
        self.cartas = ['As', 'Dos', 'Tres', 'Cuatro', 'Cinco', 'Seis', 'Siete', 'Ocho', 'Nueve', 'Diez', 'Jota', 'Reina', 'Rey'] * self.num_barajas
        self.mano = []

    def sacar_carta(self):
        if not self.cartas:
            self.mezclar()
        carta = random.choice(self.cartas)
        self.mano.append(carta)
        self.cartas.remove(carta)
        return carta

    def mezclar(self):
        self.cartas = ['As', 'Dos', 'Tres', 'Cuatro', 'Cinco', 'Seis', 'Siete', 'Ocho', 'Nueve', 'Diez', 'Jota', 'Reina', 'Rey'] * self.num_barajas
        random.shuffle(self.cartas)

    def resetear(self):
        self.cartas = ['As', 'Dos', 'Tres', 'Cuatro', 'Cinco', 'Seis', 'Siete', 'Ocho', 'Nueve', 'Diez', 'Jota', 'Reina', 'Rey'] * self.num_barajas
        self.mano = []


class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []

    def sacar_carta(self, baraja):
        carta = baraja.sacar_carta()
        self.mano.append(carta)
        return carta

    def valor_mano(self):
        valor = 0
        ases = 0
        for carta in self.mano:
            valor += valores_cartas[carta]

            if carta == 'As':
                ases += 1

        while valor > 21 and ases:
            valor -= 10
            ases -= 1

        return valor

    def mostrar_mano(self):
        return self.mano

def regresar_al_menu():
    global boton_iniciar, boton_color, boton_estadisticas

    # Limpiar la interfaz gráfica
    for widget in ventana.winfo_children():
        widget.destroy()

    # Mostrar los botones del menú principal
    boton_iniciar = tk.Button(ventana, text="Iniciar Juego", command=iniciar_juego)
    boton_iniciar.pack()

    boton_color = tk.Button(ventana, text="Elegir Color", command=elegir_color)
    boton_color.pack()

    boton_estadisticas = tk.Button(ventana, text="Estadísticas", command=mostrar_estadisticas)
    boton_estadisticas.pack()

    boton_reglas_del_juego = tk.Button(ventana, text="Reglas del Juego", command=mostrar_reglas)
    boton_reglas_del_juego.pack()


# Modificar la función iniciar_juego
def iniciar_juego():
    global baraja, jugador, dealer, juego_en_curso

    # Ocultar el botón de elegir color
    boton_color.pack_forget()

    # Crear una nueva baraja y mezclarla
    baraja = Baraja()

    # Inicializar jugador y dealer
    jugador = Jugador("Jugador")
    dealer = Jugador("Dealer")

    # Repartir dos cartas al jugador y dos al dealer
    jugador.sacar_carta(baraja)
    jugador.sacar_carta(baraja)
    dealer.sacar_carta(baraja)
    dealer.sacar_carta(baraja)

    juego_en_curso = True

    # Actualizar la interfaz gráfica para mostrar las cartas
    actualizar_interfaz()

    # Agregar un botón para volver al menú
    boton_volver_al_menu = tk.Button(ventana, text="Volver al Menú", command=regresar_al_menu, bg=color_fondo)
    boton_volver_al_menu.pack()

    cambiar_color_botones()

def pedir_carta():
    global baraja, jugador, ultima_carta

    # Guardar la última carta antes de sacar una nueva
    ultima_carta = jugador.sacar_carta(baraja)

    # Verificar si el jugador ha superado los 21 puntos
    if jugador.valor_mano() > 21:
        # Mostrar la última carta antes de mostrar el mensaje de pérdida
        actualizar_interfaz(ultima_carta)
        messagebox.showinfo("Resultado", "¡Has superado 21! ¡Has perdido!")
        with open('stats.txt', 'r') as stats_file:
            stats = stats_file.readlines()
            victorias = int(stats[0].split(': ')[1])
            derrotas = int(stats[1].split(': ')[1])
            empates = int(stats[2].split(': ')[1])

        with open('stats.txt', 'w') as stats_file:
            stats_file.write(f'Victorias: {victorias}\nDerrotas: {derrotas + 1}\nEmpates: {empates}')
        iniciar_juego()  # Iniciar un nuevo juego después de una mano perdida
    elif jugador.valor_mano() == 21:  # Si llega a 21, plantarse automáticamente
        plantarse()
    else:
        actualizar_interfaz()


def plantarse():
    global dealer, juego_en_curso
    juego_en_curso = False

    # El dealer toma cartas hasta llegar a 17 o más
    while dealer.valor_mano() < 17:
        dealer.sacar_carta(baraja)

    # Mostrar las cartas del crupier
    actualizar_interfaz()

    # Esperar un momento antes de mostrar el resultado
    mostrar_resultado()

def mostrar_resultado():
    global juego_en_curso
    # Comparar puntuaciones
    if dealer.valor_mano() > 21 or jugador.valor_mano() > dealer.valor_mano():
        messagebox.showinfo("Resultado", "¡Has ganado!")

        # Actualizar estadísticas en el archivo stats.txt
        with open('stats.txt', 'r') as stats_file:
            stats = stats_file.readlines()
            victorias = int(stats[0].split(': ')[1])
            derrotas = int(stats[1].split(': ')[1])
            empates = int(stats[2].split(': ')[1])

        with open('stats.txt', 'w') as stats_file:
            stats_file.write(f'Victorias: {victorias + 1}\nDerrotas: {derrotas}\nEmpates: {empates}')
    elif jugador.valor_mano() == dealer.valor_mano():
        messagebox.showinfo("Resultado", "¡Empate!")

        # Actualizar estadísticas en el archivo stats.txt
        with open('stats.txt', 'r') as stats_file:
            stats = stats_file.readlines()
            victorias = int(stats[0].split(': ')[1])
            derrotas = int(stats[1].split(': ')[1])
            empates = int(stats[2].split(': ')[1])

        with open('stats.txt', 'w') as stats_file:
            stats_file.write(f'Victorias: {victorias}\nDerrotas: {derrotas}\nEmpates: {empates + 1}')
    else:
        messagebox.showinfo("Resultado", "¡Has perdido!")

        # Actualizar estadísticas en el archivo stats.txt
        with open('stats.txt', 'r') as stats_file:
            stats = stats_file.readlines()
            victorias = int(stats[0].split(': ')[1])
            derrotas = int(stats[1].split(': ')[1])
            empates = int(stats[2].split(': ')[1])

        with open('stats.txt', 'w') as stats_file:
            stats_file.write(f'Victorias: {victorias}\nDerrotas: {derrotas + 1}\nEmpates: {empates}')

    iniciar_juego()  # Iniciar un nuevo juego después de una mano



def actualizar_interfaz(ultima_carta=None):
    # Limpiar la interfaz gráfica
    for widget in ventana.winfo_children():
        widget.destroy()

    # Mostrar las cartas del jugador
    etiqueta_jugador = tk.Label(ventana, text=f"Jugador: {', '.join(jugador.mostrar_mano())}", bg=color_fondo)
    etiqueta_jugador.pack()

    # Mostrar la puntuación del jugador
    etiqueta_puntuacion_jugador = tk.Label(ventana, text=f"Puntuación Jugador: {jugador.valor_mano()}", bg=color_fondo)
    etiqueta_puntuacion_jugador.pack()

    # Mostrar la última carta sacada si hay una
    if ultima_carta is not None:
        etiqueta_ultima_carta = tk.Label(ventana, text=f"Última carta: {ultima_carta}", bg=color_fondo)
        etiqueta_ultima_carta.pack()

    # Mostrar las cartas del crupier
    if not juego_en_curso:
        etiqueta_dealer = tk.Label(ventana, text=f"Dealer: {', '.join(dealer.mostrar_mano())}", bg=color_fondo)
    else:
        etiqueta_dealer = tk.Label(ventana, text=f"Dealer: {dealer.mostrar_mano()[0]}, X", bg=color_fondo)

    etiqueta_dealer.pack()

    # Añadir botones para pedir carta y plantarse
    boton_pedir = tk.Button(ventana, text="Pedir Carta", command=pedir_carta, bg=color_fondo)
    boton_pedir.pack()

    boton_plantarse = tk.Button(ventana, text="Plantarse", command=plantarse, bg=color_fondo)
    boton_plantarse.pack()


# Agregar una función para revelar la segunda carta del dealer
def revelar_carta_dealer():
    global juego_en_curso
    juego_en_curso = False
    actualizar_interfaz()

# Nueva función para cambiar el color de fondo
def cambiar_color_fondo(color):
    global color_fondo
    color_fondo = color
    ventana.configure(bg=color)

    # Actualizar color de fondo de los widgets, excepto los botones
    for widget in ventana.winfo_children():
        if not isinstance(widget, tk.Button):
            widget.configure(bg=color)


# Nueva función para elegir color
def elegir_color():
    color = askcolor(title="Elige un color")  # Abrir el selector de colores
    if color[1]:  # Verificar si se ha seleccionado un color
        cambiar_color_fondo(color[1])

def mostrar_estadisticas():
    try:
        with open('stats.txt', 'r') as stats_file:
            stats = stats_file.readlines()
            victorias = int(stats[0].split(': ')[1])
            derrotas = int(stats[1].split(': ')[1])
            empates = int(stats[2].split(': ')[1])

            total_partidas = victorias + derrotas + empates
            porcentaje_victorias = (victorias / total_partidas) * 100

            estadisticas_text = f"Estadísticas del juego:\n"
            estadisticas_text += f"Victorias: {victorias}\n"
            estadisticas_text += f"Derrotas: {derrotas}\n"
            estadisticas_text += f"Empates: {empates}\n"
            estadisticas_text += f"Porcentaje de victorias: {porcentaje_victorias:.2f}%"

            messagebox.showinfo("Estadísticas", estadisticas_text)
    except FileNotFoundError:
        messagebox.showinfo("Estadísticas", "No hay estadísticas disponibles.")

def mostrar_reglas():
    reglas = """Reglas del Juego:
    1. El objetivo del juego es obtener una mano con un valor lo más cercano posible a 21 sin pasarse.
    2. Cada carta tiene un valor en puntos: As (1 u 11), Dos (2), Tres (3), ... Rey (10).
    3. Se reparten dos cartas al jugador y al crupier al comienzo.
    4. El jugador puede pedir cartas adicionales ('Pedir Carta') o plantarse ('Plantarse').
    5. El crupier también puede pedir cartas adicionales hasta alcanzar 17 o más.
    6. Si el jugador supera 21 puntos, pierde automáticamente. Si el crupier supera 21, el jugador gana.
    7. El jugador gana si tiene una puntuación mayor que el crupier sin pasar de 21.
    8. En caso de empate, se declara un empate.
    9. ¡Disfruta del juego de Blackjack!
    """
    messagebox.showinfo("Reglas del Juego", reglas)

def cambiar_color_botones():
    for widget in ventana.winfo_children():
        if isinstance(widget, tk.Button):
            widget.configure(bg="#F0F0F0")



# Crear ventana principal
ventana = tk.Tk()
ventana.title("Blackjack")
ventana.geometry("300x150")  # Cambia el tamaño de la ventana (ancho x alto)

cambiar_color_fondo("#F0F0F0")

# Botones
boton_iniciar = tk.Button(ventana, text="Iniciar Juego", command=iniciar_juego)
boton_iniciar.pack()

# Botón para elegir color
boton_color = tk.Button(ventana, text="Elegir Color", command=elegir_color)
boton_color.pack()

boton_estadisticas = tk.Button(ventana, text="Estadísticas", command=mostrar_estadisticas)
boton_estadisticas.pack()

boton_reglas = tk.Button(ventana, text="Reglas del Juego", command=mostrar_reglas)
boton_reglas.pack()



# Ejecutar la ventana
ventana.mainloop()
