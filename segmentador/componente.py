class Componente:
    # elemento unitario o indivisible para el caso de segmentación
    # puede ser un lado o una manzana

    def __init__(self, c_id, vivs=0, longitud=0):
        self.adyacentes = []
        self.c_id = c_id
        self.vivs = vivs
        self.longitud = longitud

    def __str__(self):
        return str((self.c_id, self.vivs))

    def agregar_adyacencia(self, ady):
        self.adyacentes.append(ady)

    def adyacencias(self):
        return self.adyacentes

    def get_type(self):
        pass

