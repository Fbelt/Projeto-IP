import pygame
import math

ALTURA_SPRITE_JOGADOR = 50
INTERVALO_ANIMACAO = 150  # ms entre troca de frames andando

_sprites_jogador = {}


def _carregar_sprites_jogador():
    if not _sprites_jogador:
        idle = pygame.image.load("imagens/guilherme_idle.png").convert_alpha()
        andando1 = pygame.image.load("imagens/guilherme_walk1.png").convert_alpha()

        largura_alvo = int(idle.get_width() * (ALTURA_SPRITE_JOGADOR / idle.get_height()))

        idle = pygame.transform.smoothscale(idle, (largura_alvo, ALTURA_SPRITE_JOGADOR))
        andando1 = pygame.transform.smoothscale(andando1, (largura_alvo, ALTURA_SPRITE_JOGADOR))
        andando2 = pygame.transform.flip(andando1, True, False)

        _sprites_jogador["idle"] = idle
        _sprites_jogador["andando"] = [andando1, andando2]

    return _sprites_jogador


class jogador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 5
        self.largura = 25
        self.altura = 25
        self.cor = (0, 255, 0)

        self.sprites = _carregar_sprites_jogador()
        self.movendo = False
        self.frame_andando = 0
        self.tempo_ultimo_frame = 0
        self.direcao = 1  # 1 = direita (padrão), -1 = esquerda

    def mover(self, teclas, limite_x, limite_y, mapa_atual, funcao_colisao_mapa):
        x_antigo = self.x
        y_antigo = self.y

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= self.velocidade
            self.direcao = -1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.velocidade
            self.direcao = 1
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

        self.movendo = (self.x != x_antigo) or (self.y != y_antigo)

    def desenhar(self, tela):
        if self.movendo:
            agora = pygame.time.get_ticks()
            if agora - self.tempo_ultimo_frame > INTERVALO_ANIMACAO:
                self.frame_andando = 1 - self.frame_andando
                self.tempo_ultimo_frame = agora
            imagem = self.sprites["andando"][self.frame_andando]
        else:
            imagem = self.sprites["idle"]

        if self.direcao == -1:
            imagem = pygame.transform.flip(imagem, True, False)

        rect = imagem.get_rect(midbottom=(self.x + self.largura // 2, self.y + self.altura))
        tela.blit(imagem, rect)


class inimigo:
   def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 2.5      
        self.largura = 25
        self.altura = 25
        self.cor = (255, 0, 0)

   def mover(self, alvo, mapa_atual, funcao_colisao_mapa):
        dx = alvo.x - self.x
        dy = alvo.y - self.y
        distancia = math.hypot(dx, dy)

        if distancia < 1:
            return

        # vetor normalizado na direção do jogador
        dx /= distancia
        dy /= distancia

        # move em X e Y separadamente, pra conseguir "deslizar" nas paredes
        x_antigo = self.x
        self.x += dx * self.velocidade
        if funcao_colisao_mapa(mapa_atual, self):
            self.x = x_antigo

        y_antigo = self.y
        self.y += dy * self.velocidade
        if funcao_colisao_mapa(mapa_atual, self):
            self.y = y_antigo

   def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.largura, self.altura))