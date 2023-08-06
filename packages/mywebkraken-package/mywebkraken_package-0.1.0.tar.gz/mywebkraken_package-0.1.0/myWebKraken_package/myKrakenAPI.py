import krakenex
import pykrakenapi
import datetime
import time

intervalosValidos = {
    "1 Minuto": 1,
    "5 Minutos": 5,
    "15 Minutos": 15,
    "30 Minutos": 30,
    "1 Hora": 60,
    "4 Horas": 240,
    "1 Dia": 1440,
    "1 Semana": 10080,
    "15 Días": 21600
}


def obtenerDatosKraken(par_monedas, intervalo, inicio=None):
    """
    Esta funcion accede al API de Kraken
    Descarga la maxima historia disponible de precios
    del PAR_MONEDAS e intervalo elegido.

    Args:
        par_monedas: Par de monedas de que queremos el precio.
        intervalo: intervalo de tiempo entre precios

    Returns:
        DataFrame (pandas) con los precios de la kriptomoneda.
    """

    #Comprobamos que el intervalo es valido
    if intervalo not in intervalosValidos.values():
        print("Intervalo no Valido")
        return None
    #Accedemos al API Kraken y devolvemos el DF
    try:
        api = krakenex.API()
        k = pykrakenapi.KrakenAPI(api)
        ohlc, last = k.get_ohlc_data(par_monedas, interval=intervalo, since=inicio)
        return ohlc
    except Exception as err:
        print("Error en la descarga:", err)
        return None

#Fuente https://www.roelpeters.be/many-ways-to-calculate-the-rsi-in-python-pandas/
def rsi(df, Columnaprecio, periods=14, ema=True):
    """
    Returns a pd.Series with the relative strength index.
    """
    try:
        close_delta = df[Columnaprecio].diff()

        # Make two series: one for lower closes and one for higher closes
        up = close_delta.clip(lower=0)
        down = -1 * close_delta.clip(upper=0)

        if ema == True:
            # Use exponential moving average
            ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
            ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        else:
            # Use simple moving average
            ma_up = up.rolling(window=periods, adjust=False).mean()
            ma_down = down.rolling(window=periods, adjust=False).mean()

        rsi = ma_up / ma_down
        rsi = 100 - (100 / (1 + rsi))
        return rsi
    except Exception as err:
        print("Error en Funcion RSI:", err)
        return None


def incorporaMetricasMoviles(df, columna, periodos):
    """
    Esta funcion incorpora la media movil y el RSI de
    una columna usando periodos como ventana.

    Args:
        df: DataFrame.
        columna: la columna a promediar
        periodos: la venta a a promediar

    Returns:
        DataFrame (pandas) con las nuevas columnas.
    """
    try:
        df['RollingMean'] = df[columna].rolling(periodos).mean()
        df["RSI"] = rsi(df, columna, periodos)
        return df
    except Exception as err:
        print("Error en Funcion incorporaMetricasMoviles:", err)
        return None


def obtenerPares():
    """
    Esta funcion devuelve los pares de divisa
    disponibles en Kraken.

    Returns:
        Listado de Pares de Divisas.
    """
    try:
        api = krakenex.API()
        k = pykrakenapi.KrakenAPI(api)
        return k.get_tradable_asset_pairs().altname
    except Exception as err:
        print("Error en Funcion obtenerPares:", err)
        return None


def convierteFechaUnix(year, month, day):
    """
    Esta devuelve el tiempo Unix de una fecha

    Args:
        year: El Año.
        month: El Mes
        day: El dia

    Returns:
        Tiempo Unix
    """
    try:
        date_time = datetime.datetime(year, month, day)
        fechaUnix = int(time.mktime(date_time.timetuple()))
        print("Given Date:", date_time)
        print("UNIX timestamp:", fechaUnix)
        return fechaUnix
    except Exception as err:
        print("Error en Funcion convierteFechaUnix:", err)
        return None


def convierteFechaHoraUnix(year, month, day,hour, minute, second):
    """
    Esta devuelve el tiempo Unix de una fecha y hora

    Args:
        year: El Año.
        month: El Mes
        day: El dia
        hour: La hora
        minute: El minuto
        second: El segundo

    Returns:
        Tiempo Unix
    """
    try:
        date_time = datetime.datetime(year, month, day,hour, minute, second)
        fechaUnix = int(time.mktime(date_time.timetuple()))
        print("Given Date:", date_time)
        print("UNIX timestamp:", fechaUnix)
        return fechaUnix
    except Exception as err:
        print("Error en Funcion convierteFechaHoraUnix:", err)
        return None