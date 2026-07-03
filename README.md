# Projeto-IP: Find AI at CIN

## Integrantes da Equipe 3

- Clécio Henrique `chmm`
- Felipe Belfort `fbt3`
- Gabriel Costa `gcrs`
- Lucas Guerra `lgp`
- Lucas Pereira `lvmp`
- Matheus de Assis `mal5`

## Arquitetura/Organização do Projeto

```
Projeto-IP/
├── main.py                 # Loop principal do jogo: estados, eventos e renderização
├── README.md
│
├── game_content/
│   ├── personagens.py       # Classes Jogador, InimigoPatrulha e InimigoVigia
│   ├── mapa.py               # Matrizes dos 3 andares, colisão e portas trancadas
│   ├── coletaveis.py         # Sorteio/coleta das chaves e IAs e seus buffs/habilidades
│   ├── inventario.py         # Itens coletados e HUD do inventário
│   ├── sistema_vida.py       # Vidas, dano e invencibilidade
│   ├── visao.py               # Neblina de guerra / campo de visão do jogador
│   ├── batalha.py             # Detecção de colisão entre jogador e inimigos
│   ├── fernanda.py            # Boss e quiz da professora Fernanda
│   └── ricardo.py             # Interação com o professor Ricardo e condição de vitória
│
├── imagens/                 # Sprites dos personagens, ícones e texturas do mapa
└── fontes/                  # Fontes pixeladas usadas na interface (PixelOperator, PressStart2P)
```

### Explicando o jogo

O jogo se baseia em um labirinto dividido em 3 andares (representando o período da faculdade), em que um estudante (o personagem controlado pelo jogador) precisa coletar 3 inteligências artificiais, cada uma dando um poder extra pro jogador, e 3 chaves pra destrancar as portas e conseguir avançar pelo labirinto. Dentro desse labirinto tem os monitores: uns ficam patrulhando de um lado pro outro, e outros vigiam uma área e partem pra cima do jogador se ele entrar no campo de visão deles — em qualquer um dos dois casos, se o estudante for pego, ele perde uma de suas 3 vidas. Também tem a professora Fernanda, que aparece no caminho e só libera a passagem depois de um quiz, e o professor Ricardo, que fica no último andar: é falando com ele, já com as 3 IAs e as 3 chaves no inventário, que o jogo é vencido de fato. Se o estudante for pego 3 vezes pelos monitores, o jogo acaba em derrota.

### Organização do código

O código do nosso jogo foi dividido em 9 partes:

- **Sistema de Batalha**: Responsável por verificar se o estudante encostou em algum monitor. Na primeira versão isso também empurrava o personagem pra longe (KnockBack), mas essa parte acabou sendo removida — o motivo tá contado lá em baixo, em "Desafios e Erros Durante o Projeto".
- **Sistema de Vida**: Responsável pelo controle de quantas vidas o jogador possui, pela limitação do limite de vidas e pela invencibilidade de 3 segundos depois de ser pego pelo monitor.
- **Sistema de Visão**: Responsável por impedir que o jogador consiga ver o mapa todo o tempo todo, uma vez que por ser um labirinto não faz sentido a pessoa conseguir ver o mapa todo o tempo inteiro.
- **Personagens**: Responsável pela criação do personagem controlado pelo jogador, dos monitores (o de patrulha e o vigia) e pela movimentação de todos eles.
- **Coletáveis**: Responsável pela criação dos itens que precisam ser adquiridos pelo jogador.
  - **Chave Azul**: Desbloqueia a porta de acesso ao ChatGPT.
  - **Chave Verde**: Desbloqueia a porta onde Fernanda fica
  - **Chave Vermelha**: Desbloqueia a porta de acesso ao Gemini e a porta onde Ricardo fica
  - **ChatGPT**: assim que é coletado, a velocidade do jogador já aumenta. Além disso, dá pra apertar 2 pra revelar o mapa inteiro por 3 segundos, com 30 segundos de espera entre um uso e outro.
  - **Claude**: ao coletar, libera a habilidade de recuperar 1 vida apertando 1 — só funciona se o jogador já tiver perdido alguma vida, e só pode ser usada uma vez o jogo inteiro.
  - **Gemini**: recupera uma vida na hora que é coletado (respeitando o limite de 3) e ainda libera 3 segundos de invencibilidade apertando 3, com 45 segundos de cooldown.
- **Fernanda**: Responsável pelo controle de interação com a professora Fernanda
- **Ricardo**: Responsável pelo controle de interação com o professor Ricardo
- **Inventario**: Responsável pelo armazenamento da informação de quais itens já foram pegos pelo jogador.
- **Mapa**: Responsável pela criação dos 3 andares do mapa e das passagens entre as paredes

## Divisão do Trabalho

- **Clécio**: Mapa
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

Em geral todos os conceitos e comandos mais básicos apresentados na disiplina foram utilizados.

- **Condicionais**: O uso de condicionais foi usado por todo o código, principalmente para a validação de qualquer acontecimento no jogo, como dano e movimentação.
- **Loops**: Os loops foram essencias para o funcionamento do jogo, com destaque ao loop "while rodando" que permite que o jogo continue em funcionamento até ele acabar.
- **Listas**: O uso de listas foi importante para armazenar e fazer funcionar de forma mais efetiva coisa que eram mutiplas no jogo, como no caso dos vilões, texturas e animações.
- **Funções**: O uso de função foi essencial para programar os personagens, e todas as verificações realizadas pelo jogo, esse recurso foi majoritariamente usado dentro de POOs, e serviu para que o personagem tivesse suas caractristicas e para verificar coisas como colisões, coletas, perda e ganho de vida e etc.
- **Dicionários**: Os dicionários foram muito utilizados para armazenar intens que tiveram o acesso facilitado por causa de sua organização, logo todas as imagens, coletáveis, ou coisas grandes e que não são utilizadas 100% do tempo foram armazenadas em dicionários, como as perguntas do quiz.
- **Tuplas**: As tuplas foram utilizadas para armazenar coisas mais fixas e que não precisariam ser mudadas, como por exemplo as definições de cores em RGB que eram definidas em tuplas e não eram alteradas.

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
