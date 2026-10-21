import json
import socket
import sys
import pygame
from juego import dibujar, ANCHO, ALTO

PUERTO = 5000


def main():
    ip_servidor = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    direccion_servidor = (socket.gethostbyname(ip_servidor), PUERTO)

    pygame.init()
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('PONG UDP - CLIENTE (FLECHAS)')
    clock = pygame.time.Clock()
    fuente = pygame.font.Font(None, 70)
    fuente_info = pygame.font.Font(None, 36)
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cliente.setblocking(False)
    estado = None
    corriendo = True
    print('Conectando a', direccion_servidor)

    try:
        while corriendo:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    corriendo = False

            keys = pygame.key.get_pressed()
            controles = {
                'tipo': 'control',
                'arriba': bool(keys[pygame.K_UP]),
                'abajo': bool(keys[pygame.K_DOWN]),
            }
            cliente.sendto(json.dumps(controles).encode('utf-8'), direccion_servidor)

            # Recibir todas las actualizaciones y quedarse con la más nueva.
            while True:
                try:
                    datos, direccion = cliente.recvfrom(4096)
                except BlockingIOError:
                    break
                if direccion != direccion_servidor:
                    continue
                try:
                    nuevo_estado = json.loads(datos.decode('utf-8'))
                except (UnicodeDecodeError, ValueError):
                    continue
                if isinstance(nuevo_estado, dict) and all(
                    clave in nuevo_estado
                    for clave in ('pelota', 'y1', 'y2', 'puntos1', 'puntos2')
                ):
                    estado = nuevo_estado

            dibujar(screen, estado, fuente, fuente_info)
    finally:
        cliente.close()
        pygame.quit()


if __name__ == '__main__':
    main()
