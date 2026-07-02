import pygame

vidas_inicias = 3
vidas_maximas = 3
tempo_invencivel_pos_dano = 3000
tamanho_coracao = 30
espacamento_coracao = 10

def desenhar_coracao_colorido(tela, x, y, tamanho, cor = (220, 30, 30)):
    s = tamanho
    raio = s // 4
    pygame.draw.circle(tela, cor, (x - raio, y - s // 8), raio)
    pygame.draw.circle(tela, cor, (x + raio, y - s // 8), raio)
    pontos = [
        (x - s // 2, y - s // 8),
        (x + s // 2, y - s // 8),
        (x, y + s // 2)
    ]
    pygame.draw.polygon(tela, cor, pontos)

def desenhar_coracao_vazio(tela, x ,y, tamanho, cor = (80, 80, 80)):
    desenhar_coracao_colorido(tela, x, y, tamanho, cor)


class sistemavida:

    def __init__(self):
        self.vidas = vidas_inicias
        self.tempo_ultimo_dano = -tempo_invencivel_pos_dano
        self.fim_jogo = False 
        self.tempo_fim_invencibilidade_buff = 0


    def ativar_invencibilidade_buff(self, duracao_ms):
        tempo_atual = pygame.time.get_ticks()
        fim_proposto = tempo_atual + duracao_ms
        self.tempo_fim_invencibilidade_buff = max(
            self.tempo_fim_invencibilidade_buff,
            fim_proposto
        )


    def esta_invencivel_por_buff(self):
        tempo_atual = pygame.time.get_ticks()
        return tempo_atual < self.tempo_fim_invencibilidade_buff    


    def receber_dano(self):
        if self.fim_jogo:
            return False
        
        if self.esta_invencivel_por_buff():
            return False

        tempo_atual = pygame.time.get_ticks()
        
        if (tempo_atual - self.tempo_ultimo_dano) < tempo_invencivel_pos_dano:
            return False
        self.vidas -= 1
        self.tempo_ultimo_dano = tempo_atual

        if self.vidas <= 0:
            self.vidas = 0
            self.fim_jogo = True
        
        return True

    def ganhar_vida(self):
        if self.vidas < vidas_maximas:
            self.vidas += 1

    def jogador_morto(self):
        return not self.fim_jogo
    
    def desenhar(self, tela):
        for i in range (vidas_maximas):
            x = espacamento_coracao + tamanho_coracao // 2 + i * (tamanho_coracao + espacamento_coracao)
            y = espacamento_coracao + tamanho_coracao // 2

            if i < self.vidas:
                desenhar_coracao_colorido(tela, x, y, tamanho_coracao)
            else:
                desenhar_coracao_vazio(tela, x, y, tamanho_coracao)

        tempo_atual = pygame.time.get_ticks()
        invencivel = (tempo_atual - self.tempo_ultimo_dano) < tempo_invencivel_pos_dano
        if invencivel and not self.fim_jogo:
            fonte = pygame.font.SysFont(None, 20)
            resto = (tempo_invencivel_pos_dano - (tempo_atual - self.tempo_ultimo_dano)) // 1000 + 1
            texto = fonte.render(f'Invencivel: {resto}s', True, (255, 215, 0))
            tela.blit(texto, (espacamento_coracao, espacamento_coracao + tamanho_coracao + 5))