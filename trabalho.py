import os 
from struct import *
from funcoes import *	
arquivo = "dados"


def main():
	opcao = ''
	while opcao != 'e':
		opcao = raw_input()
		if opcao == 'i':
			chave = input()
			nome  = raw_input()
			idade = input()
			pessoa = Pessoa(chave,nome,idade)
			addArquivo(arquivo,hashFirst(pessoa.chave),pessoa)
		elif opcao == 'c':
				chave = input()
				print vericarChave(arquivo,chave)
		elif opcao == 'r':
				chave = input()
				print remove(arquivo,chave)
		elif opcao == 'p':
				imprimiArquivo(arquivo)
		elif opcao == 't':
				chave = input()
				tentarInsercao(arquivo,chave)
		elif opcao == 'm':
			print "Media"





if __name__== '__main__':
	main()