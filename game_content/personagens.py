import pygame


class jogador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 5
        self.largura = 25
        self.altura = 25
        self.cor = (0, 255, 0)

    def mover(self, teclas, limite_x, limite_y, mapa_atual, funcao_colisao_mapa):
        x_antigo = self.x
        y_antigo = self.y

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= self.velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.y -= self.velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.y += self.velocidade

        # limite da tela
        self.x = max(0, min(self.x, limite_x - self.largura))
        self.y = max(0, min(self.y, limite_y - self.altura))

        # colisão com parede do mapa
        if funcao_colisao_mapa(mapa_atual, self):
            self.x = x_antigo
            self.y = y_antigo

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.largura, self.altura))


class inimigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 20
        self.largura = 50
        self.altura = 50
        self.cor = (255, 0, 0)

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.largura, self.altura))