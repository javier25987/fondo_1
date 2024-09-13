import streamlit as st
import pandas as pd
import os
import Funciones

st.set_page_config(layout="wide")

st.session_state['preguntar clave'] = True

df = pd.read_csv(st.session_state.nombre_df)

index = st.session_state.usuario_actual_cuotas

index_de_usuario = st.sidebar.number_input('Numero de usuario.', value=0, step=1)

if st.sidebar.button('Buscar'):
    if 0 <= index_de_usuario < st.session_state.usuarios:
        if df['estado'][index_de_usuario] == 'activo':
            Funciones.arreglar_asuntos(
                index_usuario=index_de_usuario, cobrar_multas=st.session_state.cobrar_multas
            )
            df = pd.read_csv(st.session_state.nombre_df)
            if st.session_state.anular_usuarios and (df['multas'][index_de_usuario].count('n') < 47):
                Funciones.desactivar_susuario(index_usuario=index_de_usuario)
                st.session_state.usuario_actual_cuotas = -2
            else:
                st.session_state.usuario_actual_cuotas = index_de_usuario
            st.rerun()
        else:
            st.error(f'El usuario № {index_de_usuario} no esta activo.', icon="🚨")
    else:
        st.error('El numero de usuario esta fuera de rango.', icon="🚨")

if index == -1:
    st.title('Usuario indeterminado')
elif index == -2:
    st.title('Usuario desactivado 🚨')
else:
    nombre_usuario = df['nombre'][index].title()
    st.title(f'№ {index} - {nombre_usuario} : {df['puestos'][index]} puesto(s)')

    col_1, col_2 = st.columns([8, 2], vertical_alignment='bottom')
    with col_1:
        st.header(f'Numero de telefono: {df['numero_telefonico'][index]}')
    with col_2:
        if st.button('Estado de cuenta'):
            with st.spinner('Obteniendo estado de cuenta...'):
                Funciones.obtener_estado_de_cuenta(index=index)

    st.divider()

    st.table(Funciones.string_calendario_usuario(index=index))

    numero_cuotas_a_pagar = sum(1 for i in df['cuotas'][index] if i != 'p')
    numero_cuotas_a_pagar = 10 if numero_cuotas_a_pagar > 10 else numero_cuotas_a_pagar

    numero_multas_a_pagar = Funciones.contar_multas(df['multas'][index])

    cuotas_a_pagar = st.selectbox('Numero de cuotas a pagar.', (range(numero_cuotas_a_pagar+1)))
    multas_a_pagar = st.selectbox('Numero de multas a pagar.', (range(numero_multas_a_pagar+1)))
    tesorero_a_pagar = st.selectbox('Tesorero.', (1, 2, 3, 4))

    c_1, c_2 = st.columns(2)

    if c_1.button('Iniciar proceso de pago'):
        if cuotas_a_pagar == 0 and multas_a_pagar == 0:
            st.error('No se que desea pagar.', icon="🚨")
        else:
            st.balloons()
            Funciones.formulario_de_pago(index, cuotas_a_pagar, multas_a_pagar, tesorero_a_pagar)
            Funciones.crear_nuevo_cheque(
                nombre=nombre_usuario,
                numero=index,
                multas_pagadas=multas_a_pagar,
                valor_multa=st.session_state.valor_de_la_multa,
                cuotas_pagadas=cuotas_a_pagar,
                valor_cuota=st.session_state.valor_de_la_cuota,
                puestos=df['puestos'][index],
                tesorero=tesorero_a_pagar
            )
    if c_2.button('Abrir ultimo cheque'):
        with st.spinner('Abriendo cheque...'):
            os.system('notepad.exe cheque_de_cuotas.txt')