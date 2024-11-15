import os
from graphviz import Digraph
class TM:
    """
    Clase para simular una Máquina de Turing determinista.
    
    Parámetros:
        estados (list): Lista de estados de la máquina.
        alfabetoEntrada (list): Lista de símbolos del alfabeto de entrada.
        alfabetoCinta (list): Lista de símbolos del alfabeto de la cinta.
        q0 (str): Estado inicial.
        aceptacion (str): Estado de aceptación.
        rechazo (str): Estado de rechazo.
        transiciones (dict): Diccionario de transiciones con formato 
            {estado: {cache : {simbolo: [siguiente_estado, nuevo_cache, simbolo_escrito, direccion]}}}.

    Ejemplo de configuración:
        estados = ['q0', 'q1', 'q2', 'q3', 'q4']
        alfabetoEntrada = ['0', '1']
        alfabetoCinta = ['0', '1', 'B']
        q0 = 'q0'
        aceptacion = 'q4'
        rechazo = 'q3'
        transiciones = {
            'q0': {
                '0': {
                    '0': ['q1', '1' '0', 'R'],
                    '1': ['q3', '0' 1', 'R']},
                'B': {
                    '0': ['q1', 'B', '0', 'R'],
                    '1': ['q3', 'B', '1', 'R']},
            } 
            'q1': {
                '1': {
                    '0': ['q1', 'B', 0', 'R'], 
                    '1': ['q2', 'B', '1', 'R']}
                'B': {
                    '0': ['q1', 'B', '0', 'R'], 
                    '1': ['q2', 'B', '1', 'R']}
            }
        }
    """

    def __init__(self,  lector):
        self.estados = lector.estados
        self.alfabetoEntrada = lector.alfabetoEntrada
        self.alfabetoCinta = lector.tape_alphabet
        self.q0 = lector.q0
        self.aceptacion = lector.aceptacion
        self.rechazo = lector.rechazo
        self.transiciones = lector.transiciones
        self.size_cinta = 8
        self.cinta = []
        self.posCabezal = lector.posCabezal
        self.historial = []

    def isValidString(self, cadena):
        """Valida si la cadena pertenece al alfabeto de entrada de la máquina."""
        return all(symbol in self.alfabetoEntrada for symbol in cadena)

    def isValidTransitions(self):
        """Valida si las transiciones cumplen con el alfabeto de la cinta y estados definidos."""
        for estado, estados_cache in self.transiciones.items():
            if estado not in self.estados:
                return False
            for simbolo_cache, transiciones in estados_cache.items():
                if simbolo_cache not in self.alfabetoCinta:
                    # print(f"cache invalido: {simbolo_cache}")
                    return False
                for simbolo_entrada, (siguiente_estado, siguiente_cache, siguiente_letra, _, _) in transiciones.items():
                   #print(simbolo_entrada)
                    if siguiente_estado not in self.estados:
                        # print("siguiente estado invalido")
                        return False
                    if simbolo_entrada not in self.alfabetoCinta:
                        # print("simbolo entrada invalido")
                        return False
                    if siguiente_cache not in self.alfabetoCinta:
                        # print("siguiente cache invalido")
                        return False
                    if siguiente_letra not in self.alfabetoCinta:
                        # print("siguiente letra invalido")
                        return False
        return True
    
    def imprimir_tabla_transiciones(self):
        print(f"{'Estado':<10}{'Símbolo':<10}{'Siguiente Estado':<20}{'Símbolo Escrito':<20}{'Dirección'}")
        print("-" * 70)
        
        for estado in self.transiciones:
            for simbolo in self.transiciones[estado]:
                
                siguiente_estado, simbolo_escrito, direccion = self.transiciones[estado][simbolo]
                print(f"{estado:<10}{simbolo:<10}{siguiente_estado:<20}{simbolo_escrito:<20}{direccion}")
    
    def simulate(self, cadena, cintaConfiguration=[], positionCabezal=0):
        """
        Ejecuta la simulación de la máquina de Turing con la cadena de entrada.
        
        Args:
            cadena (str): La cadena de entrada a procesar.
            cintaConfiguration (list): Configuración inicial de la cinta.
            positionCabezal (int): Posición inicial del cabezal.
        
        Returns:
            result (str): Resultado de la simulación ('aceptado', 'rechazo' o 'bucle').
            historial (list): Registro paso a paso de la simulación.
        """
        if not self.isValidString(cadena):
            return "Error: Cadena contiene símbolos fuera del alfabeto de entrada.", []
        if not self.isValidTransitions():
            return "Error: Las transiciones son inválidas.", []
        
        result = ""
        estado_actual = self.q0
        cache = 'B' # Carácter para estado vacío

        self.historial = []  # Reiniciar historial en cada simulación
        isBucle = False  # Flag para controlar el bucle

        # Encabezado para la cadena actual
        self.historial.append(f"Descripciones instantáneas de cadena: {cadena}")
        
        # Usar la configuración de la cinta si se proporciona, de lo contrario, usa la cadena
        self.cinta = cintaConfiguration if cintaConfiguration else list(cadena) + ['B'] * (self.size_cinta - len(cadena))
        self.posCabezal = positionCabezal if cintaConfiguration else 0

        while not isBucle and (estado_actual != self.aceptacion and estado_actual != self.rechazo):
            simbolo_actual = self.cinta[self.posCabezal]
            cinta_formateada = (
                ''.join(self.cinta[:self.posCabezal]) +
                f"[{estado_actual}, '{cache}']{simbolo_actual}" +
                ''.join(self.cinta[self.posCabezal + 1:])
            )
            # self.historial.append(f"|- {cinta_formateada}")

            # Detectar bucle verificando si la transición no existe
            if simbolo_actual not in self.transiciones.get(estado_actual, {}).get(cache, {}):
                result = "bucle"
                self.historial.append(f"|- [{estado_actual}, '{cache}'] '{simbolo_actual}'- No tiene transición para [{simbolo_actual}], se detectó un bucle")
                isBucle = True
                continue

            # Obtener la transición y actualizar la cinta, estado y cabezal
            siguiente_estado, siguiente_cache, simbolo_escrito, direccion, num_transicion = self.transiciones[estado_actual][cache][simbolo_actual]
            
            # Registrar el paso con el número de transición
            self.historial.append(f"({num_transicion:<3}) |- {cinta_formateada}")

            self.cinta[self.posCabezal] = simbolo_escrito
            estado_actual = siguiente_estado
            cache = siguiente_cache

            # Cambiar posicion del cabezal
            if direccion == 'R':
                self.posCabezal += 1
            elif direccion == 'L':
                self.posCabezal -= 1
            elif direccion == 'S':
                pass
            else :
                self.historial.append(f"|- movimiento de cabezal invalido: {direccion}")
                isBucle = True
                continue

            # Asegurar que el cabezal no se salga de la cinta
            if self.posCabezal < 0:
                self.posCabezal = 0
            elif self.posCabezal >= len(self.cinta):
                self.cinta.append('B')

        # Determinar el resultado final si no es un bucle
        if estado_actual == self.aceptacion:
            result = "aceptado"
        elif estado_actual == self.rechazo:
            result = "rechazo"

        # Agregar la configuración final al historial si no hay bucle
        if result != "bucle":
            simbolo_actual = self.cinta[self.posCabezal]
            cinta_formateada = (
                ''.join(self.cinta[:self.posCabezal]) +
                f"[{estado_actual}, {simbolo_actual}]" +
                ''.join(self.cinta[self.posCabezal + 1:])
            )
            self.historial.append(f"|- {cinta_formateada}")

        # Añadir salto de línea al final de cada simulación
        self.historial.append("\n")
        return result, self.historial

    def writeInTXT(self):
        """Escribe el historial de la simulación en un archivo de texto con un formato específico."""
        with open('historial.txt', 'w') as f:
            for paso in self.historial:
                f.write(paso + '\n')

    def graph(self):
        """Genera un diagrama visual de la máquina de Turing usando Graphviz."""
        dot = Digraph(format='png', engine='dot')

        for estado in self.estados:
            if estado == self.aceptacion:
                dot.node(estado, shape='doublecircle', style='filled', color='lightgreen') 
            elif estado == self.rechazo:
                dot.node(estado, shape='doublecircle', style='filled', color='red') 
            else:
                dot.node(estado) 

        for estado in self.transiciones:
            for cache in self.transiciones[estado]:
                for simbolo in self.transiciones[estado][cache]:
                    siguiente_estado, siguiente_cache, simbolo_escrito, direccion, _ = self.transiciones[estado][cache][simbolo]
                    label = f'({simbolo}, {cache} / {simbolo_escrito}, {siguiente_cache} ,{direccion})'
                    dot.edge(estado, siguiente_estado, label=label)

        if not os.path.exists('graphs'):
            os.makedirs('graphs')

        # Guardar el archivo de imagen PNG
        file_path = 'graphs/maquina_turing'
        dot.render(file_path, view=False)

        print(f"Grafo de la máquina de Turing generado y guardado en {file_path}.png.")

