# -*- encoding: utf-8 -*-
import sys
sys.path.append('.')

import pilasengine

pilas = pilasengine.iniciar()
#pilas.depurador.definir_modos(fisica=True)

fondo = pilas.fondos.Fondo()
fondo.imagen = pilas.imagenes.cargar('cancha.png')

fondo.imagen.repetir_vertical = True
fondo.imagen.repetir_horizontal = True

pilas.fisica.eliminar_paredes()

class SaltarUnaVez(pilas.comportamientos.Comportamiento):
    """Realiza un salto, cambiando los atributos 'y'."""

    def iniciar(self, receptor, velocidad_inicial=10, cuando_termina=None):
        """Se invoca cuando se anexa el comportamiento a un actor.

        :param receptor: El actor que comenzará a ejecutar este comportamiento.
        """
        super(SaltarUnaVez, self).iniciar(receptor)
        self.velocidad_inicial = velocidad_inicial
        self.cuando_termina = cuando_termina
        self.sonido_saltar = self.pilas.sonidos.cargar("audio/saltar.wav")
        self.suelo = int(self.receptor.y)
        self.velocidad = self.velocidad_inicial
        self.sonido_saltar.reproducir()
        self.velocidad_aux = self.velocidad_inicial
        self.receptor.saltando = True

    def actualizar(self):
        self.receptor.y += self.velocidad
        self.velocidad -= 0.3

        if self.receptor.y <= self.suelo:
            self.velocidad_aux /= 3.5
            self.velocidad = self.velocidad_aux

            if self.velocidad_aux <= 1:
                # Si toca el suelo
                self.receptor.y = self.suelo
                if self.cuando_termina:
                    self.cuando_termina()
                self.receptor.saltando = False
                return True

teclas = {
            pilas.simbolos.a: 'izquierda',
            pilas.simbolos.d: 'derecha',
            pilas.simbolos.w: 'arriba',
            pilas.simbolos.s: 'abajo',
            pilas.simbolos.ESPACIO: 'boton',
        }

mi_control = pilas.control.Control(teclas)
"""Del ejemplo 'control_personalizado.py'"""



class AceitunaConControles(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = "aceituna.png"
        self.escala = 1.2
        self.radio_de_colision= 21

        self.saltando = False

    def actualizar(self):
        if mi_control.izquierda:
            self.x -= 4

        elif mi_control.derecha:
            self.x += 4
            
        elif mi_control.arriba:
            self.y +=1
            if not self.saltando:
                self.hacer("SaltarUnaVez")
        elif mi_control.abajo:	
            self.y -=1
    

aceituna_con_controles = AceitunaConControles(pilas)
#aceituna_con_controles.aprender(pilas.habilidades.RebotarComoPelota)
aceituna_con_controles.y -= 150
aceituna_con_controles.x -= 100

'''circulo = pilas.fisica.Circulo(0, 0, 15, dinamica=True)
aceituna_con_controles.aprender(pilas.habilidades.Imitar, circulo)'''

class MonoConControles(pilasengine.actores.mono.Mono):

    def iniciar(self):
        self.imagen = "mono.png"
        self.escala = .4
        self.radio_de_colision=21
        
        self.saltando = False

    def actualizar(self):
        if self.pilas.escena_actual().control.izquierda:
            self.x -= 4
        elif self.pilas.escena_actual().control.derecha:
            self.x += 4

        if self.pilas.escena_actual().control.arriba:
            if not self.saltando:
                self.hacer("SaltarUnaVez")


mono_con_controles = MonoConControles(pilas)
#mono_con_controles.aprender(pilas.habilidades.RebotarComoPelota)
mono_con_controles.y -= 150
mono_con_controles.x = 100

pilas.comportamientos.vincular(SaltarUnaVez)

class Pelota(pilasengine.actores.Actor):
    
        def iniciar(self):
            self.imagen = "futbol.png"
            self.escala = 0.115
            self.radio_de_colision=180

            #self.figura.sin_rotacion = True
            #self.figura.escala_de_gravedad = 2


Futbol = Pelota(pilas)
Futbol.aprender(pilas.habilidades.RebotarComoPelota)
#La siguiente habilidad se le agrega al actor unicamente para una prueba respecto a la camara
Futbol.aprender(pilas.habilidades.Arrastrable)


def Choque (Futbol, mono_con_controles):
    print "Funciona"

def Patada (Futbol, aceituna_con_controles):
    print "Funciona 2"    

def Falta (aceituna_con_controles, mono_con_controles):
    print "Funciona 3"



'''rect1=pilas.fisica.Rectangulo(-150,-100,50,50)
aceituna_con_controles.aprender(pilas.habilidades.Imitar,rect1)

rect2=pilas.fisica.Rectangulo(-150,-100,50,50)
mono_con_controles.aprender(pilas.habilidades.Imitar,rect2)'''


pilas.colisiones.agregar(Futbol, mono_con_controles, Choque)
pilas.colisiones.agregar(Futbol, aceituna_con_controles, Patada)
pilas.colisiones.agregar(aceituna_con_controles, mono_con_controles, Falta)

camara = pilas.escena_actual().camara
camara.x = [Futbol.x]

pilas.fisica.Rectangulo(0, -220, 635, 68, sensor=False, dinamica=False)
pilas.ejecutar()
