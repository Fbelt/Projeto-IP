import pygame
import math

from game_content.mapa import TAMANHO_TILE, pegar_bloco, PORTAS_TRANCADAS


ALTURA_SPRITE_JOGADOR = 70
ALTURA_SPRITE_INIMIGO = 45
INTERVALO_ANIMACAO = 150
TAMANHO_VISUAL_JOGADOR = 25

ANGULO_VISAO_VIGIA = 35
DISTANCIA_VISAO_VIGIA = 75
VELOCIDADE_ROTACAO_VIGIA = 0.35
VELOCIDADE_VIGIA = 1.6

COR_CAMPO_VISAO_VIGIA = (30, 120, 255, 70)

_sprites_jogador = {}
_sprites_fabio = {}


def _carregar_sprites(cache, caminho_idle, caminho_walk1, altura_alvo):
    if not cache:
        idle = pygame.image.load(caminho_idle).convert_alpha()
        andando1 = pygame.image.load(caminho_walk1).convert_alpha()

        largura_alvo = int(idle.get_width() * (altura_alvo / idle.get_height()))

        idle = pygame.transform.smoothscale(idle, (largura_alvo, altura_alvo))
        andando1 = pygame.transform.smoothscale(andando1, (largura_alvo, altura_alvo))
        andando2 = pygame.transform.flip(andando1, True, False)

        cache["idle"] = idle
        cache["andando"] = [andando1, andando2]

    return cache


def _carregar_sprites_jogador():
    return _carregar_sprites(_sprites_jogador, "imagens/guilherme_idle.png", "imagens/guilherme_walk1.png", ALTURA_SPRITE_JOGADOR)


def _carregar_sprites_fabio():
    return _carregar_sprites(_sprites_fabio, "imagens/fabio_idle.png", "imagens/fabio_walk1.png", ALTURA_SPRITE_INIMIGO)


class jogador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 5
        self.largura = 16
        self.altura = 16
        self.cor = (0, 255, 0)

        self.sprites = _carregar_sprites_jogador()
        self.movendo = False
        self.frame_andando = 0
        self.tempo_ultimo_frame = 0
        self.direcao = 1

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

        self.x = max(0, min(self.x, limite_x - self.largura))
        self.y = max(0, min(self.y, limite_y - self.altura))

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

        rect = imagem.get_rect(midbottom=(self.x + TAMANHO_VISUAL_JOGADOR // 2, self.y + TAMANHO_VISUAL_JOGADOR))
        tela.blit(imagem, rect)


class InimigoPatrulha:
    def __init__(self, x, y, direcao="horizontal"):
        self.x = x
        self.y = y
        self.velocidade = 2.0
        self.largura = 25
        self.altura = 25

        self.direcao_eixo = direcao
        self.sentido = 1

        self.sprites = _carregar_sprites_fabio()
        self.movendo = False
        self.frame_andando = 0
        self.tempo_ultimo_frame = 0
        self.direcao = 1

    def mover(self, mapa_atual, funcao_colisao_mapa):
        x_antigo = self.x
        y_antigo = self.y

        if self.direcao_eixo == "horizontal":
            self.x += self.velocidade * self.sentido

            if self.sentido > 0:
                self.direcao = 1
            else:
                self.direcao = -1

            if funcao_colisao_mapa(mapa_atual, self):
                self.x = x_antigo
                self.sentido *= -1
        else:
            self.y += self.velocidade * self.sentido

            if funcao_colisao_mapa(mapa_atual, self):
                self.y = y_antigo
                self.sentido *= -1

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


class InimigoVigia:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_base = x
        self.y_base = y

        self.velocidade = VELOCIDADE_VIGIA
        self.largura = 25
        self.altura = 25

        self.angulo = 0
        self.perseguindo = False
        self.movendo = False

        self.cor = (40, 80, 180)

    def centro(self):
        return (self.x + self.largura // 2, self.y + self.altura // 2)

    def centro_personagem(self, personagem):
        return (personagem.x + personagem.largura // 2, personagem.y + personagem.altura // 2)

    def diferenca_angular(self, angulo_alvo):
        diferenca = (angulo_alvo - self.angulo + 180) % 360 - 180
        return diferenca

    def parede_bloqueia_visao(self, mapa_atual, x1, y1, x2, y2):
        distancia = math.hypot(x2 - x1, y2 - y1)

        if distancia == 0:
            return False

        passos = int(distancia // 5)

        for i in range(passos + 1):
            t = i / max(1, passos)
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t

            bloco = pegar_bloco(mapa_atual, x, y)

            if bloco == "#" or bloco == "D" or bloco in PORTAS_TRANCADAS:
                return True

        return False

    def jogador_no_campo_de_visao(self, mapa_atual, jogador):
        centro_x, centro_y = self.centro()
        jogador_x, jogador_y = self.centro_personagem(jogador)

        dx = jogador_x - centro_x
        dy = jogador_y - centro_y

        distancia = math.hypot(dx, dy)

        if distancia > DISTANCIA_VISAO_VIGIA:
            return False

        angulo_jogador = math.degrees(math.atan2(dy, dx))
        diferenca = self.diferenca_angular(angulo_jogador)

        if abs(diferenca) > ANGULO_VISAO_VIGIA / 2:
            return False

        if self.parede_bloqueia_visao(mapa_atual, centro_x, centro_y, jogador_x, jogador_y):
            return False

        return True

    def mover_em_direcao(self, destino_x, destino_y, mapa_atual, funcao_colisao_mapa):
        x_antigo_total = self.x
        y_antigo_total = self.y

        dx = destino_x - self.x
        dy = destino_y - self.y

        distancia = math.hypot(dx, dy)

        if distancia < 1:
            self.movendo = False
            return

        dx /= distancia
        dy /= distancia

        x_antigo = self.x
        self.x += dx * self.velocidade

        if funcao_colisao_mapa(mapa_atual, self):
            self.x = x_antigo

        y_antigo = self.y
        self.y += dy * self.velocidade

        if funcao_colisao_mapa(mapa_atual, self):
            self.y = y_antigo

        self.movendo = (self.x != x_antigo_total) or (self.y != y_antigo_total)

    def atualizar(self, mapa_atual, jogador, funcao_colisao_mapa):
        centro_x, centro_y = self.centro()
        jogador_x, jogador_y = self.centro_personagem(jogador)

        if self.jogador_no_campo_de_visao(mapa_atual, jogador):
            self.perseguindo = True

            dx = jogador_x - centro_x
            dy = jogador_y - centro_y
            self.angulo = math.degrees(math.atan2(dy, dx))

            self.mover_em_direcao(jogador.x, jogador.y, mapa_atual, funcao_colisao_mapa)
            return

        self.perseguindo = False

        distancia_base = math.hypot(self.x_base - self.x, self.y_base - self.y)

        if distancia_base > 2:
            dx = self.x_base - self.x
            dy = self.y_base - self.y
            self.angulo = math.degrees(math.atan2(dy, dx))

            self.mover_em_direcao(self.x_base, self.y_base, mapa_atual, funcao_colisao_mapa)
        else:
            self.x = self.x_base
            self.y = self.y_base
            self.movendo = False
            self.angulo = (self.angulo + VELOCIDADE_ROTACAO_VIGIA) % 360

    def desenhar_campo_visao(self, tela):
        centro_x, centro_y = self.centro()

        superficie = pygame.Surface(tela.get_size(), pygame.SRCALPHA)

        pontos = [(centro_x, centro_y)]

        metade = ANGULO_VISAO_VIGIA / 2
        quantidade_pontos = 10

        for i in range(quantidade_pontos + 1):
            fator = i / quantidade_pontos
            angulo = self.angulo - metade + ANGULO_VISAO_VIGIA * fator
            angulo_rad = math.radians(angulo)

            x = centro_x + math.cos(angulo_rad) * DISTANCIA_VISAO_VIGIA
            y = centro_y + math.sin(angulo_rad) * DISTANCIA_VISAO_VIGIA

            pontos.append((x, y))

        pygame.draw.polygon(superficie, COR_CAMPO_VISAO_VIGIA, pontos)
        tela.blit(superficie, (0, 0))

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.largura, self.altura))

        centro_x, centro_y = self.centro()
        angulo_rad = math.radians(self.angulo)

        ponta_x = centro_x + math.cos(angulo_rad) * 12
        ponta_y = centro_y + math.sin(angulo_rad) * 12

        pygame.draw.line(tela, (255, 255, 255), (centro_x, centro_y), (ponta_x, ponta_y), 2)
