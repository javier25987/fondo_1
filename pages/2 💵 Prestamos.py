import streamlit as st
import pandas as pd
import funciones.general as Funciones

st.set_page_config(layout="wide")

st.session_state['preguntar clave'] = True

df = pd.read_csv(st.session_state.nombre_df)

index = st.session_state.usuario_actual_prestamos

index_de_usuario = st.sidebar.number_input('Numero de usuario.', value=0, step=1)

if st.sidebar.button('Buscar'):
    if 0 <= index_de_usuario < st.session_state.usuarios:
        if df['estado'][index_de_usuario] == 'activo':
            Funciones.arreglar_prestamos(index=index_de_usuario)
            st.session_state.usuario_actual_prestamos = index_de_usuario
            st.rerun()
        else:
            st.error(f'El usuario № {index_de_usuario} no esta activo.', icon="🚨")
    else:
        st.error('El numero de usuario esta fuera de rango.', icon="🚨")

if index == -1:
    st.title('Usuario Indeterminado')
else:
    nombre_usuario = df['nombre'][index].title()
    st.title(f'№ {index} - {nombre_usuario}')

    prestamos_hechos = df['prestamos hechos'][index]
    capital = df['capital'][index]

    deudas_en_prestamos = str(df['deudas en prestamos'][index])
    tabla_por_prestamos = {}
    if deudas_en_prestamos != '-':
        deudas_en_prestamos = list(map(int, deudas_en_prestamos.split('-')))
        k = 1
        for i in deudas_en_prestamos:
            tabla_por_prestamos[str(k)] = '{:,}'.format(i)
            k += 1
        total_prestamos = sum(deudas_en_prestamos)
        tabla_por_prestamos['Total'] = '{:,}'.format(total_prestamos)
    else:
        tabla_por_prestamos['Total'] = '0'
        total_prestamos = 0

    deudas_por_fiador = int(df['deudas por fiador'][index])

    interese_vencidos = str(df['intereses vencidos'][index])
    tabla_interese = {}
    if interese_vencidos != '-':
        interese_vencidos = list(map(int, interese_vencidos.split('-')))
        k = 1
        for i in interese_vencidos:
            tabla_interese[str(k)] = '{:,}'.format(i)
            k += 1
        total_intereses = sum(interese_vencidos)
        tabla_interese['Total'] = '{:,}'.format(total_intereses)
    else:
        tabla_interese['Total'] = '0'
        total_intereses = 0

    capital_disponible = int(capital*0.75 - total_prestamos - deudas_por_fiador -
                             total_intereses)

    interes_por_prestamo = str(df['intereses en prestamos'][index]).split('-')
    if interes_por_prestamo != ['', '']:
        interes_por_prestamo = list(map(lambda x: str(int(x)/1000), interes_por_prestamo))
    fiadores = str(df['fiadores'][index]).split('-')
    deudas_con_fiadores = df['deudas con fiadores'][index].split('-')
    fechas_de_pago = df['fechas de pagos'][index].split('-')
    fechas_de_pago = list(map(str, fechas_de_pago))

    tab_1, tab_2, tab_3 = st.tabs(['Ver prestamos', 'Solicitar un prestamo', 'Consultar capital'])

    with tab_1:
        if prestamos_hechos == 0:
            st.header('No hay prestamos hechos')
        else:
            k = 0
            for tab_i in st.tabs([f'prestamo №{i}' for i in range(prestamos_hechos)]):
                with tab_i:
                    st.table({'deuda de el prestamo': '{:,}'.format(deudas_en_prestamos[k]),
                              'interes por prestamo': interes_por_prestamo[k],
                              'intereses vencidos': '{:,}'.format(int(interese_vencidos[k])),
                              'numero(s) de fiador(es)': fiadores[k],
                              'deuda(s) con fiador(es)': deudas_con_fiadores[k],
                              'fechas de pago': fechas_de_pago[k]})
                    ide_abono = st.number_input(f'Abono a prestamo № {k}', value=0, step=1)
                    if st.button('Abonar', key=f'{k}0000'):
                        if ide_abono < 1:
                            st.error('No se puede abonar tal cantidad' , icon="🚨")
                        else:
                            Funciones.formulario_de_abono(
                                index=index, prestamo_n=k, abono=ide_abono, nombre=nombre_usuario
                            )
                k += 1

    with tab_2:
        st.header('Carta para la solicitud de un prestamo.')
        if st.button('Imprimir carta'):
            with st.spinner('Buscando carta...'):
                Funciones.carta_para_solicitud_de_prestamo()
        st.divider()

        st.header('Formulario para la solicitud de un prestamo.')
        valor_de_el_prestamo = st.number_input('Dinero a retirar.', value=0, step=1)

        st.divider()
        ide_fiadores = st.text_input('Fiadores de el prestamo')
        ide_deudas_con_fiadores = st.text_input('Deudas con fiadores')

        st.divider()
        if st.button('Tramitar prestamo'):
            if valor_de_el_prestamo < 0:
                if valor_de_el_prestamo < 0:
                    st.error('Creo que no se puede dar esa cantidad de dinero.', icon="🚨")
            else:
                if Funciones.viavilidad_dinero(
                        index=index, valor_de_el_prestamo=valor_de_el_prestamo,
                        fiadores=ide_fiadores, deudas_con_fiadores=ide_deudas_con_fiadores
                ):
                    st.balloons()
                    Funciones.formato_de_prestamo(
                        index=index, valor_de_el_prestamo=valor_de_el_prestamo,
                        fiadores=ide_fiadores, deudas_con_fiadores=ide_deudas_con_fiadores
                    )

    with tab_3:
        st.subheader('Capital.')
        st.write(f'capital guardado: {"{:,}".format(capital)}')
        st.write(f'Capital disponible para retirar: {"{:,}".format(int(capital*0.75))}')

        st.subheader('Descuentos.')

        st.write(f'Descuento por fiador: {'{:,}'.format(deudas_por_fiador)}.')
        st.write(f'Fiador de: {df['fiador de'][index]}')

        st.write('Descuentos por prestamos.')
        st.table(tabla_por_prestamos)

        st.write('Descuentos por intereses vencidos.')
        st.table(tabla_interese)

        st.header(f'Capital disponible para retirar: {"{:,}".format(capital_disponible)}')