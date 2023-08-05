# Calculadora

print("Bem vindo a Calculadora.")
print("Digite qual operação você deseja fazer: ")
print("1 - Adição \n2 - Subtração \n3 - Multiplicação \n4 - Divisão")

def soma(num1, num2):
  return num1 + num2 

def menos(num1, num2):
  return num1 - num2

def multi(num1, num2):
  return num1 * num2

def devisao(num1, num2):
  return num1 / num2


opcao = int(input())

num1 = float(input("Qual o primeiro valor: "))
num2 = float(input("Qual o segundo valor: "))


if opcao == 1:
  print(soma(num1, num2))

elif opcao == 2:
  print(menos(num1, num2))

elif opcao == 3:
  print(multi(num1, num2))

elif opcao == 4:
  print(divisao(num1, num2))

else:
  print("Opção invalida!")
