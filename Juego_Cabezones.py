# -*- encoding: utf-8 -*-
import sys
sys.path.append('.')

import pilasengine

pilas = pilasengine.iniciar(ancho=800, alto=640)
#pilas.depurador.definir_modos(fisica=True)

fondo_personalizado = pilas.actores.MapaTiled('es.tmx')

pilas.fisica.eliminar_paredes()
pilas.fisica.eliminar_suelo()

class SaltarUnaVez(pilas.comportamientos.Comportamiento):
    '''Realiza un salto, cambiando los atributos 'y'.'''

    def iniciar(self, receptor, velocidad_inicial=10, cuando_termina=None):
        '''Se invoca cuando se anexa el comportamiento a un actor.'''

        ''':param receptor: El actor que comenzará a ejecutar este comportamiento.'''
        
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



class Aceituna(pilasengine.actores.Actor):

    def iniciar(self):
        self.x=-240
        self.y=-100
        self.imagen = "aceituna.png"
        self.figura = pilas.fisica.Circulo(self.x, self.y, 40, friccion=0, restitucion=0)
        self.figura.sin_rotacion = True
        self.escala = 2.2
        self.radio_de_colision= 38
        self.figura.escala_de_gravedad = 2
        self.sensor_pies = pilas.fisica.Rectangulo(self.x, self.y, 0.1, sensor=True, dinamica=False)
        self.saltando = False
        
        
    def actualizar(self): 
        velocidad = 10
        salto = 10
        self.x = self.figura.x
        self.y = self.figura.y       

        if mi_control.izquierda:
            self.x -= 10
            self.figura.x -= 10

        elif mi_control.derecha:
            self.x += 10
            self.figura.x += 10
            
        elif mi_control.arriba:
            self.y += 10
            self.figura.y += 10
            if not self.saltando:
                self.hacer("SaltarUnaVez")
            

aceituna = Aceituna(pilas)

class Mono(pilasengine.actores.Actor):

    def iniciar(self):
        self.x= 240
        self.y=-100
        self.imagen = "mono.png"
        self.figura = pilas.fisica.Circulo(self.x, self.y, 40, friccion=0, restitucion=0)
        self.figura.sin_rotacion = True
        self.escala = 0.8
        self.radio_de_colision= 38
        self.figura.escala_de_gravedad = 2
        self.sensor_pies = pilas.fisica.Rectangulo(self.x, self.y, 0.1, sensor=True, dinamica=False)
        self.saltando = False


    def actualizar(self):
        velocidad = 10
        salto = 10
        self.x = self.figura.x
        self.y = self.figura.y

        if self.pilas.escena_actual().control.izquierda:
            self.x -= 10
            self.figura.x -= 10

        elif self.pilas.escena_actual().control.derecha:
            self.x += 10
            self.figura.x += 10

        elif self.pilas.escena_actual().control.arriba:
            self.y += 10
            self.figura.y += 10
            if not self.saltando:
                self.hacer("SaltarUnaVez")


mono = Mono(pilas)

pilas.comportamientos.vincular(SaltarUnaVez)

class Pelota(pilasengine.actores.Actor):
    
        def iniciar(self):
            self.x= 15
            self.y=-20
            self.imagen = "futbol.png"
            self.escala = 0.115
            self.radio_de_colision=180
            self.escala_de_gravedad = 6

        def actualizar(self):
            self.x = self.figura.x
            self.y = self.figura.y
            pilas.camara.x=self.x

Futbol = Pelota(pilas)
Futbol.aprender(pilas.habilidades.RebotarComoPelota)


#La siguiente habilidad se le agrega al actor unicamente para una prueba respecto a la camara
Futbol.aprender(pilas.habilidades.Arrastrable)


def Choque (Futbol, mono):
    print "Funciona"

def Patada (Futbol, aceituna):
    print "Funciona 2"    

def Falta (aceituna, mono):
    print "Funciona 3"

pilas.colisiones.agregar(Futbol, mono, Choque)
pilas.colisiones.agregar(Futbol, aceituna, Patada)
pilas.colisiones.agregar(aceituna, mono, Falta)


#pilas.fisica.Rectangulo(0, -220, 635, 68, sensor=False, dinamica=False)
pilas.ejecutar()
