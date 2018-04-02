'''
Universidade Federal de Pernambuco (UFPE) (http://www.ufpe.br)
Centro de Informática (CIn) (http://www.cin.ufpe.br)
Graduando em Sistemas de Informação

Autor: Ricarth Ruan da Silva Lima (rrsl)
Email: rrsl@cin.ufpe.br
Data: 2018-04-02

Copyright(c) 2018 Ricarth Ruan da Silva Lima
'''

#1. Importações
import os

#2. Funções auxiliares para a classe Código
def padroniza(texto):
    novo = ""
    ind = 0
    try:
        while ind < len(texto):            
            if texto[ind+1]+texto[ind+2] in ["==","<=",">=","!=","//","**"]:
                novo = novo + texto[ind] + " " + texto[ind+1] + texto[ind+2] + " "
                ind = ind + 3
            elif texto[ind+1] in ["=","<",">","+","-","*","%","/","#"]:
                novo = novo + texto[ind] + " " + texto[ind+1] + " "
                ind = ind + 2
            else:
                novo = novo + texto[ind]
                ind = ind + 1
    except:
        novo = novo + texto[len(texto)-2:]

    return novo

def token(texto,seps=[" "]):
    lista = []
    palavra = ""
    for letra in texto:
        if letra in seps:
            if palavra != "":
                lista.append(palavra)
                palavra = ""
        else:
            palavra = palavra + letra

    if palavra != "":
        lista.append(palavra)

    return lista

def prepara(texto):
    texto = token(texto,["\n"])
    i = 0
    while i < len(texto):
        texto[i] = token(texto[i])
        i += 1
    return texto

#3. Classe onde um bloco de texto é interpretado
class Codigo():
    '''
    Recebe o código em texto puro e busca:
    - Variáveis
    - Linhas (inteiras)
    - Linhas limpas (sem variáveis)
    - Comentários
    - Números
    '''
    def __init__(self,texto):
        texto = prepara(padroniza(texto))
        
        self.__variaveis = []
        self.__linhas = texto[:]
        self.__linhasLimpas = []
        self.__comentarios = []
        self.__numeros = []        

        for linha in texto:
            for ind in range(len(linha)):
                try:
                    if linha[ind+1] == "=":
                        if (linha[ind] in self.__variaveis) == False:
                            self.__variaveis.append(linha[ind])

                    if linha[ind].isdigit():
                        self.__numeros.append(linha[ind])

                    if linha[ind] == "#":
                        self.__comentarios.append(linha[ind:])
                except:
                    pass

        for linha in texto:
            nova = []
            for palavra in linha:
                if palavra == "#":
                    break
                elif (palavra in self.__variaveis) == False:
                    nova.append(palavra)
            self.__linhasLimpas.append(nova)

    def getVar(self):
        return self.__variaveis

    def getLin(self):
        return self.__linhas

    def getLim(self):
        return self.__linhasLimpas

    def getCom(self):
        return self.__comentarios

    def getNum(self):
        return self.__numeros

#4. Funções auxiliares da função principal
def ocorrencias(lista1,lista2):
    cont = 0    
    for elem1 in lista1:
        achou = False
        i = 0
        while i < len(lista2) and achou == False:
            if elem1 == lista2[i]:
                cont = cont + 1
                achou = True
            i = i + 1
    return cont

def compara(cod1,cod2):
    #Variaveis iguais = 30%
    #Linhas iguais = 15%
    #Linhas limpas iguais = 25%
    #Comentarios iguais = 15%
    #Numeros iguais = 15%

    var = round((ocorrencias(cod1.getVar(),cod2.getVar()) / max(len(cod1.getVar()),len(cod2.getVar()),1))*100,2)
    lin = round((ocorrencias(cod1.getLin(),cod2.getLin()) / max(len(cod1.getLin()),len(cod2.getLin()),1))*100,2)
    lim = round((ocorrencias(cod1.getLim(),cod2.getLim()) / max(len(cod1.getLim()),len(cod2.getLim()),1))*100,2)
    com = round((ocorrencias(cod1.getCom(),cod2.getCom()) / max(len(cod1.getCom()),len(cod2.getCom()),1))*100,2)
    num = 0

    if len(cod1.getNum()) < len(cod2.getNum()):
        num1 = cod1.getNum()
        num2 = cod2.getNum()
    else:
        num1 = cod2.getNum()
        num2 = cod1.getNum()
    for ind in range(len(num1)):
        if num1[ind] == num2[ind]:
            num = num + 1

    num = round((num/max(len(num1),len(num2),1))*100,2)
    
    pts = round(var*0.3 + lin*0.15 + lim*0.25 + com*0.15 + num*0.15,2)
    
    return [var,lin,lim,com,num,pts]

def formata(lista):
    string = "-\t"
    for i in range(len(lista)-1):
        string = string + str(lista[i]) + "\t"
    return string + str(lista[len(lista)-1])

#Função Principal      
def main(limite):
    try:
        listaArq = os.listdir("arquivos")
    except:
        print("Pasta 'arquivos' não encontrada.")
        return 0
    listaCod = []
    fileErro = open('erros.txt','a')
    for arq in listaArq:
        try:
            file = open("arquivos/"+arq,encoding="utf8")
            texto = file.read()           
            file.close()
            listaCod.append((arq,Codigo(texto)))
        except:
            fileErro.write(arq+"\n")

    fileErro.close()

    media = 0
    total = 0

    i = 0
    while i < len(listaCod)-1:
        j = i + 1
        while j < len(listaCod):
            pts = compara(listaCod[i][1],listaCod[j][1])[5]
            media = media + pts
            if pts > limite and listaCod[i][0][:3]!=listaCod[j][0][:3]: #O segundo operando do AND verifica se a lista não pertence a mesma pessoa.
                print(formata(compara(listaCod[i][1],listaCod[j][1])),"\t",listaCod[i][0],"\t",listaCod[j][0])
            total = total + 1
            j = j + 1
        i = i + 1

    return round(media/total,2)

#Programa
limite = int(input("Digite o limite para observação: (0~100)\n"))
print("-\tVar\tLin\tLim\tCom\tNum\t% \tARQUIVO1 \tARQUIVO2") 
media = main(limite)
print("Média: "+str(media)+"%")
