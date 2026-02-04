# Sistema de Animações e Pontuação Avançada - Tetrix

## Visão Geral

Este documento descreve as novas funcionalidades implementadas no jogo Tetrix, incluindo sistema de pontuação avançado e animações visuais.

## Funcionalidades Implementadas

### 1. Pontuação por Hard Drop

Quando o jogador usa o hard drop (tecla ESPAÇO), o jogo agora calcula quantas linhas a peça caiu e adiciona pontos bônus:

- **Cálculo**: 2 pontos por linha descida
- **Exemplo**: Se a peça cair 10 linhas = 20 pontos bônus
- **Feedback Visual**: Texto flutuante azul mostrando "+X" pontos ganhos
- **Implementação**: Método `add_drop_bonus()` em `src/scoring.py`

**Código relevante:**
```python
def add_drop_bonus(self, lines_dropped: int) -> int:
    """Add bonus points for hard drop (2 points per line)."""
    bonus = lines_dropped * 2
    self.score += bonus
    return bonus
```

### 2. Sistema de Combo/Streak

O jogo agora rastreia quantos clears consecutivos o jogador faz:

- **Multiplicador de Combo**:
  - Combo 2: 1.5x pontos
  - Combo 3: 2.0x pontos
  - Combo 4: 2.5x pontos
  - Máximo: 3.0x pontos

- **Display Visual**: Texto "COMBO x3!" aparece na tela quando há combo ativo
  - Cor amarela para combos 2-3
  - Cor laranja para combos 4+
  - Cor roxa para combos 5+

- **Som Especial**: Som de combo toca quando o multiplicador está ativo

- **Reset**: Combo é resetado quando o jogador não limpa nenhuma linha

**Código relevante:**
```python
# Combo system
self.combo += 1
if self.combo > 1:
    combo_multiplier = 1.0 + (self.combo - 1) * 0.5
    combo_multiplier = min(combo_multiplier, 3.0)  # Cap at 3x
    points_earned = int(points_earned * combo_multiplier)
```

### 3. Animações de Line Clear

Quando linhas são limpadas, há uma animação visual:

- **Efeito de Flash**: Linha pisca em branco antes de desaparecer
- **Duração**: ~300ms para clears normais
- **Tetris Especial**: 400ms com efeito mais intenso para 4 linhas
- **Pulsação**: Efeito de fade in/out durante a animação

**Características:**
- O jogo pausa entrada durante a animação para evitar confusão
- Após animação, as linhas são removidas e nova peça aparece
- A animação não trava o jogo - usa timers apropriados

### 4. Efeitos Visuais Adicionais

#### Screen Shake (Tetris)
- Tremor leve da tela quando faz Tetris (4 linhas)
- Intensidade: 10 pixels
- Duração: 400ms
- Efeito diminui gradualmente

#### Partículas/Flash (Level Up)
- Flash branco quando sobe de nível
- Texto "LEVEL UP!" com fade in/out
- Mostra o número do novo nível
- Duração total: 2 segundos

#### Texto Flutuante
- Mostra pontos ganhos (+400, +1200, etc)
- Move-se para cima e desaparece gradualmente
- Cor amarela para Tetris, branca para clears normais
- Cor azul para bônus de hard drop

### 5. Transições de Nível

Quando o jogador sobe de nível:

- **Animação**: "LEVEL UP!" aparece com efeito de fade
- **Som**: Efeito sonoro especial de level up
- **Flash**: Tela pisca brevemente em branco
- **Duração**: 2 segundos (não bloqueia gameplay)

## Arquivos Modificados

### Novos Arquivos

1. **src/animations.py** - Sistema completo de animações
   - `FloatingText`: Texto que sobe e desaparece
   - `LineClearAnimation`: Animação de linhas sendo limpadas
   - `ScreenShake`: Tremor de tela
   - `LevelUpAnimation`: Animação de subida de nível
   - `ComboAnimation`: Display de combo
   - `AnimationManager`: Gerenciador central de todas animações

### Arquivos Modificados

1. **src/scoring.py**
   - Adicionado `combo` e `last_level` para rastreamento
   - Modificado `add_score()` para retornar informações de combo/level
   - Adicionado `add_drop_bonus()` para pontos de hard drop

2. **src/game.py**
   - Integrado `AnimationManager` no loop de jogo
   - Modificado `_place_piece()` para criar animações
   - Adicionado `_complete_line_clear()` para completar após animação
   - Modificado `_handle_drop()` para calcular bônus de hard drop
   - Atualizado `render()` para desenhar animações
   - Adicionado `_pending_clear` para controlar estado de animação

3. **src/renderer.py**
   - Adicionado `anim_manager` como propriedade
   - Modificado `draw_board()` e `draw_piece()` para suportar shake offset
   - Importado `AnimationManager`

4. **src/audio.py**
   - Adicionados sons: 'combo', 'levelup', 'tetris'
   - Ajustados volumes dos novos sons

### Arquivos de Som Criados

- `assets/sounds/combo.wav` - Som de combo
- `assets/sounds/levelup.wav` - Som de level up
- `assets/sounds/tetris.wav` - Som especial para Tetris

## Fluxo de Animação

1. **Jogador faz hard drop**:
   - Peça cai até o fundo
   - Calcula distância (N linhas)
   - Adiciona N × 2 pontos
   - Mostra texto flutuante "+X"

2. **Linhas são completadas**:
   - Identifica linhas completas
   - Cria `LineClearAnimation`
   - Toca som apropriado (clear/tetris)
   - Se Tetris: adiciona screen shake
   - Se combo ativo: mostra texto de combo
   - Mostra pontos ganhos
   - Aguarda animação terminar (~300-400ms)
   - Limpa linhas do board
   - Spawna nova peça

3. **Level up detectado**:
   - Cria `LevelUpAnimation`
   - Toca som de level up
   - Mostra flash branco + texto
   - Animação roda por 2 segundos sem bloquear gameplay

## Controles de Performance

- Todas as animações usam timers baseados em tempo real
- Animações não bloqueiam o loop principal do jogo
- Sistema de `_pending_clear` garante que nova peça só aparece após animação
- Entrada do jogador é pausada durante line clear para evitar movimentos acidentais
- Máximo de FPS mantido em 60

## Como Testar

1. **Hard Drop Bonus**:
   - Deixe uma peça no topo
   - Pressione ESPAÇO
   - Observe texto azul "+X" aparecer

2. **Combo System**:
   - Limpe linhas consecutivamente
   - Observe "COMBO x2!" aparecer
   - Veja pontos aumentarem com multiplicador

3. **Tetris Animation**:
   - Limpe 4 linhas de uma vez
   - Observe tela tremer
   - Veja flash mais intenso nas linhas

4. **Level Up**:
   - Jogue até limpar 10 linhas
   - Observe "LEVEL UP!" aparecer
   - Veja flash branco na tela

## Notas Técnicas

- Animações são não-bloqueantes e thread-safe
- Sistema de shake usa random para efeito orgânico
- Floating text usa interpolação linear para movimento suave
- Line clear usa padrão de pulsação para efeito de flash
- Alpha blending é usado para todos os efeitos de fade

## Possíveis Melhorias Futuras

1. Partículas físicas para line clear
2. Trail effects para peças em movimento
3. Efeitos de explosão para Tetris
4. Animações de transição entre telas
5. Efeitos de parallax no background
6. Customização de intensidade de animações nas configurações
