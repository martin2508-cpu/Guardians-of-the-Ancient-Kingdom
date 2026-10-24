"""Pruebas automatizadas. Ejecutar con: python -m pytest -v"""
import pytest
from personajes import Personaje, Guerrero, Mago, Arquero, Combate


def test_creacion_personajes():
    assert isinstance(Guerrero("A", 100, 30, 10), Personaje)
    assert isinstance(Mago("B", 80, 40, 0), Personaje)
    assert isinstance(Arquero("C", 90, 35, 15), Personaje)


@pytest.mark.parametrize("vida", [-1, 101, 1.5, True])
def test_vida_invalida(vida):
    with pytest.raises((ValueError, TypeError)):
        Guerrero("A", vida, 10, 0)


@pytest.mark.parametrize("nombre", ["", "   ", None])
def test_nombre_invalido(nombre):
    with pytest.raises((ValueError, TypeError)):
        Guerrero(nombre, 50, 10, 0)


@pytest.mark.parametrize("ataque,defensa", [(0, 0), (-1, 0), (10, -1), (2.5, 0)])
def test_ataque_defensa_invalidos(ataque, defensa):
    with pytest.raises((ValueError, TypeError)):
        Guerrero("A", 50, ataque, defensa)


def test_guerrero_20_por_ciento_y_redondeo():
    g = Guerrero("G", 100, 30, 0)
    objetivo = Mago("M", 100, 10, 10)
    assert g.atacar(objetivo) == 26
    g2 = Guerrero("G2", 100, 11, 0)
    objetivo2 = Mago("M2", 100, 10, 0)
    assert g2.atacar(objetivo2) == 13  # floor(13.2)


def test_mago_ignora_defensa():
    m = Mago("M", 80, 40, 0)
    objetivo = Guerrero("G", 100, 10, 99)
    assert m.atacar(objetivo) == 40


def test_arquero_critico_y_sin_critico():
    a = Arquero("A", 90, 35, 0)
    objetivo = Guerrero("G", 100, 10, 15)
    assert a.atacar(objetivo) == 40
    objetivo2 = Guerrero("G2", 100, 10, 35)
    assert a.atacar(objetivo2) == 0


def test_vida_no_baja_de_cero_y_devuelve_danio_efectivo():
    m = Mago("M", 80, 40, 0)
    objetivo = Guerrero("G", 5, 10, 0)
    assert m.atacar(objetivo) == 5
    assert objetivo.vida == 0


def test_personaje_derrotado_no_ataca():
    g = Guerrero("G", 0, 30, 0)
    objetivo = Mago("M", 80, 10, 0)
    with pytest.raises(RuntimeError):
        g.atacar(objetivo)


def test_objetivo_invalido():
    g = Guerrero("G", 100, 30, 0)
    with pytest.raises(TypeError):
        g.atacar("no es personaje")


def test_combate_gandalf_gana():
    combate = Combate(Guerrero("Arthas", 100, 30, 20), Mago("Gandalf", 80, 40, 10))
    ganador = combate.iniciar(mostrar=False)
    assert ganador is not None
    assert ganador.nombre == "Gandalf"


def test_empate_tecnico_sin_danio():
    combate = Combate(Guerrero("A", 100, 1, 100), Arquero("B", 100, 1, 100))
    assert combate.iniciar(mostrar=False) is None
    assert combate._empate


def test_no_permite_dos_referencias_iguales():
    g = Guerrero("G", 100, 30, 0)
    with pytest.raises(ValueError):
        Combate(g, g)
