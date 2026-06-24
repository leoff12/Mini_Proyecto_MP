# Mini Proyecto - Movimiento Parabólico
## Problema del Mono y el Cazador

### Descripción

Este proyecto consiste en una simulación del clásico problema físico conocido como "El Mono y el Cazador", desarrollado en Python utilizando la biblioteca Tkinter para la interfaz gráfica.

La simulación demuestra que, si un cazador apunta directamente hacia un mono y dispara en el mismo instante en que el mono se deja caer, ambos objetos experimentan la misma aceleración gravitacional. Como consecuencia, el proyectil impacta al mono siempre que tenga velocidad suficiente para alcanzarlo antes de tocar el suelo.

### Características

- Modificación de velocidad inicial, distancia y altura del mono.
- Animación en tiempo real.
- Pausa y reinicio de la simulación.
- Visualización de la trayectoria del proyectil.
- Visualización de la trayectoria del mono.
- Cálculo y visualización del ángulo de disparo.
- Visualización de vectores de velocidad y gravedad.
- Cronómetro en tiempo real.
- Detección automática de colisión.
- Mensaje de impacto cuando la distancia entre ambos objetos es menor a 0.001 m.

### Ecuaciones utilizadas

Movimiento horizontal del proyectil:

x = v₀ cos(θ) · t

Movimiento vertical del proyectil:

y = v₀ sin(θ) · t − ½gt²

Movimiento vertical del mono:

y = h − ½gt²

Distancia entre ambos objetos:

d = √[(x₁ − x₂)² + (y₁ − y₂)²]

Se considera que existe impacto cuando:

d < 0.001 m

### Tecnologías utilizadas

- Python 3
- Tkinter
- Matemática del movimiento parabólico
- Física clásica (caída libre y tiro parabólico)

### Autor

Proyecto académico desarrollado para el estudio y análisis del movimiento parabólico y la interacción entre proyectiles y cuerpos en caída libre.
