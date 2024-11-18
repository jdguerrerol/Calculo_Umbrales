# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 15:58:32 2024

@author: 1016099042
"""

import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Configuración de página
st.set_page_config(page_title="Umbrales de Riesgo", layout="wide")

# Inicializar atributos en st.session_state
st.session_state.setdefault("umbrales_percentiles", [])
st.session_state.setdefault("percentiles", [])
st.session_state.setdefault("colores_percentiles", [])
st.session_state.setdefault("umbrales_desviaciones", [])
st.session_state.setdefault("desviaciones", [])
st.session_state.setdefault("colores_desviaciones", [])
st.session_state.setdefault("umbrales_experto", [])
st.session_state.setdefault("colores_experto", [])

# Barra lateral
st.sidebar.title("Configuración de Umbrales 🚀")
st.sidebar.write("Ajustes y Opciones")

# Sección Principal
st.title("Umbrales de Riesgo Basados en Simulación")
st.write("Aplicación para la gestión de umbrales de riesgo en base a simulaciones de series de tiempo.")

# Función para ajustar una distribución
def ajustar_distribucion(datos):
    distribuciones = [
        stats.norm, 
        stats.expon, 
        stats.weibull_min, 
        stats.gamma, 
        stats.lognorm, 
        stats.pareto, 
        stats.beta, 
        stats.cauchy,
        stats.t, 
        stats.laplace
    ]
    
    mejor_distribucion = None
    mejor_ks_stat = np.inf
    parametros = None

    # Probar diferentes distribuciones
    for distribucion in distribuciones:
        params = distribucion.fit(datos)
        ks_stat, _ = stats.kstest(datos, distribucion.name, args=params)
        if ks_stat < mejor_ks_stat:
            mejor_ks_stat = ks_stat
            mejor_distribucion = distribucion
            parametros = params

    return mejor_distribucion, parametros

# Función para simular datos con la distribución ajustada (con semilla fija)
def simular_datos(distribucion, parametros, n=10000, seed=42):
    np.random.seed(seed)  # Fijar semilla para garantizar consistencia
    return distribucion.rvs(*parametros, size=n)

# Inicializar la lista de umbrales disponibles
umbrales_opciones = ["Apetito", "Límite de Apetito", "Tolerancia", "Capacidad", "Zona de Estrés"]
umbrales_colores = ["blue", "green", "yellow", "red", "black"]
 
# Función para eliminar umbrales
def eliminar_umbral(tipo_umbral, indice):
    if tipo_umbral == "percentiles":
        del st.session_state.umbrales_percentiles[indice]
        del st.session_state.percentiles[indice]
        del st.session_state.colores_percentiles[indice]
    elif tipo_umbral == "desviaciones":
        del st.session_state.umbrales_desviaciones[indice]
        del st.session_state.desviaciones[indice]
        del st.session_state.colores_desviaciones[indice]
    elif tipo_umbral == "experto":
        del st.session_state.umbrales_experto[indice]
        del st.session_state.colores_experto[indice]

# Función para eliminar outliers
def eliminar_outliers(datos, metodo="desviaciones", umbral=3):
    if metodo == "desviaciones":
        media = np.mean(datos)
        desviacion = np.std(datos)
        datos_filtrados = datos[(datos > media - umbral * desviacion) & (datos < media + umbral * desviacion)]
    elif metodo == "percentiles":
        limite_inferior = np.percentile(datos, 1)
        limite_superior = np.percentile(datos, 99)
        datos_filtrados = datos[(datos > limite_inferior) & (datos < limite_superior)]
    else:
        datos_filtrados = datos
    return datos_filtrados


# Cargar el archivo de datos
archivo = st.sidebar.file_uploader("Carga tu archivo histórico (Excel)", type=["xlsx"])
if archivo:
    # Leer las hojas disponibles
    excel_file = pd.ExcelFile(archivo)
    hojas = excel_file.sheet_names

    # Selector de hojas
    hoja_seleccionada = st.sidebar.selectbox("Selecciona la hoja a procesar", hojas)

    # Leer los datos de la hoja seleccionada
    datos = pd.read_excel(archivo, sheet_name=hoja_seleccionada)

    # Asegurar que la columna de fecha y los valores están correctamente seleccionados
    if datos.shape[1] >= 2:
        st.write(f"Hoja seleccionada: **{hoja_seleccionada}**")
        st.write("Vista previa de los datos cargados:")
        st.dataframe(datos.head())

        # Asumimos que la primera columna es la fecha y la segunda columna son los valores
        datos.columns = ["Fecha", "Valor"]  # Renombrar para consistencia
        datos["Fecha"] = pd.to_datetime(datos["Fecha"], errors="coerce")  # Convertir a formato fecha si aplica
        serie_tiempo = datos["Valor"]

        # Simulación de Datos
        distribucion, parametros = ajustar_distribucion(serie_tiempo)
        simulacion = simular_datos(distribucion, parametros)

        # Tabs de la aplicación
        tab_inicio, tab1, tab2, tab_resumen = st.tabs(["Inicio", "Percentiles", "Desviaciones", "Resumen"])

    with tab_inicio:
        st.header("Resumen del Indicador 📈")
        
        # Resumen descriptivo
        fecha_inicio = datos.iloc[0, 0]  # Asume que la columna 0 contiene las fechas
        fecha_fin = datos.iloc[-1, 0]
        valor_maximo = serie_tiempo.max()
        fecha_maximo = datos.iloc[serie_tiempo.idxmax(), 0]  # Obtiene la fecha del máximo
        valor_minimo = serie_tiempo.min()
        fecha_minimo = datos.iloc[serie_tiempo.idxmin(), 0]  # Obtiene la fecha del mínimo
        media = serie_tiempo.mean()
        desviacion = serie_tiempo.std()
        
        st.markdown(f"**Fecha de inicio:** {fecha_inicio}")
        st.markdown(f"**Fecha de finalización:** {fecha_fin}")
        st.markdown(f"**Media:** {media:.4f}")
        st.markdown(f"**Desviación estándar:** {desviacion:.4f}")
        st.markdown(f"**Valor máximo:** {valor_maximo:.4f} en la fecha {fecha_maximo}")
        st.markdown(f"**Valor mínimo:** {valor_minimo:.4f} en la fecha {fecha_minimo}")
        
        # Gráfico de la serie de tiempo
        st.subheader("Gráfico del Indicador")
        fig_inicio, ax_inicio = plt.subplots()
        ax_inicio.plot(datos.iloc[:, 0], serie_tiempo, label='Indicador', color='blue')
        ax_inicio.set_title("Serie de Tiempo del Indicador")
        ax_inicio.set_xlabel("Fecha")
        ax_inicio.set_ylabel("Valor")
        ax_inicio.legend()
        st.pyplot(fig_inicio)
    
    with tab1:
        st.header("Cálculo basado en Percentiles 📊")
        
        # Inicializar listas si no están presentes
        if 'umbrales_percentiles' not in st.session_state:
            st.session_state.umbrales_percentiles = []
            st.session_state.percentiles = []
            st.session_state.colores_percentiles = []
    
        # Lista para almacenar valores calculados
        valores_percentiles = []
    
        # Mostrar los umbrales existentes
        if st.session_state.umbrales_percentiles:
            for i in range(len(st.session_state.umbrales_percentiles)):
                col1, col2, col3, col4 = st.columns([1, 1, 0.2, 0.3])
                with col1:
                    umbral_seleccionado = st.selectbox(
                        f"Umbral {i+1}",
                        umbrales_opciones,
                        index=umbrales_opciones.index(st.session_state.umbrales_percentiles[i]) if st.session_state.umbrales_percentiles[i] else 0,
                        key=f"umbral_{i}"
                    )
                    st.session_state.umbrales_percentiles[i] = umbral_seleccionado
                    st.session_state.colores_percentiles[i] = umbrales_colores[umbrales_opciones.index(umbral_seleccionado)]
                with col2:
                    percentil = st.number_input(
                        f"Percentil {i+1}",
                        min_value=0,
                        max_value=100,
                        value=st.session_state.percentiles[i],
                        key=f"percentil_{i}"
                    )
                    st.session_state.percentiles[i] = percentil
                with col3:
                    valor_percentil = np.percentile(simulacion, percentil)
                    valores_percentiles.append(valor_percentil)  # Guardar el valor calculado
                    st.markdown(f"Valor {i+1}:")
                    st.write(f"{valor_percentil:.4f}")  # Mostrar el valor calculado
                with col4:
                    st.markdown(" ")
                    if st.button("❌", key=f"eliminar_percentil_{i}"):
                        eliminar_umbral("percentiles", i)
    
        # Botón para agregar un nuevo umbral
        if st.button("Agregar umbral", key="add_percentile"):
            st.session_state.umbrales_percentiles.append(umbrales_opciones[0])  # Agregar umbral predeterminado
            st.session_state.percentiles.append(10)  # Percentil inicial predeterminado
            st.session_state.colores_percentiles.append(umbrales_colores[0])  # Color predeterminado
    
        # Gráfico con outliers
        st.subheader("Con Outliers")
        fig_con_outliers, ax_con_outliers = plt.subplots()
        ax_con_outliers.plot(serie_tiempo, label='Serie de Tiempo', color='black')
    
        for i in range(len(st.session_state.umbrales_percentiles)):
            valor_percentil = np.percentile(simulacion, st.session_state.percentiles[i])
            ax_con_outliers.axhline(valor_percentil, color=st.session_state.colores_percentiles[i], linestyle='--', label=st.session_state.umbrales_percentiles[i])
    
        ax_con_outliers.set_title("Serie de Tiempo con Umbrales de Percentiles (Con Outliers)")
        ax_con_outliers.legend()
        st.pyplot(fig_con_outliers)
    
        # Gráfico sin outliers
        st.subheader("Sin Outliers (Percentiles)")
        serie_sin_outliers = eliminar_outliers(simulacion, metodo="percentiles")
        fig_sin_outliers, ax_sin_outliers = plt.subplots()
        ax_sin_outliers.plot(serie_tiempo, label='Serie de Tiempo', color='black')
    
        for i in range(len(st.session_state.umbrales_percentiles)):
            valor_percentil = np.percentile(serie_sin_outliers, st.session_state.percentiles[i])
            ax_sin_outliers.axhline(valor_percentil, color=st.session_state.colores_percentiles[i], linestyle='--', label=f"Sin Outliers - {st.session_state.umbrales_percentiles[i]}")
    
        ax_sin_outliers.set_title("Serie de Tiempo con Umbrales de Percentiles (Sin Outliers)")
        ax_sin_outliers.legend()
        st.pyplot(fig_sin_outliers)

        
    with tab2:
        st.header("Cálculo basado en Desviaciones Estándar 🎯")
    
        # Inicializar listas si no están presentes
        if 'umbrales_desviaciones' not in st.session_state:
            st.session_state.umbrales_desviaciones = []
            st.session_state.desviaciones = []
            st.session_state.colores_desviaciones = []
    
        # Lista para almacenar valores calculados
        valores_desviaciones = []
    
        # Mostrar los umbrales existentes
        if st.session_state.umbrales_desviaciones:
            for i in range(len(st.session_state.umbrales_desviaciones)):
                col1, col2, col3, col4 = st.columns([1, 1, 0.3, 0.3])
                with col1:
                    umbral_seleccionado = st.selectbox(
                        f"Umbral {i+1}",
                        umbrales_opciones,
                        index=umbrales_opciones.index(st.session_state.umbrales_desviaciones[i]) if st.session_state.umbrales_desviaciones[i] else 0,
                        key=f"umbral_std_{i}"
                    )
                    st.session_state.umbrales_desviaciones[i] = umbral_seleccionado
                    st.session_state.colores_desviaciones[i] = umbrales_colores[umbrales_opciones.index(umbral_seleccionado)]
                with col2:
                    num_desviaciones = st.number_input(
                        f"Desviaciones {i+1}",
                        value=st.session_state.desviaciones[i] if len(st.session_state.desviaciones) > i else 0.0,
                        key=f"desviacion_{i}"
                    )
                    st.session_state.desviaciones[i] = num_desviaciones
                with col3:
                    valor_umbral = np.mean(simulacion) + (num_desviaciones * np.std(simulacion))
                    valores_desviaciones.append(valor_umbral)  # Guardar el valor calculado
                    st.markdown(f"Valor {i+1}:")
                    st.write(f"{valor_umbral:.4f}")  # Mostrar el valor calculado
                with col4:
                    st.markdown(" ")
                    if st.button("❌", key=f"eliminar_desviacion_{i}"):
                        eliminar_umbral("desviaciones", i)
    
        # Botón para agregar un nuevo umbral
        if st.button("Agregar umbral", key="add_std"):
            st.session_state.umbrales_desviaciones.append(umbrales_opciones[0])  # Agregar umbral predeterminado
            st.session_state.desviaciones.append(1.0)  # Número de desviaciones inicial
            st.session_state.colores_desviaciones.append(umbrales_colores[0])  # Color predeterminado
    
        # Cálculo y gráfico con outliers
        st.subheader("Con Outliers")
        media = np.mean(simulacion)
        desviacion = np.std(simulacion)
        fig_std_con_outliers, ax_std_con_outliers = plt.subplots()
        ax_std_con_outliers.plot(serie_tiempo, label='Serie de Tiempo', color='black')
    
        for i in range(len(st.session_state.umbrales_desviaciones)):
            valor_umbral = media + (st.session_state.desviaciones[i] * desviacion)
            ax_std_con_outliers.axhline(valor_umbral, color=st.session_state.colores_desviaciones[i], linestyle='--', label=st.session_state.umbrales_desviaciones[i])
    
        ax_std_con_outliers.set_title("Serie de Tiempo con Umbrales de Desviaciones Estándar (Con Outliers)")
        ax_std_con_outliers.legend()
        st.pyplot(fig_std_con_outliers)
    
        # Cálculo y gráfico sin outliers
        st.subheader("Sin Outliers (Desviaciones Estándar)")
        serie_sin_outliers = eliminar_outliers(simulacion, metodo="desviaciones")
        media_sin_outliers = np.mean(serie_sin_outliers)
        desviacion_sin_outliers = np.std(serie_sin_outliers)
        fig_std_sin_outliers, ax_std_sin_outliers = plt.subplots()
        ax_std_sin_outliers.plot(serie_tiempo, label='Serie de Tiempo', color='black')
    
        for i in range(len(st.session_state.umbrales_desviaciones)):
            valor_umbral = media_sin_outliers + (st.session_state.desviaciones[i] * desviacion_sin_outliers)
            ax_std_sin_outliers.axhline(valor_umbral, color=st.session_state.colores_desviaciones[i], linestyle='--', label=f"Sin Outliers - {st.session_state.umbrales_desviaciones[i]}")
    
        ax_std_sin_outliers.set_title("Serie de Tiempo con Umbrales de Desviaciones Estándar (Sin Outliers)")
        ax_std_sin_outliers.legend()
        st.pyplot(fig_std_sin_outliers)

    
    with tab_resumen:
        st.header("Resumen de Umbrales 📑")
        
        # Inicializar listas para almacenar los valores
        resumen_percentiles = []
        resumen_desviaciones = []
    
        # Calcular valores para percentiles (con y sin outliers)
        for i in range(len(st.session_state.umbrales_percentiles)):
            # Con outliers
            valor_percentil_con = np.percentile(simulacion, st.session_state.percentiles[i])
            # Sin outliers
            serie_sin_outliers = eliminar_outliers(simulacion, metodo="percentiles")
            valor_percentil_sin = np.percentile(serie_sin_outliers, st.session_state.percentiles[i])
            # Agregar al resumen
            resumen_percentiles.append((
                st.session_state.umbrales_percentiles[i],
                st.session_state.percentiles[i],
                valor_percentil_con,
                valor_percentil_sin
            ))
    
        # Calcular valores para desviaciones estándar (con y sin outliers)
        media = np.mean(simulacion)
        desviacion = np.std(simulacion)
        media_sin_outliers = np.mean(eliminar_outliers(simulacion, metodo="desviaciones"))
        desviacion_sin_outliers = np.std(eliminar_outliers(simulacion, metodo="desviaciones"))
    
        for i in range(len(st.session_state.umbrales_desviaciones)):
            # Con outliers
            valor_desviacion_con = media + (st.session_state.desviaciones[i] * desviacion)
            # Sin outliers
            valor_desviacion_sin = media_sin_outliers + (st.session_state.desviaciones[i] * desviacion_sin_outliers)
            # Agregar al resumen
            resumen_desviaciones.append((
                st.session_state.umbrales_desviaciones[i],
                st.session_state.desviaciones[i],
                valor_desviacion_con,
                valor_desviacion_sin
            ))
    
        # Mostrar los resultados en la interfaz
        if resumen_percentiles or resumen_desviaciones:
            st.subheader("Resultados de los Umbrales")
    
            # Mostrar resultados de Percentiles
            if resumen_percentiles:
                st.markdown("### Percentiles")
                for umbral, percentil, con_outliers, sin_outliers in resumen_percentiles:
                    st.write(
                        f"**{umbral}** - Percentil: {percentil}%  | "
                        f"  **Con Outliers**: {con_outliers:.4f}  | "
                        f"  **Sin Outliers**: {sin_outliers:.4f}"
                    )
    
            # Mostrar resultados de Desviaciones Estándar
            if resumen_desviaciones:
                st.markdown("### Desviaciones Estándar")
                for umbral, desviaciones, con_outliers, sin_outliers in resumen_desviaciones:
                    st.write(
                        f"**{umbral}** - Desviaciones: {desviaciones}  | "
                        f"  **Con Outliers**: {con_outliers:.4f}  | "
                        f"  **Sin Outliers**: {sin_outliers:.4f}"
                    )
        else:
            st.write("No se han configurado umbrales aún.")