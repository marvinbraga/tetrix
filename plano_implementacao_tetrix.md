# Plano de Implementação do Jogo Tetrix em Python e Pygame

## Introdução

Este documento apresenta um plano detalhado para a implementação do jogo **Tetrix**, uma versão personalizada do clássico jogo Tetris, utilizando a linguagem de programação Python e a biblioteca Pygame para gráficos e interatividade. O objetivo é criar um jogo funcional, envolvente e extensível, seguindo as melhores práticas de desenvolvimento de software.

### Visão Geral do Jogo Tetrix

Tetrix é um jogo de quebra-cabeça onde o jogador controla peças geométricas chamadas tetrominoes, que caem em um tabuleiro. O objetivo é organizar as peças para formar linhas horizontais completas, que são removidas, liberando espaço e pontuando. O jogo termina quando as peças se acumulam até o topo do tabuleiro.

### Escopo do Projeto

- **Plataforma**: Desktop (Windows, macOS, Linux).
- **Bibliotecas Principais**: Python 3.x, Pygame.
- **Funcionalidades Básicas**:
  - Queda automática e controlada de peças.
  - Rotação e movimento lateral das peças.
  - Detecção e remoção de linhas completas.
  - Sistema de pontuação e níveis.
  - Interface gráfica com tabuleiro, preview da próxima peça e HUD.
- **Funcionalidades Avançadas** (futuras expansões):
  - Salvamento de high scores.
  - Modos de jogo (clássico, timed, endless).
  - Efeitos sonoros e música.
  - Customização de cores e temas.

## Requisitos do Sistema

### Dependências Técnicas

- **Python**: Versão 3.8 ou superior.
- **Pygame**: Biblioteca para gráficos, entrada e áudio. Instalar via `pip install pygame`.
- **Outros**: NumPy (opcional, para manipulações de matrizes eficientes).

### Requisitos Funcionais

- O jogo deve rodar em uma janela de tamanho fixo (ex.: 800x600 pixels).
- Suporte a controles de teclado (setas para movimento, espaço para rotação, etc.).
- Renderização em tempo real com taxa de quadros adequada (30-60 FPS).
- Persistência de dados (pontuações) em arquivos locais.

### Requisitos Não Funcionais

- **Performance**: O jogo deve rodar suavemente em hardware moderno, com baixo consumo de recursos.
- **Usabilidade**: Interface intuitiva, controles responsivos.
- **Manutenibilidade**: Código modular, bem comentado e documentado.
- **Extensibilidade**: Estrutura que permita adições futuras, como novos modos de jogo.

## Arquitetura do Código

### Estrutura do Projeto

Organizaremos o código em uma estrutura modular para facilitar a manutenção e expansão:

```
tetrix/
├── assets/
│   ├── fonts/          # Fontes personalizadas
│   ├── images/         # Imagens (backgrounds, sprites)
│   └── sounds/         # Arquivos de áudio (opcional)
├── src/
│   ├── __init__.py
│   ├── main.py         # Ponto de entrada do jogo
│   ├── game.py         # Classe principal do jogo
│   ├── board.py        # Classe do tabuleiro
│   ├── piece.py        # Classe das peças (tetrominoes)
│   ├── renderer.py     # Módulo de renderização
│   ├── input_handler.py # Gerenciamento de entrada
│   ├── scoring.py      # Sistema de pontuação
│   └── utils.py        # Funções utilitárias
├── tests/              # Testes unitários
│   ├── test_board.py
│   ├── test_piece.py
│   └── ...
├── data/               # Dados persistentes
│   └── high_scores.txt
├── README.md           # Documentação
└── requirements.txt    # Dependências
```

### Padrões de Design

- **Orientação a Objetos**: Uso de classes para encapsular lógica relacionada (ex.: `Board`, `Piece`, `Game`).
- **MVC (Model-View-Controller)**: Separação entre modelo (lógica do jogo), visão (renderização) e controlador (entrada).
- **Singleton**: Para gerenciadores globais, como o sistema de pontuação.
- **Factory**: Para criação de peças diferentes.

## Componentes Principais

### 1. Classe Game (game.py)

A classe central que orquestra o loop principal do jogo.

- **Atributos**:
  - `board`: Instância do tabuleiro.
  - `current_piece`: Peça atual em jogo.
  - `next_piece`: Preview da próxima peça.
  - `score`: Pontuação atual.
  - `level`: Nível atual.
  - `game_over`: Flag de fim de jogo.
  - `clock`: Controle de tempo (Pygame Clock).

- **Métodos Principais**:
  - `run()`: Loop principal do jogo.
  - `update()`: Atualiza o estado do jogo (queda de peças, verificação de linhas).
  - `handle_input()`: Processa entrada do usuário.
  - `render()`: Desenha o jogo na tela.
  - `check_game_over()`: Verifica se o jogo acabou.
  - `pause_resume()`: Pausa/retoma o jogo.

### 2. Classe Board (board.py)

Representa o tabuleiro de jogo, uma grade onde as peças são colocadas.

- **Atributos**:
  - `grid`: Matriz 2D (ex.: 20 linhas x 10 colunas) representando o estado do tabuleiro.
  - `width`, `height`: Dimensões do tabuleiro.

- **Métodos Principais**:
  - `place_piece(piece, position)`: Coloca uma peça no tabuleiro.
  - `is_valid_position(piece, position)`: Verifica se uma posição é válida.
  - `clear_lines()`: Identifica e remove linhas completas.
  - `get_filled_lines()`: Retorna índices das linhas completas.
  - `draw(renderer)`: Renderiza o tabuleiro.

### 3. Classe Piece (piece.py)

Representa uma peça tetromino (I, O, T, S, Z, J, L).

- **Atributos**:
  - `shape`: Matriz 4x4 representando a forma da peça.
  - `color`: Cor da peça.
  - `position`: Posição atual (x, y) no tabuleiro.
  - `rotation`: Estado de rotação atual.

- **Métodos Principais**:
  - `rotate()`: Rotaciona a peça 90 graus no sentido horário.
  - `move(dx, dy)`: Move a peça nas direções x/y.
  - `get_positions()`: Retorna as posições ocupadas pela peça.
  - `clone()`: Cria uma cópia da peça para preview.

### 4. Módulo Renderer (renderer.py)

Responsável pela renderização gráfica.

- **Funções Principais**:
  - `draw_board(board)`: Desenha o tabuleiro.
  - `draw_piece(piece)`: Desenha uma peça.
  - `draw_ui(score, level, next_piece)`: Desenha a interface do usuário.
  - `draw_game_over()`: Tela de fim de jogo.

### 5. Módulo InputHandler (input_handler.py)

Gerencia entrada do usuário.

- **Funções Principais**:
  - `get_pressed_keys()`: Retorna teclas pressionadas.
  - `map_keys_to_actions()`: Mapeia teclas para ações (mover, rotacionar, etc.).

### 6. Módulo Scoring (scoring.py)

Sistema de pontuação e níveis.

- **Funções Principais**:
  - `calculate_score(lines_cleared, level)`: Calcula pontos por linhas removidas.
  - `increase_level(score)`: Aumenta o nível baseado na pontuação.
  - `get_speed(level)`: Retorna velocidade de queda baseada no nível.

## Mecânicas do Jogo Detalhadas

### Tetrominoes

Existem 7 tipos de peças, cada uma com 4 rotações possíveis:

1. **I (Linha)**: Forma uma linha reta. Pontos: (0,1), (1,1), (2,1), (3,1)
2. **O (Quadrado)**: Forma um quadrado. Não rotaciona.
3. **T**: Forma um T.
4. **S (Escada Esquerda)**: Forma uma escada.
5. **Z (Escada Direita)**: Forma uma escada invertida.
6. **J (Gancho Esquerdo)**: Forma um J.
7. **L (Gancho Direito)**: Forma um L.

Cada peça terá uma representação matricial e métodos para rotação.

### Controle de Movimento

- **Movimento Lateral**: Teclas esquerda/direita movem a peça horizontalmente, se houver espaço.
- **Rotação**: Tecla cima rotaciona a peça, verificando colisões.
- **Queda Acelerada**: Tecla baixo acelera a queda.
- **Queda Automática**: A peça cai automaticamente a cada intervalo de tempo, determinado pelo nível.

### Detecção de Colisões

- Verificar se a nova posição da peça está dentro dos limites do tabuleiro.
- Verificar se não há sobreposição com peças já colocadas.
- Se colidir na queda, fixar a peça no tabuleiro e gerar nova peça.

### Remoção de Linhas

- Após fixar uma peça, verificar cada linha do tabuleiro.
- Se uma linha estiver completamente preenchida, removê-la e deslocar linhas superiores para baixo.
- Pontuar baseado no número de linhas removidas simultaneamente (1, 2, 3 ou 4 linhas).

### Sistema de Pontuação

- **Pontos por Linha**:
  - 1 linha: 40 pontos × nível
  - 2 linhas: 100 pontos × nível
  - 3 linhas: 300 pontos × nível
  - 4 linhas (Tetris): 1200 pontos × nível
- **Níveis**: Aumentam a cada 10 linhas removidas, aumentando a velocidade.
- **High Scores**: Salvar as 10 maiores pontuações em arquivo.

### Condições de Fim de Jogo

- O jogo termina quando uma nova peça não pode ser colocada no topo (colisão imediata).

## Plano de Desenvolvimento

### Fase 1: Configuração e Estrutura Básica

1. **Configurar Ambiente**:
   - Criar repositório Git.
   - Instalar dependências (Pygame).
   - Definir estrutura de pastas.

2. **Implementar Classe Board**:
   - Criar matriz de grade.
   - Métodos básicos de colocação e validação.

3. **Implementar Classe Piece**:
   - Definir formas dos tetrominoes.
   - Métodos de movimento e rotação.

### Fase 2: Loop Principal e Renderização

4. **Implementar Classe Game**:
   - Loop principal com atualização e renderização.
   - Integração básica com Board e Piece.

5. **Implementar Renderer**:
   - Desenhar tabuleiro e peças.
   - Configurar janela Pygame.

6. **Adicionar Entrada**:
   - Mapeamento de teclas para ações.
   - Movimento manual de peças.

### Fase 3: Mecânicas Avançadas

7. **Implementar Queda Automática**:
   - Timer para queda periódica.
   - Ajuste baseado no nível.

8. **Implementar Detecção de Linhas**:
   - Verificação e remoção de linhas completas.
   - Animação de remoção (opcional).

9. **Implementar Sistema de Pontuação**:
   - Cálculo de pontos.
   - Progressão de níveis.

### Fase 4: Polimento e Extras

10. **Interface do Usuário**:
    - HUD com pontuação, nível, próxima peça.
    - Tela de game over.

11. **Persistência de Dados**:
    - Salvar/carregar high scores.

12. **Testes e Debugging**:
    - Testes unitários para classes principais.
    - Correção de bugs.

13. **Otimização e Polimento**:
    - Melhorar performance.
    - Adicionar efeitos visuais (sombras, animações).

## Testes

### Estratégia de Testes

- **Testes Unitários**: Usar pytest para testar classes isoladamente.
  - Board: Testes de colocação, validação e remoção de linhas.
  - Piece: Testes de rotação e movimento.
  - Scoring: Testes de cálculo de pontos.

- **Testes de Integração**: Verificar interação entre componentes.
  - Simulação de jogadas completas.

- **Testes Manuais**: Jogar o jogo para verificar usabilidade e bugs.

### Casos de Teste Exemplo

1. **Movimento de Peça**: Verificar se peça se move corretamente e para em obstáculos.
2. **Rotação**: Garantir que rotações não causem sobreposições inválidas.
3. **Remoção de Linhas**: Testar cenários com 1, 2, 3 e 4 linhas.
4. **Fim de Jogo**: Simular acúmulo até o topo.

## Considerações Finais

### Riscos e Mitigações

- **Performance**: Pygame pode ter limitações em máquinas antigas; otimizar renderização.
- **Compatibilidade**: Testar em diferentes sistemas operacionais.
- **Complexidade**: Começar simples e adicionar recursos incrementalmente.

### Próximos Passos

1. Revisar e aprovar este plano.
2. Iniciar implementação seguindo as fases definidas.
3. Iterar baseado em testes e feedback.

### Recursos Adicionais

- Documentação Pygame: https://www.pygame.org/docs/
- Tutoriais Tetris: Pesquisar implementações em Python para referência.
- Ferramentas: VS Code para desenvolvimento, Git para controle de versão.

Este plano serve como guia completo para a implementação do Tetrix. Qualquer ajuste pode ser feito conforme o progresso do desenvolvimento.