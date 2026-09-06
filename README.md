# Microtractor: Plataforma móvil y modular para el cuidado del huerto

Repositorio del proyecto elaborado como TFM para el Máster Universitario en Robótica e IA de la Universidad de León, España
<p align="center">
<img width="40%" alt="microtractor" src="https://github.com/user-attachments/assets/afffe083-8bd3-47cd-823a-36a4062a4828" />
</p>

## Puesta en marcha

Para controlar el Microtractor de forma teleoperada, se debe lanzar el siguiente comando:

```bash
ros2 launch microtractor microtractor_bringup.launch.py
```

Para acompañarlo con la localización, lanzar en otra terminal:

```bash
ros2 launch microtractor_localization microtractor_localization.launch.py
```

### Controles para teleoperación
Recuerda conectar un mando de videojuegos en uno de los puertos USB disponibles.

* **Palanca izquierda**: Mover en línea recta.
* **Palanca derecha**: Girar.
* **Botón "L"**: Mantener pulsado para habilitar el movimiento.
* **Botón "R"**: Mantener pulsado para habilitar el turbo.
* **Botón "0" ("B" para Nintendo, "X" para PlayStation, "A" para X-Box)**: Bajar el actuador lineal 5 mm.
* **Botón "1" ("A" para Nintendo, "O" para PlayStation, "B" para X-Box)**: Subir el actuador lineal 5 mm.
* **Botón "2" ("Y" para Nintendo, "□" para PlayStation, "X" para X-Box)**: Bajar el actuador lineal 50 mm.
* **Botón "3" ("X" para Nintendo, "△" para PlayStation, "Y" para X-Box)**: Subir el actuador lineal hasta arriba.

## Registrador de parcelas
<p align="center">
<img width="50%" alt="captura_land_register" src="https://github.com/user-attachments/assets/1bb3eba6-27db-4283-9bc9-b657e430797f" />
</p>
Para utilizar el registrador de parcelas, se debe lanzar:

```bash
ros2 run land_register land_register_gui
```

Se recomienda lanzar junto con la **localización** y la **teleoperación**, ya que requiere la información geográfica del RTK y mover el robot por diferentes puntos.

## Generador de rutas
<p align="center">
<img width="50%" alt="capruta_gen_rutas" src="https://github.com/user-attachments/assets/971ffe4c-2dc4-4798-83aa-1e30b85a2b4c" />
</p>
Para utilizar el generador de rutas, se debe lanzar:

```bash
python3 f2c_gui.py
```

Para generar las rutas es necesario contar con un archivo GeoJSON del terreno y un archivo de configuración con las características del apero.

Se recomienda leer la información sobre los algoritmos de [giro](https://fields2cover.github.io/source/tutorials/path_planning.html) y [pasadas](https://fields2cover.github.io/source/tutorials/route_planning.html) de Fields2Cover para comprender sus diferencias.


## Resumen de los paquetes
* **ntrip_client**: Paquete utilizado para conectarse a una estación pública y recibir las correcciones por el protocolo NTRIP
* **ublox**: Este paquete hace efectiva la comunicación entre el receptor RTK y ROS 2.
* **combined_rtk**: Paquete creado con el único propósito de albergar un archivo launch para lanzar los paquetes "ntrip_client" y "ublox".
* **land_register**: Programa con interfaz gráfica para el registrado de parcelas.
* **linear_actuator_node**: Paquete para controlar el actuador lineal de la parte trasera.
* **microtractor_interfaces**: Paquete que alberga interfaces de mensajes y servicios propios utilizados en el prototipo.
* **microtractor_localization**: Paquete encargado de establecer la localización.
* **motor_drivers**: Paquete para controlar los motores de las orugas.
* **microtractor**: Paquete principal. Alberga los datos URDF, de teleoperación y "ros2_control". Dispone de un launch denominado "microtractor_bringup.launch.py" que lanza todos los nodos para poner en marcha el Microtractor.

## Documentación gráfica

Puede ver toda la documentación gráfica (fotos del montaje, vídeos de las pruebas...), accede a esta [carpeta de Google Drive](https://drive.google.com/drive/u/0/folders/1kJPafbQBSl1W93QVNwcT1uQgwa5HNiYm).
