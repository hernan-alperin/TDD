from componente import Componente, Manzana, Lado

class Componentes(list):

    """
    TODO:
    definir
    lo_mismo
    igual
    identico
    """

    def __str__(self):
        s = '['
        for c in self:
            s += str(c) + ', '
        return s[:-2] + ']'

    def ids(self):
        return set(c.c_id for c in self)

    def min_id(self):
        return min(self.ids())

    def clausura_conexa(self, este):
        # devuelve todos los Componentes alcanzables desde este usando adyacencias
        if este not in self:
            return Componentes() # vacio, caso seguro
        else:
            clausura = Componentes([este]) # contiene al menos a este
            i = 0
            while i < len(clausura): # i es el puntero lo que que falta expandir
                # i se incrementa de a 1 expandiendo de a 1 las adyacencias
                # hasta que la variable clausura no se expande más,
                # queda en un puntos fijo, i.e. es una clausura
                adyacentes_i = [ese for ese in clausura[i].adyacencias() if ese in self]
                # los adyacentes a la i-ésimo elemento de la clausura que están en la coleccion
                nuevos = Componentes([ese for ese in adyacentes_i if ese not in clausura]) # no agragados aún
                clausura.extend(nuevos) # se agregan al final las adyacencias no agregadas
                i = i + 1
            return Componentes(clausura).ordenado()

    def conectados(self):
        # True si desde el primero se puede llagar a todos los otros
        # a través de adyacencias
        return any([len(self.clausura_conexa(uno)) == len(self) for uno in self])

    def extraer_componente(self, este):
        # devuelve las partes de Componentes conexas originales resultado de remover la manzana m del segmento
        if este not in self:
            return []
        else:
            esos = Componentes(self) # copia para no modificar el original
            esos.remove(este)
            partes = Componentes()
            while esos: # es no vacia
                ese = esos[0] # se elige uno cualquiera, se usa el 1ro
                clausura_de_ese_en_esos = esos.clausura_conexa(ese)
                for aquel in clausura_de_ese_en_esos:
                    if aquel not in esos: # (?) cómo puede ser?????
                #        pass
                        raise Exception("elemento " + str(aquel) + " no está en " + str(esos)
                            + "\nclausura_de_ese_en_esos " + str(clausura_de_ese_en_esos))
                    else:  # para que no se rompa acá....
                        esos.remove(aquel) # en esos queda el resto no conexo a aquel
                partes.append(clausura_de_ese_en_esos)
            return Segmentos(partes).ordenados()

    def transferir_componente(self, este, esos):
        # transferir este del segmento origen al los Componentes esos
        # devuelve una lista con a lo sumo 2 elementos ... los nuevos estos y esos
        if este not in self: # no se puede transferir un elemento que no esté
            return False
        elif not Componentes([este] + esos).conectados(): # no se puede transferir si no es adyacente
            return False
        elif len(self) == 1: # no queda resto, se fusiona origen con destino
            return Segmentos([Componentes(esos + [este]).ordenado()])
        else:
            estos = self.extraer_componente(este)
            print(estos)
            aquellos = Componentes(esos + [este]).ordenado()
            return Segmentos(estos + [aquellos]).ordenados()

    def unir_componentes(self, esos):
    # fusión Componentes con esos si algun elemento es adyacente con otro de esos, o viceversa
        if Componentes(self + esos).conectados():
            return Componentes(self + esos)
        else:
            return False

    def segmentos(self):
        # todos los segmento posibles respetando adyacencias
        sgms = Segmentos()
        for c in self:
            sgms.append(Segmento([c]))
        cantidad = 0
        while cantidad < len(sgms):
        # no se incrementó la cantidad de segmentos
            cantidad = len(sgms)
            for s in sgms:
                for c in s:
                    for c_i in c.adyacentes:
                        if c_i in self and c_i not in s:
                            s_mas_c_i = Segmento(s)
                            s_mas_c_i.append(c_i)
                            s_mas_c_i.ordenar()
                            if s_mas_c_i not in sgms:
                                sgms.append(s_mas_c_i)
        return sgms

    def ordenar(self):
        self.sort(key=lambda x: x.c_id)
        return

    def ordenado(self):
        # devuelve una copia del segmento con sus componentes ordenados por id
        copia = Segmento(self)
        copia.sort(key=lambda x: x.c_id)
        return copia

    def recorridos(self,
        hasta=max(1.5*segmentacion_deseada, segmentacion_deseada + 4),
        desde=min(0.5*segmentacion_deseada, segmentacion_deseada - 4)):
        sgms = Segmentos()
        for c in self:
            sgms.append(Segmento([c]))
        cantidad = 0
        while cantidad < len(sgms):
            cantidad = len(sgms)
            for s in sgms:
                ultimo = s[-1] # con el último arma recorridos
                for c in ultimo.adyacentes:
                    if (c in self and c not in s
                        and c.vivs + s.costo() < hasta):
                        s_mas_c = Segmento(s)
                        s_mas_c.append(c)
                        if s_mas_c not in sgms:
                            sgms.append(s_mas_c)
        for s in sgms:
            if s.costo()<desde:
                sgms.remove(s)
            return Segmentos(sgms)

    def componentes(self):
        # devuelve los componentes ordenados
        return self

    def manzanas(self):
        return len(list(set([c.c_id/10 for c in self.componentes()])))

    def mejor_costo_teorico(self):
        return (1.1*abs(mod(sum(c.vivs for c in self) - (segmentacion_deseada/2),
                        segmentacion_deseada)
                    - (segmentacion_deseada/2)
                    )
                + 0.01*self.manzanas())

