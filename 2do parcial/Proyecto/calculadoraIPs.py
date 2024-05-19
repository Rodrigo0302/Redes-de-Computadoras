import ipaddress

def calcular_subredes(ip, mascara_actual, nueva_mascara):
    # Convertir la dirección IP y las máscaras a objetos de la clase ipaddress.IPv4Network
    red_actual = ipaddress.IPv4Network(ip + '/' + str(mascara_actual), strict=False)
    nueva_red = ipaddress.IPv4Network(ip + '/' + str(nueva_mascara), strict=False)
    print(f'IP: {red_actual.network_address}')
    print(f'Máscara actual: {red_actual.netmask}')

    # Calcular la cantidad de subredes
    cantidad_subredes = 2 ** (nueva_mascara - mascara_actual)
    print(f'Cantidad de subredes: {cantidad_subredes}')


    # Calcular el tamaño de cada subred
    tamano_subred = int(nueva_red.num_addresses / cantidad_subredes)
    print(f'Hosts de cada subred: {tamano_subred}')

    # Imprimir información de cada subred
    for i, subred in enumerate(red_actual.subnets(new_prefix=nueva_mascara)):
        print(f'Subred {i+1}:')
        print(f'IP: {subred.network_address}')
        print(f'Máscara: {subred.netmask}')
        print(f'Rango de host: {subred.network_address + 1} - {subred.broadcast_address - 1}')
        print(f'Broadcast: {subred.broadcast_address}')
        
        print()

# Ejemplo de uso
ip = '192.168.0.0'
mascara_actual = 24
nueva_mascara = 26

calcular_subredes(ip, mascara_actual, nueva_mascara)