
#   Fonte principal da calculadora

def calc():
    import msg
    import validacao as vl
    import calculos as calc

    msg.cabecalho()
    msg.menuPrincipal()

    op = int(input('Escolha sua opção: '))

    if vl.menuOK(op):

        n1 = vl.conversor(input('Digite o 1° número:\n'))
        n2 = vl.conversor(input('Digite o 2° número:\n'))

        if op == 1:
            resultado = calc.somar(n1, n2)
            operador = '+'
        elif op == 2:
            resultado = calc.subtrair(n1, n2)
            operador = '-'
        elif op == 3:
            resultado = calc.multiplicar(n1, n2)
            operador = '*'
        elif op == 4:
            resultado = calc.dividir(n1, n2)
            operador = '/'
        elif op == 5:
            pass
        print(f'{n1:.0f} {operador} {n2:.0f} = {vl.formatacao(resultado)}')
    else:
        print('Erro, parâmetro inválido')

    print('Fim programa')
    msg.Rodape()
calc()