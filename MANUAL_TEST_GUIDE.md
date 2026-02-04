# Guia de Testes Manuais - Novas Features

## Objetivo
Validar as três novas features implementadas no jogo Tetrix através de testes manuais.

---

## Preparação

### 1. Executar o Jogo
```bash
cd /media/marvinbraga/python/marvin/games/tetrix
uv run python main.py
```

### 2. Verificações Iniciais
- [ ] O jogo inicia sem erros
- [ ] Menu principal é exibido
- [ ] Sons estão funcionando
- [ ] Tema visual está correto

---

## Teste 1: Sistema de Hold Piece

### Objetivo
Verificar funcionamento completo do hold piece system.

### Passos:

#### 1.1. Hold Básico
1. Iniciar novo jogo
2. Aguardar primeira peça spawnar
3. Pressionar **C** (ou Shift)
4. **Esperado:**
   - Som de hold é reproduzido
   - Peça atual vai para box HOLD (canto superior esquerdo)
   - Nova peça aparece (a que estava em NEXT)
   - Box NEXT atualiza com próxima peça

#### 1.2. Tentativa de Hold Duplo
1. Com uma peça ativa, pressionar C
2. Sem colocar a peça, pressionar C novamente
3. **Esperado:**
   - Segunda tentativa NÃO funciona
   - Peça permanece a mesma
   - Sem som na segunda tentativa

#### 1.3. Swap de Hold
1. Fazer hold de uma peça (ex: I-piece)
2. Colocar a próxima peça no tabuleiro
3. Aguardar nova peça spawnar
4. Pressionar C novamente
5. **Esperado:**
   - Peça atual vai para hold
   - Peça anteriormente em hold (I-piece) volta ao jogo
   - Som de hold toca
   - Box HOLD atualiza

#### 1.4. Hold no Início
1. Iniciar novo jogo
2. Imediatamente pressionar C na primeira peça
3. **Esperado:**
   - Primeira peça vai para hold
   - Segunda peça entra no jogo
   - Box HOLD exibe primeira peça

### Checklist:
- [ ] Hold funciona com tecla C
- [ ] Hold funciona com Shift esquerdo
- [ ] Hold funciona com Shift direito
- [ ] Som de hold toca
- [ ] Visual do hold box correto
- [ ] Pode fazer hold apenas uma vez por peça
- [ ] Pode fazer hold novamente após colocar peça
- [ ] Swap funciona corretamente

---

## Teste 2: Feedback de High Score

### Objetivo
Verificar mensagem e animação de novo recorde.

### Passos:

#### 2.1. Preparação
1. Verificar arquivo `data/high_scores.json`
2. Se necessário, editar para ter scores baixos (facilitar teste)
   ```json
   [
     {"score": 100, "date": "2026-01-01 00:00", "level": 1},
     {"score": 50, "date": "2026-01-01 00:00", "level": 1}
   ]
   ```

#### 2.2. Alcançar Novo High Score
1. Iniciar novo jogo
2. Jogar até alcançar score maior que o menor no top 10
3. Deixar o jogo terminar (perder)
4. **Esperado na tela de Game Over:**
   - Mensagem "NEW HIGH SCORE!" em destaque
   - Texto pulsando (mudança de cor)
   - Posição no ranking exibida (ex: "#3 in Top 10")

#### 2.3. Verificar Primeiro Lugar
1. Alcançar score maior que todos no top 10
2. Deixar jogo terminar
3. **Esperado:**
   - "NEW HIGH SCORE!"
   - "#1 in Top 10"

#### 2.4. Score Normal
1. Fazer score menor que qualquer um no top 10
2. Deixar jogo terminar
3. **Esperado:**
   - Sem mensagem de high score
   - Apenas estatísticas normais

### Checklist:
- [ ] Mensagem "NEW HIGH SCORE!" aparece
- [ ] Animação de pulso funciona
- [ ] Posição no ranking está correta
- [ ] Posição #1 funciona
- [ ] Posições intermediárias funcionam
- [ ] Sem mensagem quando não é high score

---

## Teste 3: Estatísticas de Jogo

### Objetivo
Verificar rastreamento e exibição de estatísticas.

### Passos:

#### 3.1. Verificar Tempo de Jogo
1. Iniciar novo jogo
2. Jogar por exatamente 1 minuto (usar cronômetro)
3. Deixar jogo terminar
4. **Esperado na tela Game Over:**
   - "Time: 01:00" (ou próximo, ±2 segundos)

#### 3.2. Verificar Tempo Longo
1. Jogar por 5+ minutos
2. Verificar formatação
3. **Esperado:**
   - Formato MM:SS correto
   - Ex: "Time: 05:23"

#### 3.3. Verificar Todas as Estatísticas
1. Jogar uma partida completa
2. Observar tela de Game Over
3. **Esperado - estatísticas visíveis:**
   - Score: [número]
   - Level: [número]
   - Lines: [número]
   - Time: MM:SS

#### 3.4. Verificar Precisão
1. Contar manualmente:
   - Linhas limpadas
   - Nível alcançado
2. Comparar com estatísticas exibidas
3. **Esperado:**
   - Valores corretos e precisos

### Checklist:
- [ ] Tempo é rastreado corretamente
- [ ] Formato MM:SS está correto
- [ ] Score exibido correto
- [ ] Level exibido correto
- [ ] Lines exibidas corretas
- [ ] Layout visual organizado
- [ ] Cores consistentes com tema

---

## Teste 4: Integração entre Features

### Objetivo
Verificar que features funcionam bem juntas.

### Passos:

#### 4.1. Hold + High Score + Estatísticas
1. Usar hold várias vezes durante o jogo
2. Alcançar novo high score
3. Deixar jogo terminar
4. **Esperado:**
   - Hold funcionou normalmente
   - High score detectado
   - Todas as estatísticas corretas
   - Sem crashes ou bugs visuais

#### 4.2. Múltiplos Holds em Partida Longa
1. Jogar por 5+ minutos
2. Usar hold frequentemente
3. Verificar se hold continua funcionando
4. **Esperado:**
   - Hold sempre disponível após colocar peça
   - Sem degradação de performance
   - Tempo continua contando

### Checklist:
- [ ] Features não interferem entre si
- [ ] Performance estável
- [ ] Sem memory leaks aparentes
- [ ] Visual consistente

---

## Teste 5: Compatibilidade com Temas

### Objetivo
Verificar que features funcionam com todos os temas.

### Passos:

#### 5.1. Tema Neon
1. Selecionar tema Neon no menu
2. Testar hold piece
3. Alcançar game over
4. **Esperado:**
   - Hold box com cores Neon
   - Estatísticas legíveis
   - High score message visível

#### 5.2. Tema Pastel
1. Selecionar tema Pastel
2. Repetir testes
3. **Esperado:**
   - Cores suaves mantidas
   - Tudo legível

#### 5.3. Tema Retro
1. Selecionar tema Retro (Game Boy)
2. Repetir testes
3. **Esperado:**
   - Tons de verde consistentes
   - Hold box estilizado
   - Estatísticas em verde

### Checklist:
- [ ] Hold box visível em Neon
- [ ] Hold box visível em Pastel
- [ ] Hold box visível em Retro
- [ ] Estatísticas legíveis em todos os temas
- [ ] High score message visível em todos
- [ ] Animação funciona em todos

---

## Teste 6: Casos Extremos

### Objetivo
Testar comportamentos edge case.

#### 6.1. Hold com Tabuleiro Cheio
1. Encher o tabuleiro até quase perder
2. Tentar fazer hold
3. **Esperado:**
   - Hold funciona normalmente
   - Se nova peça não cabe, game over

#### 6.2. Hold Consecutivo Após Tetris
1. Fazer um Tetris (4 linhas)
2. Imediatamente fazer hold na próxima peça
3. **Esperado:**
   - Hold funciona
   - Animações não interferem

#### 6.3. Tempo Muito Longo
1. Deixar jogo rodando por 60+ minutos (opcional)
2. Verificar tempo
3. **Esperado:**
   - Formato correto (ex: 63:45)
   - Sem overflow

### Checklist:
- [ ] Hold funciona em situações extremas
- [ ] Tempo não quebra com valores altos
- [ ] Sem crashes em edge cases

---

## Teste 7: Usabilidade

### Objetivo
Avaliar experiência do usuário.

### Avaliação Subjetiva:

#### Visual
- [ ] Hold box está bem posicionado?
- [ ] Estatísticas são fáceis de ler?
- [ ] High score message chama atenção?
- [ ] Animação de pulso é agradável?

#### Gameplay
- [ ] Hold é intuitivo de usar?
- [ ] Feedback sonoro é adequado?
- [ ] Informações são claras?

#### Performance
- [ ] Jogo roda suavemente?
- [ ] Sem lags perceptíveis?
- [ ] Responsividade mantida?

---

## Relatório de Bugs

Se encontrar bugs, documentar:

### Template:
```
Bug #[número]
Descrição: [o que aconteceu]
Reprodução:
  1. [passo 1]
  2. [passo 2]
  3. [resultado]
Esperado: [o que deveria acontecer]
Observado: [o que realmente aconteceu]
Severidade: [Crítico/Alto/Médio/Baixo]
```

---

## Conclusão do Teste

### Resumo:
- Total de testes planejados: ~40 verificações
- Testes passados: ___
- Testes falhos: ___
- Bugs encontrados: ___

### Status Final:
- [ ] Todas as features funcionando
- [ ] Pronto para uso
- [ ] Necessita correções

---

**Data do Teste:** ___________
**Testador:** ___________
**Versão:** 1.0 (novas features)
