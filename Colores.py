import colorama

class Colores:
    # Definición de códigos de escape ANSI para colores
    RESET = '\033[0m'
    NEGRO = '\033[30m'
    ROJO = '\033[31m'
    VERDE = '\033[32m'
    AMARILLO = '\033[33m'
    AZUL = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    BLANCO = '\033[37m'
    BRILLANTE_NEGRO = '\033[90m'
    BRILLANTE_ROJO = '\033[91m'
    BRILLANTE_VERDE = '\033[92m'
    BRILLANTE_AMARILLO = '\033[93m'
    BRILLANTE_AZUL = '\033[94m'
    BRILLANTE_MAGENTA = '\033[95m'
    BRILLANTE_CYAN = '\033[96m'
    BRILLANTE_BLANCO = '\033[97m'
    FONDO_NEGRO = '\033[40m'
    FONDO_ROJO = '\033[41m'
    FONDO_VERDE = '\033[42m'
    FONDO_AMARILLO = '\033[43m'
    FONDO_AZUL = '\033[44m'
    FONDO_MAGENTA = '\033[45m'
    FONDO_CYAN = '\033[46m'
    FONDO_BLANCO = '\033[47m'

# Inicializar colorama
colorama.init(autoreset=True)

# Lista de nombres a exportar cuando haces from colores import *
__all__ = ['Color']