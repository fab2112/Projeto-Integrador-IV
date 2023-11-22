# Imports
import dash_bootstrap_components as dbc
from dash import dash
from components.client_callbacks import *
from components.cards import *
from components.charts import *
from layout.layout import layout_
from settings import dbc_css
from settings import producao
from settings import port
from settings import app_path
from settings import app_title

app = dash.Dash(__name__,
                title=app_title,
                update_title="Loading Dashboard...",
                external_stylesheets=['projeto.css',
                                      dbc.themes.FLATLY,
                                      dbc_css,
                                      dbc.icons.BOOTSTRAP],
                url_base_pathname=app_path,
                external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/dayjs.min.js",
                                  "https://cdn.jsdelivr.net/npm/dayjs@1.10.8/locale/pt-br.min.js"])

app._favicon = ("image6.png")

app.layout = layout_

server = app.server


if __name__ == '__main__':
    app.run(debug=False if producao else True,
            port=port,
            host=None if producao else "0.0.0.0",
            dev_tools_hot_reload=None if producao else True)

