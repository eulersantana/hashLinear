import unittest
from pessoa import Pessoa 
from struct import *
from funcoes import *

class testa_pessoa(unittest.TestCase):
	"Verifica se a instancia do object esta correta"
	def teste_pessoa(self):
		pessoa_teste = Pessoa(20,"Euler",23)
		self.assertEqual(pessoa_teste.chave,20)
		self.assertEqual(pessoa_teste.nome,"Euler")
		self.assertEqual(pessoa_teste.idade,23)
	
	# def testa_criarArquivo(self):
	# 	criarArquivo("dados")
		
	
	def test_mod(self):
		self.assertEqual(1,hashFirst(23))

	def test_addExtra(self):
		pessoa2 = Pessoa(27,"Vida",22)
		addArquivo("dados",hashFirst(pessoa2.chave),pessoa2)
		pessoa2 = Pessoa(39,"Vida",22)
		addArquivo("dados",hashFirst(pessoa2.chave),pessoa2)
		pessoa2 = Pessoa(18,"Vida",22)
		addArquivo("dados3",hashFirst(pessoa2.chave),pessoa2)
		
	def teste_addArquivo(self):
		pessoa = Pessoa(23,"Euler Satana",32)
		pessoa2 = Pessoa(18,"Vida",22)
		addArquivo("dados",hashFirst(pessoa2.chave),pessoa2)
		fmt = "fhh"+str(len(pessoa2.nome))+"slcc"
		arq = open("dados","r+b")
		valores = arq.readlines()
		valores.sort()
		valor = valores[2] 
		indice = unpack(fmt,valor)[0]
		chave = unpack(fmt,valor)[1]
		nome  = unpack(fmt,valor)[3]
		idade = unpack(fmt,valor)[4]
		self.assertEqual(hashFirst(chave), indice)
		self.assertEqual(chave, pessoa2.chave)
		self.assertEqual(nome,pessoa2.nome)
		self.assertEqual(idade,pessoa2.idade)
		arq.close()
	
	def teste_lenNome(self):
		pessoa2 = Pessoa(35,"jkjajdlfjlajfsdjfkdsjfljdsfldsjfkljsdlfjsdklfjdskljfldsfjdklsjfkldsjfkldsjfkljsdklfjsldkjflskjfljslfj",25)
		addArquivo("dados",hashFirst(pessoa2.chave),pessoa2)
		fmt = "hhh"+str(len(pessoa2.nome))+"slc"
		arq = open("dados","r+b")
		valores = arq.readlines()
		try:
			valor = valores[3] 
			indice = unpack(fmt,valor)[0]
			chave = unpack(fmt,valor)[1]
			nome  = unpack(fmt,valor)[3]
			idade = unpack(fmt,valor)[4]
			self.assertNotEqual(hashFirst(chave), indice)
			self.assertNotEqual(chave, pessoa2.chave)
			self.assertNotEqual(nome,pessoa2.nome)
			self.assertNotEqual(idade,pessoa2.idade)			
		except Exception, e:
			self.assertEqual(False,False)
			
		arq.close()


	"Verifica se o valor de cahve existe ou nao"
	def teste_verificaChave(self):
		self.assertEqual("chave: 18",vericarChave("dados",18))
		self.assertEqual("chave: 27",vericarChave("dados",27))
		self.assertEqual("chave nao encontrada: 50",vericarChave("dados",50))

	def teste_buscaPessoa(self):
		pessoa = buscaPessoa("dados",27)
		self.assertEqual(27,pessoa.chave)
		self.assertEqual("Vida",pessoa.nome)
		self.assertEqual(22,pessoa.idade)
		self.assertEqual(None,buscaPessoa("dados",100))

	def teste_remocao(self):		
		self.assertEqual("chave nao encontrada 11",remove("dados",11))

	def teste_imprimiArquivo(self):
		try:
			imprimiArquivo("dados")
			self.assertEqual(True,True)
		except Exception, e:
			self.assertEqual(True,False)
	
	def test_buscaChave(self):
		cahve = buscaChave("dados",5)
		cahve2 = buscaChave("dados",4)
		self.assertEqual(27,cahve)		
		self.assertNotEqual(15,cahve2)		




unittest.main()