import pygame

from game_content.mapa import TAMANHO_TILE


ANDAR_FERNANDA = 1  # segundo andar, pois os andares começam em 0

LINHA_FERNANDA = 11
COLUNA_FERNANDA = 40

LARGURA_FERNANDA_TILES = 3
ALTURA_FERNANDA_TILES = 5

DISTANCIA_INTERACAO = 70

CAMINHO_SPRITE_FERNANDA = "imagens/fernanda_idle.png"
TEXTO_DIALOGO_INICIAL = (
    "Pare aí!! Para poder avançar você deve passar pela minha prova "
    "de Introdução à Programação!"
)

COR_CAIXA_DIALOGO = (0, 0, 0)
COR_BORDA_DIALOGO = (255, 255, 255)
COR_TEXTO_DIALOGO = (255, 255, 255)

class BossFernanda:
    def __init__(self):
        self.andar = ANDAR_FERNANDA

        self.linha = LINHA_FERNANDA
        self.coluna = COLUNA_FERNANDA

        self.largura_tiles = LARGURA_FERNANDA_TILES
        self.altura_tiles = ALTURA_FERNANDA_TILES

        self.derrotada = False
        self.dialogo_inicial_mostrado = False
          
        self.rect = self.criar_rect()

        imagem_original = pygame.image.load(CAMINHO_SPRITE_FERNANDA).convert_alpha()

        self.imagem = pygame.transform.smoothscale(
            imagem_original,
            (self.rect.width, self.rect.height)
        )

    def criar_rect(self):
        x = self.coluna * TAMANHO_TILE
        y = self.linha * TAMANHO_TILE

        largura = self.largura_tiles * TAMANHO_TILE
        altura = self.altura_tiles * TAMANHO_TILE

        return pygame.Rect(x, y, largura, altura)

    def obter_rect_personagem(self, personagem):
        return pygame.Rect(
            personagem.x,
            personagem.y,
            personagem.largura,
            personagem.altura
        )

    def desenhar(self, tela, andar_atual):
        if andar_atual != self.andar:
            return

        tela.blit(self.imagem, self.rect)

    def esta_perto_do_jogador(self, jogador, andar_atual):
        if andar_atual != self.andar:
            return False

        if self.derrotada:
            return False

        rect_jogador = self.obter_rect_personagem(jogador)

        area_interacao = self.rect.inflate(
            DISTANCIA_INTERACAO,
            DISTANCIA_INTERACAO
        )

        return area_interacao.colliderect(rect_jogador)

    def bloqueia_passagem(self, personagem, andar_atual):
        if andar_atual != self.andar:
            return False

        if self.derrotada:
            return False

        rect_personagem = self.obter_rect_personagem(personagem)

        return self.rect.colliderect(rect_personagem)

    def marcar_como_derrotada(self):
        self.derrotada = True

        # move 3 colunas para a esquerda após o quiz
        self.coluna -= 3
        self.rect = self.criar_rect()

    def marcar_dialogo_inicial_mostrado(self):
        self.dialogo_inicial_mostrado = True

    def quebrar_texto(self, texto, fonte, largura_maxima):
        palavras = texto.split(" ")
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            teste_linha = linha_atual + palavra + " "
            if fonte.size(teste_linha)[0] <= largura_maxima:
                linha_atual = teste_linha
            else:
                linhas.append(linha_atual)
                linha_atual = palavra + " "

        if linha_atual:
            linhas.append(linha_atual)

        return linhas


    def desenhar_dialogo(self, tela):
        fonte = pygame.font.SysFont(None, 26)
        fonte_instrucao = pygame.font.SysFont(None, 22)

        largura_caixa = 540
        margem_interna = 14
        espaco_linha = 26
        linhas = self.quebrar_texto(
                TEXTO_DIALOGO_INICIAL,
                fonte,
                largura_caixa - margem_interna * 2
            )

        altura_caixa = margem_interna * 2 + len(linhas) * espaco_linha + 26

        x = self.rect.centerx - largura_caixa // 2
        y = self.rect.top - altura_caixa - 12

        if x < 10:
            x = 10

        if x + largura_caixa > tela.get_width() - 10:
            x = tela.get_width() - largura_caixa - 10

        if y < 10:
            y = 10

        caixa = pygame.Rect(x, y, largura_caixa, altura_caixa)

        pygame.draw.rect(tela, COR_CAIXA_DIALOGO, caixa)
        pygame.draw.rect(tela, COR_BORDA_DIALOGO, caixa, 3)

        y_texto = y + margem_interna

        for linha in linhas:
            superficie = fonte.render(linha, True, COR_TEXTO_DIALOGO)
            tela.blit(superficie, (x + margem_interna, y_texto))
            y_texto += espaco_linha

        instrucao = fonte_instrucao.render(
                "Pressione ESPAÇO para continuar",
                True,
                COR_TEXTO_DIALOGO
            )

        tela.blit(
            instrucao,
                (
                    caixa.right - instrucao.get_width() - margem_interna,
                    caixa.bottom - instrucao.get_height() - 8
                )
            )