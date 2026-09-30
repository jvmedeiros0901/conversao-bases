# Projeto 1 — Conversão de Bases e Operações Elementares

Disciplina: Computação Numérica (ECT-3401) — UFRN
Professor: Joilson B. A. Rego
Unidade: I

Estudo prático em ponto flutuante: converter números reais entre bases
arbitrárias sem usar a base 10 como intermediária, e executar as operações
elementares dentro da base escolhida.

## Objetivos (do enunciado)

| Ref. | Objetivo |
|---|---|
| O1 | Conversão direta entre bases arbitrárias por aritmética polinomial, calculada na base de origem ou de destino, sem coerção decimal |
| O2 | Mapeamento dinâmico de caracteres (0-9, A-Z) com validação dos pesos posicionais |
| O3 | Não utilizar a base 10 como ponte nas conversões |
| O4 | Operações elementares (+, −, ×, ÷) armadas diretamente na base escolhida |
| O5 | Tratar dízimas periódicas nativas, identificando o padrão de repetição na base de destino |

## Distribuição da nota

| Item | Pontos |
|---|---|
| Código-fonte documentado da conversão direta (x ∈ ℝ) | 3,0 |
| Operações elementares para a base escolhida | 4,0 |
| Relatório final com interpretação e avaliação crítica | 3,0 |

## Observações ditas em aula

- A conversão deve ser pelo método direto, sem passar pela base 10 — parte
  inteira e parte fracionária.
- As **operações elementares podem passar pela base 10**. A restrição do O3
  vale para a conversão, não para elas.
- Começar pela soma e pela multiplicação; subtração e divisão vêm depois.
- Usar deslocamento de bits (`<<`, `>>`) do Python onde couber.
- Estudar conversão de fracionários por multiplicações sucessivas.
- Estudar arredondamento e truncamento de bits.

## Sobre a proibição da base 10

A linha que separa o permitido do proibido, conforme o enunciado pede para
"simular o comportamento de registradores e a manipulação direta de vetores
de dígitos":

- **Permitido:** guardar o valor de um dígito isolado e do vai-um em variáveis
  comuns — são registradores.
- **Proibido:** converter o número inteiro para um valor decimal e usar esse
  valor como ponte entre as bases.
