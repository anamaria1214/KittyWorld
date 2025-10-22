# Kitty World

Kitty World es un pequeño juego hecho con Python (probado con Python 3.11.4) y la librería pygame (probado con pygame 2.4.0).

Descripción
-----------
Controlas un cohete ubicado en la parte inferior de la pantalla. Debes disparar a los murciélagos que aparecen desde la parte superior para sumar puntos y evitar que te toquen. Si los murciélagos tocan el cohete pierdes vidas; cuando se acaban las vidas, el juego termina.

Características principales
- Menú de inicio con las opciones: "Jugar" y "Salir".
- Contador de puntaje (superior derecha).
- Contador de vidas (superior izquierda), comienza en 40.
- Pantalla de fin de juego que muestra el puntaje final y botones para reiniciar o salir.

Controles
--------
- Mover a la izquierda: tecla "a"
- Mover a la derecha: tecla "d"
- Disparar: tecla "w"

Cómo jugar
----------
Mueve el cohete para esquivar murciélagos y dispara para eliminarlos. Cada murciélago alcanzado con el láser suma 1 punto. Evita que los murciélagos te toquen para no perder vidas. La partida termina cuando tus vidas llegan a 0.

Requisitos
---------
- Python 3.11 (o compatible)
- pygame 2.4.0

Instalación rápida
------------------
1. Clona o descarga este repositorio.

2. Instala pygame:

	```powershell
	pip install pygame==2.4.0
	```

Ejecución
---------
Desde la carpeta del proyecto ejecuta:

```powershell
python videojuego.py
```

Notas y solución de problemas
-----------------------------
- Si el juego no arranca, verifica la versión de Python con `python --version` y que pygame esté instalado (`pip show pygame`).
- Si ves errores relacionados con rutas a imágenes, confirma que la carpeta `imagenes/` está en el mismo directorio que `videojuego.py`.

Créditos
-------
Desarrollado por Ana María. Basado en una idea simple de juego arcade para practicar pygame.

¡Disfruta el juego y buena suerte!

