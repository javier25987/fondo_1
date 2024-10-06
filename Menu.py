import json
import streamlit as st
import datetime
import os
import funciones.general as Funciones

st.set_page_config(layout="wide")

with open('ajustes.json', 'r') as j_a:
    ajustes = json.load(j_a)
    j_a.close()

st.session_state['preguntar clave'] = True

st.session_state.valor_de_la_multa = ajustes['valor multa']
st.session_state.valor_de_la_cuota = ajustes['valor cuota']
st.session_state.interes_menos_20M = ajustes['interes < tope']
st.session_state.interes_mas_20M = ajustes['interes > tope']
st.session_state.clave_de_acceso = ajustes['clave de acceso']
st.session_state.tope = ajustes['tope de intereses']
st.session_state.usuarios = ajustes['usuarios']
st.session_state.anular_usuarios = ajustes['anular usuarios']
st.session_state.cobrar_multas = ajustes['cobrar multas']
st.session_state.nombre_df = ajustes['nombre df']
st.session_state.modificacion_avanzada = False

st.session_state.nombre_para_busqueda = ''

st.session_state.usuario_actual_cuotas = -1
st.session_state.usuario_actual_prestamos = -1
st.session_state.usuario_actual_ver = -1
st.session_state.usuario_actual_rifas = -1

st.title('Menu de inicio')

tab_1, tab_2 = st.tabs(
    ['Que es el menu?', 'funciones extra']
)

with tab_1:
    c_1, c_2 = st.columns([2, 3])

    with c_1:
        st.header('Guardar tabla')
        st.divider()
        if st.button('📤 Guardar en GitHub'):
            with st.status("Guardando cambios...", expanded=True) as status:
                os.chdir(ajustes['path programa'])

                st.write('Subiendo archivos...')
                Funciones.ejecutar_comando_git(["git", "add", "."])

                st.write('Guardando cambios...')
                ahora = datetime.datetime.now()
                fecha_hora_str = ahora.strftime("%Y-%m-%d_%H:%M:%S")
                ajustes['commits hechos'] += 1
                mensaje_de_comit = f'{str(ajustes['commits hechos'])}_{fecha_hora_str}'
                Funciones.ejecutar_comando_git(["git", "commit", "-m", mensaje_de_comit])
                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.write('Guardando en GitHub...')
                Funciones.ejecutar_comando_git(
                    ["git", "push"]
                )
                status.update(
                    label="Los datos han sido cargados!",
                    state="complete",
                    expanded=False
                )

        st.link_button('🔗 Abrir GitHub', ajustes['enlace repo'])

    with c_2:
        st.header('Que es el menu?')
        st.text(
            '''
            El menu es la parte de el programa dedicada a cargar los
            datos necesarios para la cache y para el funcionamiento 
            de el programa de esta menera el programa puede funcionar
            por eso es recomendable volver a el menu despues de crear 
            cualuier archivo de control o almacenamiento, tambien en 
            este apartado se puede encontrar informacion sobre el 
            programa como videos de youtube y puede subir a la nuve 
            la tabla de datos actual.
            '''
        )

with tab_2:
    st.write("Cargar multas para todos los usuarios.")

    if st.button("Cargar Multas"):
        Funciones.arreglar_todos_los_asuntos()
        st.success(
            "Proceso finalizado, todas las multas han sido cargadas.",
            icon="✅"
        )
