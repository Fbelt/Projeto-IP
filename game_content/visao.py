import math
import pygame

from game_content.mapa import TAMANHO_TILE, PORTAS_TRANCADAS
RAIO_VISAO_FINAL = 125

TEMPO_MAPA_VISIVEL = 1500
TEMPO_FECHAMENTO_VISAO = 1800
RAIO_REVELACAO_PORTA = 90
DURACAO_ANIMACAO_REVELACAO = 1800
QUANTIDADE_RAIOS = 360
PASSO_RAIO = 4


def bloco_bloqueia_visao(mapa, x, y, inventario=None):
    linha = int(y // TAMANHO_TILE)
    coluna = int(x // TAMANHO_TILE)

    if linha < 0 or linha >= len(mapa):
        return True, None

    if coluna < 0 or coluna >= len(mapa[0]):
        return True, None

    bloco = mapa[linha][coluna]

    if bloco == "#" or bloco == "D":
        return True, (linha, coluna)

    if bloco in PORTAS_TRANCADAS:
        chave_necessaria = PORTAS_TRANCADAS[bloco]

        if inventario is not None and inventario.tem_item(chave_necessaria):
            return False, None

        return True, (linha, coluna)

    return False, None

def calcular_visao(mapa, centro_x, centro_y, raio_visao, inventario=None):
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

            bloqueou, parede = bloco_bloqueia_visao(mapa, x, y, inventario)

            if bloqueou:
                if parede is not None:
                    paredes_visiveis.add(parede)
                break

            distancia += PASSO_RAIO

        pontos_visiveis.append((ponto_final_x, ponto_final_y))

    return pontos_visiveis, paredes_visiveis

def revelar_area_portas_desbloqueadas(camada_escura, mapa, inventario, raio_revelacao=75):
    if inventario is None:
        return

    for linha_indice, linha in enumerate(mapa):
        for coluna_indice, bloco in enumerate(linha):
            if bloco not in PORTAS_TRANCADAS:
                continue

            chave_necessaria = PORTAS_TRANCADAS[bloco]

            if not inventario.tem_item(chave_necessaria):
                continue

            centro_x = coluna_indice * TAMANHO_TILE + TAMANHO_TILE // 2
            centro_y = linha_indice * TAMANHO_TILE + TAMANHO_TILE // 2

            pygame.draw.circle(
                camada_escura,
                (0, 0, 0, 0),
                (centro_x, centro_y),
                raio_revelacao
            )

def criar_animacao_revelacao_portas(mapa, chave):
    portas = []

    for linha_indice, linha in enumerate(mapa):
        for coluna_indice, bloco in enumerate(linha):
            if bloco not in PORTAS_TRANCADAS:
                continue

            chave_necessaria = PORTAS_TRANCADAS[bloco]

            if chave_necessaria != chave:
                continue

            centro_x = coluna_indice * TAMANHO_TILE + TAMANHO_TILE // 2
            centro_y = linha_indice * TAMANHO_TILE + TAMANHO_TILE // 2

            portas.append((centro_x, centro_y))

    if not portas:
        return None

    return {
        "chave": chave,
        "portas": portas,
        "inicio": pygame.time.get_ticks(),
        "duracao": DURACAO_ANIMACAO_REVELACAO,
        "raio_final": RAIO_REVELACAO_PORTA,
    }


def desenhar_animacoes_revelacao_portas(camada_escura, animacoes_revelacao, tempo_atual):
    if animacoes_revelacao is None:
        return []

    animacoes_ativas = []

    for animacao in animacoes_revelacao:
        tempo_passado = tempo_atual - animacao["inicio"]
        progresso = tempo_passado / animacao["duracao"]

        if progresso > 1:
            progresso = 1

        # suaviza o crescimento do círculo
        progresso_suave = 1 - ((1 - progresso) * (1 - progresso))
        raio_atual = int(animacao["raio_final"] * progresso_suave)

        for centro_x, centro_y in animacao["portas"]:
            pygame.draw.circle(
                camada_escura,
                (0, 0, 0, 0),
                (centro_x, centro_y),
                raio_atual
            )

        if progresso < 1:
            animacoes_ativas.append(animacao)

    return animacoes_ativas


def chave_esta_em_animacao(chave, animacoes_revelacao, tempo_atual):
    if animacoes_revelacao is None:
        return False

    for animacao in animacoes_revelacao:
        if animacao["chave"] != chave:
            continue

        tempo_passado = tempo_atual - animacao["inicio"]

        if tempo_passado < animacao["duracao"]:
            return True

    return False


def revelar_area_portas_desbloqueadas(camada_escura, mapa, inventario, animacoes_revelacao, tempo_atual):
    if inventario is None:
        return

    for linha_indice, linha in enumerate(mapa):
        for coluna_indice, bloco in enumerate(linha):
            if bloco not in PORTAS_TRANCADAS:
                continue

            chave_necessaria = PORTAS_TRANCADAS[bloco]

            if not inventario.tem_item(chave_necessaria):
                continue

            if chave_esta_em_animacao(chave_necessaria, animacoes_revelacao, tempo_atual):
                continue

            centro_x = coluna_indice * TAMANHO_TILE + TAMANHO_TILE // 2
            centro_y = linha_indice * TAMANHO_TILE + TAMANHO_TILE // 2

            pygame.draw.circle(
                camada_escura,
                (0, 0, 0, 0),
                (centro_x, centro_y),
                RAIO_REVELACAO_PORTA
            )

def aplicar_visao(tela, jogador, mapa, tempo_inicio_visao, inventario=None, animacoes_revelacao=None, revelar_tudo=False):
    largura_tela, altura_tela = tela.get_size()

    if revelar_tudo:
        return

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
    raio_atual,
    inventario
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
    if animacoes_revelacao is not None:
        animacoes_revelacao[:] = desenhar_animacoes_revelacao_portas(
            camada_escura,
            animacoes_revelacao,
            tempo_atual
        )

    revelar_area_portas_desbloqueadas(
        camada_escura,
        mapa,
        inventario,
        animacoes_revelacao,
        tempo_atual
        )
    tela.blit(camada_escura, (0, 0))