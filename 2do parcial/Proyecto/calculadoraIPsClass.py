from prettytable import PrettyTable
class CalculadoraIPs:

    def calcular_mascara(cidr):
        mascara = [0, 0, 0, 0]
        for i in range(cidr):
            mascara[i // 8] += 1 << (7 - i % 8)
        return '.'.join(map(str, mascara))

    

    def calcular_ips_disponibles(cidr):
        return 2 ** (32 - cidr) - 2

    def calcular_broadcast(ip, cidr):
        direccion = ip.split('.')
        mascara = CalculadoraIPs.calcular_mascara(cidr)

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
        mascara = CalculadoraIPs.calcular_mascara(cidr)

        direccion_minima = []
        for i in range(4):
            direccion_minima.append(int(direccion[i]) & int(mascara.split('.')[i]))

        direccion_minima[3] += 1

        return '.'.join(map(str, direccion_minima))

    def calcular_host_maximo(ip, cidr):
        direccion = ip.split('.')
        mascara = CalculadoraIPs.calcular_mascara(cidr)

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
            mascara = CalculadoraIPs.calcular_mascara(mascara_nueva)
            print(f'Mascara de subredes: {mascara} de {mascara_nueva} bits')
            #Calcular bits prestados
            bits_prestados = mascara_nueva - mascara_actual
            #Calcular numero de subredes
            cantidad_subredes = 2 ** (bits_prestados)
            #Calcular tamaño de cada subred
            tamano_subred = (2 ** (32 - mascara_nueva))-2
            
                
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

            texto_Descripcion = "Subneteo despues de la trancision de la mascara de red:" + str(mascara_actual) + " a " + str(mascara_nueva) + "\n"
            texto_Descripcion += f'Mascara de subredes: {mascara} de {mascara_nueva} bits\n'
            texto_Descripcion += f'Cantidad de subredes: {cantidad_subredes}\n'
            texto_Descripcion += f'Hosts de cada subred: {tamano_subred}\n'

            t = PrettyTable(['Subred', 'Direccion de subred', 'Rango de host', 'Direccion de broadcast','Cantidad de host'])
            tabla = []

            #pasar ip a bits
            ip_bin = CalculadoraIPs.calcular_en_bits(ip)
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
                    #Numero binario de 32 bits inicializado en cero
                    bin32_z = 0
                    bin32_z = bin(bin32_z).replace('0b', '')
                    bin32_z = bin32_z.zfill(32)
                    bin32_z = int(bin32_z, 2)
                else:
                    bin32_z = bin32

                #Sumar el salto a la ip en binario
                ip_bin = int(ip_bin, 2)
                ip_bin = ip_bin + bin32_z
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
                tabla.append([i+1, direccion_red, f'{direccion_minima} - {direccion_maxima}', direccion_broadcast, tamano_subred])

            print(t)
            return t,texto_Descripcion

        except ValueError as e:
            print(e)


    def main_sub(ip,mascara_actual,mascara_nueva):
        direccion_red = CalculadoraIPs.aplicarMascara(ip, CalculadoraIPs.calcular_mascara(mascara_actual))
        t = PrettyTable(['Dato', 'Direccion IP', 'Binario'])
        t.add_row(['Direccion de red', direccion_red, CalculadoraIPs.calcular_en_bits(direccion_red)])
        t.add_row(['Mascara', CalculadoraIPs.calcular_mascara(mascara_actual), CalculadoraIPs.calcular_en_bits(CalculadoraIPs.calcular_mascara(mascara_actual))])
        t.add_row(['Host minimo', CalculadoraIPs.calcular_host_minimo(ip,mascara_actual), CalculadoraIPs.calcular_en_bits(CalculadoraIPs.calcular_host_minimo(ip,mascara_actual))])
        t.add_row(['Host maximo', CalculadoraIPs.calcular_host_maximo(ip,mascara_actual), CalculadoraIPs.calcular_en_bits(CalculadoraIPs.calcular_host_maximo(ip,mascara_actual))])
        t.add_row(['Direccion de broadcast', CalculadoraIPs.calcular_broadcast(ip,mascara_actual), CalculadoraIPs.calcular_en_bits(CalculadoraIPs.calcular_broadcast(ip,mascara_actual))])
        t.add_row(['Cantidad de host', CalculadoraIPs.calcular_ips_disponibles(mascara_actual), ''])
        t.add_row(['Clase', CalculadoraIPs.obtenerClase(ip), ''])

        print(t)

        tabla_sub,texto = CalculadoraIPs.subneteo(direccion_red, mascara_actual, mascara_nueva)

        return t,tabla_sub,texto


