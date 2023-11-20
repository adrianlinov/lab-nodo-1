def dividir_diccionario(diccionario, num_divisiones):
    resultado = []

    for i in range(num_divisiones):
        division = {}
        for clave_padre, valores_hijos in diccionario.items():
            division[clave_padre] = {}
            for clave_hijo, valor_hijo in valores_hijos.items():
                if int(clave_hijo) % num_divisiones == i:
                    division[clave_padre][clave_hijo] = valor_hijo
        resultado.append(division)

    return resultado

diccionario_original = {'SO1': {'5': 11.0, '4': 10.9, '7': 11.1, '6': 11.1, '1': 10.9, '8': 11.0, '3': 10.9, '2': 11.0, '9': 11.0}, 'SC1': {'5': 0.0, '4': 0.0, '7': 0.0, '6': 0.0, '1': 0.0, '8': 0.0, '3': 0.0, '2': 0.0, '9': 0.0}, 'STW10': {'5': 0.0, '4': 0.0, '7': 0.0, '6': 0.0, '1': 0.0, '8': 0.0, '3': 0.0, '2': 0.0, '9': 0.0}, 'SPH1': {'5': 3.63, '4': 3.67, '7': 3.63, '6': 3.66, '1': 3.68, '8': 3.65, '3': 3.64, '2': 3.63, '9': 3.67}}

num_divisiones = 3
divisiones = dividir_diccionario(diccionario_original, num_divisiones)
print(divisiones)
