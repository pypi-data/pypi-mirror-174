import dash
from dash import dcc, html, Input, Output
from myWebKraken_package import myKrakenAPI
from plotly.subplots import make_subplots
import plotly.graph_objects as go

class mAppKraken(dash.Dash):

    def __init__(self):
        """
        Esta funcion inicializa la App.
        """

        #Definición de estilo
        external_stylesheets = [
            {
                "href": "https://fonts.googleapis.com/css2?"
                        "family=Lato:wght@400;700&display=swap",
                "rel": "stylesheet",
            },
        ]

        #Periodos usados para la media movil y RSI
        periodos = 5

        super().__init__(#__name__,
            external_stylesheets=external_stylesheets)

        #Establecemos Titulo y elementos de la hoja
        self.title = "Análisis de la evolución de KriptoAssets (Fuente Kraken)"
        self.layout = html.Div(
            children=[
                # Cabecera de la Web
                html.Div(
                    children=[
                        html.P(children="🐣", className="header-emoji"),
                        html.H1(
                            children="Análisis de la evolución de KriptoAssets ", className="header-title"
                        ),
                        html.P(
                            children="(Fuente Kraken)",
                            className="header-description",
                        ),
                        html.P(
                            children="by LADM",
                            className="header-description",
                        ),
                    ],
                    className="header",
                ),
                # Dos filtros para elegir el kriptoactivo y el intervalo de muestreo
                html.Div(
                    children=[
                        #Filtro de kripto activo obteniendo el listado de Kraken
                        html.Div(
                            children=[
                                html.Div(children="KriptoActivo", className="menu-title"),
                                dcc.Dropdown(
                                    id="filtro-KriptoActivo",
                                    options=[
                                        {"label": KriptoActivo, "value": KriptoActivo}
                                        for KriptoActivo in myKrakenAPI.obtenerPares()
                                    ],
                                    value="ETHUSDT",
                                    clearable=False,
                                    className="dropdown",
                                ),
                            ]
                        ),
                        # Filtro de intervalo obteniendo el listado de myKrakenAPI
                        html.Div(
                            children=[
                                html.Div(children="Intervalo", className="menu-title"),
                                dcc.Dropdown(
                                    id="filtro-intervalo",
                                    options=[
                                        {"label": intervalo, "value": intervalo}
                                        for intervalo in myKrakenAPI.intervalosValidos.keys()
                                    ],
                                    value="1 Minuto",
                                    clearable=False,
                                    searchable=False,
                                    className="dropdown",
                                ),
                            ],
                        ),
                    ],
                    className="menu",
                ),
                # Cabecera de los graficos
                html.H1(children="Analisis del precio del activo", ),
                html.P(
                    children="Analizar el comportamiento del precio del activo"
                             " su media movil "
                             " y RSI",
                ),
                # Los dos graficos que se refrescaran con callback
                html.Div(
                    children=[
                        html.Div(
                            children=dcc.Graph(
                                id="grafica-precio", config={"displayModeBar": False},
                            ),
                            className="card",
                        ),
                        html.Div(
                            children=dcc.Graph(
                                id="grafica-rsi", config={"displayModeBar": False},
                            ),
                            className="card",
                        ),
                    ],
                    className="wrapper",
                ),
            ]
        )

        # Callback para refescar los graficos
        @self.callback(
            [Output("grafica-precio", "figure"), Output("grafica-rsi", "figure")],
            [
                Input("filtro-KriptoActivo", "value"),
                Input("filtro-intervalo", "value"),
            ],
        )
        def update_charts(KriptoActivo, intervalo):
            """
            Esta funcion accede al API de Kraken
            descarga el dataframe con la cotizaacion
            de los kriptoactivos con la frecuencia de muestreo
            y devuelve los dos graficos, de precios/media movil y RSI.

            Args:
                KriptoActivo: Par de monedas de que queremos el precio.
                intervalo: intervalo de muestreo

            Returns:
                Graficos de precios/media movil y RSI.
            """

            filtered_data = myKrakenAPI.obtenerDatosKraken(KriptoActivo, myKrakenAPI.intervalosValidos[intervalo])
            if filtered_data is not None:
                filtered_data = myKrakenAPI.incorporaMetricasMoviles(filtered_data, "close", periodos)

            #Grafico de RSI
            rsi_chart_figure = {
                "data": [
                    {
                        "x": filtered_data.index,
                        "y": filtered_data["RSI"],
                        "type": "lines",
                    },
                ],
                "layout": {
                    "title": {
                        "text": "RSI",
                        "x": 0.05,
                        "xanchor": "left"
                    },
                    "xaxis": {"fixedrange": True},
                    "yaxis": {"fixedrange": True},
                    "colorway": ["#E12D39"],
                },
            }

            # Grafico de Precio y Media Movil
            price_chart_figure = make_subplots()
            price_chart_figure.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data.close,
                                                    mode='lines',
                                                    name='Close'),
                                         secondary_y=False)
            price_chart_figure.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data.RollingMean,
                                                    mode='lines',
                                                    name='RollingMean'),
                                         secondary_y=False)
            price_chart_figure.update_layout(
                title_text="Evolución del precio de " + KriptoActivo
            )

            return price_chart_figure, rsi_chart_figure


    def lanzaServidor(self):
        """
        Metodo para lanzar el servidor
        """
        try:
            self.run_server(debug=True)
        except Exception as err:
            print("Error en llamada a mAppKraken:", err)

