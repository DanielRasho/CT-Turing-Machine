import streamlit as st
import yaml
from reader import Reader
from TM import TM

st.set_page_config(page_title="Simulador Maquina de Turing", page_icon="🧠")
st.title('Simulador de Maquina de Turing')
st.subheader('Instrucciones')
st.write("<p style='font-size:17px;'>Agregue el archivo de configuracion .yaml para evaluar la maquina de turing</p>", unsafe_allow_html=True)

with st.container():
    # Cargar archivo
    uploaded_file = st.file_uploader("Subir archivo de configuración", type=["yaml"])
    if uploaded_file is not None:
        st.write("Archivo cargado exitosamente:")
        try:
            content = yaml.safe_load(uploaded_file)
            lector = Reader(content=content)
            maquina = TM(lector=lector)

            all_histories = ""
            for idx, cadena in enumerate(lector.cintas, start=1):
                result, historial = maquina.simulate(cadena)
                re = f"De la cadena \"{cadena}\" se llegó al estado de: \"{result}\""
                
                st.subheader(f'Resultado de la cadena {idx}')
                if result == "rechazo":
                    st.error(re)
                elif result == "aceptado":
                    st.success(re)
                else:
                    st.warning(re)
                
                pasos = ""
                pasos_show = ""
                for p in historial:
                    pasos += f'{p}<br>'
                    pasos_show += f'{p}\n'
                
                st.subheader(f'Configuraciones de la cinta para la cadena {idx}')
                st.write(f"<span style='font-size:20px; font-style:italic;'>{pasos}</span>", unsafe_allow_html=True)
                
                # Concatenar historial para el archivo de descarga
                all_histories += pasos_show + "\n"
            
            st.subheader('Diagrama de la Maquina de Turing')
            maquina.graph()
            st.image('./graphs/maquina_turing.png')

            # Botón para descargar el archivo de historial completo
            st.download_button(
                label="Descargar archivo de configuraciones",
                data=all_histories,
                file_name="configuraciones_TM.txt",
                mime="text/plain"
            )
        
        except yaml.YAMLError as e:
            st.error(f"Error al leer el archivo YAML: {e}")
