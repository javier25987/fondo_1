import json

import streamlit as st
import pandas as pd
import Funciones

st.set_page_config(layout="wide")

st.session_state['preguntar clave'] = True

df = pd.read_csv(st.session_state.nombre_df)

index = st.session_state.usuario_actual_ver

index_de_usuario = st.sidebar.number_input('Numero de usuario.', value=0, step=1)

if st.sidebar.button('Buscar', key='00011'):
    if 0 <= index_de_usuario < st.session_state.usuarios:
        if df['estado'][index_de_usuario] == 'activo':
            Funciones.arreglar_prestamos(index=index_de_usuario)
            st.session_state.usuario_actual_ver = index_de_usuario
            st.rerun()
        else:
            st.error(f'El usuario № {index_de_usuario} no esta activo.', icon="🚨")
    else:
        st.error('El numero de usuario esta fuera de rango.', icon="🚨")

tab_1, tab_2, tab_3, tab_4, tab_5, tab_6 = st.tabs([
    'Buscar socios', 'Anotaciones', 'Ver si necesita acuerdo', 'Buscar boleta',
    'Tabla de socios', "Archivo de ajustes"
])

with tab_1:
    c_1, c_2 = st.columns(2, vertical_alignment="bottom")

    with c_1:
        nombre_a_buscar = st.text_input('Nombre')

    with c_2:
        if st.button('Buscar'):
            st.session_state.nombre_para_busqueda = nombre_a_buscar
            st.rerun()

    st.divider()

    if st.session_state.nombre_para_busqueda == '':
        st.table(df[['numero', 'nombre','puestos', 'numero_telefonico', 'estado', 'capital']])
    else:
        nuevo_data_frame = df[df['nombre'].str.contains(nombre_a_buscar, case=False, na=False)]
        st.table(nuevo_data_frame[[
            'numero', 'nombre', 'puestos', 'numero_telefonico', 'estado', 'capital'
        ]])

with tab_2:
    if index == -1:
        st.title('Usuario indeterminado')
    else:
        st.title(f'№ {index} - {df['nombre'][index].title()}')
        st.header(f'Multas extra: {'{:,}'.format(df['multas_extra'][index])}')
        st.divider()

        col_1, col_2 = st.columns(2)
        with col_1:
            n_anotacion = st.text_input('Nueva anotacion.')

        with col_2:
            n_monto_a_multas = st.number_input('Monto a sumar a multas', value=0, step=1)

        if st.button('Hacer nueva anotacion'):
            if n_monto_a_multas >= 0:
                if '-' in n_anotacion:
                    st.error('El simbolo "-" no puede estar incluido en la anotacion',
                             icon="🚨")
                else:
                    anotacion_h = df['anotaciones'][index]
                    if anotacion_h == '-':
                        anotacion_h = f'{n_anotacion} ~> {'{:,}'.format(n_monto_a_multas)}'
                    else:
                        anotacion_h += f'-{n_anotacion} ~> {'{:,}'.format(n_monto_a_multas)}'
                    df.loc[index, 'anotaciones'] = anotacion_h

                    multas_extra = int(df['multas_extra'][index])
                    multas_extra += n_monto_a_multas
                    df.loc[index, 'multas_extra'] = multas_extra

                    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                    df.to_csv(st.session_state.nombre_df)
                    st.rerun()
            else:
                st.error('El monto no puede ser negativo.', icon="🚨")
        st.divider()

        anotaciones = df['anotaciones'][index].split('-')

        for i in anotaciones:
            st.write(i)
            st.divider()

with tab_3:
    tabla_acuerdo = df[df['dinero por si mismo'] < df['capital']//2]
    st.info(
        """
        Los siguientes usuarios no han retirado en prestamos la mitad de su capital
        """
    , icon="ℹ️")
    st.table(tabla_acuerdo[[
        'numero', 'nombre', 'capital', 'dinero por si mismo', 'numero_telefonico'
    ]])

with tab_4:
    rifa_a_buscar = st.selectbox('Seleccione la rifa en la que desea buscar.', (
        '1', '2', '3', '4'
    ))
    boleta_a_buscar = st.text_input('Selecciones la boleta que desea buscar,')

    if st.button('Buscar', key='00010'):
        tabla_boletas = df[
            df[f'r{rifa_a_buscar} boletas'].str.contains(
                boleta_a_buscar, case=False, na=False
            )
        ]
    else:
        tabla_boletas = df

    st.divider()
    st.table(tabla_boletas[['numero', 'nombre', f'r{rifa_a_buscar} boletas']])

with tab_5:
    st.table(df)

with tab_6:
    with open("ajustes.json", "r") as f:
        ajustes = json.load(f)
        f.close()

    ajustes["clave de acceso"] = "********"

    st.json(ajustes)