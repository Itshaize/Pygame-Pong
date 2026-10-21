import pygame

ANCHO = 1280
ALTO = 720
BARRA_ANCHO = 20
BARRA_ALTO = 120
RADIO = 15
MOV = 450


class Juego:
    def __init__(self):
        self.y1 = float(ALTO / 2 - BARRA_ALTO / 2)
        self.y2 = float(ALTO / 2 - BARRA_ALTO / 2)
        self.puntos1 = 0
        self.puntos2 = 0
        self.pelota = pygame.Vector2(ANCHO / 2, ALTO / 2)
        self.velocidad = pygame.Vector2(400, 250)

    def reiniciar(self):
        self.__init__()

    def actualizar(self, dt, controles1, controles2):
        # Las barras se mueven según las teclas de cada jugador.
        if controles1.get('arriba'):
            self.y1 -= MOV * dt
        if controles1.get('abajo'):
            self.y1 += MOV * dt
        if controles2.get('arriba'):
            self.y2 -= MOV * dt
        if controles2.get('abajo'):
            self.y2 += MOV * dt

        self.y1 = max(0, min(self.y1, ALTO - BARRA_ALTO))
        self.y2 = max(0, min(self.y2, ALTO - BARRA_ALTO))

        jugador1 = pygame.Rect(40, round(self.y1), BARRA_ANCHO, BARRA_ALTO)
        jugador2 = pygame.Rect(ANCHO - 60, round(self.y2), BARRA_ANCHO, BARRA_ALTO)

        self.pelota += self.velocidad * dt

        if self.pelota.y - RADIO <= 0:
            self.pelota.y = RADIO
            self.velocidad.y = abs(self.velocidad.y)
        if self.pelota.y + RADIO >= ALTO:
            self.pelota.y = ALTO - RADIO
            self.velocidad.y = -abs(self.velocidad.y)

        pelota_rect = pygame.Rect(
            round(self.pelota.x - RADIO), round(self.pelota.y - RADIO),
            RADIO * 2, RADIO * 2
        )

        if pelota_rect.colliderect(jugador1) and self.velocidad.x < 0:
            self.pelota.x = jugador1.right + RADIO
            self.velocidad.x = abs(self.velocidad.x)
            self.velocidad.y = (self.pelota.y - jugador1.centery) * 5

        if pelota_rect.colliderect(jugador2) and self.velocidad.x > 0:
            self.pelota.x = jugador2.left - RADIO
            self.velocidad.x = -abs(self.velocidad.x)
            self.velocidad.y = (self.pelota.y - jugador2.centery) * 5

        if self.pelota.x + RADIO < 0:
            self.puntos2 += 1
            self.pelota = pygame.Vector2(ANCHO / 2, ALTO / 2)
            self.velocidad = pygame.Vector2(400, 250)
        if self.pelota.x - RADIO > ANCHO:
            self.puntos1 += 1
            self.pelota = pygame.Vector2(ANCHO / 2, ALTO / 2)
            self.velocidad = pygame.Vector2(-400, -250)

    def estado(self):
        # Solo usamos datos simples para poder transmitirlos con JSON.
        return {
            'pelota': [self.pelota.x, self.pelota.y],
            'y1': self.y1,
            'y2': self.y2,
            'puntos1': self.puntos1,
            'puntos2': self.puntos2,
        }


def dibujar(screen, estado, fuente, fuente_info):
    screen.fill('blue')
    pygame.draw.line(screen, 'white', (ANCHO // 2, 0), (ANCHO // 2, ALTO), 3)

    if estado is None:
        aviso = fuente_info.render('Esperando datos del servidor...', True, 'white')
        screen.blit(aviso, aviso.get_rect(center=(ANCHO // 2, ALTO // 2)))
        pygame.display.flip()
        return

    j1 = pygame.Rect(40, round(estado['y1']), BARRA_ANCHO, BARRA_ALTO)
    j2 = pygame.Rect(ANCHO - 60, round(estado['y2']), BARRA_ANCHO, BARRA_ALTO)
    pygame.draw.rect(screen, 'cyan', j1)
    pygame.draw.rect(screen, 'orange', j2)
    pygame.draw.circle(screen, 'pink', estado['pelota'], RADIO)
    texto1 = fuente.render(str(estado['puntos1']), True, 'white')
    texto2 = fuente.render(str(estado['puntos2']), True, 'white')
    screen.blit(texto1, (ANCHO // 2 - 100, 30))
    screen.blit(texto2, (ANCHO // 2 + 65, 30))
    pygame.display.flip()
