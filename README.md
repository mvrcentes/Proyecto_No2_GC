# Proyecto_No2_GC

| Puntos | Requisito | Check | Comentario |
|----|----|----|----|
| 0 a 50 | Por implementar el proyecto en algún hardware distinto a una computadora tradicional | ✅5️⃣0️⃣ |  |
| 20 | Soporte para control | ❌ |  |
| 0 a 30 | Según la estética de su nivel | ✅3️⃣0️⃣ | Tiene reflejos y se ve bonito |
| 15 | Por mantener al rededor de 15 fps (los fps se deben desplegar) | ✅ | mantengo 240 con M1 Pro |
| 20 | Por implementar una cámara con movimiento hacia delante y hacia atrás y rotación | ✅ |  |
| 10 | Por implementar rotación con el mouse (solo horizontal) | ✅ |  |
| 10 | Por implementar un minimapa que muestre la posición de jugador en el mundo. No puede estar lado a lado del mapa principal, debe estar en una esquina.  | ❌ |  |
| 5 | Por agregar música de fondo | ✅ |  |
| 10 | Por agregar efectos de sonido | ✅ |  |
| 20 | Por agregar al menos 1 animación a alguna sprite en la pantalla | ✅ |  |
| 5 | Por agregar una pantalla de bienvenida  | ❌ |  |
| 10 | si la pantalla permite seleccionar entre multiples niveles | ❌ |  |
| 10 | Por agregar una pantalla de exito cuando se cumpla una condicion en el nivel | ❌ |  |
|  |  | Total: 160 |  |




Este es un simple juego de raycasting en 3D creado con la biblioteca Pygame y NumPy. El objetivo principal de este proyecto es proporcionar una implementación básica de raycasting para crear un entorno 3D simulado.

## Librerías utilizadas 
| Nombre | Version | Descripción|
|----|----|----|
| Pygame | 2.0.1+ |  Pygame es una biblioteca de juegos de Python que facilita la creación de juegos y aplicaciones multimedia. Proporciona funcionalidades para la creación de ventanas, manejo de eventos, gráficos y sonido. |
| NumPy | 1.21.2+ | NumPy es una biblioteca para el lenguaje de programación Python que facilita la manipulación de arreglos y matrices. En este proyecto, se utiliza para realizar operaciones numéricas eficientes en los datos de píxeles y para generar mapas aleatorios. |
| Numba (njit) | 0.54.1+ | Numba es una biblioteca de Python que proporciona compilación JIT (Just-In-Time) para acelerar funciones mediante la traducción de código Python en código de máquina. En este proyecto, se utiliza la anotación @njit para acelerar la función new_frame que realiza cálculos intensivos en el bucle principal. |

## Uso mínimo
- Pygame: La función principal main es la entrada al programa. Se encarga de inicializar Pygame, crear la ventana de juego, cargar recursos, y manejar la entrada del usuario. Para ejecutar el juego, simplemente ejecute el script.
- Controles: El movimiento del jugador se controla con las teclas `W, A, S, D` para avanzar, moverse a la izquierda, retroceder y moverse a la derecha, respectivamente. El movimiento horizontal del jugador se controla con el movimiento del ratón.

## Descripción del juego
- Generación de mapa: El mapa del juego se genera de manera aleatoria utilizando la función gen_map. El jugador comienza en una posición específica y debe encontrar la salida, representada por una casilla especial en el mapa.
- Raycasting: El motor de renderizado utiliza la técnica de raycasting para simular gráficos 3D. La función new_frame realiza cálculos para determinar cómo renderizar las paredes, el suelo y el techo en función de la posición y dirección del jugador.
- Sprites: Se han implementado sprites para agregar elementos en el juego. La espada se muestra en la pantalla y tiene una animación de balanceo. Los sprites pueden ser personalizados o expandidos según las necesidades del usuario.
- Sonidos: Se han agregado efectos de sonido para la espada, que se reproducen cuando se realiza un ataque. También hay música de fondo que se reproduce continuamente.

## Requisitos del sistema
Python 3.x
Pygame
NumPy
Numba

## Créditos y recursos
- Skybox: La textura del cielo (skybox2.jpg) fue utilizada y adaptada desde recursos gratuitos en línea.
- Texturas: Las texturas de las paredes (wall.jpg), el suelo (floor.jpg), y la espada (sword1.png) son recursos gratuitos disponibles en línea.
- Sonidos: El sonido de la espada (sword.mp3) y la música de fondo (battlemusic0.mp3) son recursos gratuitos disponibles en línea.
