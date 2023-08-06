class Nodo:
    def __init__(self):
        self._valor = None
        self._nodoAnterior = None
    
    @property
    def valor(self):
        return self._valor
    
    @valor.setter
    def valor(self, novoValor):
        self._valor = novoValor
    
    @property
    def nodoAnterior(self):
        return self._nodoAnterior
    
    @valor.setter
    def nodoAnterior(self, novoNodoAnterior):
        self._nodoAnterior = novoNodoAnterior
    
    def __str__(self):
        return str(self._valor)


class Pilha:
    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def empilhar(self, valor):
        novoNodo = Nodo()
        if novoNodo == None:
            return False
        
        novoNodo._valor = valor
        novoNodo._nodoAnterior = self.topo
        self._topo = novoNodo
        self._tamanho += 1
        return True
    
    def desempilhar(self):
        if self._topo == None:
            return False

        valor = self._topo.valor
        aux = self._topo
        self._topo = self._topo._nodoAnterior
        self._tamanho -= 1
        del aux
        return valor

    @property
    def topo(self):
        return self._topo

    def __str__(self):
        return str(self.topo)

