import math
import pygame

from game_content.mapa import TAMANHO_TILE


RAIO_VISAO_FINAL = 125

TEMPO_MAPA_VISIVEL = 1200000000000000000000000
TEMPO_FECHAMENTO_VISAO = 1800

QUANTIDADE_RAIOS = 360
PASSO_RAIO = 4


def bloco_bloqueia_visao(mapa, x, y):
    linha = int(y // TAMANHO_TILE)
    coluna = int(x // TAMANHO_TILE)

    if linha < 0 or linha >= len(mapa):
        return True, None

    if coluna < 0 or coluna >= len(mapa[0]):
        return True, None

    if mapa[linha][coluna] =="#" or  mapa[linha][coluna] =="D":
        return True, (linha, coluna)

    return False, None


def calcular_visao(mapa, centro_x, centro_y, raio_visao):
    pontos_visiveis = []
    paredes_visiveis = set()

    for indice_raio in range(QUANTIDADE_RAIOS):
        angulo = (2 * math.pi) * (indice_raio / QUANTIDADE_RAIOS)

        direcao_x = math.cos(angulo)
        direcao_y = math.sin(angulo)

        ponto_final_x = centro_x
        ponto_final_y = centro_y

        distancia = 0

        while distancia < raio_visao:
            x = centro_x + direcao_x * distancia
            y = centro_y + direcao_y * distancia

            ponto_final_x = x
            ponto_final_y = y

            bloqueou, parede = bloco_bloqueia_visao(mapa, x, y)

            if bloqueou:
                if parede is not None:
                    paredes_visiveis.add(parede)
                break

            distancia += PASSO_RAIO

        pontos_visiveis.append((ponto_final_x, ponto_final_y))

    return pontos_visiveis, paredes_visiveis


def aplicar_visao(tela, jogador, mapa, tempo_inicio_visao):
    largura_tela, altura_tela = tela.get_size()

    tempo_atual = pygame.time.get_ticks()
    tempo_passado = tempo_atual - tempo_inicio_visao

    centro_x = jogador.x + jogador.largura // 2
    centro_y = jogador.y + jogador.altura // 2

    raio_inicial = max(largura_tela, altura_tela)

    if tempo_passado < TEMPO_MAPA_VISIVEL:
        return

    tempo_fechamento = tempo_passado - TEMPO_MAPA_VISIVEL
    progresso = tempo_fechamento / TEMPO_FECHAMENTO_VISAO

    if progresso > 1:
        progresso = 1

    raio_atual = raio_inicial - ((raio_inicial - RAIO_VISAO_FINAL) * progresso)
    raio_atual = int(raio_atual)

    escuridao_atual = int(255 * progresso)

    pontos_visiveis, paredes_visiveis = calcular_visao(
        mapa,
        centro_x,
        centro_y,
        raio_atual
    )

    camada_escura = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)
    camada_escura.fill((0, 0, 0, escuridao_atual))

    # Revela a área livre visível
    if len(pontos_visiveis) >= 3:
        pygame.draw.polygon(
            camada_escura,
            (0, 0, 0, 0),
            pontos_visiveis
        )

    for linha, coluna in paredes_visiveis:
        x = coluna * TAMANHO_TILE
        y = linha * TAMANHO_TILE

        retangulo_parede = pygame.Rect(
            x,
            y,
            TAMANHO_TILE,
            TAMANHO_TILE
        )

        pygame.draw.rect(
            camada_escura,
            (0, 0, 0, 0),
            retangulo_parede
        )

    tela.blit(camada_escura, (0, 0))