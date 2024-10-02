import json
import time
import streamlit as st
import pandas as pd
import Funciones

st.set_page_config(layout="wide")

st.title("Modificar Socios")

if st.session_state["preguntar clave"]:
    clave = st.text_input("Por favor introduzca la contraseña.")

    if st.button("Continuar"):
        if clave == st.session_state.clave_de_acceso:
            st.session_state["preguntar clave"] = False
            st.rerun()
        elif clave =="":
            st.error(
                "La contraseña esta vacia",
                icon="🚨"
            )
        else:
            st.error(
                "La contraseña no es correcta",
                icon="🚨"
            )

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

    tab_1, tab_2, tab_3 = st.tabs(
        [
            'Añadir socios',
            "Modificar valores",
            'Modificar valores (avanzado)'
        ]
    )

    with tab_1:
        st.header('Añadir nuevo socio.')
        nuevo_usuario_nombre = st.text_input('Nombre.')
        nuevo_usuario_telefono = st.text_input('Numero telefonico.')
        nuevo_usuario_puestos = st.number_input(
            'Numero de puestos.',
            value=0,
            step=1
        )
        paso_1 = False
        paso_2 = False

        if st.button('Añadir'):
            if nuevo_usuario_nombre == '':
                st.error(
                    'Me temo que el nombre esta vacio.',
                    icon="🚨"
                )
            else:
                paso_1 = True

            if nuevo_usuario_puestos < 1:
                st.error(
                    'No creo que sea util un usuario con puestos menores a 1.',
                    icon="🚨"
                )
            else:
                paso_2 = True

            if paso_1 and paso_2:
                Funciones.menu_para_insertar_socio(
                    nombre=nuevo_usuario_nombre,
                    puestos=nuevo_usuario_puestos,
                    telefono=nuevo_usuario_telefono
                )
                st.balloons()
                # st.success('El usuario ha sido añadido.', icon="✅")

    with tab_2:
        m_index_usuario = st.number_input(
            "Numero de socio.",
            value=0,
            step=1
        )
        m_columna = st.selectbox(
            "columna.",
            (
                'nombre', 'numero_telefonico', 'cuotas',
                'multas', 'estado', 'puestos', 'capital',
            )
        )

        st.divider()
        st.subheader(
            f"{df["nombre"][m_index_usuario].title()} № {m_index_usuario}"
        )
        st.divider()

        match m_columna:
            case "nombre":
                n_nombre = st.text_input(
                    "Nuevo nombre de usuario."
                )
                if st.button("Cambiar nombre"):
                    Funciones.modificar_valor_en_csv(
                        index=m_index_usuario,
                        nuevo_valor=n_nombre,
                        columna=m_columna
                    )

            case "numero_telefonico":
                n_numero_telefonico = st.text_input(
                    "Nuevo numero telefonico."
                )
                if st.button("Cambiar numero telefonico"):
                    Funciones.modificar_valor_en_csv(
                        index=m_index_usuario,
                        nuevo_valor=n_numero_telefonico,
                        columna=m_columna
                    )

            case "cuotas":
                usuario_cuotas = df["cuotas"][m_index_usuario]
                n_pagos = st.number_input(
                    "Pagos que desea añadir o quitar.",
                    value=0,
                    step=1
                )
                if st.button("Añadir pagos"):
                    Funciones.modificar_valor_en_csv(
                        index=m_index_usuario,
                        nuevo_valor=Funciones.sumar_y_restar_multas(
                            usuario_cuotas,
                            n_pagos
                        ),
                        columna=m_columna
                    )

                if st.button("Quitar pagos"):
                    Funciones.modificar_valor_en_csv(
                        index=m_index_usuario,
                        nuevo_valor=Funciones.sumar_y_restar_multas(
                            usuario_cuotas,
                            n_pagos,
                            sumar=False
                        ),
                        columna=m_columna
                    )
                st.divider()
                n_deudas = st.number_input(
                    "Deudas que desea añadir o quitar.",
                    value=0,
                    step=1
                )
                if st.button("Añadir deudas"):
                    Funciones.modificar_valor_en_csv(
                        index=m_index_usuario,
                        nuevo_valor=Funciones.sumar_y_quitar_deudas(
                            usuario_cuotas,
                            n_deudas
                        ),
                        columna=m_columna
                    )

                if st.button("Quitar deudas"):
                    Funciones.modificar_valor_en_csv(
                        index=m_index_usuario,
                        nuevo_valor=Funciones.sumar_y_quitar_deudas(
                            usuario_cuotas,
                            n_deudas,
                            sumar=False
                        ),
                        columna=m_columna
                    )

            case "multas":
                n_multas = st.number_input(
                    "Multas que desea añadir o quitar.",
                    value=0,
                    step=1
                )
                usuario_multas = df["multas"][m_index_usuario]
                if st.button("Añadir multas"):
                    Funciones.modificar_valor_en_csv(
                        index=m_index_usuario,
                        nuevo_valor=Funciones.sumar_y_restar_multas(
                            usuario_multas,
                            n_multas
                        ),
                        columna=m_columna
                    )

                if st.button("Quitar multas"):
                    Funciones.modificar_valor_en_csv(
                        index=m_index_usuario,
                        nuevo_valor=Funciones.sumar_y_restar_multas(
                            usuario_multas,
                            n_multas,
                            sumar=False
                        ),
                        columna=m_columna
                    )

            case "estado":
                st.divider()
                n_estado = df["estado"][m_index_usuario]
                st.write(
                    f"Estado: {n_estado}"
                )
                if st.button("Invertir estado"):
                    if n_estado == "activo":
                        n_estado = "no activo"
                    else:
                        n_estado = "activo"
                    Funciones.modificar_valor_en_csv(
                        index=m_index_usuario,
                        nuevo_valor=n_estado,
                        columna=m_columna
                    )

            case "puestos":
                n_puestos = st.number_input(
                    "Nuevo numero de puestos.",
                    value=0,
                    step=1
                )
                if st.button("Cambiar numero de puestos"):
                    Funciones.modificar_valor_en_csv(
                        index=m_index_usuario,
                        text=False,
                        nuevo_valor=n_puestos,
                        columna=m_columna
                    )

            case "capital":
                n_capital = st.number_input(
                    "Nuevo capital.",
                    value=0,
                    step=1
                )
                if st.button("Cambiar capital"):
                    Funciones.modificar_valor_en_csv(
                        index=m_index_usuario,
                        text=False,
                        nuevo_valor=n_capital,
                        columna=m_columna
                    )

            case _:
                st.error(
                    "Esto es un error serio, como es que siquiera se llego a esto?",
                    icon="🚨"
                )

    with tab_3:
        if st.session_state.modificacion_avanzada:
            st.header('Modificar elementos:')

            index_row = st.number_input(
                'Index de la fila.',
                value=0,
                step=1
            )

            columna_col = st.selectbox(
                'Columna a modificar',
                (
                    'nombre', 'numero_telefonico', 'cuotas', 'multas', 'tesorero',
                    'estado', 'deudas en prestamos', 'intereses vencidos',
                    'revisiones de intereses', 'intereses en prestamos', 'fiadores',
                    'deudas con fiadores', 'fechas de pagos', 'fiador de',
                    'anotaciones', 'r1 boletas', 'r2 boletas', 'r3 boletas',
                    'r4 boletas', 'puestos', 'revisiones', 'capital',
                    'aporte_a_multas', 'deudas', 'multas_extra', 'prestamos hechos',
                    'dinero en prestamos', 'dinero por si mismo', 'deudas por fiador',
                    'r1 deudas', 'r2 deudas', 'r3 deudas', 'r4 deudas'
                )
            )

            st.subheader('Modificar texto.')

            nuevo_valor_texto = st.text_input('Nuevo valor de texto.')

            if st.button('Modificar texto'):
                if columna_col in [
                    'nombre', 'numero_telefonico', 'cuotas', 'multas', 'tesorero',
                    'estado', 'deudas en prestamos', 'intereses vencidos',
                    'revisiones de intereses', 'intereses en prestamos', 'fiadores',
                    'deudas con fiadores', 'fechas de pagos', 'fiador de',
                    'anotaciones', 'r1 boletas','r2 boletas', 'r3 boletas',
                    'r4 boletas',
                ]:
                    Funciones.modificar_valor_en_csv(
                        index=index_row,
                        nuevo_valor=str(nuevo_valor_texto),
                        columna=columna_col
                    )
                else:
                    st.error(
                        'La columna a modificar es una columna de numeros',
                        icon="🚨"
                    )

            st.subheader('Modificar numeros.')

            nuevo_valor_numero = st.number_input(
                'Nuevo valor numerico.',
                value=0,
                step=1
            )

            if st.button('Modificar numero'):
                if columna_col in [
                    'puestos', 'revisiones', 'capital', 'aporte_a_multas', 'deudas',
                    'multas_extra', 'prestamos hechos', 'dinero en prestamos',
                    'dinero por si mismo', 'deudas por fiador', 'r1 deudas',
                    'r2 deudas', 'r3 deudas', 'r4 deudas'
                ]:
                    Funciones.modificar_valor_en_csv(
                        index=index_row,
                        text=False,
                        nuevo_valor=int(nuevo_valor_numero),
                        columna=columna_col
                    )
                else:
                    st.error(
                        'La columna a modificar es una columna de texto',
                        icon="🚨"
                    )
        else:
            clave_m_a = st.text_input(
                "Introduzca la clave para modificaciones avanzadas."
            )

            if st.button("Confirmar"):
                if clave_m_a == "alexandra":
                    st.session_state.modificacion_avanzada = True
                    st.rerun()
                else:
                    st.error("La clave no es correcta.", icon="🚨")
