import streamlit as st
import pandas as pd
import funciones.general as Funciones
import json

from funciones.general import crear_tablas_talonarios

st.set_page_config(layout="wide")

st.session_state['preguntar clave'] = True

df = pd.read_csv(st.session_state.nombre_df)

with open('ajustes.json', 'r') as f:
    ajustes = json.load(f)

index = st.session_state.usuario_actual_rifas

index_de_usuario = st.sidebar.number_input('Numero de usuario.', value=0, step=1)

if st.sidebar.button('Buscar'):
    if 0 <= index_de_usuario < st.session_state.usuarios:
        if df['estado'][index_de_usuario] == 'activo':
            st.session_state.usuario_actual_rifas = index_de_usuario
            st.rerun()
        else:
            st.error(f'El usuario № {index_de_usuario} no esta activo.', icon="🚨")
    else:
        st.error('El numero de usuario esta fuera de rango.', icon="🚨")

if index == -1:
    st.title('Usuario indeterminado')
else:
    st.title(f'№ {index} - {df['nombre'][index].title()}')

    tab_1, tab_2, tab_3, tab_4 = st.tabs(['Rifa 1', 'Rifa 2', 'Rifa 3', 'Rifa 4'])

    with tab_1:
        if ajustes["r1 estado"]:
            col1_1, col1_2 = st.columns(2)
            with col1_1:
                st.header('Entregar talonarios.')
                if st.button('Entregar un talonario', key='00035'):
                    st.balloons()
                    Funciones.cargar_talonario(
                        index=index, columnas=ajustes['r1 numeros por boleta'],
                        filas= ajustes['r1 boletas por talonario'], rifa='1'
                    )
            with col1_2:
                st.header('Deudas en boletas.')
                deuda_act_1 = df['r1 deudas'][index]
                st.write(f'Deudas en boletas: {'{:,}'.format(deuda_act_1)}')
                n_pago_1 = st.number_input('Pago en boletas.', step=1, value=0, key='00036')
                if st.button('Pagar boletas', key='00037'):
                    if deuda_act_1 <= 0:
                        st.error('No entiendo que desea pagar.', icon="🚨")
                    else:
                        if n_pago_1 > deuda_act_1:
                            st.error('No se puede pagar mas de lo que se debe.', icon="🚨")
                        elif n_pago_1 == 0:
                            st.error('No se puede pagar cero.', icon="🚨")
                        else:
                            st.balloons()
                            Funciones.pago_de_boletas(index=index, pago=n_pago_1, rifa='1')

            st.divider()

            st.header('Talonarios entregados:')
            boletas_r_1 = df['r1 boletas'][index]
            if boletas_r_1 == '-':
                st.subheader('🚨 No se han entregado talonarios,', key='00041')
            else:
                talonarios_r_1 = boletas_r_1.split('-')
                tablas_r_1 = crear_tablas_talonarios(boletas_r_1)
                for i in range(len(talonarios_r_1)):
                    st.subheader(f'Talonario {i + 1}:')
                    st.table(tablas_r_1[i])
        else:
            st.title('🚨 La rifa no esta activa. ')

    with tab_2:
        if ajustes["r2 estado"]:
            col2_1, col2_2 = st.columns(2)
            with col2_1:
                st.header('Entregar talonarios.')
                if st.button('Entregar un talonario', key='00042'):
                    st.balloons()
                    Funciones.cargar_talonario(
                        index=index, columnas=ajustes['r2 numeros por boleta'],
                        filas=ajustes['r2 boletas por talonario'], rifa='2'
                    )
            with col2_2:
                st.header('Deudas en boletas.')
                deuda_act_2 = df['r2 deudas'][index]
                st.write(f'Deudas en boletas: {'{:,}'.format(deuda_act_2)}')
                n_pago_2 = st.number_input('Pago en boletas.', step=1, value=0, key='00043')
                if st.button('Pagar boletas', key='00044'):
                    if deuda_act_2 <= 0:
                        st.error('No entiendo que desea pagar.', icon="🚨")
                    else:
                        if n_pago_2 > deuda_act_2:
                            st.error('No se puede pagar mas de lo que se debe.', icon="🚨")
                        elif n_pago_2 == 0:
                            st.error('No se puede pagar cero.', icon="🚨")
                        else:
                            st.balloons()
                            Funciones.pago_de_boletas(index=index, pago=n_pago_2, rifa='2')

            st.divider()

            st.header('Talonarios entregados:')
            boletas_r_2 = df['r2 boletas'][index]
            if boletas_r_2 == '-':
                st.subheader('🚨 No se han entregado talonarios,')
            else:
                talonarios_r_2 = boletas_r_2.split('-')
                tablas_r_2 = crear_tablas_talonarios(boletas_r_2)
                for i in range(len(talonarios_r_2)):
                    st.subheader(f'Talonario {i + 1}:')
                    st.table(tablas_r_2[i])
        else:
            st.title('🚨 La rifa no esta activa. ')

    with tab_3:
        if ajustes["r3 estado"]:
            col3_1, col3_2 = st.columns(2)
            with col3_1:
                st.header('Entregar talonarios.')
                if st.button('Entregar un talonario', key='00048'):
                    st.balloons()
                    Funciones.cargar_talonario(
                        index=index, columnas=ajustes['r3 numeros por boleta'],
                        filas=ajustes['r3 boletas por talonario'], rifa='3'
                    )
            with col3_2:
                st.header('Deudas en boletas.')
                deuda_act_3 = df['r3 deudas'][index]
                st.write(f'Deudas en boletas: {'{:,}'.format(deuda_act_3)}')
                n_pago_3 = st.number_input('Pago en boletas.', step=1, value=0, key='00049')
                if st.button('Pagar boletas', key='00050'):
                    if deuda_act_3 <= 0:
                        st.error('No entiendo que desea pagar.')
                    else:
                        if n_pago_3 > deuda_act_3:
                            st.error('No se puede pagar mas de lo que se debe.')
                        elif n_pago_3 == 0:
                            st.error('No se puede pagar cero.', icon="🚨")
                        else:
                            st.balloons()
                            Funciones.pago_de_boletas(index=index, pago=n_pago_3, rifa='3')

            st.divider()

            st.header('Talonarios entregados:')
            boletas_r_3 = df['r3 boletas'][index]
            if boletas_r_3 == '-':
                st.subheader('🚨 No se han entregado talonarios,')
            else:
                talonarios_r_3 = boletas_r_3.split('-')
                tablas_r_3 = crear_tablas_talonarios(boletas_r_3)
                for i in range(len(talonarios_r_3)):
                    st.subheader(f'Talonario {i + 1}:')
                    st.table(tablas_r_3[i])
        else:
            st.title('🚨 La rifa no esta activa. ')

    with tab_4:
        if ajustes["r4 estado"]:
            col4_1, col4_2 = st.columns(2)
            with col4_1:
                st.header('Entregar talonarios.')
                if st.button('Entregar un talonario', key='00054'):
                    st.balloons()
                    Funciones.cargar_talonario(
                        index=index, columnas=ajustes['r4 numeros por boleta'],
                        filas=ajustes['r4 boletas por talonario'], rifa='4'
                    )
            with col4_2:
                st.header('Deudas en boletas.')
                deuda_act_4 = df['r4 deudas'][index]
                st.write(f'Deudas en boletas: {'{:,}'.format(deuda_act_4)}')
                n_pago_4 = st.number_input('Pago en boletas.', step=1, value=0, key='00055')
                if st.button('Pagar boletas', key='00056'):
                    if deuda_act_4 <= 0:
                        st.error('No entiendo que desea pagar.', icon="🚨")
                    else:
                        if n_pago_4 > deuda_act_4:
                            st.error('No se puede pagar mas de lo que se debe.', icon="🚨")
                        elif n_pago_4 == 0:
                            st.error('No se puede pagar cero.', icon="🚨")
                        else:
                            st.balloons()
                            Funciones.pago_de_boletas(index=index, pago=n_pago_4, rifa='4')

            st.divider()

            st.header('Talonarios entregados:')
            boletas_r_4 = df['r4 boletas'][index]
            if boletas_r_4 == '-':
                st.subheader('🚨 No se han entregado talonarios,')
            else:
                talonarios_r_4 = boletas_r_4.split('-')
                tablas_r_4 = crear_tablas_talonarios(boletas_r_4)
                for i in range(len(talonarios_r_4)):
                    st.subheader(f'Talonario {i + 1}:')
                    st.table(tablas_r_4[i])
        else:
            st.title('🚨 La rifa no esta activa. ')