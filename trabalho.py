import os 
from struct import *
from funcoes import *	
arquivo = "file"


def main():
	if not os.path.exists("fileInfo"):
		addInfo(0,0,0)

	opcao = ''
	while opcao != 'e':
		opcao = raw_input()
		if opcao == 'i':
			chave = input()
			nome  = raw_input()
			idade = input()
			pessoa = Pessoa(chave,nome,idade)
			info = lerInfo()
			addArquivo(arquivo,hashing(pessoa.chave,info[1]),pessoa)
		elif opcao == 'c':
				chave = input()
				pessoa = buscaPessoa(arquivo,chave)
				if(pessoa):
					print "chave: "+str(pessoa.chave)
					print str(pessoa.nome)
					print str(pessoa.idade)
				else:
					print "chave nao encontrada: "+str(chave)
		elif opcao == 'r':
				chave = input()
				print remover(arquivo,chave)
		elif opcao == 'p':
				imprimiIndice(arquivo)
		elif opcao == 'm':
				print media(arquivo)

if __name__== '__main__':
	main()