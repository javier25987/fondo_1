import json
import time
import streamlit as st
import pandas as pd
import Funciones

st.set_page_config(layout="wide")

st.title('Modificar Socios')

if st.session_state['preguntar clave']:
    clave = st.text_input('Por favor introduzca la contraseña.')

    if st.button('Continuar'):
        if clave == st.session_state.clave_de_acceso:
            st.session_state['preguntar clave'] = False
            st.rerun()
        elif clave == '':
            st.error('La contraseña esta vacia', icon="🚨")
        else:
            st.error('La contraseña no es correcta', icon="🚨")

else:
    #st.info('Apesar de que el programa muestra que el proceso ya fue terminado se recomienda oprimir el boton dos veces'
    #       ',SOLO 2 VECES!!!', icon="ℹ️")

    with open('ajustes.json', 'r') as f:
        ajustes = json.load(f)
        f.close()

    st.session_state.usuarios = ajustes['usuarios']

    df = pd.read_csv(st.session_state.nombre_df)

    st.divider()

    st.table(df)

    tab_1, tab_2 = st.tabs(['Añadir socios', 'Modificar valores'])

    with tab_1:
        st.header('Añadir nuevo socio.')
        nuevo_usuario_nombre = st.text_input('Nombre.')
        nuevo_usuario_telefono = st.text_input('Numero telefonico.')
        nuevo_usuario_puestos = st.number_input('Numero de puestos.', value=0, step=1)
        paso_1 = False
        paso_2 = False

        if st.button('Añadir'):
            if nuevo_usuario_nombre == '':
                st.error('Me temo que el nombre esta vacio.', icon="🚨")
            else:
                paso_1 = True

            if nuevo_usuario_puestos < 1:
                st.error('No creo que sea util un usuario con puestos menores a 1.', icon="🚨")
            else:
                paso_2 = True

            if paso_1 and paso_2:
                Funciones.insertar_socios(
                    nombre=nuevo_usuario_nombre,
                    puestos=nuevo_usuario_puestos,
                    numero_telefonico=nuevo_usuario_telefono
                )
                st.balloons()
                #st.success('El usuario ha sido añadido.', icon="✅")
                st.toast('Nuevo socio añadido', icon='🎉')
                time.sleep(1.5)
                st.rerun()

    with tab_2:
        st.header('Modificar elementos:')

        index_row = st.number_input('Index de la fila.', value=0, step=1)

        columna_col = st.selectbox('Columna a modificar', (
            'nombre', 'numero_telefonico', 'cuotas', 'multas', 'tesorero', 'estado',
            'deudas en prestamos', 'intereses vencidos', 'revisiones de intereses',
            'intereses en prestamos', 'fiadores', 'deudas con fiadores',
            'fechas de pagos', 'fiador de', 'anotaciones', 'r1 boletas', 'r2 boletas',
            'r3 boletas', 'r4 boletas', 'puestos', 'revisiones', 'capital',
            'aporte_a_multas', 'deudas', 'multas_extra', 'prestamos hechos',
            'dinero en prestamos', 'dinero por si mismo', 'deudas por fiador',
            'r1 deudas', 'r2 deudas', 'r3 deudas', 'r4 deudas'
        ))

        st.subheader('Modificar texto.')

        nuevo_valor_texto = st.text_input('Nuevo valor de texto.')

        if st.button('Modificar texto'):
            if columna_col in [
                'nombre', 'numero_telefonico', 'cuotas', 'multas', 'tesorero', 'estado',
                'deudas en prestamos', 'intereses vencidos', 'revisiones de intereses',
                'intereses en prestamos', 'fiadores', 'deudas con fiadores',
                'fechas de pagos', 'fiador de', 'anotaciones', 'r1 boletas','r2 boletas',
                'r3 boletas','r4 boletas',
            ]:
                df.at[index_row, columna_col] = str(nuevo_valor_texto)
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                df.to_csv(st.session_state.nombre_df)
                st.success('Valor modificado', icon="✅")
                st.rerun()
            else:
                st.error('La columna a modificar es una columna de numeros', icon="🚨")

        st.subheader('Modificar numeros.')

        nuevo_valor_numero = st.number_input('Nuevo valor numerico.', value=0, step=1)

        if st.button('Modificar numero'):
            if columna_col in [
                'puestos', 'revisiones', 'capital', 'aporte_a_multas', 'deudas',
                'multas_extra', 'prestamos hechos', 'dinero en prestamos',
                'dinero por si mismo', 'deudas por fiador', 'r1 deudas', 'r2 deudas',
                'r3 deudas', 'r4 deudas'
            ]:
                df.at[index_row, columna_col] = nuevo_valor_numero
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                df.to_csv(st.session_state.nombre_df)
                st.success('Valor modificado', icon="✅")
                st.rerun()
            else:
                st.error('La columna a modificar es una columna de texto', icon="🚨")