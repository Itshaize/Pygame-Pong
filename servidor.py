import json
import socket
import time
import pygame
from juego import Juego, dibujar, ANCHO, ALTO

PUERTO = 5000


def main():
    pygame.init()
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('PONG UDP - SERVIDOR (W/S)')
    clock = pygame.time.Clock()
    fuente = pygame.font.Font(None, 70)
    fuente_info = pygame.font.Font(None, 36)
    juego = Juego()

    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind(('0.0.0.0', PUERTO))
    servidor.setblocking(False)
    print(f'Servidor UDP escuchando en puerto {PUERTO}')
    print('Jugador 1: W/S | Reiniciar: R')

    direccion_cliente = None
    ultimo_paquete = 0.0
    controles2 = {'arriba': False, 'abajo': False}
    corriendo = True

    try:
        while corriendo:
            dt = min(clock.tick(60) / 1000, 0.05)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    corriendo = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    juego.reiniciar()

            # Leer los controles UDP sin detener el juego.
            while True:
                try:
                    datos, direccion = servidor.recvfrom(4096)
                except BlockingIOError:
                    break
                try:
                    mensaje = json.loads(datos.decode('utf-8'))
                except (UnicodeDecodeError, ValueError):
                    continue
                if not isinstance(mensaje, dict) or mensaje.get('tipo') != 'control':
                    continue
                # Este Pong acepta un cliente a la vez.
                if direccion_cliente is None:
                    direccion_cliente = direccion
                    print('Cliente conectado:', direccion_cliente)
                if direccion != direccion_cliente:
                    continue
                controles2 = {
                    'arriba': mensaje.get('arriba') is True,
                    'abajo': mensaje.get('abajo') is True,
                }
                ultimo_paquete = time.monotonic()

            # Evita que una barra siga moviéndose si se pierde la conexión.
            if direccion_cliente and time.monotonic() - ultimo_paquete > 3:
                direccion_cliente = None
                controles2 = {'arriba': False, 'abajo': False}
                print('Cliente desconectado: esperando otro cliente...')

            keys = pygame.key.get_pressed()
            controles1 = {'arriba': bool(keys[pygame.K_w]),
                         'abajo': bool(keys[pygame.K_s])}
            juego.actualizar(dt, controles1, controles2)
            estado = juego.estado()
            dibujar(screen, estado, fuente, fuente_info)

            if direccion_cliente:
                paquete = json.dumps(estado).encode('utf-8')
                servidor.sendto(paquete, direccion_cliente)
    finally:
        servidor.close()
        pygame.quit()


if __name__ == '__main__':
    main()
