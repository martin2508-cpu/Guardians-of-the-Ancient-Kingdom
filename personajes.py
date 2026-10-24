"""Clases del sistema Guardians of the Ancient Kingdom."""

from abc import ABC, abstractmethod
from math import floor


def _entero(valor, nombre, minimo=None, maximo=None):
    """Valida enteros reales (bool no se acepta como entero)."""
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError(f"{nombre} debe ser un número entero.")
    if minimo is not None and valor < minimo:
        raise ValueError(f"{nombre} debe ser como mínimo {minimo}.")
    if maximo is not None and valor > maximo:
        raise ValueError(f"{nombre} debe ser como máximo {maximo}.")
    return valor


class Personaje(ABC):
    """Clase base abstracta para todos los guardianes."""

    def __init__(self, nombre, vida, ataque, defensa):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str):
            raise TypeError("El nombre debe ser texto.")
        valor = valor.strip()
        if not valor:
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = valor

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, valor):
        self.__vida = _entero(valor, "La vida", 0, 100)

    @property
    def ataque(self):
        return self.__ataque

    @ataque.setter
    def ataque(self, valor):
        self.__ataque = _entero(valor, "El ataque", 1)

    @property
    def defensa(self):
        return self.__defensa

    @defensa.setter
    def defensa(self, valor):
        self.__defensa = _entero(valor, "La defensa", 0)

    def recibir_danio(self, cantidad):
        """Aplica daño ya calculado y devuelve el daño efectivamente recibido."""
        _entero(cantidad, "El daño", 0)
        efectivo = min(cantidad, self.vida)
        self.vida = self.vida - efectivo
        return efectivo

    def esta_vivo(self):
        return self.vida > 0

    def mostrar_estado(self):
        return (
            f"{self.nombre} ({self.__class__.__name__}) | "
            f"Vida: {self.vida} | Ataque: {self.ataque} | Defensa: {self.defensa}"
        )

    def _validar_objetivo(self, objetivo):
        if not self.esta_vivo():
            raise RuntimeError(f"{self.nombre} no puede atacar porque está derrotado.")
        if not isinstance(objetivo, Personaje):
            raise TypeError("El objetivo debe ser un objeto Personaje.")
        if objetivo is self:
            raise ValueError("Un personaje no puede atacarse a sí mismo.")
        if not objetivo.esta_vivo():
            raise RuntimeError(f"{objetivo.nombre} ya está derrotado.")

    @abstractmethod
    def atacar(self, objetivo):
        """Calcula y aplica el ataque específico de cada subclase."""
        raise NotImplementedError


class Guerrero(Personaje):
    """Ataca con un golpe potenciado un 20 %."""

    def atacar(self, objetivo):
        self._validar_objetivo(objetivo)
        ataque_potenciado = floor(self.ataque * 1.20)
        danio = max(0, ataque_potenciado - objetivo.defensa)
        return objetivo.recibir_danio(danio)


class Mago(Personaje):
    """Sus hechizos ignoran por completo la defensa del objetivo."""

    def atacar(self, objetivo):
        self._validar_objetivo(objetivo)
        return objetivo.recibir_danio(self.ataque)


class Arquero(Personaje):
    """Duplica el daño base si su ataque supera la defensa enemiga."""

    def atacar(self, objetivo):
        self._validar_objetivo(objetivo)
        if self.ataque > objetivo.defensa:
            danio_base = self.ataque - objetivo.defensa
            danio = danio_base * 2
        else:
            danio = 0
        return objetivo.recibir_danio(danio)


class Combate:
    """Administra turnos de dos personajes creados independientemente."""

    MAX_RONDAS = 50

    def __init__(self, personaje1, personaje2):
        if not isinstance(personaje1, Personaje) or not isinstance(personaje2, Personaje):
            raise TypeError("Combate necesita dos objetos de tipo Personaje.")
        if personaje1 is personaje2:
            raise ValueError("Los participantes deben ser personajes diferentes.")
        self.participantes = (personaje1, personaje2)
        self._indice_turno = 0
        self._ganador = None
        self._empate = False
        self._iniciado = False

    def cambiar_turno(self):
        """Alterna el participante que tiene el turno."""
        self._indice_turno = 1 - self._indice_turno
        return self.participantes[self._indice_turno]

    def verificar_ganador(self):
        vivos = [p for p in self.participantes if p.esta_vivo()]
        if len(vivos) == 1:
            self._ganador = vivos[0]
            return self._ganador
        if len(vivos) == 0:
            self._ganador = None
            self._empate = True
        return None

    def mostrar_resultado(self):
        if self._ganador is not None:
            mensaje = f"GANADOR: {self._ganador.nombre} ({self._ganador.__class__.__name__})"
        elif self._empate:
            mensaje = "EMPATE: ambos personajes han sido derrotados."
        elif self._iniciado:
            mensaje = "EMPATE: el combate terminó sin un ganador."
        else:
            mensaje = "El combate todavía no ha comenzado."
        print("\n" + "=" * 52)
        print(mensaje)
        for personaje in self.participantes:
            print(personaje.mostrar_estado())
        print("=" * 52)
        return mensaje

    def iniciar(self, mostrar=True):
        """Ejecuta hasta 50 rondas; cada ronda da un turno a cada participante."""
        if self._iniciado:
            raise RuntimeError("Este combate ya fue iniciado.")
        self._iniciado = True
        if any(not p.esta_vivo() for p in self.participantes):
            self.verificar_ganador()
            if mostrar:
                self.mostrar_resultado()
            return self._ganador

        if mostrar:
            print("\n=== GUARDIANS OF THE ANCIENT KINGDOM ===")
            print("ESTADO INICIAL")
            for personaje in self.participantes:
                print(personaje.mostrar_estado())

        for ronda in range(1, self.MAX_RONDAS + 1):
            danio_ronda = 0
            for _ in range(2):
                atacante = self.participantes[self._indice_turno]
                objetivo = self.participantes[1 - self._indice_turno]
                if atacante.esta_vivo() and objetivo.esta_vivo():
                    danio = atacante.atacar(objetivo)
                    danio_ronda += danio
                    if mostrar:
                        print(
                            f"\nRonda {ronda} | {atacante.nombre} ataca a {objetivo.nombre}: "
                            f"{danio} de daño efectivo."
                        )
                        for personaje in self.participantes:
                            print("  " + personaje.mostrar_estado())
                    self.cambiar_turno()
                    ganador = self.verificar_ganador()
                    if ganador is not None:
                        if mostrar:
                            self.mostrar_resultado()
                        return ganador
                else:
                    break
            if danio_ronda == 0:
                self._empate = True
                if mostrar:
                    print(f"\nEmpate técnico: nadie causó daño en la ronda {ronda}.")
                    self.mostrar_resultado()
                return None

        self._empate = True
        if mostrar:
            print(f"\nEl combate llegó al límite de {self.MAX_RONDAS} rondas.")
            self.mostrar_resultado()
        return None
