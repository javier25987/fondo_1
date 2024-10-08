import streamlit as st
import pandas as pd
import os
import json
import Funciones

st.set_page_config(layout="wide")

st.title('Ajustes')

control_1, control_2 = False, False

try:
    with open('ajustes.json', 'r') as j_a:
        j_a.close()

    control_1 = True
except:
    st.error(
        'Se necesita un archivo de ajustes.',
        icon="🚨"
    )

try:
    with open('ajustes.json', 'r') as j_a:
        ajustes = json.load(j_a)
        j_a.close()

    df = pd.read_csv(ajustes['nombre df'])

    control_2 = True
except:
    st.error('Se necesita una tabla de socios.', icon="🚨")

if not (control_1 and control_2):

    st.header('Creacion de archivos de ajustes y almacenamiento.')

    st.info(
        """En caso de necesitarse crear el archivo de ajustes y la tabla
        de socios cree primero el archivo de ajustes y despues la tabla
        ese orden es el adecuado para la operacion""",
        icon="ℹ️"
    )

    c1_1, c1_2 = st.columns(2)

    with c1_1:
        if st.button('crear ajustes de el programa'):
            Funciones.crear_ajustes_de_el_programa()
            st.success(
                'Los ajustes han sido creados',
                icon="✅"
            )

    with c1_2:
        if st.button('Crear nueva tabla de socios'):
            Funciones.crear_data_frame_principal()
            st.success(
                'La tabla ha sido creada',
                icon="✅"
            )

else:
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
        with open('ajustes.json', 'r') as f:
            ajustes = json.load(f)
            f.close()

        tab_1, tab_2, tab_3, tab_4, tab_5, tab_6, tab_7, tab_8, tab_9 = st.tabs(
            [
                'Calendario', 'Cuotas y multas', 'Contraseñas', 'Intereses',
                'Usuarios', 'Fechas', 'Tabla de socios', 'Guardar datos',
                'Rifas'
            ]
        )

        with tab_1:
            st.header('Calendario')

            calendario = ajustes['calendario']

            if calendario == '-':
                st.error('No hay un calendario.', icon="🚨")
            else:
                calendario = calendario.split('-')
                hora_de_corte = calendario[1][-2:]
                calendario = list(map(lambda x: x[:-3], calendario))
                #calendario += ['____/__/__']

                st.write(f'Hora de corte: {hora_de_corte}')
                st.table(
                    pd.DataFrame(
                        {
                            'columna 1': calendario[:10],
                            'columna 2': calendario[10:20],
                            'columna 3': calendario[20:30],
                            'columna 4': calendario[30:40],
                            'columna 5': calendario[40:]

                        }
                    )
                )

            st.subheader('Crear calendario.')

            n_hora = st.number_input('Hora de corte.', value=0, step=1)

            n_fecha_inicial = st.date_input('Fecha inicial.')
            n_fecha_doble_1 = st.date_input('Primera fecha doble.')
            n_fecha_doble_2 = st.date_input('Segunda fecha doble.')

            if st.button('Crear calendario'):
                n_fecha_inicial = n_fecha_inicial.strftime('%Y/%m/%d') + '/' + str(n_hora)
                n_fecha_doble_1 = n_fecha_doble_1.strftime('%Y/%m/%d') + '/' + str(n_hora)
                n_fecha_doble_2 = n_fecha_doble_2.strftime('%Y/%m/%d') + '/' + str(n_hora)

                if n_fecha_doble_1 == n_fecha_doble_2:
                    st.error('Las fechas dobles no pueden coincidir', icon="🚨")
                else:
                    n_dobles = [n_fecha_doble_1, n_fecha_doble_2]

                    fechas = Funciones.crear_listado_de_fechas(
                        primera_fecha=n_fecha_inicial, dobles=n_dobles
                    )
                    s_fechas = '-'.join(fechas)
                    ajustes['calendario'] = s_fechas

                    with open('ajustes.json', 'w') as f:
                        json.dump(ajustes, f)
                        f.close()

                    st.rerun()

        with tab_2:

            st.header('Valor de la cuota por puesto y por multa.')

            st.info(
                """
                Por favor al ingresar cantidades en miles no ingrese las comas,
                solo el numero plano.
                """,
                icon="ℹ️"
            )

            st.subheader('Por puesto.')
            st.write(
                f'Valor de la cuota por puesto: {'{:,}'.format(ajustes['valor cuota'])}'
            )
            n_cuota_puesto = st.number_input(
                'Nuevo valor de la cuota.',
                value=0,
                step=1
            )

            if st.button('Modificar.', key='00001'):
                ajustes['valor cuota'] = n_cuota_puesto
                st.session_state.valor_de_la_cuota = n_cuota_puesto

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado. ', icon="✅")
                st.rerun()

            st.subheader('Por multa.')
            st.write(
                f'Valor de la multa por puesto: {'{:,}'.format(ajustes['valor multa'])}'
            )
            n_cuota_multa = st.number_input(
                'Nuevo valor de la multa.', value=0, step=1
            )

            if st.button('Modificar', key='00002'):
                ajustes['valor multa'] = n_cuota_multa
                st.session_state.valor_de_la_multa = n_cuota_multa

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

        with tab_3:

            st.header('Clave de acceso.')

            st.write(f'La clave actual es: {ajustes['clave de acceso']}')
            st.subheader('Modificar clave de acceso.')
            nueva_clave = st.text_input('Nueva clave de acceso.')

            if st.button('Modificar.', key='00003'):
                ajustes['clave de acceso'] = nueva_clave
                st.session_state.clave_de_acceso = nueva_clave

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

        with tab_4:
            st.header('Tope de intereses.')

            st.write(
                f'Tope de diferencia entre intereses de prestamo: {
                '{:,}'.format(ajustes['tope de intereses'])
                }'
            )
            nuevo_tope = st.number_input('Nuevo tope de intereses.', value=0, step=1)

            if st.button('Modificar.', key='00013'):
                ajustes['tope de intereses'] = nuevo_tope
                st.session_state.tope = nuevo_tope

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

            st.header('Interes por prestamo.')

            st.subheader('Menos de el tope.')
            st.write(f'el interes actual por prestamo es: {ajustes['interes < tope']}')
            st.subheader('Modificar el interes.')

            nuevo_interes_m_tope = st.number_input('Nuevo interes.', value=0, step=1, key='00010')

            if st.button('Modificar.', key='00004'):
                ajustes['interes < tope'] = nuevo_interes_m_tope
                st.session_state.interes_menos_20M = nuevo_interes_m_tope

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

            st.subheader('Mas de el tope.')

            st.write(f'el interes actual por prestamo es: {ajustes['interes > tope']}')
            st.subheader('Modificar el interes.')
            nuevo_interes_M_tope = st.number_input('Nuevo interes.', value=0, step=1, key='00009')

            if st.button('Modificar.', key='00008'):
                ajustes['interes > tope'] = nuevo_interes_M_tope
                st.session_state.interes_mas_20M = nuevo_interes_M_tope

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

        with tab_5:
            st.header('Usuarios')

            st.subheader('Numero de usuarios')

            st.write(f'El numero actual de usuarios en el programa es: {ajustes['usuarios']}')
            nuevo_usuarios = st.number_input('Nuevo numero de usuarios.', value=0, step=1)

            if st.button('Modificar.', key='00005'):
                ajustes['usuarios'] = nuevo_usuarios
                st.session_state.usuarios = nuevo_usuarios

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

            st.subheader('Desactivar usuarios.')
            desactivar_usuarios = ajustes['anular usuarios']

            if desactivar_usuarios:
                st.write('Los usuarios seran desactivados.')
            else:
                st.write('Los usuarios NO seran desactivados.')

            if st.button('invertir', key='00006'):
                desactivar_usuarios = not desactivar_usuarios
                st.session_state.anular_usuarios = desactivar_usuarios
                ajustes['anular usuarios'] = desactivar_usuarios

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

            st.subheader('Cobrar multas.')
            cobra_multas = ajustes['cobrar multas']

            if cobra_multas:
                st.write('Actualmente se generan multas.')
            else:
                st.write('Actualmete NO se generan multas.')


            if st.button('invertir', key='00007'):
                cobra_multas = not cobra_multas
                st.session_state.cobrar_multas = cobra_multas
                ajustes['cobrar multas'] = cobra_multas

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

        with tab_6:
            st.subheader(f'Fecha de cierre.')

            st.write(f'Fecha de cierre actual: {ajustes['fecha de cierre']}')
            n_fecha = st.date_input('Nueva fecha de cierre.')

            if st.button('Modificar', key='000014'):
                n_fecha = n_fecha.strftime('%Y/%m/%d')
                ajustes['fecha de cierre'] = n_fecha

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

        with tab_7:
            st.subheader('Nombre de la tabla.')

            st.write(f'Tabla de trabajo actual: {ajustes['nombre df']}')
            n_nombre_tabla = st.text_input('Nuevo nombre.')

            if st.button('Modificar', key='00015'):
                ajustes['nombre df'] = n_nombre_tabla
                st.session_state.nombre_df = n_nombre_tabla

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

            st.subheader('Numero de generacion.')

            st.write(f'Numero de generacion actual: {ajustes['numero de creacion']}')
            n_numero_gen = st.number_input('Nuevo numero de generacion.', value=0, step=1)

            if st.button('Modificar', key='00016'):
                ajustes['numero de creacion'] = n_numero_gen
                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

        with tab_8:
            st.subheader('Ruta de el programa')

            st.write(f'Ruta de el programa: {ajustes['path programa']}')

            if st.button('Añadir ruta', key='00017'):
                ajustes['path programa'] = os.getcwd()
                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

            st.subheader('Enlace de el repositorio')

            st.write(f'Enlace actual: {ajustes['enlace repo']}')
            n_enlace = st.text_input('Nuevo enlace.')

            if st.button('Modificar', key='00018'):
                ajustes['enlace repo'] = n_enlace
                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

            st.subheader('Commits hechos')

            st.write(f'Commits realizados: {ajustes['commits hechos']}')
            n_comits = st.number_input('Nuevos commits.', value=0, step=1)

            if st.button('Modificar', key='00019'):
                ajustes['commits hechos'] = n_comits
                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

        with tab_9:
            rifa_1, rifa_2, rifa_3, rifa_4, act_r, cer_r = st.tabs([
                'Rifa 1', 'Rifa 2', 'Rifa 3', 'Rifa 4', 'Activar rifas', "Cerrar rifas"
            ])

            with rifa_1:
                r1_dict = {
                    "Numero de boletas": "{:,}".format(ajustes["r1 numero de boletas"]),
                    "Numeros por boleta": str(ajustes["r1 numeros por boleta"]),
                    "Premios": str(ajustes["r1 premios"]),
                    "Costo por boleta": "{:,}".format(ajustes["r1 costo de boleta"]),
                    "Boletas por talonario": str(ajustes["r1 boletas por talonario"]),
                    "Costos de administracion": "{:,}".format(ajustes["r1 costos de administracion"]),
                    "Ganancias por boleta": "{:,}".format(ajustes["r1 ganancia por boleta"]),
                    "Fecha de cierre": str(ajustes["r1 fecha de cierre"])
                }
                st.table(r1_dict)
                st.divider()

                r1_numero_de_boletas = st.number_input(
                    "Numero de boletas.", step=1, value=0, key='00024'
                )
                r1_numeros_por_boleta = st.number_input(
                    "Numeros por boleta,", step=1, value=0, key='00025'
                )
                r1_premios = st.text_input("Premios por boletas", key='00026')
                r1_costo_de_boleta = st.number_input(
                    'Costo por boleta.', value=0, step=1, key='00027'
                )
                r1_boletas_por_talonario = st.number_input(
                    "Boletas por talonario.", value=0, step=1, key="00028"
                )
                r1_costos_de_administracion = st.number_input(
                    "Costos de administracion.", step=1, value=0, key="00029"
                )
                r1_fecha_de_cierre = st.date_input("Fecha de cierre.", key="00030")

                if st.button("Cargar nuevos datos", key="00031"):
                    r1_suma_de_premios = sum(map(int, r1_premios.split(",")))
                    r1_ganancias_por_boleta = (r1_numero_de_boletas*r1_costo_de_boleta) - \
                                              (r1_costos_de_administracion + r1_suma_de_premios)
                    r1_ganancias_por_boleta /= r1_numero_de_boletas
                    r1_ganancias_por_boleta = int(r1_ganancias_por_boleta)

                    ajustes["r1 numero de boletas"] = r1_numero_de_boletas
                    ajustes["r1 numeros por boleta"] = r1_numeros_por_boleta
                    ajustes["r1 premios"] = r1_premios
                    ajustes["r1 costo de boleta"] = r1_costo_de_boleta
                    ajustes["r1 boletas por talonario"] = r1_boletas_por_talonario
                    ajustes["r1 costos de administracion"] = r1_costos_de_administracion
                    ajustes["r1 ganancia por boleta"] = r1_ganancias_por_boleta
                    ajustes["r1 fecha de cierre"] = r1_fecha_de_cierre.strftime('%Y/%m/%d')

                    with open('ajustes.json', 'w') as f:
                        json.dump(ajustes, f)
                        f.close()

                    st.success('Valor modificado.', icon="✅")
                    st.rerun()

            with rifa_2:
                r2_dict = {
                    "Numero de boletas": "{:,}".format(ajustes["r2 numero de boletas"]),
                    "Numeros por boleta": str(ajustes["r2 numeros por boleta"]),
                    "Premios": str(ajustes["r2 premios"]),
                    "Costo por boleta": "{:,}".format(ajustes["r2 costo de boleta"]),
                    "Boletas por talonario": str(ajustes["r2 boletas por talonario"]),
                    "Costos de administracion": "{:,}".format(ajustes["r2 costos de administracion"]),
                    "Ganancias por boleta": "{:,}".format(ajustes["r2 ganancia por boleta"]),
                    "Fecha de cierre": str(ajustes["r2 fecha de cierre"])
                }
                st.table(r2_dict)
                st.divider()

                r2_numero_de_boletas = st.number_input(
                    "Numero de boletas.", step=1, value=0, key='00032'
                )
                r2_numeros_por_boleta = st.number_input(
                    "Numeros por boleta,", step=1, value=0, key='00033'
                )
                r2_premios = st.text_input("Premios por boletas", key='00034')
                r2_costo_de_boleta = st.number_input(
                    'Costo por boleta.', value=0, step=1, key='00035'
                )
                r2_boletas_por_talonario = st.number_input(
                    "Boletas por talonario.", value=0, step=1, key="00036"
                )
                r2_costos_de_administracion = st.number_input(
                    "Costos de administracion.", step=1, value=0, key="00037"
                )
                r2_fecha_de_cierre = st.date_input("Fecha de cierre.", key="00038")

                if st.button("Cargar nuevos datos", key="00039"):
                    r2_suma_de_premios = sum(map(int, r2_premios.split(",")))
                    r2_ganancias_por_boleta = (r2_numero_de_boletas * r2_costo_de_boleta) - \
                                              (r2_costos_de_administracion + r2_suma_de_premios)
                    r2_ganancias_por_boleta /= r2_numero_de_boletas
                    r2_ganancias_por_boleta = int(r2_ganancias_por_boleta)

                    ajustes["r2 numero de boletas"] = r2_numero_de_boletas
                    ajustes["r2 numeros por boleta"] = r2_numeros_por_boleta
                    ajustes["r2 premios"] = r2_premios
                    ajustes["r2 costo de boleta"] = r2_costo_de_boleta
                    ajustes["r2 boletas por talonario"] = r2_boletas_por_talonario
                    ajustes["r2 costos de administracion"] = r2_costos_de_administracion
                    ajustes["r2 ganancia por boleta"] = r2_ganancias_por_boleta
                    ajustes["r2 fecha de cierre"] = r2_fecha_de_cierre.strftime('%Y/%m/%d')

                    with open('ajustes.json', 'w') as f:
                        json.dump(ajustes, f)
                        f.close()

                    st.success('Valor modificado.', icon="✅")
                    st.rerun()

            with rifa_3:
                r3_dict = {
                    "Numero de boletas": "{:,}".format(ajustes["r3 numero de boletas"]),
                    "Numeros por boleta": str(ajustes["r3 numeros por boleta"]),
                    "Premios": str(ajustes["r3 premios"]),
                    "Costo por boleta": "{:,}".format(ajustes["r3 costo de boleta"]),
                    "Boletas por talonario": str(ajustes["r3 boletas por talonario"]),
                    "Costos de administracion": "{:,}".format(ajustes["r3 costos de administracion"]),
                    "Ganancias por boleta": "{:,}".format(ajustes["r3 ganancia por boleta"]),
                    "Fecha de cierre": str(ajustes["r3 fecha de cierre"])
                }
                st.table(r3_dict)
                st.divider()

                r3_numero_de_boletas = st.number_input(
                    "Numero de boletas.", step=1, value=0, key='00040'
                )
                r3_numeros_por_boleta = st.number_input(
                    "Numeros por boleta,", step=1, value=0, key='00041'
                )
                r3_premios = st.text_input("Premios por boletas", key='00042')
                r3_costo_de_boleta = st.number_input(
                    'Costo por boleta.', value=0, step=1, key='00043'
                )
                r3_boletas_por_talonario = st.number_input(
                    "Boletas por talonario.", value=0, step=1, key="00044"
                )
                r3_costos_de_administracion = st.number_input(
                    "Costos de administracion.", step=1, value=0, key="00045"
                )
                r3_fecha_de_cierre = st.date_input("Fecha de cierre.", key="00046")

                if st.button("Cargar nuevos datos", key="00047"):
                    r3_suma_de_premios = sum(map(int, r3_premios.split(",")))
                    r3_ganancias_por_boleta = (r3_numero_de_boletas * r3_costo_de_boleta) - \
                                              (r3_costos_de_administracion + r3_suma_de_premios)
                    r3_ganancias_por_boleta /= r3_numero_de_boletas
                    r3_ganancias_por_boleta = int(r3_ganancias_por_boleta)

                    ajustes["r3 numero de boletas"] = r3_numero_de_boletas
                    ajustes["r3 numeros por boleta"] = r3_numeros_por_boleta
                    ajustes["r3 premios"] = r3_premios
                    ajustes["r3 costo de boleta"] = r3_costo_de_boleta
                    ajustes["r3 boletas por talonario"] = r3_boletas_por_talonario
                    ajustes["r3 costos de administracion"] = r3_costos_de_administracion
                    ajustes["r3 ganancia por boleta"] = r3_ganancias_por_boleta
                    ajustes["r3 fecha de cierre"] = r3_fecha_de_cierre.strftime('%Y/%m/%d')

                    with open('ajustes.json', 'w') as f:
                        json.dump(ajustes, f)
                        f.close()

                    st.success('Valor modificado.', icon="✅")
                    st.rerun()

            with rifa_4:
                r4_dict = {
                    "Numero de boletas": "{:,}".format(ajustes["r4 numero de boletas"]),
                    "Numeros por boleta": str(ajustes["r4 numeros por boleta"]),
                    "Premios": str(ajustes["r4 premios"]),
                    "Costo por boleta": "{:,}".format(ajustes["r4 costo de boleta"]),
                    "Boletas por talonario": str(ajustes["r4 boletas por talonario"]),
                    "Costos de administracion": "{:,}".format(ajustes["r4 costos de administracion"]),
                    "Ganancias por boleta": "{:,}".format(ajustes["r4 ganancia por boleta"]),
                    "Fecha de cierre": str(ajustes["r4 fecha de cierre"])
                }
                st.table(r4_dict)
                st.divider()

                r4_numero_de_boletas = st.number_input(
                    "Numero de boletas.", step=1, value=0, key='00048'
                )
                r4_numeros_por_boleta = st.number_input(
                    "Numeros por boleta,", step=1, value=0, key='00049'
                )
                r4_premios = st.text_input("Premios por boletas", key='00050')
                r4_costo_de_boleta = st.number_input(
                    'Costo por boleta.', value=0, step=1, key='00051'
                )
                r4_boletas_por_talonario = st.number_input(
                    "Boletas por talonario.", value=0, step=1, key="00052"
                )
                r4_costos_de_administracion = st.number_input(
                    "Costos de administracion.", step=1, value=0, key="00053"
                )
                r4_fecha_de_cierre = st.date_input("Fecha de cierre.", key="00054")

                if st.button("Cargar nuevos datos", key="00055"):
                    r4_suma_de_premios = sum(map(int, r4_premios.split(",")))
                    r4_ganancias_por_boleta = (r4_numero_de_boletas * r4_costo_de_boleta) - \
                                              (r4_costos_de_administracion + r4_suma_de_premios)
                    r4_ganancias_por_boleta /= r4_numero_de_boletas
                    r4_ganancias_por_boleta = int(r4_ganancias_por_boleta)

                    ajustes["r4 numero de boletas"] = r4_numero_de_boletas
                    ajustes["r4 numeros por boleta"] = r4_numeros_por_boleta
                    ajustes["r4 premios"] = r4_premios
                    ajustes["r4 costo de boleta"] = r4_costo_de_boleta
                    ajustes["r4 boletas por talonario"] = r4_boletas_por_talonario
                    ajustes["r4 costos de administracion"] = r4_costos_de_administracion
                    ajustes["r4 ganancia por boleta"] = r4_ganancias_por_boleta
                    ajustes["r4 fecha de cierre"] = r4_fecha_de_cierre.strftime('%Y/%m/%d')

                    with open('ajustes.json', 'w') as f:
                        json.dump(ajustes, f)
                        f.close()

                    st.success('Valor modificado.', icon="✅")
                    st.rerun()

            with act_r:
                st.header('Rifa 1')
                if ajustes["r1 estado"]:
                    st.write('La rifa 1 esta activa.')
                else:
                    st.write('La rifa 1 NO esta activa.')

                if st.button('Modificar', key='00020'):
                    ajustes["r1 estado"] = not ajustes["r1 estado"]
                    with open('ajustes.json', 'w') as f:
                        json.dump(ajustes, f)
                        f.close()

                    st.success('Valor modificado.', icon="✅")
                    st.rerun()

                st.divider()
                st.header('Rifa 2')
                if ajustes["r2 estado"]:
                    st.write('La rifa 2 esta activa.')
                else:
                    st.write('La rifa 2 NO esta activa.')

                if st.button('Modificar', key='00021'):
                    ajustes["r2 estado"] = not ajustes["r2 estado"]
                    with open('ajustes.json', 'w') as f:
                        json.dump(ajustes, f)
                        f.close()

                    st.success('Valor modificado.', icon="✅")
                    st.rerun()

                st.divider()
                st.header('Rifa 3')
                if ajustes["r3 estado"]:
                    st.write('La rifa 3 esta activa.')
                else:
                    st.write('La rifa 3 NO esta activa.')

                if st.button('Modificar', key='00022'):
                    ajustes["r3 estado"] = not ajustes["r3 estado"]
                    with open('ajustes.json', 'w') as f:
                        json.dump(ajustes, f)
                        f.close()

                    st.success('Valor modificado.', icon="✅")
                    st.rerun()

                st.divider()
                st.header('Rifa 4')
                if ajustes["r4 estado"]:
                    st.write('La rifa 4 esta activa.')
                else:
                    st.write('La rifa 4 NO esta activa.')

                if st.button('Modificar', key='00023'):
                    ajustes["r4 estado"] = not ajustes["r4 estado"]
                    with open('ajustes.json', 'w') as f:
                        json.dump(ajustes, f)
                        f.close()

                    st.success('Valor modificado.', icon="✅")
                    st.rerun()

            with cer_r:
                st.header("Rifa 1")
                if st.button("Cerrar rifa", key="00056"):
                    Funciones.cerrar_una_rifa('1')

                st.divider()

                st.header("Rifa 2")
                if st.button("Cerrar rifa", key="00057"):
                    Funciones.cerrar_una_rifa('2')

                st.divider()

                st.header("Rifa 3")
                if st.button("Cerrar rifa", key="00058"):
                    Funciones.cerrar_una_rifa('3')

                st.divider()

                st.header("Rifa 4")
                if st.button("Cerrar rifa", key="00059"):
                    Funciones.cerrar_una_rifa('4')
