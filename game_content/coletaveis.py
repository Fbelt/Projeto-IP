import pygame
import random
from game_content import mapa as mapa_modulo

PROXIMIDADE = 50
DIST_MINIMA_ENTRE_ITENS = 80
TAMANHO_SPRITE = 20  
VELOCIDADE_BUFF_GPT = 7
DURACAO_HABILIDADE_GPT = 3000
COOLDOWN_HABILIDADE_GPT = 30000
DURACAO_HABILIDADE_GEMINI = 3000
COOLDOWN_HABILIDADE_GEMINI = 45000

_fonte_mensagem = None

CAMINHOS_IMAGEM = {
    "chave_azul": "imagens/chave_azul.png",
    "chave_verde": "imagens/chave_verde.png",
    "chave_vermelha": "imagens/chave_vermelha.png",
    "logo_claude": "imagens/logoclaude.png",
    "logo_gpt": "imagens/logogpt.png",
    "logo_gemini": "imagens/logogemini.png",
}

_imagens_carregadas = {}


def carregar_imagem(tipo):
    if tipo not in _imagens_carregadas:
        caminho = CAMINHOS_IMAGEM[tipo]
        imagem = pygame.image.load(caminho).convert_alpha()
        imagem = pygame.transform.scale(imagem, (TAMANHO_SPRITE, TAMANHO_SPRITE))
        _imagens_carregadas[tipo] = imagem
    return _imagens_carregadas[tipo]


class Coletaveis(pygame.sprite.Sprite):
    def __init__(self, x, y, andar, tipo):
        super().__init__()
        self.image = carregar_imagem(tipo)
        self.rect = self.image.get_rect(center=(x, y))
        self.andar = andar
        self.tipo = tipo
        self.coletado = False

PONTOS_SPAWN_COLETAVEIS = {
    "chave_azul": [
        (0, 13, 0),
        (0, 25, 9),
        (0, 3, 46),
    ],

    "chave_verde": [
        (1, 26, 18),
        (1, 1, 0),
        (1, 23, 10),
    ],

    "chave_vermelha": [
        (2, 28, 46),
        (2, 25, 15),
    ],

    "logo_gpt": [
        (0, 24, 41),
        (0, 29, 44),
        (0, 29, 37),
    ],

    "logo_gemini": [
        (2, 21, 28),
        (2, 7, 32),
        (2, 3, 8),
    ],
}


def converter_tile_para_pixel(linha, coluna):
    x = coluna * mapa_modulo.TAMANHO_TILE + mapa_modulo.TAMANHO_TILE // 2
    y = linha * mapa_modulo.TAMANHO_TILE + mapa_modulo.TAMANHO_TILE // 2

    return x, y


def sortear_posicoes_coletaveis():
    coletaveis = []

    for tipo, pontos_possiveis in PONTOS_SPAWN_COLETAVEIS.items():
        andar, linha, coluna = random.choice(pontos_possiveis)
        x, y = converter_tile_para_pixel(linha, coluna)

        coletavel = Coletaveis(x, y, andar, tipo)
        coletaveis.append(coletavel)

    return coletaveis


def obter_rect_jogador(player):
    return pygame.Rect(player.x, player.y, player.largura, player.altura)


def checar_proximidade(player, coletaveis, andar_atual):
    rect_jogador = obter_rect_jogador(player)
    item_proximo = None

    for item in coletaveis:
        if item.andar != andar_atual or item.coletado:
            continue
        dist = pygame.math.Vector2(rect_jogador.center).distance_to(item.rect.center)
        if dist <= PROXIMIDADE:
            item_proximo = item
            break

    return item_proximo


def desenhar_mensagem(tela, texto, rect_referencia):
    global _fonte_mensagem
    if _fonte_mensagem is None:
        _fonte_mensagem = pygame.font.SysFont(None, 28)

    superficie = _fonte_mensagem.render(texto, True, (255, 255, 255))
    fundo = superficie.get_rect()
    fundo.midbottom = (rect_referencia.centerx, rect_referencia.top - 10)
    pygame.draw.rect(tela, (0, 0, 0), fundo.inflate(10, 6))
    tela.blit(superficie, fundo)


def aplicar_buff(tipo, player, sistema_vida):
    if tipo == "logo_gpt":
        player.velocidade = VELOCIDADE_BUFF_GPT

    elif tipo == "logo_gemini":
        sistema_vida.ganhar_vida()



def atualizar_coletaveis(tela, player, coletaveis, andar_atual, eventos, inventario, sistema_vida):
    rect_jogador = obter_rect_jogador(player)
    item_proximo = checar_proximidade(player, coletaveis, andar_atual)
    item_coletado = None

    if item_proximo:
        desenhar_mensagem(tela, "Aperte F para coletar este item", rect_jogador)

    for evento in eventos:
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_f:
            if item_proximo:
                item_proximo.coletado = True
                coletaveis.remove(item_proximo)
                inventario.adicionar_item(item_proximo.tipo)
                item_coletado = item_proximo
                aplicar_buff(item_proximo.tipo, player, sistema_vida)

    return item_coletado