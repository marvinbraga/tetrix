# Guia de Uso - Novas Funcionalidades Tetrix

## Como Usar as Novas Funcionalidades

### 1. Pontuação por Hard Drop

**O que é**: Ganhe pontos extras ao fazer hard drop (queda rápida).

**Como usar**:
1. Posicione sua peça horizontalmente onde deseja
2. Pressione **ESPAÇO** para hard drop
3. A peça cairá instantaneamente
4. Você ganhará 2 pontos por cada linha descida
5. Texto azul "+X" aparecerá mostrando o bônus

**Exemplo**:
```
Situação: Peça está na linha 2, vai cair até linha 18
Distância: 16 linhas
Bônus: 16 × 2 = 32 pontos
Display: "+32" em azul aparece na tela
```

**Dica**: Use hard drop para ganhar pontos extras e acelerar o gameplay!

---

### 2. Sistema de Combo

**O que é**: Multiplicador de pontos por limpar linhas consecutivamente.

**Como funciona**:
- Limpe linhas sem deixar peças caírem sem limpar
- Cada clear consecutivo aumenta o multiplicador
- Multiplicador máximo: 3.0x

**Progressão de Combo**:
```
Combo 1: 1.0x (normal)
Combo 2: 1.5x → "COMBO x2!" (amarelo)
Combo 3: 2.0x → "COMBO x3!" (amarelo)
Combo 4: 2.5x → "COMBO x4!" (laranja)
Combo 5+: 3.0x → "COMBO x5!" (roxo)
```

**Exemplo de Pontuação**:
```
Sem combo:
  1 linha = 40 × nível 1 = 40 pontos

Com combo x3:
  1 linha = 40 × nível 1 × 2.0 = 80 pontos

Tetris com combo x5:
  4 linhas = 1200 × nível 1 × 3.0 = 3600 pontos!
```

**Como manter combo**:
1. Limpe pelo menos 1 linha com cada peça
2. Ou posicione peças estrategicamente para clears futuros
3. Evite deixar buracos que impedem clears

**Como perder combo**:
- Deixar uma peça cair sem limpar nenhuma linha
- Combo reseta para 0

---

### 3. Animações Visuais

#### Line Clear (Linhas Limpas)

**O que acontece**:
- Linhas piscam em branco antes de desaparecer
- Efeito de pulsação (fade in/out)
- Duração: ~300ms

**Tetris Special** (4 linhas):
- Animação mais longa (400ms)
- Efeito mais intenso
- Tela treme levemente
- Som especial de Tetris

**Durante a animação**:
- Input é pausado temporariamente
- Evita movimentos acidentais
- Game continua fluido após animação

#### Screen Shake (Tremor de Tela)

**Quando acontece**: Ao fazer Tetris (4 linhas)

**Efeito**:
- Tela treme por 400ms
- Intensidade: 8-10 pixels
- Diminui gradualmente
- Adiciona impacto visual

#### Floating Text (Texto Flutuante)

**O que mostra**:
- Pontos ganhos: "+400", "+1200", etc
- Bônus de hard drop: "+32" (azul)
- Pontos de combo: amarelo/branco

**Comportamento**:
- Aparece no centro da tela
- Sobe ~80 pixels
- Desaparece gradualmente (1.5s)
- Múltiplos textos podem aparecer simultaneamente

#### Combo Display

**Visual**:
- "COMBO x3!" aparece próximo ao topo
- Escala aumenta rapidamente (1.5x)
- Depois diminui para 1.25x
- Desaparece com fade out

**Cores por nível**:
```
Combo 2-3: Amarelo
Combo 4+:  Laranja
Combo 5+:  Roxo
```

---

### 4. Level Up

**Quando acontece**: A cada 10 linhas limpas

**Efeito Visual**:
1. Flash branco na tela (0.5s)
2. "LEVEL UP!" aparece com fade in
3. Mostra número do novo nível
4. Mantém por 1 segundo
5. Fade out (0.5s)

**Efeito Sonoro**: Som especial de level up

**Mudanças no Gameplay**:
- Velocidade de queda aumenta
- Pontos por linha aumentam
- Dificuldade aumenta gradualmente

---

## Tabela de Pontuação Completa

### Pontos Base por Linhas

| Linhas | Pontos Base | × Nível | Exemplo (Nível 5) |
|--------|-------------|---------|-------------------|
| 1      | 40          | × 5     | 200 pontos        |
| 2      | 100         | × 5     | 500 pontos        |
| 3      | 300         | × 5     | 1500 pontos       |
| 4      | 1200        | × 5     | 6000 pontos       |

### Com Multiplicador de Combo

| Combo | Mult. | 1 Linha (Nv1) | 4 Linhas (Nv1) | 4 Linhas (Nv5) |
|-------|-------|---------------|----------------|----------------|
| 1     | 1.0x  | 40            | 1200           | 6000           |
| 2     | 1.5x  | 60            | 1800           | 9000           |
| 3     | 2.0x  | 80            | 2400           | 12000          |
| 4     | 2.5x  | 100           | 3000           | 15000          |
| 5+    | 3.0x  | 120           | 3600           | 18000          |

### Bônus de Hard Drop

```
Pontos = Linhas descidas × 2

Exemplos:
- Drop de 5 linhas = 10 pontos
- Drop de 10 linhas = 20 pontos
- Drop de 18 linhas = 36 pontos
```

---

## Estratégias para Maximizar Pontos

### 1. Combo Tetris
**Objetivo**: Fazer múltiplos Tetris consecutivos

**Como fazer**:
1. Deixe uma coluna vazia (geralmente lateral)
2. Empilhe peças sem limpar linhas
3. Espere peças I aparecerem
4. Faça Tetris consecutivos
5. Mantenha combo ativo

**Pontos possíveis**:
```
Tetris 1: 1200 × nível × 1.0 = 1200
Tetris 2: 1200 × nível × 1.5 = 1800
Tetris 3: 1200 × nível × 2.0 = 2400
Tetris 4: 1200 × nível × 2.5 = 3000
Tetris 5: 1200 × nível × 3.0 = 3600
Total (Nível 1): 12000 pontos!
```

### 2. Hard Drop Estratégico
**Quando usar**:
- Peça está muito alto e precisa descer
- Quer ganhar pontos extras rápido
- Está sob pressão de tempo

**Quando NÃO usar**:
- Precisa ajustar posição com precisão
- Quer manter controle fino
- Ainda está decidindo onde colocar

### 3. Manutenção de Combo
**Dicas**:
- Sempre tente limpar pelo menos 1 linha
- Use peças I e T para salvar situações difíceis
- Mantenha tabuleiro baixo para facilitar clears
- Evite criar buracos isolados

### 4. Progressão de Nível
**Foco**:
- Nos primeiros níveis: construa combos
- Níveis médios: maximize Tetris
- Níveis altos: sobreviva e mantenha combo básico

---

## Sons do Jogo

| Ação | Som | Quando Toca |
|------|-----|-------------|
| Movimento | move.wav | Peça move lateralmente |
| Rotação | rotate.wav | Peça rotaciona |
| Drop | drop.wav | Hard drop ou peça aterriza |
| Clear | clear.wav | 1-3 linhas limpas |
| Tetris | tetris.wav | 4 linhas limpas |
| Combo | combo.wav | Combo ativo (2+) |
| Level Up | levelup.wav | Sobe de nível |
| Game Over | gameover.wav | Jogo termina |

---

## Feedback Visual Resumido

| Evento | Animação | Duração | Cor |
|--------|----------|---------|-----|
| Hard Drop Bonus | Texto flutuante | 1.5s | Azul |
| Line Clear | Flash/Pulse | 0.3s | Branco |
| Tetris | Flash + Shake | 0.4s | Branco |
| Combo | Texto escalado | 1.0s | Amarelo/Laranja/Roxo |
| Pontos Ganhos | Texto flutuante | 1.5s | Branco/Amarelo |
| Level Up | Flash + Texto | 2.0s | Tema atual |

---

## Teclas de Controle

```
SETAS:     Mover peça (esquerda/direita/baixo)
SETA CIMA: Rotacionar peça
ESPAÇO:    Hard drop (queda instantânea + bônus)
C:         Hold piece (segurar peça)
P:         Pausar jogo
ESC:       Menu principal
R:         Reiniciar (na tela de game over)
```

---

## Dicas Finais

1. **Pratique Hard Drop**: Acostume-se com ESPAÇO para ganhar pontos extras

2. **Mantenha Combos**: Tente sempre limpar pelo menos 1 linha para manter multiplicador

3. **Use Hold**: Segure peças I para Tetris combos devastadores

4. **Observe Animações**: Elas dão feedback importante sobre seu desempenho

5. **Balance Velocidade vs Pontos**: Hard drop dá pontos mas reduz tempo de decisão

6. **Foque em Combos**: Um combo x3 vale mais que clears individuais

7. **Priorize Tetris**: 4 linhas = muito mais pontos que 4× 1 linha

8. **Evite Buracos**: Eles quebram combos e dificultam clears futuros
