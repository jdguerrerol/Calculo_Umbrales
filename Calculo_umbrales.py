# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 18:57:25 2024

@author: 1016099042
"""

# streamlit run "Z:\info_Juan_David\Aplicativo Calculo de Umbrales\CalculoUmbrales_201124.py"

import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64

# Función para generar el archivo PDF

from datetime import datetime  # Para obtener la fecha actual

from datetime import datetime
from fpdf import FPDF

# Clase personalizada para manejar pie de página
class PDFWithFooter(FPDF):
    def footer(self):
        self.set_y(-15)  # Posición desde la parte inferior
        self.set_font("Arial", size=10)
        self.cell(0, 10, "Documento generado con la Calculadora de Umbrales de Riesgo", align="C")
        self.cell(0, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", ln=True, align="R")

# Función para generar el archivo PDF
def generar_pdf(nombre_indicador, resumen_percentiles, resumen_desviaciones, fig_indicador, fig_percentiles, fig_desviaciones):
    pdf = PDFWithFooter()  # Usa la clase personalizada
    pdf.set_auto_page_break(auto=True, margin=15)

    # Ruta del logo
    logo_path = 'logo_pdf2.JPG'  # Cambia por la ruta del logo
    
    # Portada
    pdf.add_page()
    pdf.image(logo_path, x=10, y=8, w=50)  # Logo en la portada
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, txt="Reporte de Umbrales de Riesgo", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Indicador: {nombre_indicador}", ln=True, align="C")
    pdf.ln(20)

    # Resumen del Indicador
    pdf.set_font("Arial", size=14, style="B")
    pdf.cell(200, 10, txt="Resumen del Indicador", ln=True, align="L")
    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.cell(0, 10, txt="Percentiles y desviaciones configurados:", ln=True)
    pdf.ln(5)

    # Percentiles
    if resumen_percentiles:
        pdf.cell(0, 10, txt="Umbrales por Percentiles:", ln=True)
        for umbral, percentil, con_outliers, sin_outliers in resumen_percentiles:
            pdf.cell(0, 10, txt=f"{umbral} - Percentil: {percentil}% | Con Outliers: {con_outliers:.2f} | Sin Outliers: {sin_outliers:.2f}", ln=True)
        pdf.ln(5)

    # Desviaciones
    if resumen_desviaciones:
        pdf.cell(0, 10, txt="Umbrales por Desviaciones:", ln=True)
        for umbral, desviaciones, con_outliers, sin_outliers in resumen_desviaciones:
            pdf.cell(0, 10, txt=f"{umbral} - Desviaciones: {desviaciones} | Con Outliers: {con_outliers:.2f} | Sin Outliers: {sin_outliers:.2f}", ln=True)
        pdf.ln(5)

    # Guardar gráficos temporalmente para incluirlos en el PDF
    fig_indicador.savefig("indicador.png")
    fig_percentiles.savefig("percentiles.png")
    fig_desviaciones.savefig("desviaciones.png")

    # Insertar gráficos
    def agregar_pagina_con_logo(pdf, img_path, titulo):
        pdf.add_page()
        pdf.image(logo_path, x=10, y=8, w=50)  # Logo en la parte superior
        pdf.ln(30)  # Espacio para separar el logo del contenido
        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(200, 10, txt=titulo, ln=True, align="C")
        pdf.image(img_path, x=15, y=50, w=180)  # Inserta el gráfico

    # Agregar gráficos al PDF
    agregar_pagina_con_logo(pdf, "indicador.png", "Gráfico del Indicador")
    agregar_pagina_con_logo(pdf, "percentiles.png", "Gráfico de Percentiles")
    agregar_pagina_con_logo(pdf, "desviaciones.png", "Gráfico de Desviaciones")

    return pdf



# Configuración de página
st.set_page_config(page_title="📊 Umbrales de Riesgo", layout="wide")

# Estilo personalizado con fondo en la barra lateral
# Estilo personalizado con fondo en la barra lateral y texto blanco

st.markdown(
    """
    <style>
    /* Fondo personalizado de la barra lateral */
    [data-testid="stSidebar"] {
        background-image: url("https://img.freepik.com/foto-gratis/resumen-borroso-estudio-degradado-verde-vacio-bien-uso-como-fondo-plantilla-sitio-web-marco-informe-empresarial_1258-52607.jpg");
        background-size: cover;
        color: white; /* Cambia el color del texto en la barra lateral */
    }
    
    /* Asegura que los títulos y subtítulos sean blancos */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] h5, 
    [data-testid="stSidebar"] h6, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] div {
        color: white !important; /* Forza el texto blanco */
    }

    /* Asegura que las etiquetas de texto y widgets sean blancas */
    [data-testid="stSidebar"] .css-h5rgaw, 
    [data-testid="stSidebar"] .css-1n76uvr, 
    [data-testid="stSidebar"] .css-1vbd788, 
    [data-testid="stSidebar"] .css-2trqyj {
        color: white !important;
    }

    /* Mantén el texto negro para el área de carga de archivos */
    [data-testid="stSidebar"] .stFileUploader label,
    [data-testid="stSidebar"] .stFileUploader div {
        color: black !important; /* Asegura contraste en la carga de archivos */
    }
    
    /* Contenedor para el logo en el sidebar */
    .sidebar-logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    .sidebar-logo-container img {
        max-width: 100px; /* Ajusta el tamaño del logo */
        max-height: 100px;
    }
    
    /* Cambiar el fondo del botón de descarga */
    .stDownloadButton>button {
        background-color: #4CAF50; /* Color de fondo (verde) */
        color: white; /* Color del texto */
        border: none; /* Quitar borde */
        padding: 10px 20px; /* Espaciado interno */
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px; /* Bordes redondeados */
    }

    /* Cambiar el fondo al pasar el mouse por encima */
    .stDownloadButton>button:hover {
        background-color: #45a049; /* Color más oscuro al pasar el mouse */
    }
    </style>
    """,
    unsafe_allow_html=True
)




# Añadir CSS con margen superior negativo para subir el logo
st.sidebar.markdown("""
    <style>
    .sidebar-logo {
        margin-top: -30px; /* Ajusta este valor según sea necesario */
    }
    </style>
""", unsafe_allow_html=True)

# Mostrar el logo con la clase personalizada
st.sidebar.image('logo-bp2.png', use_container_width=False, width=250)

# Barra lateral
#st.sidebar.title("⚙️ Configuración")
#st.sidebar.write("Selecciona los ajustes iniciales.")

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
#st.sidebar.title("Configuración de umbrales")
#st.sidebar.write("Ajustes y opciones")

# Sección Principal
st.title("📊 Calculadora de umbrales")

st.write("""
    Esta aplicación te permite calcular y visualizar umbrales de riesgo basados en series de tiempo. 
    Puedes cargar un archivo de Excel, ajustar umbrales utilizando percentiles o desviaciones estándar 
    y generar reportes en PDF para compartir tus resultados.
""")

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

    # Nota explicativa para la carga de información
st.sidebar.markdown("""
    ### 📂 Carga de datos
    Carga un archivo de Excel en formato .xlsx. 
    Asegúrate de que:
    - La primera columna contiene fechas.
    - La segunda columna contiene valores numéricos.
    - No hay celdas vacías en estas columnas.
""")

with open("Muestra.xlsx", "rb") as file:
            st.sidebar.download_button(
                label="📥 Descargar archivo de muestra",
                data=file,
                file_name="archivo_muestra.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)    
        

   
# Cargar el archivo de datos
archivo = st.sidebar.file_uploader(" ", type=["xlsx"])
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
        #st.write(f"Hoja seleccionada: **{hoja_seleccionada}**")
        #st.write("Vista previa de los datos cargados:")
        st.markdown(f"<p class='big-font'>📋 Hoja seleccionada: {hoja_seleccionada}</p>", unsafe_allow_html=True)
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
            st.header("📈 Resumen del Indicador")
            st.write("""
                Aquí puedes visualizar un resumen general de tu serie de tiempo, incluyendo 
                estadísticas descriptivas y un gráfico que muestra su evolución.
            """)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("📅 Fecha de Inicio", datos["Fecha"].min().strftime('%Y-%m-%d'), "Fecha del primer dato en tu serie.")
            col2.metric("📅 Fecha de Fin", datos["Fecha"].max().strftime('%Y-%m-%d'), "Fecha del último dato en tu serie.")
            col3.metric("🔢 Total Registros", len(datos), "Número total de observaciones en tu serie.")

            col4, col5, col6 = st.columns(3)
            col4.metric("🔹 Media", f"{serie_tiempo.mean():.2f}")
            col5.metric("🔸 Desviación Estándar", f"{serie_tiempo.std():.2f}")
            col6.metric("🔺 Valor Máximo", f"{serie_tiempo.max():.2f}", f"en {datos.loc[serie_tiempo.idxmax(), 'Fecha']}")

            st.subheader("📊 Gráfico del Indicador")
            fig, ax = plt.subplots()
            ax.plot(datos["Fecha"], serie_tiempo, label="Serie de Tiempo", color="blue")
            ax.set_title("Evolución del Indicador")
            ax.set_xlabel("Fecha")
            ax.set_ylabel("Valor")
            ax.legend()
            st.pyplot(fig)
    
        with tab1:
            st.header("Cálculo basado en Percentiles 📊")

            # Nota explicativa
            st.write("""
                Utiliza percentiles para definir umbrales que dividan tu serie de tiempo 
                en partes específicas. Por ejemplo:
                - El **Percentil 10** indica el valor por debajo del cual se encuentra el 10% de los datos.
                - El **Percentil 90** indica el valor por debajo del cual se encuentra el 90% de los datos.
            """)
            st.info("""
                1️⃣ Presiona en "Agregar Umbral" y selecciona un nombre para cada umbral (por ejemplo, Apetito, Límite, etc.).  
                2️⃣ Ingresa el valor del percentil que deseas para cada umbral (entre 0 y 100).  
                3️⃣ Observa el gráfico para visualizar los umbrales configurados.  
                4️⃣ Agrega o elimina umbrales según sea necesario.
            """)
            
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

            st.write("""
                Define umbrales basados en la dispersión de los datos respecto a su media. 
                Las desviaciones estándar son útiles para identificar valores extremos.
            """)
            st.warning("""
                1️⃣ Presiona en "Agregar Umbral" y selecciona un nombre para cada umbral (por ejemplo, Apetito, Límite, etc.).  
                2️⃣ Define cuántas desviaciones estándar quieres aplicar (por ejemplo, 1, 2, ... o -1,-2,... según corresponda).  
                3️⃣ Observa cómo cambian los límites en el gráfico según tu configuración.  
                4️⃣ Elimina umbrales si ya no los necesitas.
            """)
                    
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
    
        
        # Pestaña Resumen
        with tab_resumen:
            st.header("Resumen de Umbrales 📑")
            
            st.write("""
                Consulta un resumen de todos los umbrales configurados. 
                Compara los valores calculados **con** y **sin outliers** para cada configuración.
            """)
            
            st.info("""
                📄 **Generar Reporte en PDF**  
                - Haz clic en el botón para generar un archivo PDF con todos los detalles, gráficos y configuraciones.  
                - El reporte incluirá un resumen de tus configuraciones y un pie de página con la fecha de creación.
            """)
            
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
            
            # Botón para descargar el resumen en PDF
            st.subheader("Descargar Resumen 📄")
            if st.button("📄 Generar PDF"):
                nombre_indicador = f"{hoja_seleccionada}"
                pdf = generar_pdf(
                    nombre_indicador,
                    resumen_percentiles,
                    resumen_desviaciones,
                    fig,  # Figura del gráfico principal
                    fig_con_outliers,  # Figura de percentiles
                    fig_std_con_outliers  # Figura de desviaciones
                )
                # Guardar PDF en archivo temporal
                pdf.output("reporte_umbral.pdf")
                # Leer el archivo generado y convertirlo a Base64 para descarga
                with open("reporte_umbral.pdf", "rb") as pdf_file:
                    pdf_data = pdf_file.read()
                b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
                pdf_href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="reporte_umbral.pdf">📥 Descargar Resumen PDF</a>'
                st.markdown(pdf_href, unsafe_allow_html=True)
