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


class Fila:
    def __init__(self):
        self._inicio = None
        self._final = None
        self._tamanho = 0

    def inserir(self, valor):
        novoNodo = Nodo()
        if novoNodo == None:
            return False
        
        novoNodo._valor = valor
        novoNodo._proximoNodo = None
        if self._inicio == None:
            self._inicio = self._final = novoNodo
        else:
            self._final._proximoNodo = novoNodo
            self._final = novoNodo
        self._tamanho += 1
        return True
    
    def remover(self):
        if self._inicio == None:
            return False

        aux = self._inicio
        self._inicio = aux._proximoNodo
        del aux
        if self._inicio == None:
            self._final =  None
        self._tamanho -= 1
        return True
    
    def esvaziar(self):
        while self._tamanho > 0:
            self.remover()

    @property
    def primeiro(self):
        return self._inicio

    def __str__(self):
        return str(self._inicio)





