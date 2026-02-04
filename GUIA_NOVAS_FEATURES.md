# Guia de Uso - Novas Features do Tetrix

## Sistema de Hold Piece

### Como usar:
1. Durante o jogo, pressione **C** ou **Shift** (esquerdo ou direito)
2. A peça atual será guardada no box "HOLD" (lado esquerdo da tela)
3. Você receberá a próxima peça da fila
4. Pressione novamente **C** ou **Shift** para trocar com a peça guardada

### Regras:
- Você só pode fazer hold **uma vez por peça**
- Depois de colocar uma peça no tabuleiro, você pode fazer hold novamente
- O box "HOLD" mostra a peça guardada (se houver)
- Um som é tocado quando você faz hold

### Estratégia:
- Use hold para guardar peças especiais (como o I-piece) para momentos críticos
- Troque peças indesejadas por outras mais úteis no momento
- Planeje com antecedência usando as peças NEXT e HOLD

---

## Feedback de Novo Recorde

### O que esperar:
Quando você fizer um novo high score, verá:

1. **"NEW HIGH SCORE!"** em destaque com animação de pulso
2. Sua posição no ranking (ex: "#1 in Top 10", "#5 in Top 10")
3. As estatísticas completas da partida

### Animação:
- O texto "NEW HIGH SCORE!" pulsa com mudança de cor
- Destaque visual especial para celebrar sua conquista
- Informação clara da sua posição no top 10

---

## Estatísticas de Jogo

### Informações exibidas no Game Over:

1. **Score Final**: Pontuação total alcançada
2. **Level**: Nível máximo atingido
3. **Lines**: Total de linhas limpadas
4. **Time**: Tempo total jogado (formato MM:SS)

### Exemplo de visualização:
```
GAME OVER

NEW HIGH SCORE!
#3 in Top 10

Score: 15420
Level: 8
Lines: 45
Time: 05:23

Press 'R' to Restart
Press 'ESC' for Menu
```

---

## Controles Completos

### Durante o Jogo:
- **←/→**: Mover peça horizontalmente
- **↓**: Descida suave (soft drop)
- **↑**: Rotacionar peça
- **Espaço**: Queda rápida (hard drop)
- **C ou Shift**: Hold piece
- **P**: Pausar
- **ESC**: Voltar ao menu

### No Game Over:
- **R**: Reiniciar jogo
- **ESC**: Voltar ao menu principal

---

## Dicas de Gameplay

1. **Use o Hold estrategicamente**: Não guarde peças sem necessidade. Reserve para momentos críticos.

2. **Planeje com antecedência**: Olhe sempre as peças NEXT e HOLD para planejar suas jogadas.

3. **Busque combos**: Limpar linhas consecutivamente aumenta sua pontuação com multiplicadores.

4. **Hard drops dão bônus**: Usar espaço (hard drop) dá pontos extras pela distância.

5. **Alcance níveis mais altos**: Quanto maior o nível, mais pontos por linha limpa.

---

## Sistema de Pontuação

### Base:
- 1 linha: 40 × nível
- 2 linhas: 100 × nível
- 3 linhas: 300 × nível
- 4 linhas (Tetris): 1200 × nível

### Bônus:
- **Combo**: Multiplicador de até 3× por limpar linhas consecutivamente
- **Hard Drop**: Pontos extras baseados na distância da queda

### Progressão:
- A cada 10 linhas, você sobe de nível
- Velocidade de queda aumenta com o nível
- Nível máximo: 20

---

## Temas Visuais

O jogo mantém três temas disponíveis no menu:

1. **Neon**: Cores vibrantes e modernas
2. **Pastel**: Cores suaves e agradáveis
3. **Retro**: Estilo Game Boy clássico (verde monocromático)

Todas as novas features são compatíveis com todos os temas!

---

## Troubleshooting

### Sons não tocam:
- Verifique se os arquivos de som estão em `assets/sounds/`
- O jogo continua funcionando sem som

### Hold não funciona:
- Certifique-se de não ter usado hold já nesta peça
- Coloque a peça atual no tabuleiro para liberar hold novamente

### Estatísticas não aparecem:
- As estatísticas só aparecem na tela de Game Over
- Certifique-se de que o jogo terminou normalmente

---

## Aproveite o jogo! 🎮
