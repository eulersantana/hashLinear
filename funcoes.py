import os, array
from struct import *
# Muda o tamanho do arquivo
TAMANHO_ARQUIVO = 11

class Pessoa:
	def __init__(self,chave,nome,idade):
		self.chave 	= chave
		self.nome 	= nome
		self.idade	= idade


def hashFirst(chave):
	return chave % TAMANHO_ARQUIVO

def hashSecond(chave):
	return (chave / TAMANHO_ARQUIVO)%TAMANHO_ARQUIVO
 
def criarArquivo(arquivo):
	data = open(arquivo,"w+b")
	data.close()


#Insercao sem tramento de colisao, so trata repeticao e iguadade de chaves
def addArquivo(arquivo,indice,pessoa):

	if os.path.exists(arquivo):
		mode = "ab+"
		arq = open(arquivo,mode)
	else:
		mode = "w+b"
		arq = open(arquivo,mode)
	removeRimovido(arquivo,pessoa.chave)
	if vericarChave(arquivo,pessoa.chave) != "chave: "+str(pessoa.chave) and len(pessoa.nome) <= 20:
		fmt = "fhh"+str(len(pessoa.nome))+"slcc"
		dados = pack(fmt,indice,pessoa.chave,len(pessoa.nome),pessoa.nome,pessoa.idade," ","\n")
		arq.write(dados)
		arq.close()
	elif len(pessoa.nome) <= 20:
		print "chave ja existente: "+str(pessoa.chave)




def vericarChave(arquivo,chave):
	mode = "rb"
	arq = open(arquivo, mode)
	valores = arq.readlines()
	for valor in valores:
		if array.array("b",valor)[4] == chave:
			arq.close()
			return "chave: "+str(chave)
	arq.close()
	return "chave nao encontrada: "+str(chave)

# def removeResgistro(arquivo,cahve):
def imprimiArquivo(arquivo):
	if os.path.exists(arquivo):
		for linha in range(TAMANHO_ARQUIVO):
			print imprimiIndice(arquivo,linha)
			
	

def imprimiIndice(arquivo, indice):
	arq = open(arquivo,"r+b")
	valores = arq.readlines()
	valores.sort()
	for linha in valores:
		tNome = array.array('b',linha)[6]
		fmt = "fhh"+str(tNome)+"slcc"
		info = unpack(fmt,linha)
		if int(info[0]) == indice:
			if info[5] != '*':
				return str(int(info[0]))+": "+str(info[1])+" "+str(info[3])+" "+str(info[4])+" "+str(info[5])
			else:
				return str(int(info[0]))+": *" 
	arq.close()
	return str(indice)+": "+"vazio"

def buscaPessoa(arquivo,chave):
	if os.path.exists(arquivo):
		arq = open(arquivo,"rb")
		valores = arq.readlines()
			
		for linha in valores:
			tNome = array.array('b',linha)[6]
			chaveaux = array.array('b',linha)[4]
			if chaveaux == chave:
				fmt = "fhh"+str(tNome)+"slcc"
				info = unpack(fmt,linha)
				arq.close()
				return Pessoa(info[1],info[3],info[4]) 
	arq.close()
	return None	


def remove(arquivo,chave):
	if os.path.exists(arquivo):
		arq = open(arquivo,"rb+")
		valores = arq.readlines()
		valores.sort()
		for linha in valores:
			tNome = array.array('b',linha)[6]
			fmt = "fhh"+str(tNome)+"slcc"
			info = unpack(fmt,linha)
			if info[1] == chave:
				data = pack(fmt,info[0],info[1],info[2],info[3],info[4],"*","\n")
				valores.remove(linha)
				valores.append(data)
				arq.close()
				arq = open(arquivo,"w+b")
				for linha2 in valores:
					arq.write(linha2)
				arq.close()
				return ""
		return "chave nao encontrada: "+str(chave)

def removeRimovido(arquivo,chave):
	if os.path.exists(arquivo):
		arq = open(arquivo,"rb+")
		valores = arq.readlines()
		valores.sort()
		for linha in valores:
			tNome = array.array('b',linha)[6]
			fmt = "fhh"+str(tNome)+"slcc"
			info = unpack(fmt,linha)
			if info[5] == '*':
				valores.remove(linha)
				arq.close()
				arq = open(arquivo,"w+b")
				for linha2 in valores:
					arq.write(linha2)
				arq.close()
				return

				
def buscaChave(arquivo,indice):
	if os.path.exists(arquivo):
		arq = open(arquivo,"rb")
		valores = arq.readlines()
		valores.sort()
		for linha in valores:
			tNome = array.array('b',linha)[6]
			fmt = "fhh"+str(tNome)+"slcc"
			info = unpack(fmt,linha)
			if int(info[0]) == indice:
				if info[5] != '*':
					return array.array('b',linha)[4]
		return -1

def filhoEsquerda(i):
	return (2 * i) + 1

def filhoDireita(i):
	return 	(2 * i) + 2

def pai(i):
	return i / 2
		
def tentarInsercao(arquivo,chave):
	tree = []
	ftm = "hh"
	data = pack(ftm,hashFirst(chave),buscaChave(arquivo,hashFirst(chave)))
	tree.append(data)
	i = 0
	if unpack("hh",tree[pai(i)])[1] == -1:
		print str(unpack("hh",tree[pai(i)])[0])+": "+"vazio"
	else:
		print str(unpack("hh",tree[pai(i)])[0])+": "+str(unpack("hh",tree[pai(i)])[1])

		while unpack("hh",tree[i])[1] != -1 :

			if (i > 1) and ((i%2) == 0):
				indice1 = hashFirst(hashSecond(unpack("hh",tree[pai(i) - 1])[1]) + unpack("hh",tree[i])[0]) 
				key = buscaChave(arquivo,indice1)
				data = pack("hh",indice1,key)
				tree.append(data)			
			else:		
				indice1 = hashFirst(hashSecond(chave) + unpack("hh",tree[i])[0]) 
				key = buscaChave(arquivo,indice1)
				data = pack("hh",indice1,key)
				tree.append(data)

			if (unpack("hh",tree[filhoEsquerda(i)])[1] != -1) :
				print str(unpack("hh",tree[filhoEsquerda(i)])[0])+": "+str(unpack("hh",tree[filhoEsquerda(i)])[1])
			else:
				print str(unpack("hh",tree[filhoEsquerda(i)])[0])+": "+"vazio"
				break

			indice2 = hashFirst(hashSecond(unpack("hh",tree[i])[1]) + unpack("hh",tree[i])[0])
			key = buscaChave(arquivo,indice2)
			data = pack("hh",indice2,key)
			tree.append(data)

			if (unpack("hh",tree[filhoDireita(i)])[1] != -1) :
				print str(unpack("hh",tree[filhoDireita(i)])[0])+": "+str(unpack("hh",tree[filhoDireita(i)])[1])
			else:
				print str(unpack("hh",tree[filhoDireita(i)])[0])+": "+"vazio"
				break
			i = i + 1

def resolverColisao(arquivo,pessoa):
	tree = []
	ftm = "fhh"+str(len(pessoa.nome))+"slcc"
	data = pack(ftm,hashFirst(pessoa.chave),pessoa.chave,len(pessoa.nome),pessoa.nome,pessoa.idade,"","\n")
	tree.append(data)
	i = 0
	while unpack("fhh"+str(len( array.array('b',tree[i])[6]))+"slcc",tree[i])[1] != -1 :
		if (i > 1) and ((i%2) == 0):
			indice1 = hashFirst(hashSecond(unpack("fhh"+str(len( array.array('b',tree[pai(i)])[6]))+"slcc",tree[pai(i) - 1])[1]) + unpack("fhh"+str(len( array.array('b',tree[i])[6]))+"slcc",tree[i])[0]) 
			pess = buscaPessoa(arquivo,indice1)
			data = pack("fhh"+str(len(pess.nome))+"slcc",indice1,pess.chave,len(pess.nome),pess.nome,pess.idade," ","\n")
			tree.append(data)
		
		else:		
			indice1 = hashFirst(hashSecond(pessoa.chave) + unpack("fhh"+str(len( array.array('b',tree[i])[6]))+"slcc",tree[i])[0]) 
			pess = buscaChave(arquivo,indice1)
			data = pack("fhh"+str(len(pess.nome))+"slcc",indice1,pess.chave,len(pess.nome),pess.nome,pess.idade," ","\n")
			tree.append(data)
		
		
		if (unpack("fhh"+str(len( array.array('b',tree[filhoEsquerda(i)])[6]))+"slcc",tree[filhoEsquerda(i)])[1] != -1) and (unpack("fhh"+str(len( array.array('b',tree[filhoEsquerda(i)])[6]))+"slcc",tree[filhoEsquerda(i)])[5] != '*' ):
			# print str(unpack("hh",tree[filhoEsquerda(i)])[0])+": "+str(unpack("hh",tree[filhoEsquerda(i)])[1])
			continue
		else:
			# print str(unpack("hh",tree[filhoEsquerda(i)])[0])+": "+"vazio"
			addArquivo(arquivo,indice1,pess)
			break

		indice2 = hashFirst(hashSecond("fhh"+str(len( array.array('b',tree[i])[6]))+"slcc",tree[i])[1]) + unpack("fhh"+str(len( array.array('b',tree[i])[6]))+"slcc",tree[i])[0]
		data = pack("fhh"+str(len(pess.nome))+"slcc",indice1,pess.chave,len(pess.nome),pess.nome,pess.idade," ","\n")
		tree.append(data)
	
		if (unpack("fhh"+str(len( array.array('b',tree[filhoEsquerda(i)])[6]))+"slcc",tree[filhoDireita(i)])[1] != -1) and (unpack("fhh"+str(len( array.array('b',tree[filhoDireita(i)])[6]))+"slcc",tree[filhoDireita(i)])[5] != '*' ):
			# print str(unpack("hh",tree[filhoDireita(i)])[0])+": "+str(unpack("hh",tree[filhoDireita(i)])[1])
			continue
		else:
			# print str(unpack("hh",tree[filhoDireita(i)])[0])+": "+"vazio"
			addArquivo(arquivo,indice2,pess)
			break
		i = i + 1


# Nao foi implementando a media

# def mediaAcesso(arquivo):
# 	arq = open(arquivo,"rb")
# 	valores = arq.readlines)()
# 	acesso = 0
# 	for indice in range(TAMANHO_ARQUIVO):
# 		chave = buscaChave(arquivo,indice)
# 		if chave != -1:
# 			if(hashFirst(chave) == indice):
# 				acesso = acesso + 1
# 			else:

# 				while :
# 					pass


