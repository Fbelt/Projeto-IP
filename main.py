import pygame
from personagens import jogador
from personagens import inimigo

pygame.init()

#configurando a tela
altura, largura = 750, 1200
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Find AI at CIN")
clock = pygame.time.Clock()

#onde vai nascer os personagens
jogador = jogador(x=15, y=15)
inimigo = inimigo(x=400, y=400)

#loop do jogo
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit();  break
    
    teclas = pygame.key.get_pressed()
    jogador.mover(teclas, largura, altura)
    
    tela.fill((30, 10, 30))
    jogador.desenhar(tela)
    inimigo.desenhar(tela)

    pygame.display.flip()
    clock.tick(45) 