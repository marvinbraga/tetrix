# Changelog - Novas Features de Gameplay

## Data: 2026-02-04

### 1. Sistema de Hold Piece

**Implementação Completa:**
- Adicionada variável `held_piece` na classe `Game` para armazenar o tipo da peça segurada
- Adicionada variável `can_hold` para controlar se o jogador pode fazer hold (apenas uma vez por peça)
- Implementado método `_hold_piece()` que:
  - Permite trocar a peça atual pela peça segurada
  - Na primeira vez, guarda a peça atual e pega a próxima
  - Nas trocas subsequentes, faz swap entre peça atual e segurada
  - Reseta a posição da nova peça para o topo central do tabuleiro
- Adicionado suporte para teclas 'C', 'Shift Left' e 'Shift Right'
- Novo enum `Action.HOLD` no `InputHandler`
- Renderização da hold piece box no lado esquerdo da tela
- Som de hold adicionado (reutiliza o som 'move.wav')

**Arquivos Modificados:**
- `src/game.py`: Lógica principal do hold piece
- `src/input_handler.py`: Mapeamento de teclas
- `src/renderer.py`: Renderização da hold box
- `src/audio.py`: Som de hold

### 2. Feedback de Recorde no Game Over

**Implementação Completa:**
- Verificação automática se o score alcançado é um novo high score
- Mensagem "NEW HIGH SCORE!" em destaque com animação de pulso
- Exibição da posição no ranking (ex: "#3 in Top 10")
- Efeito visual de pulso que varia a cor do texto
- Integração com o sistema de high scores existente

**Arquivos Modificados:**
- `src/renderer.py`: Método `draw_game_over()` com animação de high score

### 3. Estatísticas no Game Over

**Implementação Completa:**
- Rastreamento de tempo de jogo usando `pygame.time.get_ticks()`
- Variável `game_start_time` para marcar início do jogo
- Variável `game_time` atualizada continuamente durante o jogo
- Exibição no Game Over de:
  - Score final
  - Nível alcançado
  - Total de linhas limpadas
  - Tempo total jogado (formato MM:SS)
- Layout organizado e visualmente consistente com o design atual

**Arquivos Modificados:**
- `src/game.py`: Rastreamento de tempo
- `src/renderer.py`: Exibição de estatísticas

## Detalhes Técnicos

### Hold Piece System
```python
# Exemplo de uso no código:
if Action.HOLD in actions and self.can_hold:
    self._hold_piece()
    return
```

### Game Time Tracking
```python
# Inicialização no start_game():
self.game_start_time = pygame.time.get_ticks()
self.game_time = 0

# Atualização contínua:
if self.state == GameState.PLAYING:
    self.game_time = (pygame.time.get_ticks() - self.game_start_time) / 1000
```

### High Score Animation
```python
# Efeito de pulso no texto:
pulse = abs((pygame.time.get_ticks() % 1000) - 500) / 500.0
highlight_color = tuple(
    int(self.COLOR_TEXT[i] + (255 - self.COLOR_TEXT[i]) * pulse * 0.5)
    for i in range(3)
)
```

## Compatibilidade

Todas as features foram implementadas mantendo:
- Consistência visual com o design atual
- Compatibilidade com os três temas (Neon, Pastel, Retro)
- Estrutura de código existente
- Sistema de high scores com top 10

## Testes Recomendados

1. **Hold Piece:**
   - Pressione C ou Shift durante o jogo
   - Verifique se a peça é trocada corretamente
   - Tente fazer hold duas vezes seguidas (deve falhar na segunda)
   - Coloque uma peça e verifique se pode fazer hold novamente

2. **Feedback de High Score:**
   - Alcance um novo high score
   - Verifique se a mensagem aparece
   - Confirme se a posição no ranking está correta
   - Observe a animação de pulso

3. **Estatísticas:**
   - Jogue por alguns minutos
   - Verifique se o tempo está sendo contado corretamente
   - Confirme se todas as estatísticas estão visíveis no Game Over
   - Verifique formatação do tempo (MM:SS)
