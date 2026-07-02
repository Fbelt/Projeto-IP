Projeto-IP: Find AI at CIN
Integrantes da Equipe 3:
  -Clecio Henrique <chmm>
  -Felipe Belfort <fbt3>
  -Gabriel Costa <gcrs>
  -Lucas Guerra <lgp>
  -Lucas Pereira <lvmp>
  -Matheus de Assis <mal5>


Arquitetura/Organização do Projeto:

  -Explicando o jogo:
    O jogo se baseia em um labirinto divido em 3 andares (Representando o período da faculdade), em que um estudante (Personagem controlado pelo jogador) precisa coletar 3 inteligências artificiais, em que cada uma delas fornece um poder extra para o jogador, e 3 chaves para conseguir passar do labirinto (Representando a conclusão do período). Dentro desse labirinto temos os monitores (Personagem que segue o jogador pelo labirinto), em que caso o estudante seja pego pelo monitor ele perde uma de suas 3 vidas. O jogo se encerra ou quando o estudante conseguir coletar as 3 IAs e as 3 chaves ou quando o estudante for pego 3 vezes pelo monitor.
    
  -Organização do codigo:
    O código do nosso jogo foi dividido em 7 fases:
      Sistema de Batalha: Responsável por verificar se o estudante foi pego pelo monitor e caso ele seja pego sofra um KnockBack.
      Sistema de Vida: Responsável pelo controle de quantas vidas o jogador possui, pela limitação do limite de vidas e pela invencibilidade de 3 segundos depois de ser pego pelo monitor. 
      Sistema de Visão: Responsável por impedir que o jogador consiga ver o mapa todo o tempo todo, uma vez que por ser um labirinto não faz sentido a pessoa conseguir ver o mapa todo o tempo inteiro.
      Personagens: Responsável pela criação do personagem controlado pelo jogador, pela criação do inimigo e pela movimentação dos personagens. 
      Coletáveis: Responsável pela criação dos itens que precisam ser adquiridos pelo jogador. 
        -Chaves: Necessárias para finalizar o jogo e conseguir passar de período.
        -ChatGPT: Ao coletar o ChatGPT a velocidade do jogador aumenta de 5 para 7.
        -Gemini: Ao coloetar o Gemini, caso o jogador tenha sido pego pelo monitor pelo menos uma vez, ele recupera uma vida. Não podendo ultrapassar o limite de 3 vidas.
        -Claude: Ao coletar o Calude o jogador consegue uma invencibilidade durante 15 segundos.
      Inventario: Responsável pelo armazenamento da informação de quais itens já foram pegos pelo jogador.
      Mapa: Responsável pela criação dos 3 andares do mapa e das passagens entre as paredes


Divisão do Trabalho:
  -Clecio: Mapa
  -Felipe: Identidade Visual e Solução de Problemas
  -Gabriel: Sistema de vida e Relatório
  -Lucas Guerra: Personagens 
  -Lucas Pereira: Resultado final do jogo
  -Matheus: Coletáveis 
  -Todos: Preenchimento dos checkpoints e criação dos slides


Ferramentas, Bibliotecas e FrameWorks utilizados no projeto:
##########     TEXTO     ##########
##########     ESPAÇAMENTO    ##########
##########     ESPAÇAMENTO    ##########
Conceitos apresentados na disciplina e onde eles foram usados
##########     TEXTO     ##########
##########     ESPAÇAMENTO    ##########
##########     ESPAÇAMENTO    ##########
Desafios e Erros Durante o Projeto:

1. Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?
   O maior erro cometido pelo grupo foi a implementação individual de cada parte do código. O que resultou em alguns conflitos na hora de juntar as funcionalidades no código principal. Lidar com esse erro foi relativamente simples, porém acabou gerando um trabalho muito maior, uma vez que toda vez que uma alteração era feita os outros membros do grupo precisavam comparar o que tinha sido feito e se essa alteração impactava outra funcionalidade já existente dentro do jogo.
   
2. Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?
   O maior desafio enfrentado pelo grupo foi um problema que acontecia quando o estudante era pego pelo monitor e o efeito do KnockBack empurrava o estudante em direção a parede do labirinto, resultando em um bug que o estudante entrava dentro da parede e ficava imovel. Para lidar com esse problema o grupo pensou em diversas soluções distintas, o que gerou uma divergência entre os participantes, mas a solução final tomada pelo grupo foi a remoção do KnockBack

3. Quais as lições aprendidas durante o projeto?
   As principais lições que aprendemos foi que a organização previa do que tem que ser feito facilita muito o trabalho, uma vez que ao traçar o caminho que deve ser seguido antes de começar fica muito mais nítido o que deve ser feito. Além disso, aprendemos a importância do trabalho em equipe e da divisão bem definida de tarefas. Visto que não sabiamos nada de PyGame e de como fazer um jogo, mas a divisão facilitou muito esse trabalho e deixou o processo como um todo mais divertido.
