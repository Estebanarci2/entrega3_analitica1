# Cargar datos
import numpy as np
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import base64


# Utilizar la página completa en lugar de una columna central estrecha
st.set_page_config(layout="wide")

# Título principal, h1 denota el estilo del título 1
st.markdown("<h1 style='text-align: center; color: #951F0F;'>Análisis datos de la NBA 🏀</h1>", unsafe_allow_html=True)
#----------------------------------------

#CARGAR DATOS

birth1 = pd.read_csv('birth1.csv') #DF completo de birthplace
data1 = pd.read_csv('data1.csv') #DF completo de data
draft1 = pd.read_csv('draft1.csv') #DF completo del draft
draft_groups = pd.read_csv('draft_groups.csv') #Bodega con jugador, posición del draft, categoría del -- draft draft_tabla
draft_stats = pd.read_csv('draft_stats.csv') #Bodega con jugador, promedios de peso, altura, agilidad, velocidad
state_year = pd.read_csv('state_year.csv') #Bodega con jugador, estado y años que ha jugado en la NBA -- birth_tabla
team_pos = pd.read_csv('team_pos.csv') #Bodega con jugador, equipos a los que ha pertenecido y posición -- data_tabla
coord = pd.read_excel('coordenadas.xlsx') #coordenadas de cada estado de EE.UU
dic = {'DC':'Washington'}
birth1['state'] = birth1['state'].replace(dic)


# Función para descargar base de datos de birth place
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="birth_place.csv">Descargar archivo csv de birth_place</a>'
    return href

# Función para descargar base de datos con mas estadísticas 
def get_table_download_link2(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Descargar archivo csv de mas estadísticas</a>'
    return href

# Función para descargar base de datos de los draft
def get_table_download_link3(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="draft.csv">Descargar archivo csv de draft</a>'
    return href

# Función para descargar base de datos jugadores, equipo y posición
def get_table_download_link4(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="draft_groups.csv">Descargar archivo csv con jugador, posición del draft, categoría del</a>'
    return href

# Función para descargar base de datos jugadores con sus atributos y draft pick
def get_table_download_link5(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="draft_stats.csv">Descargar archivo csv de jugadores con sus atributos y draft pick</a>'
    return href

# Función para descargar base de datos jugadores, estado y región
def get_table_download_link6(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="birth_player.csv">Descargar archivo csv de cantidad de jugadores por estado y región</a>'
    return href

# Función para descargar base de datos jugadores, estado y región
def get_table_download_link7(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="team_pos.csv">Descargar archivo csv de jugadores por equipo y posición</a>'
    return href

# Función para descargar base de datos jugadores, estado y región
def get_table_download_link8(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="coordinates.csv">Descargar archivo csv de coordenadas de estados de EE.UU</a>'
    return href

#----------------------------------------
c1, c2, c3, c4= st.columns((1,1,1,1)) # Dividir el ancho en 4 columnas de igual tamaño

#--------------- Top anotadores de 3 puntos
c1.markdown("<h3 style='text-align: center; color: grey;'> Top 3 anotadores de 3 puntos </h3>", unsafe_allow_html=True)

# Obtener el top 3 de jugadores con más puntos triples
top_3_triples = birth1.nlargest(3, "3p")

# Seleccionar las columnas "PLAYER" y "3P" para el top 13
jugadores_top_3 = top_3_triples[["player", "3p"]]

c1.text('TOP 1: '+str(jugadores_top_3.iloc[0,0])+', '+str(jugadores_top_3.iloc[0,1])+'')
c1.text('TOP 2: '+str(jugadores_top_3.iloc[1,0])+', '+str(jugadores_top_3.iloc[1,1])+'')
c1.text('TOP 3: '+str(jugadores_top_3.iloc[2,0])+', '+str(jugadores_top_3.iloc[2,1])+'')

#--------------- jugador mas y menos eficiente de puntos por partido jugado
c2.markdown("<h3 style='text-align: center; color: grey;'> Top eficiencia points/games </h3>", unsafe_allow_html=True)

# Calcular la eficiencia de puntos por partido
birth1["efficiency"] = birth1["pts"] / birth1["g"]

# Encontrar el jugador más eficiente en términos de puntos por partido jugado
jugador_mas_eficiente = birth1.loc[birth1["efficiency"].idxmax()]
jugador_menos_eficiente = birth1.loc[birth1["efficiency"].idxmin()]

c2.text('Mas: '+str(jugador_mas_eficiente['player'])+', '+str(jugador_mas_eficiente['efficiency'])+'')
c2.text('Menos: '+str(jugador_menos_eficiente['player'])+', '+str(jugador_menos_eficiente['efficiency'])+'')

#--------------- top 5 estados con mas jugadores
c3.markdown("<h3 style='text-align: center; color: grey;'> Top 5 estados con mas jugadores en la NBA </h3>", unsafe_allow_html=True)

#Agrupar por estado y sacar el top 5
top_5 = birth1.groupby(['state'])[['player']].count()
top_5 = top_5.nlargest(5, "player").reset_index()

c3.text('TOP 1: '+str(top_5.iloc[0,0])+', '+str(top_5.iloc[0,1])+'')
c3.text('TOP 2: '+str(top_5.iloc[1,0])+', '+str(top_5.iloc[1,1])+'')
c3.text('TOP 3: '+str(top_5.iloc[2,0])+', '+str(top_5.iloc[2,1])+'')
c3.text('TOP 4: '+str(top_5.iloc[3,0])+', '+str(top_5.iloc[3,1])+'')
c3.text('TOP 5: '+str(top_5.iloc[4,0])+', '+str(top_5.iloc[4,1])+'')

#--------------- Distribución de los jugadores en EE.UU
c4.markdown("<h3 style='text-align: center; color: grey;'> Distribución de los jugadores por región </h3>", unsafe_allow_html=True)

# Calcular el porcentaje de jugadores por región
tabla_porcentaje = birth1.groupby('region').agg({'player': 'count'})
tabla_porcentaje['porcentaje'] = tabla_porcentaje['player'] / tabla_porcentaje['player'].sum() 

c4.write(tabla_porcentaje)

#---------------------------------------------------------------------
# Título de la siguiente sección
st.markdown("<h3 style='text-align: center; color: black;'> ¿Cómo ha sido la evolución del promedio de los principales atributos de los jugadores en cada año del draft? </h3>", unsafe_allow_html=True)

#serie de tiempo anual de los promedios de atributos mas relevantes de los jugadores en el draft

#Se grafican los promedios de cada variable por año
# definir gráfica
fig = px.line(draft_stats, x ='año', y=['height_mean', 'weight_mean', 'vertical_mean','agility_mean'], 
              title ='<b>atributos promedio draft_stats<b>',width=1100, height=450)

# agregar detalles
fig.update_layout(
    xaxis_title = 'índice',
    yaxis_title = 'valor',
    template = 'simple_white',
    title_x = 0.5,
    legend_title = 'nombre del atributo:')

# Enviar gráfica a streamlit
st.plotly_chart(fig)

#---------------------------------------------------------------------
st.markdown("<h3 style='text-align: center; color: black;'> ¿Existe alguna relación entre los atributos de los jugadores que escoge la NBA? </h3>", unsafe_allow_html=True)

#cuál es la relación entre el peso, la altura, el alcance vertical, y la agilidad

# definir figura
fig = px.parallel_coordinates(draft1, color ='year', labels = ['year'],
                        dimensions = ['weight', 'height', 'vertical', 'agility','draft_pick'],
                        color_continuous_scale = px.colors.diverging.Tealrose, width=1100, height=450)

st.plotly_chart(fig)

#---------------------------------------------------------------------------
st.markdown("<h3 style='text-align: center; color: black;'> ¿Cómo está distribuído el historial del draft pick? </h3>", unsafe_allow_html=True)

#Pareto con la suma de los jugadores que pertenecieron a cada categoría del draft_pick

#crear base
draft_groups['category'] = draft_groups['category'].astype(str)
df0 = draft_groups.groupby(['category'])[['player']].count().sort_values('player', ascending = False).rename(columns={'player':'counts'})
df0['ratio'] = df0.apply(lambda x: x.cumsum()/df0['counts'].sum())

# definir figura
fig = go.Figure([go.Bar(x=df0.index, y=df0['counts'], yaxis='y1', name='total jugadores'),
                 go.Scatter(x=df0.index, y=df0['ratio'], yaxis='y2', name='porcentaje acumulado', hovertemplate='%{y:.1%}', marker={'color': '#000000'})])

# agregar detalles
fig.update_layout(template='plotly_white', width=1100, 
                  height=450, showlegend=False, hovermode='x', bargap=.3,
                  title={'text': '<b>Pareto # de jugadores por draft pick<b>', 'x': .5}, 
                  yaxis={'title': 'jugadores'},
                  yaxis2={'rangemode': "tozero", 'overlaying': 'y', 'position': 1, 'side': 'right', 'title': 'ratio', 'tickvals': np.arange(0, 1.1, .2), 'tickmode': 'array', 'ticktext': [str(i) + '%' for i in range(0, 101, 20)]})

# Enviar gráfica a streamlit
st.plotly_chart(fig)

#---------------------------------------------------------------------------
c1, c2 = st.columns((1,1)) # Dividir el ancho en 2 columnas de igual tamaño

c1.markdown("<h3 style='text-align: center; color: black;'> ¿Cómo están distribuídos los jugadores según la divisón a la que pertenece su equipo? </h3>", unsafe_allow_html=True)

#¿Cómo están distribuídos los jugadores según la divisón a la que pertenece su equipo?

# crear dataset
base = data1.groupby(['division'])[['player']].count().reset_index()

# sacar valor total de los jugadores en el DF
cant_jugadores = data1['player'].count()

# hacer la gráfica
fig = px.pie(base , values = 'player', names = 'division', title = '<b>% Jugadores<b>',
             hole = .5)

# poner detalles a la gráfica
fig.update_layout(
    template = 'simple_white',
    legend_title = 'División',
    width=370,
    height=370,
    title_x = 0.5,
    annotations = [dict(text = str(cant_jugadores), x=0.5, y = 0.5, font_size = 40, showarrow = False )])

c1.plotly_chart(fig)


#---------------------------------------------------------------------
c2.markdown("<h3 style='text-align: center; color: black;'> Rango de años que llevan los jugadores en la NBA </h3>", unsafe_allow_html=True)

# Calcular el número de grupos necesarios
num_grupos = (state_year['yrs'].max() - 1) // 5 + 1

# Definir los límites para los grupos de años
limites = list(range(1, 5 * num_grupos + 1, 5))

# Definir las etiquetas de los grupos
etiquetas = [f'{limite - 5}-{limite-1}' for limite in limites[1:]]

# Agregar una columna con las agrupaciones
state_year['group'] = pd.cut(state_year['yrs'], bins=limites, labels=etiquetas, include_lowest=True)

# Crear categoría para organizar el orden de las edades
state_year['group2'] = state_year['group'].replace({'1-5':'1',
                              '6-10':'2',
                              '11-15':'3',
                              '16-20':'4',
                              '21-25':'5'})

# Aplicar orden al DataFrame
state_year= state_year.sort_values('group2',ascending = False)

#Crear base para la gráfica 
state_year2 = state_year.groupby(['group'])[['player']].count().reset_index().rename(columns = {'player':'jugadores'})

# Hacer gráfica
fig = px.bar(state_year2 , x="jugadores", y="group", orientation='h', width=370,  height=370)
fig.update_layout(xaxis_title="<b>Jugador<b>",
                  yaxis_title="<b>Grupo", template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')

# Enviar gráfica a streamlit
c2.plotly_chart(fig)

#---------------------------------------------------------------------

# Agrupar por región y estado y contar el número de jugadores
region_state_counts = birth1.groupby(['region', 'state']).size().reset_index(name='jugadores')

# Configurar la visualización del mapa en Streamlit
st.markdown("<h3 style='text-align: center; color: black;'>Puedes interactuar con las regiones de la tabla dentro del checkbox</h3>", unsafe_allow_html=True)

# Mostrar selectbox para seleccionar una región
region_selected = st.selectbox('Selecciona una región', region_state_counts['region'].unique())


# Filtrar los datos según la región seleccionada
filtered_data = region_state_counts[region_state_counts['region'] == region_selected]

# Hacer un checkbox
if st.checkbox('Obtener datos de jugadores por region y estado', False):

    
    # Código para convertir el DataFrame en una tabla plotly resumen
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(filtered_data.columns),
        fill_color='lightgrey',
        line_color='darkslategray'),
        cells=dict(values=[filtered_data.region, filtered_data.state, filtered_data.jugadores]
                   ,fill_color='white',line_color='lightgrey'))
       ])
    fig.update_layout(width=1100, height=450)

# Enviar tabla a streamlit
    st.write(fig)

#---------------------------------------------------------------------
st.markdown("<h3 style='text-align: center; color: black;'>Aquí tienes el link de descarga de los DataFrame originales</h3>", unsafe_allow_html=True)


# Generar link de descarga
st.markdown(get_table_download_link(birth1), unsafe_allow_html=True)
st.markdown(get_table_download_link2(data1), unsafe_allow_html=True)
st.markdown(get_table_download_link3(draft1), unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: black;'>Y finalmente algunas de las bodegas de datos</h3>", unsafe_allow_html=True)

# Generar link de descarga
st.markdown(get_table_download_link4(draft_groups), unsafe_allow_html=True)
st.markdown(get_table_download_link5(draft_stats), unsafe_allow_html=True)
st.markdown(get_table_download_link6(state_year), unsafe_allow_html=True)
st.markdown(get_table_download_link7(team_pos), unsafe_allow_html=True)
st.markdown(get_table_download_link8(coord), unsafe_allow_html=True)
