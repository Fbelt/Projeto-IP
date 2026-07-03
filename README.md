# Projeto-IP: Find AI at CIN

## Integrantes da Equipe 3

- Clecio Henrique `chmm`
- Felipe Belfort `fbt3`
- Gabriel Costa `gcrs`
- Lucas Guerra `lgp`
- Lucas Pereira `lvmp`
- Matheus de Assis `mal5`

## Arquitetura/Organização do Projeto

### Explicando o jogo

O jogo se baseia em um labirinto divido em 3 andares (Representando o período da faculdade), em que um estudante (Personagem controlado pelo jogador) precisa coletar 3 inteligências artificiais, em que cada uma delas fornece um poder extra para o jogador, e 3 chaves para conseguir passar do labirinto (Representando a conclusão do período). Dentro desse labirinto temos os monitores (Personagem que segue o jogador pelo labirinto), em que caso o estudante seja pego pelo monitor ele perde uma de suas 3 vidas. O jogo se encerra ou quando o estudante conseguir coletar as 3 IAs e as 3 chaves ou quando o estudante for pego 3 vezes pelo monitor.

### Organização do código

O código do nosso jogo foi dividido em 9 partes:

- **Sistema de Batalha**: Responsável por verificar se o estudante foi pego pelo monitor e caso ele seja pego sofra um KnockBack.
- **Sistema de Vida**: Responsável pelo controle de quantas vidas o jogador possui, pela limitação do limite de vidas e pela invencibilidade de 3 segundos depois de ser pego pelo monitor.
- **Sistema de Visão**: Responsável por impedir que o jogador consiga ver o mapa todo o tempo todo, uma vez que por ser um labirinto não faz sentido a pessoa conseguir ver o mapa todo o tempo inteiro.
- **Personagens**: Responsável pela criação do personagem controlado pelo jogador, pela criação do inimigo e pela movimentação dos personagens.
- **Coletáveis**: Responsável pela criação dos itens que precisam ser adquiridos pelo jogador.
  - **Chave Azul**: Desbloqueia a porta de acesso ao ChatGPT.
  - **Chave Verde**: Desbloqueia a porta onde Fernanda fica
  - **Chave Vermelha**: Desbloqueia a porta de acesso ao Gemini e a porta onde Ricardo Massa fica
  - **ChatGPT**: Ao coletar o ChatGPT o jogador ganha a habilidade de revelar o mapa por 3 segundos ao apertar 2.
  - **Claude**: Ao coletar o Calude, caso o jogador tenha sido pego pelo monitor pelo menos uma vez, ele recupera uma vida. Não podendo ultrapassar o limite de 3 vidas.
  - **Gemini**: Ao coletar o Calude o jogador consegue uma invencibilidade durante 3 segundos.
- **Fernanda**: Responsável pelo controle de interação com a professora Fernanda
- **Ricardo**: Responsável pelo controle de interação com o professor Ricardo
- **Inventario**: Responsável pelo armazenamento da informação de quais itens já foram pegos pelo jogador.
- **Mapa**: Responsável pela criação dos 3 andares do mapa e das passagens entre as paredes

## Divisão do Trabalho

- **Clecio**: Mapa
- **Felipe**: Identidade Visual e Solução de Problemas
- **Gabriel**: Sistema de vida e Relatório
- **Lucas Guerra**: Personagens
- **Lucas Pereira**: Resultado final do jogo
- **Matheus**: Coletáveis
- **Todos**: Preenchimento dos checkpoints e criação dos slides

## Ferramentas, Bibliotecas e FrameWorks utilizados no projeto
Pygame foi o framework central do projeto e a principal ferramenta externa utilizada, responsável por:

  - **Renderização gráfica**: Desenho do Mapa, HUD, Caixas de Diálogo, Corações de Vida e Campo de Visão dos Monitores, Através de Surface, blit() e das Funções draw.rect, draw.circle, draw.polygon e draw.line.
  - **Carregamento e manipulação de imagens**: Sprites do Estudante, Monitores, Professores e dos Ícones dos Coletáveis, Usando image.load() e as Funções de Transformação (scale, smoothscale, flip) para Redimensionar e Espelhar as Imagens Conforme a Direção do Personagem.
  - **Sistema de sprites**: A Classe Coletaveis Herda de pygame.sprite.Sprite, Aproveitando a Estrutura Pronta do PyGame para Agrupar e Gerenciar os Itens Coletáveis do Mapa.
  - **Detecção de colisão**: uso de pygame.Rect e colliderect() para identificar colisão entre o estudante e as paredes, entre o estudante e os monitores, e para as áreas de interação com os professores e coletáveis.
  - **Máscaras de pixel**: pygame.mask.from_surface() foi usado para gerar o contorno e a silhueta dos ícones no inventário, criando o efeito visual de item "bloqueado" antes de ser coletado.
  - **Captura de entrada do jogador**: pygame.key.get_pressed() e o evento KEYDOWN para movimentação (WASD e setas) e para as interações do jogo (tecla F para coletar/falar, ESPAÇO para avançar diálogos, teclas numéricas para responder o quiz).
  - **Textos e fontes**: pygame.font.SysFont() para os textos padrão do jogo e pygame.font.Font() com uma fonte pixelada customizada (PressStart2P) para reforçar a estética retrô nos ícones do HUD.
  - **Controle de tempo**: pygame.time.get_ticks() foi essencial para implementar os cooldowns das habilidades do ChatGPT e do Gemini, a invencibilidade temporária após ser pego pelo monitor e as animações de revelação de portas — dessa forma o jogo funciona de maneira consistente independente da velocidade do computador de quem está jogando.

Além do Pygame, utilizamos duas bibliotecas padrão do próprio Python:

  - **math**: aplicada no sistema de visão dos monitores do tipo "Vigia", para calcular ângulos e distâncias (funções atan2, hypot, cos, sin) que definem o campo de visão em cone e simulam a percepção do inimigo. Também é usada no algoritmo de "raycasting" que gera o efeito de neblina de guerra, limitando o quanto o jogador enxerga do labirinto.
  - **random**: usada para sortear, a cada nova partida, em qual dos pontos pré-definidos cada chave e cada IA vai aparecer, tornando o mapa menos previsível.
Não foram utilizadas bibliotecas externas além do Pygame — os mapas dos três andares, por exemplo, foram construídos manualmente como matrizes de texto (strings), sem uso de editores de mapa como o Tiled.

## Conceitos apresentados na disciplina e onde eles foram usados

> TEXTO

## Desafios e Erros Durante o Projeto

1. **Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?**

   O maior erro cometido pelo grupo foi a implementação individual de cada parte do código. O que resultou em alguns conflitos na hora de juntar as funcionalidades no código principal. Lidar com esse erro foi relativamente simples, porém acabou gerando um trabalho muito maior, uma vez que toda vez que uma alteração era feita os outros membros do grupo precisavam comparar o que tinha sido feito e se essa alteração impactava outra funcionalidade já existente dentro do jogo.

2. **Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?**

   O maior desafio enfrentado pelo grupo foi um problema que acontecia quando o estudante era pego pelo monitor e o efeito do KnockBack empurrava o estudante em direção a parede do labirinto, resultando em um bug que o estudante entrava dentro da parede e ficava imovel. Para lidar com esse problema o grupo pensou em diversas soluções distintas, o que gerou uma divergência entre os participantes, mas a solução final tomada pelo grupo foi a remoção do KnockBack.

3. **Quais as lições aprendidas durante o projeto?**

   As principais lições que aprendemos foi que a organização previa do que tem que ser feito facilita muito o trabalho, uma vez que ao traçar o caminho que deve ser seguido antes de começar fica muito mais nítido o que deve ser feito. Além disso, aprendemos a importância do trabalho em equipe e da divisão bem definida de tarefas. Visto que não sabiamos nada de PyGame e de como fazer um jogo, mas a divisão facilitou muito esse trabalho e deixou o processo como um todo mais divertido.

## Capturas de Tela do Sistema em funcionamento

<img width="1200" height="779" alt="image" src="https://github.com/user-attachments/assets/fff78bda-a53b-4555-86e5-f6cc908b3c41" />
<img width="1202" height="782" alt="image" src="https://github.com/user-attachments/assets/b1f665d2-f774-47b0-ad49-d0013e2e8de7" />
<img width="1199" height="787" alt="image" src="https://github.com/user-attachments/assets/83231c9a-8957-414d-8bf6-6fb018263c19" />
<img width="1201" height="781" alt="image" src="https://github.com/user-attachments/assets/5f0791e1-687d-49a3-a559-75b850c1b098" />
<img width="1204" height="785" alt="image" src="https://github.com/user-attachments/assets/b0f98128-57f5-46bc-b926-d1ae3de02610" />
<img width="1201" height="781" alt="image" src="https://github.com/user-attachments/assets/f1e2fe42-f065-4632-b8d2-c0985c3ae7b0" />
