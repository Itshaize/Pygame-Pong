# Pygame Pong UDP

Juego Pong para dos computadoras desarrollado con **Python, Pygame y sockets UDP**.

## Archivos
- `juego.py`: lógica de la pelota, colisiones, puntos y dibujo.
- `servidor.py`: ejecuta la partida, controla al jugador 1 y sincroniza datos por UDP.
- `cliente.py`: controla al jugador 2 y muestra el estado recibido.

## Instalación
Se necesita Python y Pygame en ambas computadoras.

```bash
python -m pip install -r requirements.txt
```

## Jugar por la misma red (LAN)

**Servidor** (jugador 1):
```bash
python servidor.py
```

Obtén la IP local en Linux con `hostname -I`.

**Cliente** (jugador 2), reemplazando la IP por la del servidor:
```bash
python cliente.py 192.168.1.100
```

Para probar en una sola computadora:
```bash
python cliente.py 127.0.0.1
```

## Controles
| Jugador | Teclas |
| --- | --- |
| Servidor | W / S |
| Cliente | Flechas arriba / abajo |
| Reiniciar puntuación | R en servidor |

Usa el puerto **5000/UDP**. Ambos equipos deben poder comunicarse por la red; algunas redes universitarias aíslan dispositivos. Si el firewall UFW bloquea el puerto en Linux, puedes permitirlo con `sudo ufw allow 5000/udp`.

## Protocolo
El cliente envía un JSON con `tipo: control` y los booleanos `arriba` y `abajo`. El servidor calcula el juego y envía la pelota, las posiciones de las barras y los marcadores. La partida admite un cliente remoto a la vez.
