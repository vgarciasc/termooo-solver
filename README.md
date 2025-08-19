# Solucionador do Term.ooo

Um solucionador em Python para o term.ooo (versão brasileira do Wordle). Este projeto implementa um algoritmo de estratégia inteligente para encontrar os melhores palpites e resolver o jogo da forma mais otimizada possível.

## Como funciona?

O solucionador usa uma estratégia que minimiza o número esperado de soluções possíveis restantes após cada suposição. Para cada palpite potencial, ele:

1. Calcula quantas palavras restariam para cada resposta possível do jogo
2. Pontua os palpites com base na sua capacidade de reduzir o espaço de soluções
3. Seleciona a palavra que fornece mais informações em média

Um write-up completo pode ser encontrado [aqui](https://vinizinho.net/projects/termooo).

## Como rodar

Faça uma cópia local e instale os pacotes necessários:

```bash
git clone https://github.com/vgarciasc/termooo-solver
cd termooo-solver
pip install requirements.txt
```

Com o ambiente configurado, execute o solucionador principal para obter palpites de palavras passo-a-passo:

```bash
python solver.py
```

O solucionador irá:
- Sugerir um palpite
- Pedir a resposta fornecida pelo jogo (0=cinza, 1=verde, 2=amarelo)
- Filtrar soluções possíveis com base nas respostas
- Continuar até encontrar a solução

### Formato da Resposta do Jogo

Quando o solucionador pedir uma resposta do jogo, forneça 5 dígitos:
- `0` = Letra não está na palavra (cinza)
- `1` = Letra na posição correta (verde)
- `2` = Letra na palavra mas posição errada (amarelo)

Exemplos: 
1. `"serio"` → `01000` (⬛🟩⬛⬛⬛): significa que 'e' está na posição correta, e nenhuma das outras letras existe na solução. 
2. `"quase"` → `20000` (🟨⬛⬛⬛⬛): significa que a resposta final contém 'q', mas não nesta posição, e nenhuma das outras letras aparece na solução. 
