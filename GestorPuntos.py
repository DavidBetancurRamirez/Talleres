import os
import random
import platform
from Colores import Colores

class GestorPuntos:
    def __init__(self):
        self.fin = None
        self.nombre = ''
        self.materia = ''
        self.inicio = None
        self.restantes = []
        self.realizados = []
        self.guardado = True
        self.cantidad_puntos = None


    def add(self):
        self.printColor("Ingrese los puntos realizados\nSepárelos con coma (,)", Colores.MAGENTA)
        agregar_realizados = input()
        numeros = [int(numero.strip()) for numero in agregar_realizados.split(",")]
        
        for numero in numeros:
            if numero not in self.realizados:
                self.realizados.append(numero)

                if self.guardado:
                    self.guardado = False

        self.setRestantes()


    def clsConsole(self):
        if platform.system() == 'Windows':
            # # Windows
            os.system('cls')

        else:
            # # Linux
            os.system('clear')
        
        
    def delete(self):
        self.printColor("Ingrese los que desea eliminar\nSepárelos con coma (,)", Colores.MAGENTA)
        agregar_realizados = input()
        numeros = [int(numero.strip()) for numero in agregar_realizados.split(",")]
        
        for num in numeros:
            if num in self.realizados:
                self.realizados.remove(num)

                if self.guardado:
                    self.guardado = False
                    
        self.setRestantes()
    
    
    def editInfo(self):
        self.guardado = False
        clear = True

        while True:
            self.editMenu(clear)
            opcion = input(Colores.FONDO_CYAN + "Ingrese su opción: ")
            print("" + Colores.RESET)

            if opcion == "0":
                break

            elif opcion == "1":
                self.materia = input(Colores.BRILLANTE_AZUL + "Ingrese el nombre de la materia: ")

            elif opcion == "2":
                self.nombre = input(Colores.BRILLANTE_AZUL + "Ingrese el nombre del taller: ")

            elif opcion == "3":
                self.inicio = int(input(Colores.BRILLANTE_AZUL + "Ingrese el valor de inicio: "))
                self.setCantidadPuntos()
                
            elif opcion == "4":
                self.fin = int(input(Colores.BRILLANTE_AZUL + "Ingrese el valor final: "))
                self.setCantidadPuntos()

            elif opcion == "5":
                self.add()
                print("")
                
            elif opcion == "6":
                self.delete()
                print("")
                
            elif opcion == "7":
                mensaje = self.recover()
                self.clsConsole()
                self.printColor(mensaje, Colores.VERDE)
                clear = False

            else:
                print("Opcion invalida")
                clear = False

        self.clsConsole()
    

    def editMenu(self, clear):
        if clear: 
            self.clsConsole()

        self.printObj()

        str = (
            "\nQue opcion desea editar:\n"
            "\t1 nombre materia\n"
            "\t2 nombre taller\n"
            "\t3 valor inicio\n"
            "\t4 valor fin\n"
            "\t5 agregar números realizados\n"
            "\t6 eliminar números realizados\n"
            "\t7 recuperar progreso\n"
            "\t0 regresar menu principal\n"
        )

        self.printColor(str, Colores.AZUL)


    def exitSave(self, mensaje):
        if self.guardado:
            self.clsConsole()
            return True
        
        while True:
            r = input(Colores.ROJO + mensaje).lower()
            
            if r == "s":
                self.save()

            if r == "n" or r == "s" or r == "0":
                self.clsConsole()
                return True


    def mainMenu(self):
        str = (
            "\nOprima cualquier tecla para nuevo número\n"
            "\t1 ver realizados\n"
            "\t2 ver números restantes\n"
            "\t3 buscar número realizado\n"
            "\t4 guardar progreso\n"
            "\t5 ver info completa\n"
            "\t6 editar info\n"
            "\t0 salir\n"
        )

        self.printColor(str, Colores.AMARILLO)


    def newNumber(self):
        if self.inicio is None or self.fin is None:
            print("Valor inicial o final aun no han sido definidos")
            return

        if len(self.restantes) == 0:
            print("Ya has hecho todos los puntos")
            return

        # Obtener nuevo numero de posicion aleatoria del arreglo de restantes
        nuevo = self.restantes[random.randint(0, len(self.restantes)-1)]    

        # Agregar el nuevo numero a realizados
        self.realizados.append(nuevo)
        self.restantes.remove(nuevo)
        self.guardado = False

        self.printObj()
        self.printColor("\n\tNUEVO: " + str(nuevo), Colores.FONDO_VERDE)


    def nextValue(self, archivo):
        linea = next(archivo).strip()
        return linea.split(":")[1].strip()


    def recover(self):
        self.exitSave("Desea guardar antes de recuperar? (S/N) ")

        self.setInfo(True)
        path = os.path.join('materias', self.materia + '.txt')

        if os.path.exists(path):
            with open(path, 'r') as archivo:
                fin = None
                inicio = None
                realizados = []
                nombre_taller = ""

                for linea in archivo:
                    linea = linea.strip()
                    if linea.startswith("NombreTaller:"):
                        nombre_taller = linea.split(":")[1].strip()

                        if nombre_taller == self.nombre:
                            value = self.nextValue(archivo)
                            inicio = int(value) if value else None

                            value = self.nextValue(archivo)
                            fin = int(value) if value else None

                            value = self.nextValue(archivo)
                            realizados = [int(num) for num in value.split(',') if num.strip()]

                            self.nombre = nombre_taller
                            self.inicio = inicio
                            self.fin = fin
                            self.realizados = realizados
                            self.setCantidadPuntos()
                            self.setRestantes()
                            self.guardado = True
                            return "Recuperacion exitosa"

                archivo.close()
                return f"No se encontro el taller {self.nombre} en la materia {self.materia}"

        else:
            return f"No se encuentra la materia {self.materia}"

    
    def save(self):
        self.setInfo()

        if self.guardado:
            self.printColor("El taller ya esta guardado", Colores.VERDE)
            return

        path = os.path.join('materias', self.materia + '.txt')
        taller_existente = self.tallerExists(path)

        mensaje = ""

        if taller_existente:
            # Editar la información del taller existente
            i = 0

            with open(path, 'r') as archivo:
                lineas = archivo.readlines()

            with open(path, 'w') as archivo:
                for linea in lineas:
                    if linea.strip() == "NombreTaller: {}".format(self.nombre):
                        # Sobrescribir la información del taller existente
                        archivo.write("NombreTaller: {}\n".format(self.nombre))
                        archivo.write("Inicio: {}\n".format(self.inicio))
                        archivo.write("Fin: {}\n".format(self.fin))
                        archivo.write("Realizados: {}\n".format(','.join(map(str, self.realizados))))
                        archivo.write("-------\n")
                        i = 1

                    else:
                        if 0 < i <= 4:  
                            # Borrar info anterior 
                            i += 1

                        else:
                            archivo.write(linea)

            mensaje = "Información del taller editada correctamente"

        else:   
            # Agregar la informacion del taller     
            with open(path, 'a') as archivo:
                archivo.write("NombreTaller: {}\n".format(self.nombre))
                archivo.write("Inicio: {}\n".format(self.inicio))
                archivo.write("Fin: {}\n".format(self.fin))
                archivo.write("Realizados: {}\n".format(','.join(map(str, self.realizados))))
                archivo.write("-------\n")

                archivo.close()
                mensaje = "Guardado correctamente"

        self.guardado = True
        
        self.clsConsole()
        self.printObj()
        self.printColor(mensaje, Colores.VERDE)

    
    def search(self, number):
        return number in self.realizados


    def setCantidadPuntos(self):
        if self.inicio and self.fin:
            self.cantidad_puntos = (self.fin - self.inicio) + 1
            self.setRestantes()


    def setInfo(self, flag=False):
        if self.materia == '' or flag:
            self.materia = input(Colores.BRILLANTE_AZUL + "Ingrese la materia: ")

        if self.nombre == '' or flag:
            self.nombre = input(Colores.BRILLANTE_AZUL + "Ingrese el nombre del taller: ")

        self.printObj()


    def setIntervalo(self):
        self.inicio = int(input(Colores.BRILLANTE_AZUL + "Inicio: "))
        self.fin = int(input("Fin: "))
        self.setCantidadPuntos()
        self.setRestantes()
        

    def setRestantes(self):
        if self.inicio and self.fin:
            self.restantes = [num for num in range(self.inicio, self.fin + 1) if not self.search(num)]


    def start(self):
        self.printColor("Marque 1 para recuperar progreso", Colores.AZUL)
        self.printColor("Marque otra opcion para empezar", Colores.AZUL)
        opcion = input(Colores.FONDO_CYAN + "\nIngrese su opción: ")
        print("" + Colores.RESET)
        self.clsConsole()

        if opcion == "1":
            mensaje = self.recover()
            self.clsConsole()
            self.printObj()
            self.printColor(mensaje, Colores.VERDE)

        else:
            self.setIntervalo()


        flag = True
        while flag:
            self.mainMenu()
            opcion = input(Colores.FONDO_CYAN + "Ingrese su opción: ")
            print("" + Colores.RESET)
            self.clsConsole()

            if opcion == "0":
                flag = not self.exitSave("Desea guardar antes de salir? (S/N) ")

            elif opcion == "1":
                print(self.realizados)

            elif opcion == "2":
                print(self.restantes)

            elif opcion == "3":
                print(self.realizados)
                print("" + Colores.BRILLANTE_AZUL)
                buscar = int(input("Ingrese el número que desea buscar: "))
                if self.search(buscar):
                    self.printColor(f"El punto {buscar} ya se ha realizado", Colores.VERDE)
                else:
                    self.printColor(f"El punto {buscar} no se ha realizado", Colores.ROJO)

            elif opcion == "4":
                self.save()
                
            elif opcion == "5":
                self.printObj()
                
            elif opcion == "6":
                self.editInfo()

            else:
                self.newNumber()


    def tallerExists(self, path):
        # Verificar si el taller ya existe en el archivo
        taller_existente = False

        try:
            with open(path, 'r') as archivo:
                for linea in archivo:
                    if linea.strip() == "NombreTaller: {}".format(self.nombre):
                        taller_existente = True
                        break

                archivo.close()
        except FileNotFoundError:
            # Controlar excepcion en caso de que el archivo no exista
            pass
        
        return taller_existente
    

    def printColor(self, mensaje, color = Colores.NEGRO):
        print(color + mensaje + Colores.RESET)

    
    def printObj(self):
        str = self.strInfo()
        self.printColor(str, Colores.BRILLANTE_MAGENTA)


    def strInfo(self):
        return f"Materia: {self.materia}\nTaller: {self.nombre}\nInicio: {self.inicio}\nFin: {self.fin}\nCantidad total de puntos: {self.cantidad_puntos}\nPuntos realizados: {self.realizados}\nCantidad puntos realizados: {len(self.realizados)}\nGuardado: {self.guardado}"
    