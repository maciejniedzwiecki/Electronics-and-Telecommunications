import dash
from dash import dcc, html, dash_table, ctx
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import time
import dash_bootstrap_components as dbc

# Połączenie z MongoDB Atlas
uri = "mongodb+srv://TestUser:TestUser@cluster0.sxqy8it.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print(f"{time.time()} - Połączono z MongoDB!")
except Exception as e:
    print(e)

# Baza i kolekcja
db = client['Radioprogramowalne']
collection = db['PUT']

external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",
    "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap"
]

# Aplikacja Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Layout aplikacji
app.layout = html.Div([
    html.H1(
        "Wizualizacja Mocy i Częstotliwości",
        className="text-center",
        style={
            "textAlign": "center",
            "fontWeight": "600",
            "fontSize": "2rem",
            "color": "#1975FA",
            "margin": "20px 0px",
        }
    ),

    html.Div([
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date_placeholder_text="Wybierz datę",
            display_format='YYYY-MM-DD',
            style={'padding': '10px'}
        )
        ,
        dcc.Dropdown(
            id='value-dropdown',
            options=[],
            value=[],
            placeholder="Wybierz ID USRP",
            searchable=False,
            multi=True,
            style={'minWidth': '200px'}
        )
    ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'}),

    dcc.Interval(
        id='interval-component',
        interval=15 * 1000,
        n_intervals=0
    ),

    dcc.Tabs([
        dcc.Tab(label='Wykres 2D', children=[
            html.Div([
                dcc.Graph(id='spectral-usage-graph')
            ])
        ]),
        dcc.Tab(label='Wykres 3D', children=[
            html.Div([
                dcc.Graph(id='spectral-usage-3d-graph')
            ])
        ]),
        dcc.Tab(label='Kanały', children=[
            html.Div([
                dcc.Graph(id='channel-power-graph'),
                dcc.Slider(id='time-slider', step=1, tooltip={"placement": "bottom", "always_visible": True}),
            ], style={'padding': '20px'}),
            dcc.Graph(id='channel-180-graph'),
            dcc.Graph(id='channel-200-graph')

        ])
    ])
])


@app.callback(
    [Output('value-dropdown', 'options'),
     Output('value-dropdown', 'value')],
    Input('interval-component', 'n_intervals'),
    Input('value-dropdown', 'value'),
    prevent_initial_call=False
)
def update_dropdown(n_intervals, selected):
    data = list(collection.find({}, {'ID': 1}))
    df = pd.DataFrame(data)

    if 'ID' not in df.columns:
        return [], []

    unique_ids = sorted(df['ID'].dropna().unique())
    options = [{'label': 'Wybierz wszystko', 'value': 'ALL'}] + [{'label': str(u), 'value': u} for u in unique_ids]
    all_values = [u for u in unique_ids]

    if not selected:
        return options, all_values

    if 'ALL' in selected:
        return options, all_values

    return options, selected

#WYKRES OGÓLNY
@app.callback(
    Output('spectral-usage-graph', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('interval-component', 'n_intervals'),
     Input('value-dropdown', 'value')]
)
def update_graph(start_date, end_date, n_intervals, selected_ids):
    data = list(collection.find({}))
    df = pd.DataFrame(data)

    if '_id' in df.columns:
        df.drop(columns=['_id'], inplace=True)

    df['Time'] = pd.to_datetime(df['Time'])

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    filtered_df = df[(df['Time'] >= start_date) & (df['Time'] < (end_date + pd.Timedelta(days=1)))]

    if selected_ids:
        filtered_df = filtered_df[filtered_df['ID'].isin(selected_ids)]

    # Dodanie kanałów bocznych do wykresu
    extra_rows = []
    for _, row in filtered_df.iterrows():
        if isinstance(row['Channel_Powers'], list) and len(row['Channel_Powers']) == 2:
            span = row['Span_MHz']
            center = row['CenterFrequency_MHz']
            timestamp = row['Time']
            extra_rows.append({
                'Time': timestamp,
                'Total_Power': row['Channel_Powers'][0],
                'CenterFrequency_MHz': center - span/2
            })
            extra_rows.append({
                'Time': timestamp,
                'Total_Power': row['Channel_Powers'][1],
                'CenterFrequency_MHz': center + span/2
            })

    extra_df = pd.DataFrame(extra_rows)
    merged_df = pd.concat([filtered_df[['Time', 'Total_Power', 'CenterFrequency_MHz']], extra_df], ignore_index=True)

    fig = px.line(
        merged_df,
        x='Time',
        y='Total_Power',
        color='CenterFrequency_MHz',
        title="Moc sygnału w czasie (w tym boczne częstotliwości)",
        labels={"Time": "Data", "Total_Power": "Moc [dBm]", "CenterFrequency_MHz": "Częstotliwość (MHz)"},
        markers=True
    )

    fig.update_traces(marker=dict(size=10))
    fig.update_layout(
        xaxis_title='Data',
        yaxis_title='Moc [dBm]',
        uirevision='fixed-zoom'
    )

    return fig



#WYKRES 3D
@app.callback(
    Output('spectral-usage-3d-graph', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('interval-component', 'n_intervals'),
     Input('value-dropdown', 'value')]
)
def update_3d_graph(start_date, end_date, n_intervals, selected_ids):
    data = list(collection.find({}))
    df = pd.DataFrame(data)

    if '_id' in df.columns:
        df.drop(columns=['_id'], inplace=True)

    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
    df = df.dropna(subset=['Time'])

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    filtered_df = df[(df['Time'] >= start_date) & (df['Time'] < (end_date + pd.Timedelta(days=1)))]

    if selected_ids:
        filtered_df = filtered_df[filtered_df['ID'].isin(selected_ids)]

    if filtered_df.empty:
        return go.Figure()

    # Przelicz czas na sekundy od pierwszego punktu
    time_start = filtered_df['Time'].min()
    filtered_df['Seconds'] = (filtered_df['Time'] - time_start).dt.total_seconds()

    fig = go.Figure(data=[go.Scatter3d(
        x=filtered_df['Seconds'],
        y=filtered_df['CenterFrequency_MHz'],
        z=filtered_df['Total_Power'],
        mode='markers',
        marker=dict(
            size=5,
            color=filtered_df['Total_Power'],
            colorscale='Viridis',
            opacity=0.8,
            colorbar=dict(title='Moc [dBm]')
        ),
        hovertemplate=
            'Czas: %{x:.1f} s<br>' +
            'Częstotliwość: %{y} MHz<br>' +
            'Moc: %{z:.2f} dBm<br>' +
            '<extra></extra>'
    )])

    fig.update_layout(
        title="Wykres 3D: Czas (s), Częstotliwość, Moc",
        scene=dict(
            xaxis=dict(
                title='Czas (s od początku)',
                showgrid=True
            ),
            yaxis=dict(
                title='Częstotliwość (MHz)',
                showgrid=True
            ),
            zaxis=dict(
                title='Moc [dBm]',
                showgrid=True
            ),
            aspectmode='cube'
        ),
        scene_camera=dict(
            eye=dict(x=2, y=2, z=1.5)
        ),
        height=700,
        uirevision='fixed-zoom'
    )

    return fig


#WYKRES KANAŁY
@app.callback(
    [Output('time-slider', 'min'),
     Output('time-slider', 'max'),
     Output('time-slider', 'marks'),
     Output('time-slider', 'value'),
     Output('channel-power-graph', 'figure')],
    [Input('interval-component', 'n_intervals'),
     Input('time-slider', 'value')]
)
def update_channel_graph(n_intervals, selected_index):
    data = list(collection.find({}))
    df = pd.DataFrame(data)

    if '_id' in df.columns:
        df.drop(columns=['_id'], inplace=True)

    if df.empty or 'Time' not in df.columns:
        return 0, 0, {}, 0, go.Figure()

    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
    df = df.dropna(subset=['Time'])
    df = df.sort_values(by='Time').reset_index(drop=True)


    min_val = 0
    max_val = len(df) - 1
    marks = {i: df.loc[i, 'Time'].strftime('%H:%M:%S') for i in range(0, len(df), max(1, len(df)//10))}

    if selected_index is None or not (min_val <= selected_index <= max_val):
        selected_index = max_val

    row = df.iloc[selected_index]

    # Przygotuj dane
    freqs = []
    powers = []
    if isinstance(row.get('Channel_Powers'), list) and len(row['Channel_Powers']) == 2:
        span = row.get('Span_MHz')
        center = row.get('CenterFrequency_MHz')
        freqs = [center - span, center, center + span]
        powers = [row['Channel_Powers'][0], row['Total_Power'], row['Channel_Powers'][1]]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
    x=freqs,
    y=powers,
    mode='markers',
    name='Moc kanałów'
    ))


    fig.update_layout(
        title=f"Wykres mocy odebranej dla {row['Time']:%Y-%m-%d %H:%M:%S}",
        xaxis_title='Częstotliwość (MHz)',
        yaxis_title='Moc [dBm]',
        xaxis=dict(tickmode='linear'),
        yaxis=dict(tickmode='linear'),
        uirevision='fixed-slider'
    )

    return min_val, max_val, marks, selected_index, fig


#SLIDER DO DATY
@app.callback(
    [Output('date-picker-range', 'start_date'),
     Output('date-picker-range', 'end_date')],
    Input('interval-component', 'n_intervals')
)
def set_date_range(n):
    data = list(collection.find({}, {'Time': 1}))
    df = pd.DataFrame(data)

    if '_id' in df.columns:
        df.drop(columns=['_id'], inplace=True)

    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
    df = df.dropna(subset=['Time'])

    if df.empty:
        today = datetime.now().date()
        return today, today

    return df['Time'].min().date(), df['Time'].max().date()



#KANAŁ 1
@app.callback(
    Output('channel-180-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_180mhz_graph(n):
    data = list(collection.find({}))
    df = pd.DataFrame(data)

    if '_id' in df.columns:
        df.drop(columns=['_id'], inplace=True)

    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
    df = df.dropna(subset=['Time'])

    timestamps = []
    powers = []

    for _, row in df.iterrows():
        center = row.get('CenterFrequency_MHz')
        span = row.get('Span_MHz')
        chans = row.get('Channel_Powers')

        if not (isinstance(chans, list) and len(chans) == 2):
            continue

        if center - span/2 == 180:
            timestamps.append(row['Time'])
            powers.append(chans[0])
        elif center + span/2 == 180:
            timestamps.append(row['Time'])
            powers.append(chans[1])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=powers,
        mode='markers+lines',
        name='Kanał 180 MHz'
    ))

    fig.update_layout(
        title="Kanał 1 - 180 MHz",
        xaxis_title="Czas",
        yaxis_title="Moc [dBm]",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )

    return fig


#KANAŁ 2
@app.callback(
    Output('channel-200-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_180mhz_graph(n):
    data = list(collection.find({}))
    df = pd.DataFrame(data)

    if '_id' in df.columns:
        df.drop(columns=['_id'], inplace=True)

    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
    df = df.dropna(subset=['Time'])

    timestamps = []
    powers = []

    for _, row in df.iterrows():
        center = row.get('CenterFrequency_MHz')
        span = row.get('Span_MHz')
        chans = row.get('Channel_Powers')

        if not (isinstance(chans, list) and len(chans) == 2):
            continue

        if center - span/2 == 200:
            timestamps.append(row['Time'])
            powers.append(chans[0])
        elif center + span/2 == 200:
            timestamps.append(row['Time'])
            powers.append(chans[1])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=powers,
        mode='markers+lines',
        name='Kanał 200 MHz'
    ))

    fig.update_layout(
        title="Kanał 2 - 200 MHz",
        xaxis_title="Czas",
        yaxis_title="Moc [dBm]",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )

    return fig





if __name__ == '__main__':
    app.run(debug=True)
