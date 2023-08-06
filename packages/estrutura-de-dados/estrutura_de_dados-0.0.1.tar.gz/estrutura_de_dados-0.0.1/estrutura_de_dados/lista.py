class Nodo:
    def __init__(self):
        self._valor = None
        self._proximoNodo = None
    
    @property
    def valor(self):
        return self._valor
    
    @valor.setter
    def valor(self, novoValor):
        self._valor = novoValor
    
    @property
    def proximoNodo(self):
        return self._proximoNodo
    
    @valor.setter
    def proximoNodo(self, novoProximoNodo):
        self._proximoNodo = novoProximoNodo
    
    def __str__(self):
        return str(self._valor)


class Lista:
    def __init__(self):
        self._inicio = None
        self._final = None
        self._tamanho = 0

    def inserirNoInicio(self, valor):
        novoNodo = Nodo()
        if novoNodo == None:
            return False
        
        novoNodo._valor = valor
        novoNodo._proximoNodo = self._inicio
        self._inicio = novoNodo
        if self._final == None:
            self._final = novoNodo
        self._tamanho += 1
        return True
    
    def inserirNoFinal(self, valor):
        novoNodo = Nodo()
        if novoNodo == None:
            return False
        
        novoNodo._valor = valor
        novoNodo._proximoNodo = None
        if self._inicio == None:
            self._inicio = novoNodo
        else:
            self._final._proximoNodo = novoNodo
        self._final = novoNodo
        self._tamanho += 1
        return True
    
    def inserirNaPosicao(self, valor,posicao):
        novoNodo = Nodo()
        if novoNodo == None:
            return False
        
        novoNodo._valor = valor
        novoNodo._proximoNodo = None

        if posicao == 0:
            novoNodo._proximoNodo = self._inicio
            self._inicio = novoNodo
            if self._final == None:
                self._final = novoNodo
            self._tamanho += 1
            return True
        
        else:
            anterior = self._inicio
            proximo = self._inicio._proximoNodo
            i = 1
            while proximo != None:
                if posicao == i:
                    novoNodo._proximoNodo = proximo
                    anterior._proximoNodo = novoNodo
                    self._tamanho += 1
                    return True
                else:
                    anterior = proximo
                    proximo = proximo._proximoNodo
                    i+=1
        return False

    def removerDoInicio(self):
        if self._inicio == None:
            return False

        aux = self._inicio
        self._inicio = aux._proximoNodo
        del aux
        if self._inicio == None:
            self._final =  None
        self._tamanho -= 1
        return True
    
    def removerDoFinal(self):
        if self._inicio == None:
            return False
        
        anterior = self._inicio
        proximo = self._inicio._proximoNodo
        i = 1
        while i != self._tamanho-1:
            anterior = proximo
            proximo = proximo._proximoNodo
            i+=1
        
        anterior._proximoNodo = proximo._proximoNodo
        del proximo
        self._tamanho -= 1
        return True
        
    
    def removerDaPosicao(self, posicao):
        if self._inicio == None:
            return False
        
        if posicao == 0:
            aux = self._inicio
            self._inicio = aux._proximoNodo
            del aux
            if self._inicio == None:
                self._final =  None
            self._tamanho -= 1
            return True
            
        else:
            anterior = self._inicio
            proximo = self._inicio._proximoNodo
            i = 1
            while proximo != None:
                if posicao == i:
                    anterior._proximoNodo = proximo._proximoNodo
                    if proximo._proximoNodo == None:
                        self._final = anterior
                    del proximo
                    self._tamanho -= 1
                    return True
                else:
                    anterior = proximo
                    proximo = proximo._proximoNodo
                    i+=1
        return False
    
    
    def mostrarLista(self):
        if self._inicio == None:
            print("A lista está vazia!")
            return False
            
        nodo = self._inicio
        while nodo != None:
            print(nodo.valor,end=" ")
            nodo = nodo._proximoNodo
        
        print("Final: "+str(self._final.valor))
    
    def consultarValor(self,valor):
        nodo = self._inicio
        while nodo != None:
            if nodo.valor == valor:
                return True
            nodo = nodo._proximoNodo
        return False

