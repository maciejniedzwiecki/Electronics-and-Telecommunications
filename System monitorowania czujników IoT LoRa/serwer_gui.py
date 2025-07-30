import dash
from dash import Dash, html, Input, Output, State, dcc
from flask import Flask, jsonify, request
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.graph_objects as go


latest_message = False
id = 1
gps_enabled = True
location = (10.30, 30.30)
#id_database = []

# Serwer Flask + Dash
server = Flask(__name__)
app = Dash(__name__)

# Domyślne współrzędne
DEFAULT_LAT = 52.4064
DEFAULT_LON = 16.9252

# Layout strony
app.layout = dmc.MantineProvider(
    children=[
        html.Div(
            children=[
                html.H1("Raspberry Pi configurator"),

                dmc.Select(
                    id="device-select",
                    placeholder="Select Raspberry Pi",
                    label="Configure device",
                    data=[
                        {"label": "raspberry-pi-01", "value": "pi_01"},
                        {"label": "raspberry-pi-02", "value": "pi_02"},
                        {"label": "raspberry-pi-03", "value": "pi_03"},
                    ],
                    variant="default",
                    size="sm",
                    radius="sm",
                    withAsterisk=True,
                    disabled=False,
                    clearable=True,
                    searchable=True,
                    allowDeselect=True,
                    maxDropdownHeight=120,
                    comboboxProps={"zIndex": 1000, "dropdownPadding": 10},
                    style={"width": 310, "margin": 6},
                ),

                dmc.Button(
                    "Restart Device",
                    id="restart-button",
                    leftSection=DashIconify(icon="solar:restart-bold", width=18),
                    variant="light",
                    color="red",
                    size="sm",
                    radius="sm",
                    style={"margin": 10}
                ),
                html.Div(
                    id="restart-status",
                    style={
                        "color": "#fa5252",  # ten sam czerwony co Mantine
                        "fontSize": "12px",
                        "fontWeight": 400,
                        "marginTop": "-8px",
                        #"marginBottom": "6px",
                        "textAlign": "left",
                        "width": "150px",
                        "fontFamily": "-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif",
                    }
                ),

                dmc.Switch(
                    id="gps-switch",
                    label="Set custom localization",
                    checked=False,
                    color="green",
                    size="sm",
                    radius="lg",
                    style={"margin": 10}
                ),

                html.Div([
                    dmc.NumberInput(
                        id="input-lat",
                        label="Latitude",
                        value=DEFAULT_LAT,
                        min=-90, max=90,
                        step=0.0001,
                        style={"marginRight": 10, "width": 150}
                    ),
                    dmc.NumberInput(
                        id="input-lon",
                        label="Longitude",
                        value=DEFAULT_LON,
                        min=-180, max=180,
                        step=0.0001,
                        style={"width": 150}
                    )
                ], style={"display": "flex", "justifyContent": "center", "marginBottom": 20}),

                dcc.Graph(
                    id="map-graph",
                    style={
                        "borderRadius": "16px",
                        "overflow": "hidden",
                        "height": "350px",
                        "width": "600px"
                    }
                ),

                html.Div(id='dummy-output-restart', style={'display': 'none'}),
                html.Div(id='dummy-output', style={'display': 'none'}),

                dcc.Interval(id="restart-timer", interval=2000, n_intervals=0, disabled=True)

            ],
            style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}
        ),

        html.Div(
            html.A(
                dmc.Button(
                    children=[
                        DashIconify(icon="mdi:arrow-left", width=16, style={"marginRight": 6}),
                        "Go to Grafana"
                    ],
                    variant="subtle",
                    color="green",
                    size="sm"
                ),
                #href="http://localhost:3000",
                href="http://localhost:3000/public-dashboards/5bc72a6ab9704095aa7f02209d3c35eb",
                target="_blank",
                style={"textDecoration": "none"}
            ),
            style={
                "position": "fixed",
                "top": "12px",
                "left": "12px",
                "zIndex": 9999
            }
        )
    ]
)


# Device mandatory
@app.callback(
    Output("restart-button", "disabled"),
    Output("gps-switch", "disabled"),
    Output("device-select", "error"),
    Input("device-select", "value")
)
def toggle_controls(selected_value):
    is_disabled = selected_value is None or selected_value == ""
    error_text = "Device selection is required" if is_disabled else ""

    if is_disabled:
        print("SERVER: no device selected")
    else:
        print(f"SERVER: selected device = {selected_value}")

    return is_disabled, is_disabled, error_text


# Switch OFF when no selected device
@app.callback(
    Output("gps-switch", "checked", allow_duplicate=True),
    Input("device-select", "value"),
    prevent_initial_call=True
)
def sync_gps_switch_with_device(selected_device):
    if selected_device is None or selected_device == "":
        print("SERVER: device deselected → gps-switch turned off")
        return False
    raise dash.exceptions.PreventUpdate  # nie zmieniaj nic jeśli urządzenie zostało wybrane


# Restart
@app.callback(
    Output('restart-status', 'children'),
    Output('device-select', 'value'),
    Output('restart-timer', 'disabled'),
    Input('restart-button', 'n_clicks'),
    Input('restart-timer', 'n_intervals'),
    State('device-select', 'value'),
    prevent_initial_call=True
)
def handle_restart(n_clicks, n_intervals, selected_device):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == "restart-button":
        if selected_device:
            global latest_message
            latest_message = True
            print(f"SERVER: Restart for device {selected_device}")
            return "Restart sent", dash.no_update, False  # start timer
        else:
            return "Device not selected", dash.no_update, True

    elif triggered_id == "restart-timer":
        print("SERVER: Timer finished – clearing status and select")
        return "", None, True

    raise dash.exceptions.PreventUpdate


# Switch
@app.callback(
    Output('dummy-output', 'children'),
    Input('gps-switch', 'checked'),
    State('device-select', 'value')
)
def update_gps(checked, selected_device):
    global gps_enabled
    gps_enabled = checked
    print(f"SERVER: gps_enabled = {gps_enabled} for device = {selected_device}")
    return ""


# Localization Inputs
@app.callback(
    Output("map-graph", "figure"),
    Input("input-lat", "value"),
    Input("input-lon", "value"),
    State("device-select", "value")
)
def update_map(lat, lon, selected_device):
    print(f"SERVER: location set to (lat: {lat}, lon: {lon}) for device = {selected_device}")

    fig = go.Figure(go.Scattermapbox(
        lat=[lat],
        lon=[lon],
        mode='markers',
        marker=go.scattermapbox.Marker(size=16,
                                       color='red',
                                       opacity=0.8)
    ))
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=10,
        mapbox_center={"lat": lat, "lon": lon},
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=400,
        width=600
    )
    return fig


#  Wpisywanie lokalizacji
@app.callback(
    Output('input-lon', 'disabled'),
    Output('input-lat', 'disabled'),
    Input('gps-switch', 'checked')
)
def toggle_inputs(checked):
    return not checked, not checked


#############################################################################
# GET: Klient odczytuje status
@server.route('/api/message', methods=['GET'])
def get_message():
    global latest_message
    msg = latest_message
    latest_message = False
    print('SERVER: restart button has been clicked')
    return jsonify({"device_id": id,
                    "restart_device": msg,
                    "gps_enabled": gps_enabled,
                    "location": location})

# POST: Klient wysyła wiadomość
@server.route('/api/message', methods=['POST'])
def odbierz_wiadomosc():
    dane = request.get_json()
    if not dane:
        print("SERVER: error - Brak wiadomości o inicjalizacji")
        return jsonify({"error": "Brak wiadomości o inicjalizacji"}), 400

    print("SERVER: inicjalizacja urzadzenia", dane)

    global latest_message
    latest_message = dane

    return jsonify({"status": "OK", "received": dane}), 200


# Uruchom serwer
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8050)
