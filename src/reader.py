class Reader(object):
    def __init__(self, content):
        self.tm_machine = content
        self.estados = []
        self.alfabeto = []
        self.alfabetoEntrada = []
        self.tape_alphabet = []
        self.q0 = None
        self.aceptacion = None
        self.rechazo = None
        self.transiciones = {}
        self.cintas = []  # Almacena todas las cadenas a simular
        self.posCabezal = None
        self.get_states_and_alphabets()
        self.get_create_Transitions()
    
    def get_states_and_alphabets(self):
        self.estados = self.tm_machine['q_states']['q_list']
        self.alfabeto = self.tm_machine['alphabet']
        self.alfabetoEntrada = self.alfabeto
        self.tape_alphabet = self.tm_machine['tape_alphabet'] + self.alfabeto + ['']
        self.q0 = self.tm_machine['q_states']['initial']
        self.aceptacion = self.tm_machine['q_states']['final']
        self.rechazo = self.tm_machine['q_states']['reject']
        self.posCabezal = self.tm_machine.get('posHead', 0)
        # Guarda todas las cadenas en una lista en lugar de solo la primera
        self.cintas = self.tm_machine['simulation_strings']
    
    def get_create_Transitions(self):
        transiciones = {}
        lista_params = self.tm_machine['delta']
        for l in lista_params:
            input_state = l['params']['initial_state']
            input_cache = l['params']['mem_cache_value']
            input_tape = l['params']['tape_input']
            if input_state not in transiciones.keys():  # crear diccionario estado si no existe.
                transiciones[input_state] = {}
            if input_cache not in transiciones[input_state].keys():  # crear diccionario cache si no existe.
                transiciones[input_state][input_cache] = {}
            if input_tape not in transiciones[input_state][input_cache].keys():  # Agregar configuracion de salida.
                transiciones[input_state][input_cache][input_tape] = [
                    l['output']['final_state'],
                    l['output']['mem_cache_value'],
                    l['output']['tape_output'],
                    l['output']['tape_displacement']
                ]
            else:  # Error, porque cada configuracion estado, cache, input solo puede tener UN output
                print('ERROR.')
        self.transiciones = transiciones
        # print(self.transiciones)
