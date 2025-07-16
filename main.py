from modulo import restar

print("Hello PyCharm")
# Este es un comentario

libro = "El programador pragmatico"
print (libro)
numentero = 1
numeros = [1,2,3,5,8,13,21]
print(numeros[3])
tuti = [1,"gato", 1.1]
print(tuti[2])

lista = {
    10: "Messi",
    7: "Cristiano",
    "gato": "nadie"
}
print(lista["gato"])

PI = 3.14

print(PI)

resultado = PI * 2 +1

print(resultado)

print(4==4)

autorizado = True
if autorizado:
    print("date")
elif PI==1:
    print("no")
else:
    print("yes")

def sumar(primero, segundo):
    return primero + segundo

resultado = sumar(1,5)

print(resultado)

def printlista(lista):
    for elemento in lista:
        print(elemento)

    return

printlista(numeros)

print("reset")

while len(numeros) > 1:
    print(numeros[0])
    numeros.pop(0)


print("listo")

printlista(numeros)


import modulo

print(restar(10,5))
