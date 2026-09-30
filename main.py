# Projeto 1 - Conversão de bases e operações elementares
# Computação Numérica (ECT-3401) - UFRN

alfabeto = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MAX_CASAS = 20  # limite de casas na parte fracionária


def para_digitos(texto, base):
    # troca cada caractere pelo valor do dígito (A=10, B=11, ...)
    digitos = []
    for c in texto:
        if c not in alfabeto or alfabeto.index(c) >= base:
            raise ValueError(f"'{c}' não é dígito válido na base {base}")
        digitos.append(alfabeto.index(c))
    return digitos


def para_texto(digitos):
    return "".join(alfabeto[d] for d in digitos)


def ler_numero(texto, base):
    # separa sinal, parte inteira e parte fracionária
    texto = texto.strip().upper().replace(",", ".")
    negativo = texto.startswith("-")
    texto = texto.lstrip("-+")
    if texto.count(".") > 1 or texto in ("", "."):
        raise ValueError("número inválido")
    if "." in texto:
        inteira, frac = texto.split(".")
    else:
        inteira, frac = texto, ""
    inteira = para_digitos(inteira, base) or [0] #Para o caso de "0" ou ".5"
    frac = para_digitos(frac, base)
    return negativo, inteira, frac


# ---------- conversão ----------

def converter_inteira(digitos, b_origem, b_destino):
    # divisões sucessivas pela base de destino (como na aula),
    # com a divisão armada na base de origem
    resultado = []
    while sum(digitos) > 0:  # enquanto o número não for zero
        resto = 0
        quociente = []
        for d in digitos:  # divisão na chave, dígito por dígito
            valor = resto * b_origem + d
            quociente.append(valor // b_destino)
            resto = valor % b_destino
        resultado.insert(0, resto)  # o resto vira um dígito do resultado
        digitos = quociente  # continua dividindo o quociente
    return resultado or [0]


def converter_frac(digitos, b_origem, b_destino):
    # multiplicações sucessivas pela base de destino, armadas na base de origem.
    # o que passa para a parte inteira é o próximo dígito do resultado
    frac = digitos[:]
    resultado = []
    vistos = []
    while sum(frac) > 0:
        if frac in vistos:
            return resultado, vistos.index(frac), False  # dízima periódica
        if len(resultado) == MAX_CASAS:
            return resultado, None, True  # truncado
        vistos.append(frac[:])
        vai_um = 0
        for i in range(len(frac) - 1, -1, -1):
            valor = frac[i] * b_destino + vai_um
            frac[i] = valor % b_origem
            vai_um = valor // b_origem
        resultado.append(vai_um)
    return resultado, None, False  # exato


def converter(texto, b_origem, b_destino):
    negativo, inteira, frac = ler_numero(texto, b_origem)
    nova_inteira = converter_inteira(inteira, b_origem, b_destino)
    nova_frac, inicio, truncado = converter_frac(frac, b_origem, b_destino)

    resultado = para_texto(nova_inteira)
    if nova_frac:
        casas = para_texto(nova_frac)
        if inicio is not None:
            casas = casas[:inicio] + "(" + casas[inicio:] + ")"
        resultado += "." + casas
    if negativo and sum(inteira) + sum(frac) > 0:
        resultado = "-" + resultado
    return resultado, inicio, truncado


# ---------- operações (armadas na própria base) ----------

def somar(a, b, base):
    # soma da direita pra esquerda com vai-um
    tam = max(len(a), len(b))
    a = [0] * (tam - len(a)) + a
    b = [0] * (tam - len(b)) + b
    resultado = []
    vai_um = 0
    for i in range(tam - 1, -1, -1):
        s = a[i] + b[i] + vai_um
        resultado.insert(0, s % base)
        vai_um = s // base
    if vai_um > 0:
        resultado.insert(0, vai_um)
    return resultado


def multiplicar(a, b, base):
    # para cada dígito de b: multiplica a pelo dígito, desloca e soma.
    # em base 2 isso é o shift-and-add visto em aula
    resultado = [0]
    for i in range(len(b)):
        d = b[len(b) - 1 - i]
        parcial = []
        vai_um = 0
        for j in range(len(a) - 1, -1, -1):
            p = a[j] * d + vai_um
            parcial.insert(0, p % base)
            vai_um = p // base
        if vai_um > 0:
            parcial.insert(0, vai_um)
        parcial = parcial + [0] * i  # deslocamento de i casas
        resultado = somar(resultado, parcial, base)
    return resultado


def montar(digitos, casas):
    # coloca o ponto de volta e tira os zeros que sobram
    digitos = [0] * (casas + 1 - len(digitos)) + digitos
    inteira = digitos[:len(digitos) - casas]
    frac = digitos[len(digitos) - casas:]
    while len(inteira) > 1 and inteira[0] == 0:
        inteira.pop(0)
    while frac and frac[-1] == 0:
        frac.pop()
    texto = para_texto(inteira)
    if frac:
        texto += "." + para_texto(frac)
    return texto


def calcular(texto1, op, texto2, base):
    neg1, int1, frac1 = ler_numero(texto1, base)
    neg2, int2, frac2 = ler_numero(texto2, base)
    if neg1 or neg2:
        raise ValueError("negativos ainda não suportados (vêm junto com a subtração)")

    # os números são escritos sem o ponto, guardando quantas casas tinham depois dele
    # ex: 1.01 vira 101 com 2 casas (como o 1,01 = 101 x 2^-2 da aula)
    if op == "+":
        casas = max(len(frac1), len(frac2)) #Aqui é somente para trabalhar com a mesma qtd de casas.
        a = int1 + frac1 + [0] * (casas - len(frac1))
        b = int2 + frac2 + [0] * (casas - len(frac2))
        return montar(somar(a, b, base), casas)
    if op == "*":
        casas = len(frac1) + len(frac2)
        return montar(multiplicar(int1 + frac1, int2 + frac2, base), casas)
    raise ValueError("operação inválida")


# ---------- terminal ----------

def ler_base(mensagem):
    while True:
        try:
            base = int(input(mensagem))
            if 2 <= base <= 36:
                return base
        except ValueError:
            pass
        print("A base deve ser um número de 2 a 36.")


def menu_conversor():
    numero = input("Número: ")
    b_origem = ler_base("Da base: ")
    b_destino = ler_base("Para a base: ")
    resultado, inicio, truncado = converter(numero, b_origem, b_destino)
    print(f"\n{numero.strip().upper()} (base {b_origem}) = {resultado} (base {b_destino})")
    if inicio is not None:
        print("Dízima periódica: o trecho entre parênteses se repete.")
    if truncado:
        print(f"Parte fracionária cortada em {MAX_CASAS} casas.")


def menu_calculadora():
    base = ler_base("Base: ")
    n1 = input("Primeiro número: ")
    op = input("Operação (+ ou *): ").strip()
    n2 = input("Segundo número: ")
    resultado = calcular(n1, op, n2, base)
    print(f"\n{n1.strip().upper()} {op} {n2.strip().upper()} = {resultado} (base {base})")
    if base != 10:
        em_decimal, _, _ = converter(resultado, base, 10)
        print(f"Em decimal: {em_decimal}")


def main():
    while True:
        print("\n1 - Converter base")
        print("2 - Calculadora")
        print("0 - Sair")
        opcao = input("Opção: ").strip()
        try:
            if opcao == "1":
                menu_conversor()
            elif opcao == "2":
                menu_calculadora()
            elif opcao == "0":
                break
            else:
                print("Opção inválida.")
        except ValueError as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
