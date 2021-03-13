#! /usr/bin/python
import filecmp
resultado = filecmp.cmp('/etc/network/interfaces', 'interfaces_bck')

print('Los ficheros son iguales' if resultado else 'Los ficheros no son iguales :(')

