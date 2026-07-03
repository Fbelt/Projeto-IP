import pygame

from game_content.mapa import TAMANHO_TILE


ANDAR_RICARDO = 2  # terceiro andar

LINHA_RICARDO = 14
COLUNA_RICARDO = 18

LARGURA_RICARDO_TILES = 4
ALTURA_RICARDO_TILES = 6

DISTANCIA_INTERACAO = 70

CAMINHO_SPRITE_RICARDO = "imagens/ricardo_idle.png"

TEXTO_INTERACAO_RICARDO = "Aperte F para falar"

FALAS_RICARDO_FINAL = [
    "Finalmente!!",
    "Obrigado querido estudante!! Agora poderemos criar a super IA que criará o mundo perfeito!!"
]

FALAS_RICARDO_INCOMPLETO = [
    "Desculpe, ainda não podemos completar a nossa tarefa sem todas as IA...",
    "Volte depois de adquirir todas elas."
]

COR_CAIXA_MENSAGEM = (0, 0, 0)
COR_BORDA_MENSAGEM = (255, 255, 255)
COR_TEXTO_MENSAGEM = (255, 255, 255)


class ProfessorRicardo:
    def __init__(self):
        self.andar = ANDAR_RICARDO

        self.linha = LINHA_RICARDO
        self.coluna = COLUNA_RICARDO

        self.largura_tiles = LARGURA_RICARDO_TILES
        self.altura_tiles = ALTURA_RICARDO_TILES

        self.indice_fala = 0
        self.falas_atuais = []
        self.dialogo_final = False

        self.rect = self.criar_rect()

        imagem_original = pygame.image.load(CAMINHO_SPRITE_RICARDO).convert_alpha()

        self.imagem = pygame.transform.smoothscale(
            imagem_original,
            (self.rect.width, self.rect.height)
        )

        self.imagem_dialogo = pygame.transform.smoothscale(
            imagem_original,
            (230, 360)
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

        rect_jogador = self.obter_rect_personagem(jogador)

        area_interacao = self.rect.inflate(
            DISTANCIA_INTERACAO,
            DISTANCIA_INTERACAO
        )

        return area_interacao.colliderect(rect_jogador)

    def desenhar_mensagem_interacao(self, tela, jogador, andar_atual):
        if not self.esta_perto_do_jogador(jogador, andar_atual):
            return

        fonte = pygame.font.SysFont(None, 26)

        texto = fonte.render(
            TEXTO_INTERACAO_RICARDO,
            True,
            COR_TEXTO_MENSAGEM
        )

        caixa = texto.get_rect()
        caixa.midbottom = (
            self.rect.centerx,
            self.rect.top - 10
        )

        caixa = caixa.inflate(14, 8)

        if caixa.left < 10:
            caixa.left = 10

        if caixa.right > tela.get_width() - 10:
            caixa.right = tela.get_width() - 10

        if caixa.top < 10:
            caixa.top = 10

        pygame.draw.rect(tela, COR_CAIXA_MENSAGEM, caixa)
        pygame.draw.rect(tela, COR_BORDA_MENSAGEM, caixa, 2)

        texto_rect = texto.get_rect(center=caixa.center)
        tela.blit(texto, texto_rect)

    def iniciar_dialogo(self, inventario_completo):
        self.indice_fala = 0
        self.dialogo_final = inventario_completo

        if inventario_completo:
            self.falas_atuais = FALAS_RICARDO_FINAL
        else:
            self.falas_atuais = FALAS_RICARDO_INCOMPLETO

    def avancar_dialogo(self):
        if self.indice_fala < len(self.falas_atuais) - 1:
            self.indice_fala += 1
            return "continuar"

        if self.dialogo_final:
            return "vitoria"

        return "normal"

    def quebrar_texto(self, texto, fonte, largura_maxima):
        palavras = texto.split(" ")
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            teste_linha = linha_atual + palavra + " "

            if fonte.size(teste_linha)[0] <= largura_maxima:
                linha_atual = teste_linha
            else:
                if linha_atual:
                    linhas.append(linha_atual)
                linha_atual = palavra + " "

        if linha_atual:
            linhas.append(linha_atual)

        return linhas

    def desenhar_texto_quebrado(self, tela, texto, fonte, cor, x, y, largura_maxima, espaco_linha):
        linhas = self.quebrar_texto(texto, fonte, largura_maxima)

        for linha in linhas:
            superficie = fonte.render(linha, True, cor)
            tela.blit(superficie, (x, y))
            y += espaco_linha

        return y

    def desenhar_tela_dialogo(self, tela):
        largura_tela, altura_tela = tela.get_size()

        tela.fill((12, 12, 18))

        fonte_titulo = pygame.font.SysFont(None, 52)
        fonte_fala = pygame.font.SysFont(None, 32)
        fonte_instrucao = pygame.font.SysFont(None, 24)

        titulo = fonte_titulo.render("Professor Ricardo Massa", True, (255, 255, 255))

        tela.blit(
            titulo,
            (
                largura_tela // 2 - titulo.get_width() // 2,
                40
            )
        )

        rect_ricardo = self.imagem_dialogo.get_rect(
            center=(largura_tela // 2, altura_tela // 2 - 20)
        )

        tela.blit(self.imagem_dialogo, rect_ricardo)

        caixa = pygame.Rect(130, altura_tela - 175, largura_tela - 260, 120)

        pygame.draw.rect(tela, (0, 0, 0), caixa)
        pygame.draw.rect(tela, (255, 255, 255), caixa, 3)

        fala = self.falas_atuais[self.indice_fala]

        self.desenhar_texto_quebrado(
            tela,
            fala,
            fonte_fala,
            (255, 255, 255),
            caixa.x + 20,
            caixa.y + 22,
            caixa.width - 40,
            34
        )

        instrucao = fonte_instrucao.render(
            "Pressione ESPAÇO para continuar",
            True,
            (255, 255, 255)
        )

        tela.blit(
            instrucao,
            (
                largura_tela // 2 - instrucao.get_width() // 2,
                altura_tela - 38
            )
        )