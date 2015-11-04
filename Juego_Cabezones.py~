# -*- encoding: utf-8 -*-
import sys
sys.path.append('.')

import pilasengine

pilas = pilasengine.iniciar()
fondo = pilas.fondos.Espacio()

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



class AceitunaConControles(pilasengine.actores.aceituna.Aceituna):

    def iniciar(self):
        self.imagen = "aceituna.png"
        self.escala = 1.2

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



class MonoConControles(pilasengine.actores.mono.Mono):

    def iniciar(self):
        self.imagen = "mono.png"
        self.escala = .4
        self.radio_de_colision=15
        

        self.saltando = False

    def actualizar(self):
        if self.pilas.escena_actual().control.izquierda:
            self.x -= 4
        elif self.pilas.escena_actual().control.derecha:
            self.x += 4

        if self.pilas.escena_actual().control.arriba:
            if not self.saltando:
                self.hacer("SaltarUnaVez")



pilas.comportamientos.vincular(SaltarUnaVez)
mono_con_controles = MonoConControles(pilas)
pilas.ejecutar()
