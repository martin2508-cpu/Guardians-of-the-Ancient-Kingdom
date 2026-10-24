"""Punto de entrada: demostración y casos de prueba manuales."""

from personajes import Personaje, Guerrero, Mago, Arquero, Combate


def ejecutar_pruebas():
    """Ejecuta verificaciones básicas sin depender de Pytest."""
    print("\n=== PRUEBAS MANUALES ===")
    pruebas = []

    # 1. Creación de los tres tipos.
    g = Guerrero("Arthas", 100, 30, 20)
    m = Mago("Gandalf", 80, 40, 10)
    a = Arquero("Legolas", 90, 35, 15)
    pruebas.append(("Crear los tres personajes", isinstance(g, Personaje) and isinstance(m, Personaje) and isinstance(a, Personaje)))

    # 2-4. Validaciones.
    for etiqueta, constructor in [
        ("Rechazar vida mayor que 100", lambda: Guerrero("X", 101, 10, 0)),
        ("Rechazar vida negativa", lambda: Guerrero("X", -1, 10, 0)),
        ("Rechazar nombre vacío", lambda: Guerrero("  ", 50, 10, 0)),
        ("Rechazar ataque cero", lambda: Guerrero("X", 50, 0, 0)),
        ("Rechazar defensa negativa", lambda: Guerrero("X", 50, 10, -1)),
    ]:
        try:
            constructor()
            resultado = False
        except (TypeError, ValueError):
            resultado = True
        pruebas.append((etiqueta, resultado))

    # 5. Guerrero: floor(30 * 1.2) - 10 = 26.
    objetivo = Mago("Objetivo", 80, 10, 10)
    pruebas.append(("Habilidad del Guerrero: 26 de daño", g.atacar(objetivo) == 26 and objetivo.vida == 54))

    # 6. Mago ignora defensa.
    objetivo = Guerrero("Tanque", 100, 10, 99)
    pruebas.append(("Mago ignora defensa: 40 de daño", m.atacar(objetivo) == 40 and objetivo.vida == 60))

    # 7. Arquero duplica daño si ataque > defensa: (35 - 15) * 2 = 40.
    objetivo = Guerrero("Objetivo", 100, 10, 15)
    pruebas.append(("Crítico del Arquero: 40 de daño", a.atacar(objetivo) == 40 and objetivo.vida == 60))

    # 8. La vida no queda negativa.
    objetivo = Guerrero("Débil", 5, 10, 0)
    pruebas.append(("La vida nunca es negativa", m.atacar(objetivo) == 5 and objetivo.vida == 0))

    # 9. Un derrotado no puede atacar.
    try:
        objetivo.atacar(g)
        resultado = False
    except RuntimeError:
        resultado = True
    pruebas.append(("Un derrotado no puede atacar", resultado))

    # 10-11. Combate completo y ganador.
    duelo = Combate(Guerrero("Arthas", 100, 30, 20), Mago("Gandalf", 80, 40, 10))
    ganador = duelo.iniciar(mostrar=False)
    pruebas.append(("Combate completo: gana Gandalf", ganador is not None and ganador.nombre == "Gandalf"))

    # 12. Empate técnico cuando ninguno puede dañar al otro.
    duelo_sin_danio = Combate(Guerrero("Defensor1", 100, 1, 100), Arquero("Defensor2", 100, 1, 100))
    resultado_empate = duelo_sin_danio.iniciar(mostrar=False) is None and duelo_sin_danio._empate
    pruebas.append(("Empate técnico sin daño", resultado_empate))

    for nombre, ok in pruebas:
        print(f"[{'OK' if ok else 'ERROR'}] {nombre}")
    aprobadas = sum(ok for _, ok in pruebas)
    print(f"\nResultado: {aprobadas}/{len(pruebas)} pruebas aprobadas.")
    return aprobadas == len(pruebas)


def main():
    print("=== DEMOSTRACIÓN DEL COMBATE ===")
    arthas = Guerrero("Arthas", 100, 30, 20)
    gandalf = Mago("Gandalf", 80, 40, 10)
    combate = Combate(arthas, gandalf)
    combate.iniciar()
    ejecutar_pruebas()


if __name__ == "__main__":
    main()
