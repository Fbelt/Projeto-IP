import pygame

pygame.init()

#configurando a tela
altura, largura = 750, 1200
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Find AI at CIN")
clock = pygame.time.Clock()

#onde vai nascer o personagem
x, y = 15, 15
velocidade = 4

#loop do jogo
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit();  break
        
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:  x -= velocidade
    if teclas[pygame.K_RIGHT]: x += velocidade
    if teclas[pygame.K_UP]:   y -= velocidade
    if teclas[pygame.K_DOWN]: y += velocidade

    #limite do mapa
    x = max(0, min(x, largura - 25))
    y = max(0, min(y, altura - 25))
    
    tela.fill((30, 10, 30))
    pygame.draw.rect(tela, (255, 0, 0), (x, y, 25, 25))

    pygame.display.flip()
    clock.tick(45) 