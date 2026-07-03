import pygame

from game_content.mapa import TAMANHO_TILE


ANDAR_FERNANDA = 1  # segundo andar

LINHA_FERNANDA = 11
COLUNA_FERNANDA = 39

LARGURA_FERNANDA_TILES = 4
ALTURA_FERNANDA_TILES = 6

DISTANCIA_INTERACAO = 70

CAMINHO_SPRITE_FERNANDA = "imagens/fernanda_idle.png"

TEXTO_DIALOGO_INICIAL = (
    "Pare aí!! Para poder avançar você deve passar pela minha prova "
    "de Introdução à Programação!"
)

COR_CAIXA_DIALOGO = (0, 0, 0)
COR_BORDA_DIALOGO = (255, 255, 255)
COR_TEXTO_DIALOGO = (255, 255, 255)

QUESTOES_FERNANDA = [
    {
        "pergunta": "Qual estrutura é usada para repetir comandos enquanto uma condição for verdadeira?",
        "alternativas": ["if", "while", "def", "import"],
        "correta": 1
    },
    {
        "pergunta": "Em Python, qual palavra-chave é usada para criar uma função?",
        "alternativas": ["class", "def", "for", "return"],
        "correta": 1
    },
    {
        "pergunta": "Qual tipo de dado representa valores verdadeiro ou falso?",
        "alternativas": ["str", "int", "float", "bool"],
        "correta": 3
    }
]

CAMINHO_LOGO_CLAUDE = "imagens/logoclaude.png"

FALAS_RECOMPENSA = [
    "Parabéns! Você passou no teste!",
    "Aqui está! O Claude vai lhe ajudar no próximo andar.",
    "Aperte 1 para usar o Claude e recuperar uma vida caso tenha perdido!"
]

class BossFernanda:
    def __init__(self):
        self.andar = ANDAR_FERNANDA

        self.linha = LINHA_FERNANDA
        self.coluna = COLUNA_FERNANDA

        self.largura_tiles = LARGURA_FERNANDA_TILES
        self.altura_tiles = ALTURA_FERNANDA_TILES

        self.derrotada = False
        self.dialogo_inicial_mostrado = False

        self.questao_atual = 0
        self.acertos = 0
        self.alternativa_escolhida = None
        self.ultima_resposta_correta = None
        self.mensagem_feedback = ""
        self.indice_fala_recompensa = 0
        self.rect = self.criar_rect()

        imagem_original = pygame.image.load(CAMINHO_SPRITE_FERNANDA).convert_alpha()
        self.imagem = pygame.transform.smoothscale(imagem_original, (self.rect.width, self.rect.height))
        self.imagem_quiz = pygame.transform.smoothscale(imagem_original, (180, 260))

        logo_original = pygame.image.load(CAMINHO_LOGO_CLAUDE).convert_alpha()
        self.logo_claude = pygame.transform.smoothscale(logo_original, (80, 80))

    def criar_rect(self):
        x = self.coluna * TAMANHO_TILE
        y = self.linha * TAMANHO_TILE

        largura = self.largura_tiles * TAMANHO_TILE
        altura = self.altura_tiles * TAMANHO_TILE

        return pygame.Rect(x, y, largura, altura)

    def obter_rect_personagem(self, personagem):
        return pygame.Rect(personagem.x, personagem.y, personagem.largura, personagem.altura)

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
        area_interacao = self.rect.inflate(DISTANCIA_INTERACAO, DISTANCIA_INTERACAO)

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

        self.coluna -= 3
        self.rect = self.criar_rect()

    def marcar_dialogo_inicial_mostrado(self):
        self.dialogo_inicial_mostrado = True

    def iniciar_quiz(self):
        self.questao_atual = 0
        self.acertos = 0
        self.alternativa_escolhida = None
        self.ultima_resposta_correta = None
        self.mensagem_feedback = ""

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

    def desenhar_dialogo(self, tela):
        fonte = pygame.font.SysFont(None, 26)
        fonte_instrucao = pygame.font.SysFont(None, 22)

        largura_caixa = 540
        margem_interna = 14
        espaco_linha = 26

        linhas = self.quebrar_texto(TEXTO_DIALOGO_INICIAL, fonte, largura_caixa - margem_interna * 2)
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

        instrucao = fonte_instrucao.render("Pressione ESPAÇO para continuar", True, COR_TEXTO_DIALOGO)
        tela.blit(instrucao, (caixa.right - instrucao.get_width() - margem_interna, caixa.bottom - instrucao.get_height() - 8))

    def responder_quiz(self, indice_alternativa, sistema_vida):
        if self.alternativa_escolhida is not None:
            return None

        pergunta = QUESTOES_FERNANDA[self.questao_atual]

        self.alternativa_escolhida = indice_alternativa
        self.ultima_resposta_correta = indice_alternativa == pergunta["correta"]

        if self.ultima_resposta_correta:
            self.acertos += 1
            self.mensagem_feedback = "Muito bem!"
        else:
            sistema_vida.perder_vida_quiz()
            self.mensagem_feedback = "Resposta incorreta! Você perdeu 1 vida."

        if sistema_vida.fim_jogo:
            return "game_over"

        return None

    def avancar_feedback_quiz(self):
        if self.alternativa_escolhida is None:
            return None

        if self.ultima_resposta_correta:
            if self.acertos >= len(QUESTOES_FERNANDA):
                return "aprovado"

            self.questao_atual += 1

        self.alternativa_escolhida = None
        self.ultima_resposta_correta = None
        self.mensagem_feedback = ""

        return None

    def desenhar_tela_quiz(self, tela, sistema_vida):
        largura_tela, altura_tela = tela.get_size()

        tela.fill((18, 18, 24))

        fonte_titulo = pygame.font.SysFont(None, 42)
        fonte_pergunta = pygame.font.SysFont(None, 30)
        fonte_alternativa = pygame.font.SysFont(None, 28)
        fonte_feedback = pygame.font.SysFont(None, 32)
        fonte_instrucao = pygame.font.SysFont(None, 24)

        titulo = fonte_titulo.render("Prova de Introdução à Programação", True, (255, 255, 255))
        tela.blit(titulo, (largura_tela // 2 - titulo.get_width() // 2, 25))

        tela.blit(self.imagem_quiz, (80, 250))

        nome = fonte_alternativa.render("Prof. Fernanda", True, (255, 255, 255))
        tela.blit(nome, (90, 520))

        sistema_vida.desenhar(tela)

        pergunta = QUESTOES_FERNANDA[self.questao_atual]

        # quadro-negro com a pergunta
        quadro = pygame.Rect(330, 95, 800, 170)
        pygame.draw.rect(tela, (20, 85, 45), quadro)
        pygame.draw.rect(tela, (180, 120, 55), quadro, 6)

        self.desenhar_texto_quebrado(tela, pergunta["pergunta"], fonte_pergunta, (255, 255, 255), quadro.x + 25, quadro.y + 30, quadro.width - 50, 34)

        x_card = 360
        y_card = 300
        largura_card = 720
        altura_card = 65
        espaco_card = 18

        for indice, alternativa in enumerate(pergunta["alternativas"]):
            card = pygame.Rect(x_card, y_card + indice * (altura_card + espaco_card), largura_card, altura_card)

            cor_card = (235, 235, 235)
            cor_borda = (40, 40, 40)
            cor_texto = (0, 0, 0)

            if self.alternativa_escolhida == indice:
                if self.ultima_resposta_correta:
                    cor_card = (60, 170, 80)
                    cor_texto = (255, 255, 255)
                else:
                    cor_card = (190, 40, 40)
                    cor_texto = (255, 255, 255)

            pygame.draw.rect(tela, cor_card, card)
            pygame.draw.rect(tela, cor_borda, card, 3)

            texto_alternativa = f"{indice + 1}) {alternativa}"
            superficie = fonte_alternativa.render(texto_alternativa, True, cor_texto)
            tela.blit(superficie, (card.x + 20, card.centery - superficie.get_height() // 2))

        progresso = fonte_instrucao.render(f"Acertos: {self.acertos}/3", True, (255, 255, 255))
        tela.blit(progresso, (360, 655))

        if self.mensagem_feedback:
            feedback = fonte_feedback.render(self.mensagem_feedback, True, (255, 255, 255))
            tela.blit(feedback, (largura_tela // 2 - feedback.get_width() // 2, 620))

            instrucao = fonte_instrucao.render("Pressione ESPAÇO para continuar", True, (255, 255, 255))
        else:
            instrucao = fonte_instrucao.render("Pressione 1, 2, 3 ou 4 para responder", True, (255, 255, 255))

        tela.blit(instrucao, (largura_tela // 2 - instrucao.get_width() // 2, altura_tela - 45))

    def desenhar_resultado_quiz_temporario(self, tela):
        largura_tela, altura_tela = tela.get_size()

        tela.fill((0, 0, 0))

        fonte_titulo = pygame.font.SysFont(None, 52)
        fonte_texto = pygame.font.SysFont(None, 30)

        texto1 = fonte_titulo.render("Quiz concluído!", True, (0, 255, 0))
        texto2 = fonte_texto.render("Na próxima etapa vamos adicionar a recompensa do Claude.", True, (255, 255, 255))

        tela.blit(texto1, (largura_tela // 2 - texto1.get_width() // 2, altura_tela // 2 - 70))
        tela.blit(texto2, (largura_tela // 2 - texto2.get_width() // 2, altura_tela // 2 + 10))

    def iniciar_recompensa(self):
        self.indice_fala_recompensa = 0

    def avancar_recompensa(self):
        if self.indice_fala_recompensa < len(FALAS_RECOMPENSA) - 1:
            self.indice_fala_recompensa += 1
            return "continuar"

        return "coletar_claude"

    def desenhar_tela_recompensa(self, tela):
        largura_tela, altura_tela = tela.get_size()

        tela.fill((12, 12, 18))

        fonte_titulo = pygame.font.SysFont(None, 52)
        fonte_fala = pygame.font.SysFont(None, 32)
        fonte_instrucao = pygame.font.SysFont(None, 24)

        titulo = fonte_titulo.render("Teste concluído!", True, (255, 255, 255))
        tela.blit(titulo, (largura_tela // 2 - titulo.get_width() // 2, 50))

        rect_fernanda = self.imagem_quiz.get_rect(center=(largura_tela // 2, altura_tela // 2))
        tela.blit(self.imagem_quiz, rect_fernanda)

        if self.indice_fala_recompensa >= 1:
            rect_logo = self.logo_claude.get_rect(center=(largura_tela // 2 + 150, altura_tela // 2 + 30))
            tela.blit(self.logo_claude, rect_logo)

        caixa = pygame.Rect(150, altura_tela - 170, largura_tela - 300, 110)

        pygame.draw.rect(tela, (0, 0, 0), caixa)
        pygame.draw.rect(tela, (255, 255, 255), caixa, 3)

        fala = FALAS_RECOMPENSA[self.indice_fala_recompensa]
        self.desenhar_texto_quebrado(tela, fala, fonte_fala, (255, 255, 255), caixa.x + 20, caixa.y + 25, caixa.width - 40, 34)

        instrucao = fonte_instrucao.render("Pressione ESPAÇO para continuar", True, (255, 255, 255))
        tela.blit(instrucao, (largura_tela // 2 - instrucao.get_width() // 2, altura_tela - 40))
