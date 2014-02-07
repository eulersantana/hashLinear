import os, array
from struct import *
import operator
# Numero de paginas iniciais
N = 2
REGISTRO_POR_PAGINA = 3
arqInfo = "fileInfo"

class Pessoa:
	def __init__(self,chave,nome,idade):
		self.chave 	= chave
		self.nome 	= nome
		self.idade	= idade


# #####################################################################################################################
# Funcao de calculo do hash
def hashing(chave,nivel):
	return chave % (N * 2**nivel)

#Insercao  com split
def addArquivo(arquivo,indice,pessoa):
	if os.path.exists(arquivo):
		mode = "ab+"
		arq = open(arquivo,mode)
	else:
		mode = "w+b"
		arq = open(arquivo,mode)
	
	if vericarChave(arquivo,pessoa.chave) != "chave: "+str(pessoa.chave) and len(pessoa.nome) <= 20:
		fmt = "fhh"+str(len(pessoa.nome))+"sl3sc"
		if qtdElementoPorPagina(arquivo,indice) >= REGISTRO_POR_PAGINA and lerInfo()[0] != indice :
			dados = pack(fmt,indice,pessoa.chave,len(pessoa.nome),pessoa.nome,pessoa.idade,str(indice)+"-1","\n")
			arq.write(dados)
			arq.close()
			info = lerInfo()
			qtdOverFlow(arquivo)
		else:
			dados = pack(fmt,indice,pessoa.chave,len(pessoa.nome),pessoa.nome,pessoa.idade,str(indice)+"-0","\n")
			arq.write(dados)
			arq.close()		
		split(arquivo)
	else: print "chave ja existente: "+str(pessoa.chave)

#Insercao sem com split
def addArquivoS(arquivo,indice,pessoa):
	if os.path.exists(arquivo):
		mode = "ab+"
		arq = open(arquivo,mode)
	else:
		mode = "w+b"
		arq = open(arquivo,mode)
	
	if vericarChave(arquivo,pessoa.chave) != "chave: "+str(pessoa.chave) and len(pessoa.nome) <= 20:
		fmt = "fhh"+str(len(pessoa.nome))+"sl3sc"
		if qtdElementoPorPagina(arquivo,indice) >= REGISTRO_POR_PAGINA :
			dados = pack(fmt,indice,pessoa.chave,len(pessoa.nome),pessoa.nome,pessoa.idade,str(indice)+"-1","\n")
			arq.write(dados)
			arq.close()
			info = lerInfo()
			qtdOverFlow(arquivo)
		else:
			dados = pack(fmt,indice,pessoa.chave,len(pessoa.nome),pessoa.nome,pessoa.idade,str(indice)+"-0","\n")
			arq.write(dados)
			arq.close()
		arq.close()


def addInfo(next,nivelAtual,totalSplit):
	mode = "w+b"
	arq = open(arqInfo,mode)
	# posicao atual no next e o nivel atual
	fmt = "hhh"
	dados = pack(fmt,next,nivelAtual,totalSplit)
	arq.write(dados);
	arq.close()	

def lerInfo():
	mode = "r+b"
	arq = open(arqInfo,mode)
	dados = arq.readline()
	fmt = "hhh"
	valores = unpack(fmt,dados)
	arq.close()
	return valores	

def pegarPagina(arquivo,indice):
	arq = open(arquivo,"r+b")
	valores = arq.readlines()
	valores.sort()
	pagina = []
	for linha in valores:
		tNome = array.array('b',linha)[6]
		fmt = "fhh"+str(tNome)+"sl3sc"
		info = unpack(fmt,linha)
		if indice == info[0]:
			pagina.append(Pessoa(info[1],info[3],info[4]))	
	return pagina

def split(arquivo):
	info = lerInfo()
	if ocupacao(arquivo,info[1]) >= 0.8:
		print str(ocupacao(arquivo,info[1]))+"\n"
		print str(info[2])+"\n"
		valores = pegarPagina(arquivo,info[0])
		proxNivel = info[1] + 1
		for pes in valores:
			remover(arquivo,pes.chave)
		for pessoa in valores:
			addArquivoS(arquivo,hashing(pessoa.chave,proxNivel),pessoa)
		if (info[0]+1) == N * 2**info[1]:
			addInfo(0,info[1]+1,0)
		else:
			addInfo(info[0] + 1 ,info[1],info[2]+1)	

def unSplit(arquivo):
	info = lerInfo()
	if ocupacao(arquivo,info[1]) <= 0.4:
		valores = pegarPagina(arquivo,info[0])
		proxNivel = info[1] + 1
		for pes in valores:
			remover(arquivo,pes.chave)
		for pessoa in valores:
			addArquivoS(arquivo,hashing(pessoa.chave,proxNivel),pessoa)
		if (info[0]+1) == N * 2**info[1]:
			addInfo(0,info[1]+1,0)
		else:
			addInfo(info[0] + 1 ,info[1],info[2]+1)	

# precisa conta a se houver paginas extra.
def ocupacao(arquivo,nivel):
	arq = open(arquivo,"r+b")
	info = lerInfo()
	valores = arq.readlines() 
	arq.close()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
	total = (REGISTRO_POR_PAGINA * (N * 2**nivel)) + (REGISTRO_POR_PAGINA * info[2])
	return round(float(len(valores))/float(total),2)

def qtdElementoPorPagina(arquivo,indice):
	arq = open(arquivo,"r+b")
	valores = arq.readlines()
	valores.sort()
	cont = 0
	for linha in valores:
		tNome = array.array('b',linha)[6]
		fmt = "fhh"+str(tNome)+"sl3sc"
		info = unpack(fmt,linha)
		if indice == info[0]:
			cont = cont + 1	
	return cont

def imprimiIndice(arquivo):
	print "nivel: "+str(lerInfo()[1])
	print "next: "+str(lerInfo()[0])
	arq = open(arquivo,"r+b")
	valores = arq.readlines()
	qtdElem = N*(2**lerInfo()[1])
	for ind in range(0,qtdElem):
		print "pagina: "+str(ind)
		imprimiPaginas(arquivo,ind)
		print "----------"		
	arq.close()

def imprimiPaginas(arquivo,indice):
	arq = open(arquivo,"r+b")
	valores = arq.readlines()
	for linha in valores:
		tNome = array.array('b',linha)[6]
		fmt = "fhh"+str(tNome)+"sl3sc"
		info = unpack(fmt,linha)

		if str(int(info[0])) == str(indice):
			print "chave: "+str(info[1])+" nome: "+str(info[3])+" idade: "+str(info[4])+" "+str(info[6])
	arq.close()	

def qtdOverFlow(arquivo):
	arq = open(arquivo,"r+b")
	info = lerInfo();
	numPaginas = N * 2**(info[1]+1)
	cont = 0
	valores = arq.readlines()
	
	for indice in range(0,numPaginas):
		print "qunatidade valores:"+str(indice)+" "+str(len(valores))
		for linha in valores:
			tNome = array.array('b',linha)[6]
			fmt = "fhh"+str(tNome)+"sl3sc"
			infoArq = unpack(fmt,linha)
			# print str(int(infoArq[0]))+"--"+str(indice)
			if str(int(infoArq[0])) == str(indice):
				if str(infoArq[5])[2] == '1':
					cont = cont + 1
					break

	addInfo(info[0],info[1],cont)	
	arq.close()
	return cont			
	

def remover(arquivo,chave):
	if os.path.exists(arquivo):
		arq = open(arquivo,"rb+")
		valores = arq.readlines()
		valores.sort()
		for linha in valores:
			tNome = array.array('b',linha)[6]
			fmt = "fhh"+str(tNome)+"sl3sc"
			info = unpack(fmt,linha)
			if info[1] == chave:
				valores.remove(linha)
				arq.close()
				arq = open(arquivo,"w+b")
				for linha2 in valores:
					arq.write(linha2)
				arq.close()
				return ""
		return "chave nao encontrada: "+str(chave)
def buscaPessoa(arquivo,chave):
	if os.path.exists(arquivo):
		arq = open(arquivo,"rb")
		valores = arq.readlines()
			
		for linha in valores:
			tNome = array.array('b',linha)[6]
			chaveaux = array.array('b',linha)[4]
			if chaveaux == chave:
				fmt = "fhh"+str(tNome)+"sl3sc"
				info = unpack(fmt,linha)
				arq.close()
				return Pessoa(info[1],info[3],info[4]) 
	arq.close()
	return None	

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

def media(arquivo):
	mode = "rb"
	arq = open(arquivo, mode)
	valores = arq.readlines()
	info = lerInfo()
	nivel = lerInfo()[1]
	return round(float(len(valores))/float((REGISTRO_POR_PAGINA * (N * 2**nivel)) + (REGISTRO_POR_PAGINA * info[2])),1)



# #####################################################################################################################

