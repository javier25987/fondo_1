import time
import pandas as pd
import streamlit as st
import subprocess
import datetime
import json
import os

def modificar_string(s: str, index_s: int, new_elemento: str):
    lista_s = [i for i in s]
    lista_s[index_s] = new_elemento
    return "".join(lista_s)

def fecha_string_formato(fecha: str):
    s = fecha.split("/")
    s = list(map(int, s))
    return datetime.datetime(*s)


def crear_listado_de_fechas(primera_fecha: str, dobles: list) -> list:
    fecha = fecha_string_formato(primera_fecha)
    dias = 7
    fechas = []
    n_semanas = 50 - len(dobles)

    for i in range(0, n_semanas):
        new_f = fecha + datetime.timedelta(days=dias * i)
        f_new = new_f.strftime('%Y/%m/%d/%H')
        if f_new in dobles:
            fechas.append(f_new)
        fechas.append(f_new)

    for i in dobles:
        if i not in fechas:
            return ['-']

    return fechas


def insertar_socios(nombre: str = '', puestos: int = 1, numero_telefonico: str = ''):
    if numero_telefonico == '':
        numero_telefonico = '_'
    nombre = nombre.lower()

    with open('ajustes.json', 'r') as f:
        ajustes = json.load(f)
        f.close()

    nuevo_usuario = pd.DataFrame({
        'numero': [ajustes['usuarios']],
        'nombre': [nombre],
        'puestos': [puestos],
        'revisiones': [0],
        'cuotas': ['n'*50],
        'multas': ['n'*50],
        'tesorero': ['n'*50],
        'estado': ['activo'],
        'capital': [0],
        'aporte_a_multas': [0],
        'deudas': [0],
        'multas_extra': [0],
        'numero_telefonico': [numero_telefonico],
        'prestamos hechos': [0],
        'dinero en prestamos': [0],
        'dinero por si mismo': [0],
        'deudas en prestamos': ['-'],
        'intereses vencidos': ['-'],
        'revisiones de intereses': ['-'],
        'intereses en prestamos': ['-'],
        'fiadores': ['-'],
        'deudas con fiadores': ['-'],
        'fechas de pagos': ['-'],
        'deudas por fiador': [0],
        'fiador de': ['-'],
        'anotaciones': ['-'],
        'r1 boletas': ['-'],
        'r1 deudas': [0],
        'r2 boletas': ['-'],
        'r2 deudas': [0],
        'r3 boletas': ['-'],
        'r3 deudas': [0],
        'r4 boletas': ['-'],
        'r4 deudas': [0]
    })

    data_frame = pd.read_csv(st.session_state.nombre_df)
    data_frame = pd.concat([data_frame, nuevo_usuario], ignore_index = True)
    data_frame = data_frame.loc[:, ~data_frame.columns.str.contains('^Unnamed')]
    data_frame.to_csv(st.session_state.nombre_df)

    ajustes['usuarios'] += 1

    with open('ajustes.json', 'w') as f:
        json.dump(ajustes, f)
        f.close()


def r_multas_tesoreros(s):
    match s:
        case 'n':
            return ' '
        case _:
            return s


def r_cuotas(s):
    match s:
        case 'p':
            return '✅ pago'
        case 'd':
            return '🚨 debe'
        case _:
            return ' '


def tablas_para_cuotas_y_multas(index: int = 0):
    with open('ajustes.json', 'r') as f:
        ajustes = json.load(f)
        calendario = ajustes['calendario']
        f.close()

    df = pd.read_csv(st.session_state.nombre_df)

    calendario = calendario.split('-')
    calendario = list(map(lambda x: x[:-3], calendario))
    numeros = [str(i) for i in range(1, 51)]

    multas = [i for i in df['multas'][index]]
    multas = list(map(r_multas_tesoreros, multas))
    cuotas = [i for i in df['cuotas'][index]]
    cuotas = list(map(r_cuotas, cuotas))
    tesoreros = [i for i in df['tesorero'][index]]
    tesoreros = list(map(r_multas_tesoreros, tesoreros))

    df_1 = pd.DataFrame(
        {
            "numeros": numeros[:25],
            'fechas': calendario[:25],
            'cuotas': cuotas[:25],
            'tesorero': tesoreros[:25],
            'multas': multas[:25]
        }
    )

    df_2 = pd.DataFrame(
        {
            "numeros": numeros[25:],
            'fechas': calendario[25:],
            'cuotas': cuotas[25:],
            'tesorero': tesoreros[25:],
            'multas': multas[25:]
        }
    )

    return df_1, df_2


def crear_data_frame_principal():
    nombre = 'FONDO_'
    try:
        with open('ajustes.json', 'r') as file:
            ajustes = json.load(file)
            lineas = str(ajustes['numero de creacion'])
            file.close()

        nombre = nombre + lineas + '_' + datetime.datetime.now().strftime('%Y') + '.csv'

        ajustes['numero de creacion'] += 1
        ajustes['nombre df'] = nombre

        with open('ajustes.json', 'w') as file:
            json.dump(ajustes, file)
            file.close()

        df = pd.DataFrame({
            'numero': [],
            'nombre': [],
            'puestos': [],
            'revisiones': [],
            'cuotas': [],
            'multas': [],
            'tesorero': [],
            'estado': [],
            'capital': [],
            'aporte_a_multas': [],
            'deudas': [],
            'multas_extra': [],
            'numero_telefonico': [],
            'prestamos hechos': [],
            'dinero en prestamos': [],
            'dinero por si mismo': [],
            'deudas en prestamos': [],
            'intereses vencidos': [],
            'revisiones de intereses': [],
            'intereses en prestamos': [],
            'fiadores': [],
            'deudas con fiadores': [],
            'fechas de pagos': [],
            'deudas por fiador': [],
            'fiador de': [],
            'anotaciones': [],
            'r1 boletas': [],
            'r1 deudas': [],
            'r2 boletas': [],
            'r2 deudas': [],
            'r3 boletas': [],
            'r3 deudas': [],
            'r4 boletas': [],
            'r4 deudas': []
        })

        df.to_csv(nombre)

    except:
        st.error('No se encuentran los ajustes', icon="🚨")


def crear_ajustes_de_el_programa():
    ajustes = {"valor multa": 3000,
               "valor cuota": 10000,
               "interes < tope": 30,
               "interes > tope": 20,
               "tope de intereses": 20000000,
               "clave de acceso": "1234",
               "calendario": "-",
               "usuarios": 0,
               "anular usuarios": False,
               "cobrar multas": False,
               "fecha de cierre": "2024/12/01",
               "numero de creacion": 1,
               "nombre df": "",
               "path programa": f"{os.getcwd()}",
               "enlace repo": "",
               "commits hechos": 0,
               "r1 estado": False,
               "r1 numero de boletas": 0,
               "r1 numeros por boleta": 0,
               "r1 premios": "",
               "r1 costo de boleta": 0,
               "r1 boletas por talonario": 0,
               "r1 costos de administracion": 0,
               "r1 ganancia por boleta": 0,
               "r1 fecha de cierre": "",
               "r2 estado": False,
               "r2 numero de boletas": 0,
               "r2 numeros por boleta": 0,
               "r2 premios": "",
               "r2 costo de boleta": 0,
               "r2 boletas por talonario": 0,
               "r2 costos de administracion": 0,
               "r2 ganancia por boleta": 0,
               "r2 fecha de cierre": "",
               "r3 estado": False,
               "r3 numero de boletas": 0,
               "r3 numeros por boleta": 0,
               "r3 premios": "",
               "r3 costo de boleta": 0,
               "r3 boletas por talonario": 0,
               "r3 costos de administracion": 0,
               "r3 ganancia por boleta": 0,
               "r3 fecha de cierre": "",
               "r4 estado": False,
               "r4 numero de boletas": 0,
               "r4 numeros por boleta": 0,
               "r4 premios": "",
               "r4 costo de boleta": 0,
               "r4 boletas por talonario": 0,
               "r4 costos de administracion": 0,
               "r4 ganancia por boleta": 0,
               "r4 fecha de cierre": ""
               }

    with open('ajustes.json', 'w') as j_a:
        json.dump(ajustes, j_a)
        j_a.close()


def sumar_una_multa(s: list, semana: int = 0):
    valor_semana = s[semana]

    if valor_semana == 'n':
        s[semana] = '1'
    else:
        k = str(int(valor_semana) + 1)
        s[semana] = k

    return s


def arreglar_asuntos(index_usuario: int):
    with open('ajustes.json', 'r') as f:
        ajustes = json.load(f)
        calendario = ajustes['calendario'].split('-')
        f.close()

    df = pd.read_csv(ajustes['nombre df'])

    cuotas = df['cuotas'][index_usuario]
    multas = df['multas'][index_usuario]

    multas = [i for i in multas]

    semanas_revisadas = int(df['revisiones'][index_usuario])

    calendario = list(map(lambda x: list(map(lambda y: int(y), x.split('/'))), calendario))
    calendario = list(map(lambda x: datetime.datetime(*x), calendario))

    fecha_actual = datetime.datetime.now()

    semanas_a_revisar = list(map(lambda x: x < fecha_actual, calendario))
    semanas_a_revisar = sum(map(int, semanas_a_revisar))

    if semanas_a_revisar > semanas_revisadas:
        for i in range(50):
            if calendario[i] > fecha_actual:
                break
            else:
                if cuotas[i] == 'p':
                    pass
                else:
                    if ajustes["cobrar multas"]:
                        multas = sumar_una_multa(multas, i)

                    cuotas = modificar_string(cuotas, i, 'd')

        df.loc[index_usuario, 'cuotas'] = cuotas

        multas = ''.join(multas)
        df.loc[index_usuario, 'multas'] = multas

        df.loc[index_usuario, 'revisiones'] = semanas_a_revisar

        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        df.to_csv(ajustes['nombre df'])


def desactivar_susuario(index_usuario: int):
    df = pd.read_csv(st.session_state.nombre_df)

    df.loc[index_usuario, 'estado'] = 'no activo'

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    df.to_csv(st.session_state.nombre_df)


def contar_multas(s: str):
    k = [i for i in s if i != 'n']
    if not k:
        return 0
    k = sum(map(int, k))

    return k


def pagar_n_cuotas(s: str, n: int):
    cuotas_pagas = s.count('p')

    if cuotas_pagas == 50:
        return  s

    if 50 - cuotas_pagas < n:
        return s

    for _ in range(n):
        k = 0
        for i in s:
            if i != 'p':
                s = modificar_string(s, k, 'p')
                break
            k += 1

    return s


def pagar_n_multas(s: str, n: int):
    multas_a_pagar = contar_multas(s)

    if multas_a_pagar == 0:
        return s

    if n > multas_a_pagar:
        return s

    for _ in range(n):
        k = 0
        for i in s:
            if i != 'n':
                n_v = int(i) - 1
                n_v = 'n' if n_v == 0 else str(n_v)
                s = modificar_string(s, k, n_v)
                break
            k += 1

    return s


def poner_tesorero(s: str, n: int, tesorero: str):
    tesorero = str(tesorero)
    semanas_disponibles = s.count('n')

    if n > semanas_disponibles:
        return s

    if semanas_disponibles == 0:
        return s

    for _ in range(n):
        semana = s.find('n')
        s = modificar_string(s, semana, tesorero)

    return s


@st.dialog("Formulario de pago.")
def formulario_de_pago(index: int, cuotas: int, multas: int, tesorero: str):
    df = pd.read_csv(st.session_state.nombre_df)

    st.header(f'№ {index} - {df['nombre'][index].title()}')
    st.divider()

    puestos = int(df['puestos'][index])
    capital_actual = int(df['capital'][index])
    multas_aportes_actual = int(df['aporte_a_multas'][index])
    cuotas_actual = df['cuotas'][index]
    multas_actual = df['multas'][index]
    tesorero_actual = df['tesorero'][index]

    st.write(f'Puestos: {puestos}')
    st.divider()

    st.write(f'Cuotas a pagar: {cuotas}')
    st.write(f'Valor de cuota por puesto: {'{:,}'.format(st.session_state.valor_de_la_cuota)}')
    total_cuotas = cuotas*st.session_state.valor_de_la_cuota*puestos
    st.write(f'Total en cuotas: {'{:,}'.format(total_cuotas)}')
    st.divider()

    st.write(f'Multas a pagar: {multas}')
    st.write(f'Valor de multa por puesto: {'{:,}'.format(st.session_state.valor_de_la_multa)}')
    total_multas = multas*st.session_state.valor_de_la_multa*puestos
    st.write(f'Total en multas: {'{:,}'.format(total_multas)}')
    st.divider()

    st.write(f'Total neto a pagar: {'{:,}'.format(total_multas + total_cuotas)}')
    st.write(f'Se paga a el tesorero: {tesorero}')
    st.divider()

    st.info('Por favor asegurese de recibir el dinero y de certificar que todo este bien.'
            ' puesto que una vez aceptado el pago no hay vuelta atraz y por favor oprima'
            ' el boton solo una vez.', icon="ℹ️")
    st.divider()

    if st.button('Aceptar pago'):
        tesorero_actual = poner_tesorero(tesorero_actual, cuotas, tesorero)
        cuotas_actual = pagar_n_cuotas(cuotas_actual, cuotas)
        multas_actual = pagar_n_multas(multas_actual, multas)
        capital_actual += total_cuotas
        multas_aportes_actual += total_multas

        df.loc[index, 'cuotas'] = cuotas_actual
        df.loc[index, 'multas'] = multas_actual
        df.loc[index, 'tesorero'] = tesorero_actual
        df.loc[index, 'capital'] = capital_actual
        df.loc[index, 'aporte_a_multas'] = multas_aportes_actual

        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        df.to_csv(st.session_state.nombre_df)

        st.rerun()


def crear_nuevo_cheque(
        nombre: str = '', numero: int = 0, multas_pagadas: int = 0, valor_multa: int = 0,
        cuotas_pagadas: int = 0, valor_cuota: int = 0, puestos: int = 0, tesorero: int = 1
):
    cheque = ['===========================',
              '=                         =',
              '=    FONDO SAN JAVIER     =',
              '=                         =',
              '===========================',
              '> Nombre:',
              '> Numero:',
              '> Puestos:',
              '===========================',
              '> Multas pagadas:',
              '> Valor multa:',
              '> TOTAL multas:',
              '===========================',
              '> Cuotas pagadas:',
              '> Valor cuota:',
              '> TOTAL cuotas:',
              '===========================',
              '> Tesorero:',
              '> Total pagado:',
              '===========================',
              '> Fecha:',
              '> Hora:',
              '===========================']

    if len(nombre) > 17:
        nombre = nombre[:18]

    cheque[5] += nombre
    cheque[6] += str(numero)
    cheque[9] += str(multas_pagadas)
    cheque[10] += str('{:,}'.format(valor_multa))

    total_multas = multas_pagadas*valor_multa*puestos
    cheque[11] += str('{:,}'.format(total_multas))

    cheque[13] += str(cuotas_pagadas)
    cheque[14] += str('{:,}'.format(valor_cuota))
    cheque[7] += str(puestos)

    total_cuotas = cuotas_pagadas*valor_cuota*puestos
    cheque[15] += str('{:,}'.format(total_cuotas))

    cheque[17] += str(tesorero)

    total_pagado = total_cuotas + total_multas
    cheque[18] += str('{:,}'.format(total_pagado))

    cheque[20] += str(datetime.datetime.now().strftime('%Y.%m.%d'))
    cheque[21] += str(datetime.datetime.now().strftime('%H:%M'))

    cheque = list(map(lambda x: x + '\n', cheque))
    cheque[-1] = cheque[-1].strip()

    with open('cheque_de_cuotas.txt', 'w', encoding='utf_8') as f:
        f.write(''.join(cheque))
        f.close()


def calendario_n_meses():
    with open('ajustes.json', 'r') as f:
        ajustes = json.load(f)
        f.close()

    clos_data = ajustes['fecha de cierre']
    clos_data = list(map(int, clos_data.split('/')))
    clos_data = datetime.datetime(*clos_data)

    now = datetime.datetime.now()
    fechas = []

    if now.day > 28:
        for i in range(1, 20):
            n_now = now
            while True:
                try:
                    new_now = n_now.replace(month=now.month + i)
                    break
                except:
                    n_now = n_now - datetime.timedelta(days=1)

            if new_now < clos_data:
                fechas.append(new_now)
            else:
                break
    else:
        for i in range(1, 20):
            n_now = now
            new_now = n_now.replace(month=now.month + i)

            if new_now < clos_data:
                fechas.append(new_now)
            else:
                break

    fechas = list(map(lambda x: x.strftime('%Y/%m/%d'), fechas))
    fechas = ','.join(fechas)
    return  fechas


def consultar_capital(index):
    df = pd.read_csv(st.session_state.nombre_df)
    capital = df['capital'][index]
    estado = df['estado'][index]

    if estado != 'activo':
        return 2

    deudas_en_prestamos = str(df['deudas en prestamos'][index])
    tabla_por_prestamos = 0
    if deudas_en_prestamos != '-':
        deudas_en_prestamos = list(map(int, deudas_en_prestamos.split('-')))
        tabla_por_prestamos = sum(deudas_en_prestamos)

    deudas_por_fiador = int(df['deudas por fiador'][index])

    interese_vencidos = df['intereses vencidos'][index]
    tabla_interese = 0
    if interese_vencidos != '-':
        interese_vencidos = list(map(float, interese_vencidos.split('-')))
        tabla_interese = sum(interese_vencidos)

    capital_disponible = int(
        capital * 0.75 - tabla_por_prestamos - deudas_por_fiador - tabla_interese
    )

    return capital_disponible


def generar_prestamo(
    index: int, valor_de_el_prestamo: int, fiadores: str = '', deudas_con_fiadores: str = ''
):
    df = pd.read_csv(st.session_state.nombre_df)

    with open('ajustes.json', 'r') as f:
        ajustes = json.load(f)
        f.close()

    prestamos_hechos = int(df['prestamos hechos'][index])
    prestamos_hechos += 1
    df.loc[index, 'prestamos hechos'] = prestamos_hechos

    deudas_en_prestamos = str(df['deudas en prestamos'][index])
    if deudas_en_prestamos == '-':
        deudas_en_prestamos = str(valor_de_el_prestamo)
    else:
        deudas_en_prestamos +=  f'-{str(valor_de_el_prestamo)}'
    df.loc[index, 'deudas en prestamos'] = deudas_en_prestamos

    if deudas_con_fiadores == '':
        dinero_a_restar = 0
    else:
        dinero_a_restar = sum(map(int, deudas_con_fiadores.split(',')))
    dinero_por_si_mismo = df['dinero por si mismo'][index]
    dinero_por_si_mismo += valor_de_el_prestamo - dinero_a_restar
    df.loc[index, 'dinero por si mismo'] = dinero_por_si_mismo

    intereses_vencidos = str(df['intereses vencidos'][index])
    if intereses_vencidos == '-':
        intereses_vencidos = '0'
    else:
        intereses_vencidos += '-0'
    df.loc[index, 'intereses vencidos'] = intereses_vencidos

    revisiones_de_intereses = str(df['revisiones de intereses'][index])
    if revisiones_de_intereses == '-':
        revisiones_de_intereses = '0'
    else:
        revisiones_de_intereses += '-0'
    df.loc[index, 'revisiones de intereses'] = revisiones_de_intereses

    interes = str(df['intereses en prestamos'][index])
    n_interes = str(ajustes['interes < tope'])

    if valor_de_el_prestamo > ajustes['tope de intereses']:
        n_interes = str(ajustes['interes > tope'])

    if interes == '-':
        interes = n_interes
    else:
        interes += f'-{n_interes}'
    df.loc[index, 'intereses en prestamos'] = interes

    fechas_de_pagos = str(df['fechas de pagos'][index])
    n_fechas = calendario_n_meses()
    if fechas_de_pagos == '-':
        fechas_de_pagos = n_fechas
    else:
        fechas_de_pagos += f'-{n_fechas}'
    df.loc[index, 'fechas de pagos'] = fechas_de_pagos

    n_fiadores = str(df['fiadores'][index])
    if fiadores != '':
        if n_fiadores == '-':
            n_fiadores = fiadores
        else:
            n_fiadores += f'-{fiadores}'
    else:
        if n_fiadores == '-':
            n_fiadores = 'n'
        else:
            n_fiadores += '-n'
    df.loc[index, 'fiadores'] = n_fiadores

    deuda_con_fiadores = str(df['deudas con fiadores'][index])
    if deudas_con_fiadores != '':
        if deuda_con_fiadores == '-':
            deuda_con_fiadores = deudas_con_fiadores
        else:
            deuda_con_fiadores += f'-{deudas_con_fiadores}'
    else:
        if deuda_con_fiadores == '-':
            deuda_con_fiadores = 'n'
        else:
            deuda_con_fiadores += '-n'
    df.loc[index, 'deudas con fiadores'] = deuda_con_fiadores

    dinero_en_prestamos = int(df['dinero en prestamos'][index])
    dinero_en_prestamos += valor_de_el_prestamo
    df.loc[index, 'dinero en prestamos'] = dinero_en_prestamos

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    df.to_csv(st.session_state.nombre_df)


def viavilidad_dinero(index: int, valor_de_el_prestamo: int, fiadores: str = '',
                      deudas_con_fiadores: str = ''):
    capital = consultar_capital(index=index)

    if (fiadores == '') and (deudas_con_fiadores == ''):
        if capital >= valor_de_el_prestamo:
            return True
        else:
            st.error(
                f'''
                Usted puede retirar {'{:,}'.format(capital)} para hacer un prestamo y quiere
                relizar un prestamo por {'{:,}'.format(valor_de_el_prestamo)}, solicite 
                fiadores para hacer su prestamo, de otra manera no sera posible.
                '''
            , icon="🚨")
            return False
    else:
        try:
            n_fiadores = list(map(int, fiadores.split(',')))
            n_deudas = list(map(int, deudas_con_fiadores.split(',')))

            if len(set(n_fiadores)) != len(n_fiadores):
                st.error(f'No pueden haber fiadores repetidos.', icon="🚨")
                return False

            for i, j in zip(n_fiadores, n_deudas):
                temporal_capital = consultar_capital(i)
                if temporal_capital <= j:
                    st.error(f'El fiador №-{i} no tiene dinero para este prestamo.', icon="🚨")
                    break
                elif temporal_capital < 0:
                    st.error(f'El fiador №-{i} tiene saldo negativo.', icon="🚨")
                    break
                elif temporal_capital == 2:
                    st.error(f'El fiador №-{i} esta desactivado.', icon="🚨")
                    break
                elif i == index:
                    st.error(f'No se puede ser fiador de si mismo.', icon="🚨")
                    break
            else:
                suma_de_deudas = sum(n_deudas)
                if suma_de_deudas > valor_de_el_prestamo:
                    st.error(f'La deuda con fiadores supera el valor de el prestamo.', icon="🚨")
                    return False
                elif (capital + suma_de_deudas) >= valor_de_el_prestamo:
                    return True
                else:
                    st.error(f'A pesar de tener fiadores no alcanza para este prestamo.', icon="🚨")
                    return False
            return False
        except:
            st.error(
                '''
                El formato de fiadores y deudas con ellas esta mal escrito, por favor confirme que
                todo este en regla.'''
            , icon="🚨")
            return False


def escribir_deudas_fiadores(index: int, fiadores: str, deudas_con_fiadores: str):
    df = pd.read_csv(st.session_state.nombre_df)

    fiadores = list(map(int, fiadores.split(',')))
    deudas_con_fiadores = list(map(int, deudas_con_fiadores.split(',')))

    index = str(index)

    for i, j in zip(fiadores, deudas_con_fiadores):
        fiador_de = df['fiador de'][i]
        if fiador_de == '-':
            fiador_de = index
        else:
            fiador_de += f'-{index}'
        df.loc[i, 'fiador de'] = fiador_de

        deudas_con = int(df['deudas por fiador'][i])
        deudas_con += j
        df.loc[i, 'deudas por fiador'] = deudas_con

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    df.to_csv(st.session_state.nombre_df)


@st.dialog("Formulario de prestamo.")
def formato_de_prestamo(
        index: int, valor_de_el_prestamo: int, fiadores: str, deudas_con_fiadores: str
):
    df = pd.read_csv(st.session_state.nombre_df)

    st.header(f'№ {index} - {df['nombre'][index].title()}')
    st.divider()

    st.write(f'Valor de el prestamo: {'{:,}'.format(valor_de_el_prestamo)}')

    with open('ajustes.json', 'r') as f:
        ajustes = json.load(f)
        f.close()

    interes = ajustes['interes < tope']/1000

    if ajustes['tope de intereses'] < valor_de_el_prestamo:
        interes = ajustes['interes > tope']/1000

    st.write(f'Interes por prestamo: {interes}')

    st.write(f'Dinero a entregar: {'{:,}'.format(int(valor_de_el_prestamo*(1-interes)))}')

    st.divider()
    fechas_de_pago = calendario_n_meses().split(',')
    st.write('Fechas de cuotas:')
    for i in fechas_de_pago:
        st.write(i)

    st.divider()
    st.write(f'Fiadores: {fiadores}')
    st.write(f'Deudas con fiadores: {deudas_con_fiadores}')

    st.divider()
    st.info(
        '''
        Por favor asegurese de entregar el dinero, haber impreso la carta y 
        confirmar que todos los datos sean correctos, ya que de haberse equivocado
        todas las correcciones se tendran que hacer de manera manual en "Modificar socios"
        y no es nada agradable hacer eso manualmete
        '''
    , icon="ℹ️")

    if st.button('confirmar'):
        generar_prestamo(index=index, valor_de_el_prestamo=valor_de_el_prestamo,
                         fiadores=fiadores, deudas_con_fiadores=deudas_con_fiadores)
        if (fiadores == '') or (deudas_con_fiadores == ''):
            pass
        else:
            escribir_deudas_fiadores(index=index, fiadores=fiadores,
                                 deudas_con_fiadores=deudas_con_fiadores)
        st.toast('Prestamo realizado con exito.')
        st.rerun()


def pagar_a_str_comp(s: str, pago: int):
    s = list(map(int, s.split(',')))

    i = 0
    while True:
        if pago >= s[i]:
            pago -= s[i]
            s[i] = 0
        else:
            s[i] -= pago
            break
        i += 1

    s = list(map(str, s))
    return ','.join(s)


def abonar_deuda(index: int = 0, prestamo_n: int = 0, abono: int = 0):
    df = pd.read_csv(st.session_state.nombre_df)

    deuda_actual = str(df['deudas en prestamos'][index])
    intereses_vencidos = str(df['intereses vencidos'][index])
    fiadores = str(df['fiadores'][index])
    deudas_con_fiadores = str(df['deudas con fiadores'][index])

    deuda_actual = deuda_actual.split('-')
    intereses_vencidos = intereses_vencidos.split('-')
    fiadores = fiadores.split('-')
    deudas_con_fiadores = deudas_con_fiadores.split('-')

    n_d_a = int(deuda_actual[prestamo_n])
    n_i_v = int(intereses_vencidos[prestamo_n])

    if not (0 < abono <= (n_i_v + n_d_a)):
        st.error('No creo que abonar esa cantidad sea correcto.', icon="🚨")
        return None

    n_f = fiadores[prestamo_n]
    n_d_f = deudas_con_fiadores[prestamo_n].split(',')

    n_f = [] if n_f == 'n' else list(map(int, n_f.split(',')))

    d_f = 0 if n_d_f == ['n'] else sum(map(int, n_d_f))

    if abono >= n_i_v:
        abono -= n_i_v
        aporte_a_multa_extra = n_i_v
        n_i_v = 0
    else:
        n_i_v -= abono
        aporte_a_multa_extra = abono
        abono = 0
    intereses_vencidos[prestamo_n] = str(n_i_v)
    df.loc[index, 'intereses vencidos'] = '-'.join(intereses_vencidos)

    if aporte_a_multa_extra > 0:
        multas_extra = int(df['multas_extra'][index])
        multas_extra += aporte_a_multa_extra
        df.loc[index, 'multas_extra'] = multas_extra

        anotaciones = str(df['anotaciones'][index])
        if anotaciones == '-':
            anotaciones = f'Pago {'{:,}'.format(aporte_a_multa_extra)} por intereses vencidos,'
        else:
            anotaciones += f'-Pago {'{:,}'.format(aporte_a_multa_extra)} por intereses vencidos,'
        df.loc[index, 'anotaciones'] = anotaciones

    abono_a_fiadores = d_f if abono >= d_f else abono
    if deudas_con_fiadores[prestamo_n] != 'n':
        deudas_con_fiadores[prestamo_n] = pagar_a_str_comp(
            deudas_con_fiadores[prestamo_n], abono_a_fiadores
        )
        df.loc[index, 'deudas con fiadores'] = '-'.join(deudas_con_fiadores)

    n_d_a -= abono
    deuda_actual[prestamo_n] = str(int(n_d_a))
    df.loc[index, 'deudas en prestamos'] = '-'.join(deuda_actual)

    n_d_f = [] if n_d_f == ['n'] else list(map(int, n_d_f))
    for i, j in zip(n_f, n_d_f):
        deuda_de_fiador = int(df['deudas por fiador'][i])
        if abono_a_fiadores >= j:
            deuda_de_fiador -= j
            abono_a_fiadores -= j
            df.loc[i, 'deudas por fiador'] = deuda_de_fiador
        else:
            deuda_de_fiador -= abono_a_fiadores
            df.loc[i, 'deudas por fiador'] = deuda_de_fiador
            break

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    df.to_csv(st.session_state.nombre_df)

    st.rerun()


@st.dialog("Formulario de abono.")
def formulario_de_abono(
        index: int = 0, prestamo_n: int = 0, abono: int = 0, nombre: str = ''
):
    st.title(nombre)

    st.divider()
    st.write(f'Desea abonar {'{:,}'.format(abono)} a el prestamo № {prestamo_n}?')

    st.divider()
    st.info(
        '''
        Por favor asegurese de recibir el dinero y certificar los datos ya que
        aceptado el abono no hay vuelta atraz.
        '''
    , icon="ℹ️")

    st.divider()
    if st.button('Abonar'):
        abonar_deuda(
            index=index, prestamo_n=prestamo_n, abono=abono
        )
        st.rerun()


def arreglar_prestamos(index: int):
    df = pd.read_csv(st.session_state.nombre_df)

    prestamos_hechos = int(df['prestamos hechos'][index])
    if prestamos_hechos == 0:
        return None

    deudas_en_prestamos = df['deudas en prestamos'][index]
    deudas_en_prestamos = list(map(int, str(deudas_en_prestamos).split('-')))

    intereses_vencidos = df['intereses vencidos'][index]
    intereses_vencidos = list(map(int, str(intereses_vencidos).split('-')))

    intereses_en_prestamos = df['intereses en prestamos'][index]
    intereses_en_prestamos = list(map(int, str(intereses_en_prestamos).split('-')))

    revisiones_de_intereses = df['revisiones de intereses'][index]
    revisiones_de_intereses = list(map(int, str(revisiones_de_intereses).split('-')))

    fechas_de_pagos = df['fechas de pagos'][index]
    fechas_pasadas = []
    fecha_actual = datetime.datetime.now()
    lista_fechas = fechas_de_pagos.split('-')
    for i in lista_fechas:
        tem_data = i.split(',')
        tem_data = list(map(lambda x: list(map(int, x.split('/'))), tem_data))
        tem_data = list(map(lambda x: datetime.datetime(*x), tem_data))

        fechas_anteriores = list(map(lambda x: x < fecha_actual, tem_data))
        fechas_anteriores = sum(map(int, fechas_anteriores))

        fechas_pasadas.append(fechas_anteriores)

    for i in range(prestamos_hechos):
        if fechas_pasadas[i] > revisiones_de_intereses[i]:
            diferencia = fechas_pasadas[i] - revisiones_de_intereses[i]
            d = deudas_en_prestamos[i]
            if d > 0:
                intereses_vencidos[i] += int(d*(intereses_en_prestamos[i]/1000)*diferencia)
            revisiones_de_intereses[i] = fechas_pasadas[i]

    deudas_en_prestamos = '-'.join(list(map(str, deudas_en_prestamos)))
    intereses_vencidos = '-'.join(list(map(str, intereses_vencidos)))
    revisiones_de_intereses = '-'.join(list(map(str, revisiones_de_intereses)))

    df.loc[index, 'deudas en prestamos'] = deudas_en_prestamos
    df.loc[index, 'intereses vencidos'] = intereses_vencidos
    df.loc[index, 'revisiones de intereses'] = revisiones_de_intereses

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    df.to_csv(st.session_state.nombre_df)


def modificar_str_compuesto_simple(s: str, index: int, nuevo_valor: str):
    s = s.split('-')
    s[index] = nuevo_valor
    s = '-'.join(s)
    return  s


def modificar_str_compuesto_multiple(s: str, index_1: int, index_2: int, nuevo_valor: str):
    s = s.split('-')
    s = list(map(lambda x: x.split(','), s))
    s[index_1][index_2] = nuevo_valor
    s = list(map(lambda x: ','.join(x), s))
    s = '-'.join(s)
    return s


def ejecutar_comando_git(comando):
    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    salida, error = proceso.communicate()

    if proceso.returncode != 0:
        print(f"Error: {error.decode('utf-8')}")
    else:
        print(f"Salida: {salida.decode('utf-8')}")


def obtener_estado_de_cuenta(index: int):
    df = pd.read_csv(st.session_state.nombre_df)

    ahora = datetime.datetime.now()
    fecha_hora_str = ahora.strftime("%Y/%m/%d %H:%M")

    formato = [
        f'============================== Fondo San Javier ==============================\n',
        '\n',
        f'     № {df['numero'][index]}: {df['nombre'][index].title()} - {df['puestos'][index]} puesto(s)\n',
        '\n',
        f'los siguientes datos son validos para la fecha "{fecha_hora_str}" para otras\n',
        f'fechas no se confirma su veracidad.\n',
        f'\n',
        f'Pago de cuotas:\n',
        f'- Cuotas pagas: {df['cuotas'][index].count('p')}\n',
        f'- Cuotas que se deben: {df['cuotas'][index].count('d')}\n',
        f'- Multas pendientes: {contar_multas(df['multas'][index])}\n',
        f'- Estado: {df['estado'][index]}\n',
        f'- Capital: {'{:,}'.format(df['capital'][index])}\n',
        f'- Dinero pagado en multas: {'{:,}'.format(df['aporte_a_multas'][index])}\n',
        f'- Multas extra: {'{:,}'.format(df['multas_extra'][index])} \n',
        f'- Numero de telefono: {df['numero_telefonico'][index]}\n',
        f'\n',
        f'Prestamos:\n',
        f'- Prestamos solitados: {df['prestamos hechos'][index]}\n',
        f'- Dinero retirado en prestamos: {'{:,}'.format(df['dinero en prestamos'][index])}\n',
        f'- Deudas actuales en prestamos: {df['deudas en prestamos'][index]}\n',
        f'- Intereses vencidos por un prestamos: {df['intereses vencidos'][index]}\n',
        f'- Fiadores por prestamos: {df['fiadores'][index]}\n',
        f'- Deudas con fiadores: {df['deudas con fiadores'][index]}\n',
        f'\n',
        f'- Deudas por fiador: {'{:,}'.format(df['deudas por fiador'][index])}\n',
        f'- Fiador de: {df['fiador de'][index]}\n'
    ]

    with open('estado de cuenta.txt', 'w', encoding='utf-8') as f:
        f.write(''.join(formato))
        f.close()

    os.system('notepad.exe estado de cuenta.txt')


def carta_para_solicitud_de_prestamo():
    ahora = datetime.datetime.now()
    fecha_hora_str = ahora.strftime("%Y/%m/%d %H:%M")
    carta = [
        fecha_hora_str + '\n',
        '\n',
        'Señores de el fondo, yo __________________________ usuari@ № _______ de el fondo San Javier\n',
        '\n',
        'solicito un prestamo por el valor de _______________, con el interes de ______ % tengo la \n',
        '\n',
        'intencion de pagar el prestamo en _______ mes(es) si mi dinero no llegase a ser suficiente\n',
        '\n',
        'solicito como fiador(es) con las siguientes deudas a:\n',
        '\n',
        '          Nombre                    Numero                    Deuda\n',
        '-------------------------------------------------------------------------------------\n',
        '                              |                 |\n',
        '-------------------------------------------------------------------------------------\n',
        '                              |                 |\n',
        '-------------------------------------------------------------------------------------\n',
        '                              |                 |\n',
        '-------------------------------------------------------------------------------------\n',
        '                              |                 |\n',
        '-------------------------------------------------------------------------------------\n',
        '                              |                 |\n',
        '-------------------------------------------------------------------------------------\n',
        '\n',
        '\n',
        '\n',
        '\n',
        '\n',
        '\n',
        '\n',
        '\n',
        '          _________________________                         _________________________\n',
        '           socio de el fondo                                 tesorero'
    ]

    with open('carta_prestamo.txt', 'w', encoding='utf-8') as f:
        f.write(''.join(carta))
        f.close()

    os.system('notepad.exe carta_prestamo.txt')


@st.dialog('Entrega de talonario')
def cargar_talonario(index: int, columnas: int, filas: int, rifa: str):
    df = pd.read_csv(st.session_state.nombre_df)

    st.header(f'№ {df['numero'][index]}: {df['nombre'][index].title()}')
    st.divider()

    with open('ajustes.json', 'r') as f:
        ajustes = json.load(f)
        f.close()

    l_col = [str(i) for i in range(1, columnas+1)]
    l_fil = [str(i) for i in range(1, filas+1)]

    for i in l_fil:
        st.write(f'Boleta № {i} de el talonario.')
        for col_j, j in zip(st.columns(columnas), l_col):
            with col_j:
                st.text_input(f'№ {j}', key=f'{i},{j}')
        st.divider()

    st.info(
        '''
        Antes de entregar el talonario por favor confirme que todas las boletas
        fueron escritas correctamente y que no hay errores en ellas, ya que una 
        vez entregado el talonario no es sencillo repararlo asi que por favor 
        asegurese de rectificar los datos correctamente.
        '''
    , icon="ℹ️")
    st.divider()

    if st.button('Entregar talonario'):
        talonario = []
        for i in l_fil:
            boleta = []
            for j in l_col:
                boleta.append(st.session_state[f'{i},{j}'])

            talonario.append('/'.join(boleta))

        talonario = ','.join(talonario)

        boletas_act = df[f'r{rifa} boletas'][index]
        if boletas_act == '-':
            boletas_act = talonario
        else:
            boletas_act += f'-{talonario}'
        df.loc[index, f'r{rifa} boletas'] = boletas_act

        deuda_act = df[f'r{rifa} deudas'][index]
        valor_talonario = (
            ajustes[f'r{rifa} costo de boleta'] * ajustes[f'r{rifa} boletas por talonario']
        )
        deuda_act += valor_talonario
        df.loc[index, f'r{rifa} deudas'] = deuda_act

        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        df.to_csv(st.session_state.nombre_df)

        st.rerun()


@st.dialog('Pago de boletas')
def pago_de_boletas(index: int, pago: int, rifa: str):
    df = pd.read_csv(st.session_state.nombre_df)

    st.header(f'№ {df['numero'][index]}: {df['nombre'][index].title()}')
    st.divider()

    deuda_act = df[f'r{rifa} deudas'][index]

    st.write(f'Deuda por boletas: {'{:,}'.format(deuda_act)}')
    st.write(f'Pago que se realiza: {'{:,}'.format(pago)}')
    st.divider()

    st.info('Por favor asegurese de recibir el dinero y certificar que todo este'
            'bien, una ves aceptado el pago no hay vuelta atraz.', icon="ℹ️")
    st.divider()

    if st.button('Aceptar pago'):
        deuda_act -= pago
        df.loc[index, f'r{rifa} deudas'] = deuda_act

        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        df.to_csv(st.session_state.nombre_df)

        st.rerun()


def crear_tablas_talonarios(boletas: str):
    talonarios = boletas.split('-')
    lista_r = []
    for i in talonarios:
        i_b = i.split(',')
        i_b = list(map(lambda x: x.split('/'), i_b))

        dict_t = dict()

        dict_t['Boletas'] = [f'Boleta № {k + 1}' for k in range(len(i_b))]

        i_b = list(map(list, zip(*i_b)))

        for j in range(len(i_b)):
            dict_t[f'№ {j + 1}'] = i_b[j]

        lista_r.append(pd.DataFrame(dict_t))

    return lista_r


def cerrar_una_rifa(rifa: str):
    with open('ajustes.json', 'r') as f:
        ajustes = json.load(f)
        f.close()

    df = pd.read_csv(st.session_state.nombre_df)

    if ajustes[f"r{rifa} estado"]:
        fecha_de_cierre = ajustes[f"r{rifa} fecha de cierre"]
        fecha_de_cierre = fecha_string_formato(fecha_de_cierre)

        if fecha_de_cierre < datetime.datetime.now():
            print(f"Iniciando el cierre de la rifa {rifa}")

            nombre_rifa = f"r{rifa} deudas"

            numeros = tuple(df["numero"])
            nombres = tuple(df["nombre"])
            deudas = tuple(df[nombre_rifa])

            for i in range(len(nombres)):
                if deudas[i] > 0:
                    generar_prestamo(numeros[i], deudas[i])
                    df.loc[numeros[i], nombre_rifa] = 0
                    print(f"> Se ha generado un prestamo para: {nombres[i]}; \t por {deudas[i]}")

            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            df.to_csv(st.session_state.nombre_df)

            ajustes[f"r{rifa} estado"] = False
            with open('ajustes.json', 'w') as f:
                json.dump(ajustes, f)
                f.close()

            print(f"El proceso ha terminado exitosamente...")
            st.success('Rifa cerrada correctamente.', icon="✅")
        else:
            st.error(
                "La rifa no puede ser cerrada antes de la fecha de cierre.",
                icon="🚨"
            )
    else:
        st.error(
            "La rifa no puede ser cerrada, ya que esta no esta activa.",
            icon="🚨"
        )


def arreglar_todos_los_asuntos():
    with open('ajustes.json', 'r') as f:
        ajustes = json.load(f)
        f.close()

    print("Iniciando proceso, arreglar asuntos de todos los usuarios,")
    for i in range(ajustes["usuarios"]):
        arreglar_asuntos(i)
        print(f"> Proceso exitosamente aplicado a {i}")
    print("Proceso finalizado")


def modificar_valor_en_csv(
    index: int = 0, text: bool = True, nuevo_valor = "", columna: str = ""
) -> None:
    df = pd.read_csv(st.session_state.nombre_df)

    if text:
        df.at[index, columna] = str(nuevo_valor)
    else:
        df.at[index, columna] = nuevo_valor

    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    df.to_csv(st.session_state.nombre_df)
    st.success("Valor modificado", icon="✅")
    st.balloons()
    time.sleep(0.5)
    st.rerun()


def sumar_y_restar_multas(s, n, sumar=True) -> str:
    numero = lambda x: int(x) if x != "n" else 0
    s = [numero(i) for i in s]
    if sumar:
        for i in range(50):
            if s[i] < 9:
                diferencia = 9 - s[i]
                if n - diferencia > 0:
                    n -= diferencia
                    s[i] =  9
                else:
                    s[i] += n
                    n = 0
            if n <= 0:
                break
    else:
        for i in range(50):
            if n >= s[i]:
                n -= s[i]
                s[i] = 0
            else:
                s[i] -= n
                n = 0
            if n <= 0:
                break
    return "".join(
        map(
            lambda x: "n" if x == 0 else str(x),
            s
        )
    )


def sumar_y_quitar_cuotas(s, n, sumar=True) -> str:
    s = [i for i in s]
    if sumar:
        for i in range(50):
            if s[i] != "p":
                s[i] = "p"
                n -= 1
            if n <= 0:
                break
    else:
        for i in range(49, -1, -1):
            if s[i] == "p":
                s[i] = "n"
                n -= 1
            if n <= 0:
                break
    return "".join(s)


def sumar_y_quitar_deudas(s, n, sumar=True) -> str:
    s = [i for i in s]
    if sumar:
        for i in range(50):
            if s[i] == "n":
                s[i] = "d"
                n -= 1
            if n <= 0:
                break
    else:
        for i in range(49, -1, -1):
            if s[i] == "d":
                s[i] = "n"
                n -= 1
            if n <= 0:
                break
    return "".join(s)


@st.dialog('Insertar un nuevo socio')
def menu_para_insertar_socio(
    nombre: str = "", puestos: int = 0, telefono: str = ""
) -> None:

    st.divider()

    st.subheader("nombre:")
    st.write(nombre.title())
    st.subheader("puestos:")
    st.write(puestos)
    st.subheader("telefono:")
    st.write(telefono)

    st.divider()

    if st.button("Insertar"):
        insertar_socios(
            nombre=nombre,
            puestos=puestos,
            numero_telefonico=telefono
        )
        st.toast("Nuevo socio añadido", icon="🎉")
        time.sleep(1.5)
        st.rerun()


if __name__ == "__main__":
    print(
        """
        se esta ejecutando el archivo de funciones por favor.
        por favor no continue, este archivo solo contiene las 
        funciones necesarias para el programa.
        """
    )
