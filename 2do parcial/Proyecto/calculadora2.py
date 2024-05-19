from prettytable import PrettyTable
def calcular_mascara(cidr):
    mascara = [0, 0, 0, 0]
    for i in range(cidr):
        mascara[i // 8] += 1 << (7 - i % 8)
    return '.'.join(map(str, mascara))

def calcular_rango_direcciones(ip, cidr):
    direccion = ip.split('.')
    mascara = calcular_mascara(cidr)

    direccion_red = []
    for i in range(4):
        direccion_red.append(int(direccion[i]) & int(mascara.split('.')[i]))

    direccion_broadcast = []
    for i in range(4):
        direccion_broadcast.append(int(direccion[i]) | (255 - int(mascara.split('.')[i])))

    return '.'.join(map(str, direccion_red)), '.'.join(map(str, direccion_broadcast))

def calcular_ips_disponibles(cidr):
    return 2 ** (32 - cidr) - 2

def calcular_mascara(cidr):
    mascara = [0, 0, 0, 0]
    for i in range(cidr):
        mascara[i // 8] += 1 << (7 - i % 8)
    return '.'.join(map(str, mascara))
def calcular_broadcast(ip, cidr):
    direccion = ip.split('.')
    mascara = calcular_mascara(cidr)

    direccion_broadcast = []
    for i in range(4):
        direccion_broadcast.append(int(direccion[i]) | (255 - int(mascara.split('.')[i])))

    return '.'.join(map(str, direccion_broadcast))

def calcular_en_bits(ip):
    octetos = ip.split('.')
    octetos_bin = [bin(int(octeto)).replace('0b', '') for octeto in octetos]
    octetos_completos = [octeto.zfill(8) for octeto in octetos_bin]
    return '.'.join(octetos_completos)

def calcular_host_minimo(ip, cidr):
    direccion = ip.split('.')
    mascara = calcular_mascara(cidr)

    direccion_minima = []
    for i in range(4):
        direccion_minima.append(int(direccion[i]) & int(mascara.split('.')[i]))
    
    direccion_minima[3] += 1

    return '.'.join(map(str, direccion_minima))

def calcular_host_maximo(ip, cidr):
    direccion = ip.split('.')
    mascara = calcular_mascara(cidr)

    direccion_maxima = []
    for i in range(4):
        direccion_maxima.append(int(direccion[i]) | (255 - int(mascara.split('.')[i])))

    direccion_maxima[3] -= 1

    return '.'.join(map(str, direccion_maxima))


def obtenerClase(ip):
    octetos = ip.split('.')
    primer_octeto = int(octetos[0])

    if primer_octeto >= 0 and primer_octeto <= 127:
        return 'A'
    elif primer_octeto >= 128 and primer_octeto <= 191:
        return 'B'
    elif primer_octeto >= 192 and primer_octeto <= 223:
        return 'C'
    elif primer_octeto >= 224 and primer_octeto <= 239:
        return 'D'
    elif primer_octeto >= 240 and primer_octeto <= 255:
        return 'E'
    
def aplicarMascara(ip, mascara):
    octetos_ip = ip.split('.')
    octetos_mascara = mascara.split('.')
    octetos_red = [str(int(octetos_ip[i]) & int(octetos_mascara[i])) for i in range(4)]
    return '.'.join(octetos_red)

def subneteo(ip, mascara_actual, mascara_nueva):
    try:
        mascara_actual = int(mascara_actual)
        mascara_nueva = int(mascara_nueva)

        if mascara_actual < 0 or mascara_actual > 32 or mascara_nueva < 0 or mascara_nueva > 32:
            raise ValueError('La máscara debe estar entre 1 y 32')

        if mascara_nueva < mascara_actual:
            raise ValueError('La nueva máscara debe ser mayor o igual a la actual')

        print("Subneteo despues de la trancision de la mascara de red:" ,str(mascara_actual) , " a " , str(mascara_nueva))
        #Calcular la mascara de red
        mascara = calcular_mascara(mascara_nueva)
        print(f'Mascara de subredes: {mascara} de {mascara_nueva} bits')
        #Calcular bits prestados
        bits_prestados = mascara_nueva - mascara_actual
        #Calcular numero de subredes
        cantidad_subredes = 2 ** (bits_prestados)
        #Calcular tamaño de cada subred
        tamano_subred = (2 ** (32 - mascara_nueva))-2
        #Obtener el ultimo octeto de la mascara diferente de cero y Obtener en que octeto se realizaran los saltos
        octeto = 0
        mascara = mascara.split('.')
        for i in range(4):
            if mascara[3-i] != '0':
                octeto = int(mascara[3-i])
                break
        
        #Numero binario de 32 bits inicializado en cero
        bin32 = 0
        bin32 = bin(bin32).replace('0b', '')
        bin32 = bin32.zfill(32)
        #print('Bin32:', bin32)

        #Poner un uno en la posicion mascara_nueva - 1
        bin32 = list(bin32)
        bin32[mascara_nueva-1] = '1'
        bin32 = ''.join(bin32)
        #print('Bin32:', bin32)
        bin32 = int(bin32, 2)
        
        #print(f'Salto en binario: {salto_bin}')
        #print('Octeto donde se realizaran los saltos:', octeto_i)

        print(f'Cantidad de subredes: {cantidad_subredes}')
        print(f'Hosts de cada subred: {tamano_subred}')
        t = PrettyTable(['Subred', 'Direccion de subred', 'Rango de host', 'Direccion de broadcast','Cantidad de host'])
        

        #pasar ip a bits
        ip_bin = calcular_en_bits(ip)
        ip_bin = ip_bin.split('.')
        #Juntar los octetos de la ip en una sola cadena
        ip_bin = ''.join(ip_bin)
        #Convertir ip_bin a binario
        ip_bin = bin(int(ip_bin, 2)).replace('0b', '')
        #print('IP en binario INICIAL:', ip_bin)
        
        for i in range(cantidad_subredes):
            if i == 1000:
                break
            
            if i == 0:
               #Sumar el salto a la ip en binario
                
                ip_bin = ip_bin.zfill(32)   
                #print('IP en binario:', ip_bin)
                #Pasarlo a octetos
                direccion_red = []
                direccion_red.append(str(int(ip_bin[0:8], 2)))
                direccion_red.append(str(int(ip_bin[8:16], 2)))
                direccion_red.append(str(int(ip_bin[16:24], 2)))
                direccion_red.append(str(int(ip_bin[24:32], 2)))
                direccion_red = '.'.join(direccion_red)
                #print('Direccion de red:', direccion_red)

                #Calcular el broadcast en binario
                broadcast = ip_bin

                broadcast = list(broadcast)

                for j in range(mascara_nueva, 32):
                    broadcast[j] = '1'
                broadcast = ''.join(broadcast)
                #print('Broadcast en binario:', broadcast)
                direccion_broadcast = []
                direccion_broadcast.append(str(int(broadcast[0:8], 2)))
                direccion_broadcast.append(str(int(broadcast[8:16], 2)))
                direccion_broadcast.append(str(int(broadcast[16:24], 2)))
                direccion_broadcast.append(str(int(broadcast[24:32], 2)))
                direccion_broadcast = '.'.join(direccion_broadcast)
                #print('Direccion de broadcast:', direccion_broadcast)

                #Calcular el rango de host
                ip_minima = int(ip_bin, 2)+1
                ip_minima = bin(ip_minima).replace('0b', '')
                ip_minima = ip_minima.zfill(32)
                direccion_minima = []
                direccion_minima.append(str(int(ip_minima[0:8], 2)))
                direccion_minima.append(str(int(ip_minima[8:16], 2)))
                direccion_minima.append(str(int(ip_minima[16:24], 2)))
                direccion_minima.append(str(int(ip_minima[24:32], 2)))
                direccion_minima = '.'.join(direccion_minima)



                #print('IP minima:', direccion_minima)
                ip_maxima = int(broadcast, 2) - 1
                ip_maxima = bin(ip_maxima).replace('0b', '')
                ip_maxima = ip_maxima.zfill(32)
                direccion_maxima = []
                direccion_maxima.append(str(int(ip_maxima[0:8], 2)))
                direccion_maxima.append(str(int(ip_maxima[8:16], 2)))
                direccion_maxima.append(str(int(ip_maxima[16:24], 2)))
                direccion_maxima.append(str(int(ip_maxima[24:32], 2)))
                direccion_maxima = '.'.join(direccion_maxima)
            else:
                #Sumar el salto a la ip en binario
                ip_bin = int(ip_bin, 2)
                ip_bin = ip_bin + bin32
                ip_bin = bin(ip_bin).replace('0b', '')
                ip_bin = ip_bin.zfill(32)   
                #print('IP en binario:', ip_bin)
                #Pasarlo a octetos
                direccion_red = []
                direccion_red.append(str(int(ip_bin[0:8], 2)))
                direccion_red.append(str(int(ip_bin[8:16], 2)))
                direccion_red.append(str(int(ip_bin[16:24], 2)))
                direccion_red.append(str(int(ip_bin[24:32], 2)))
                direccion_red = '.'.join(direccion_red)
                #print('Direccion de red:', direccion_red)

                #Calcular el broadcast en binario
                broadcast = ip_bin

                broadcast = list(broadcast)

                for j in range(mascara_nueva, 32):
                    broadcast[j] = '1'
                broadcast = ''.join(broadcast)
                #print('Broadcast en binario:', broadcast)
                direccion_broadcast = []
                direccion_broadcast.append(str(int(broadcast[0:8], 2)))
                direccion_broadcast.append(str(int(broadcast[8:16], 2)))
                direccion_broadcast.append(str(int(broadcast[16:24], 2)))
                direccion_broadcast.append(str(int(broadcast[24:32], 2)))
                direccion_broadcast = '.'.join(direccion_broadcast)
                #print('Direccion de broadcast:', direccion_broadcast)

                #Calcular el rango de host
                ip_minima = int(ip_bin, 2)+1
                ip_minima = bin(ip_minima).replace('0b', '')
                ip_minima = ip_minima.zfill(32)
                direccion_minima = []
                direccion_minima.append(str(int(ip_minima[0:8], 2)))
                direccion_minima.append(str(int(ip_minima[8:16], 2)))
                direccion_minima.append(str(int(ip_minima[16:24], 2)))
                direccion_minima.append(str(int(ip_minima[24:32], 2)))
                direccion_minima = '.'.join(direccion_minima)



                #print('IP minima:', direccion_minima)
                ip_maxima = int(broadcast, 2) - 1
                ip_maxima = bin(ip_maxima).replace('0b', '')
                ip_maxima = ip_maxima.zfill(32)
                direccion_maxima = []
                direccion_maxima.append(str(int(ip_maxima[0:8], 2)))
                direccion_maxima.append(str(int(ip_maxima[8:16], 2)))
                direccion_maxima.append(str(int(ip_maxima[16:24], 2)))
                direccion_maxima.append(str(int(ip_maxima[24:32], 2)))
                direccion_maxima = '.'.join(direccion_maxima)
                #print('IP maxima:', direccion_maxima)
                #print('Rango de host:', ip_minima, '-', ip_maxima)

            t.add_row([i+1, direccion_red, f'{direccion_minima} - {direccion_maxima}', direccion_broadcast, tamano_subred])
            
        print(t)
        
    except ValueError as e:
        print(e)

# Uso del programa
ip = '198.51.100.1'
mascara_actual = 15
mascara_nueva = 28

direccion_red = aplicarMascara(ip, calcular_mascara(mascara_actual))
t = PrettyTable(['Dato', 'Direccion IP', 'Binario'])
t.add_row(['Direccion de red', direccion_red, calcular_en_bits(ip)])
t.add_row(['Mascara', calcular_mascara(mascara_actual), calcular_en_bits(calcular_mascara(mascara_actual))])
t.add_row(['Host minimo', calcular_host_minimo(ip,mascara_actual), calcular_en_bits(calcular_host_minimo(ip,mascara_actual))])
t.add_row(['Host maximo', calcular_host_maximo(ip,mascara_actual), calcular_en_bits(calcular_host_maximo(ip,mascara_actual))])
t.add_row(['Direccion de broadcast', calcular_broadcast(ip,mascara_actual), calcular_en_bits(calcular_broadcast(ip,mascara_actual))])
t.add_row(['Cantidad de host', calcular_ips_disponibles(mascara_actual), ''])
t.add_row(['Clase', obtenerClase(ip), ''])


print(t)

subneteo(direccion_red, mascara_actual, mascara_nueva)
