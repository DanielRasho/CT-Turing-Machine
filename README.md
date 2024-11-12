# 🤖Turing Machine

Este proyecto implementa una maquina de turing monocinta, que puede ser configurada por medio de archivos .yaml

[⭕ **VIDEO DEMO**]()

## 🚀 Getting Started

1. **Descargar Dependencias**: si planeas hacer un ambiente virtual hazlo primero antes de instalar las dependencias.

```bash
pip install -r requirements.txt
```

2. **Crear un archivo de configuracion**: debe tener la siguiente estructura
   
   ```yaml
    # turing_machine_config.yaml
   
    # States
    q_states:
      q_list:
        - q0
        - q1
        - q2
      initial: q0
      final: q1
      reject: q2
   
    # Alphabets
    alphabet:
      - 'a'
      - 'b'
      - 'c'
    tape_alphabet:
      - 'a'
      - 'b'
      - 'c'
      - 'B'
   
    # Transition Function
    delta:
      - params:
          initial_state: q0
          tape_input: 'a'
        output:
          final_state: q1
          tape_output: 'a'
          tape_displacement: R
      - params:
          initial_state: q0
          tape_input: 'b'
        output:
          final_state: q5
          tape_output: 'b'
          tape_displacement: R
    # Simulation
    posHead: 0 # initial head's position
    simulation_strings:
      - 'aaabbb' # Accepted
   ```

3. Ahora puedes correr el proyecto tan simple como:
   
   ```bash
   streamlit run ./src/main.py
   ```
