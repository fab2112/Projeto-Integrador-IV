# Imports
from dash import html, dcc, Input, Output, clientside_callback, MATCH
from dash_bootstrap_templates import load_figure_template, template_from_url
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc


class ThemeSwitch(html.Div):
    class ids:
        switch = lambda aio_id: {
            "component": "ThemeSwitch",
            "subcomponent": "switch",
            "aio_id": aio_id,
        }
        icons_sun_moon = lambda aio_id: {
            "component": "ThemeSwitch",
            "subcomponent": "icons_sun_moon",
            "aio_id": aio_id,
        }
        store = lambda aio_id: {
            "component": "ThemeSwitch",
            "subcomponent": "store",
            "aio_id": aio_id,
        }
        dummy_div = lambda aio_id: {
            "component": "ThemeSwitch",
            "subcomponent": "dummy_div",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(self, themes=None, aio_id=None,):

        if aio_id is None:
            aio_id = 'theme-aio'

        if themes is None:
            themes = [dbc.themes.CYBORG, dbc.themes.FLATLY]
            
        load_figure_template([template_from_url(themes[0]), template_from_url(themes[1])])
            
        super().__init__(
            [
                dmc.Switch(
                    id=self.ids.switch(aio_id),
                    thumbIcon=DashIconify(icon="tabler:sun-filled",
                                          color="#ffc145",
                                          id=self.ids.icons_sun_moon(aio_id),
                                          height=15,
                                          width=15),
                    size="md",
                    checked=True,
                    color="orange",
                    radius='lg',
                    style={"margin":"0px",
                           "padding": "0px",
                           "display":"flex",
                           "align-items": "center",
                           "justify-content": "center"}),  
                                                                                                                           
                dcc.Store(id=self.ids.store(aio_id), data=themes),
                html.Div(id=self.ids.dummy_div(aio_id)),
            ]
        )
    
        
    clientside_callback(
        """
        function(themeValue, theme_urls) { 
                   
            var figure_icon = "tabler:sun-filled";
            var themeLink = themeValue ? theme_urls[0] : theme_urls[1];
    
            if (!themeValue) {
                figure_icon = "tabler:moon-filled";
            }
        
            let urls = [themeLink, "https://use.fontawesome.com/releases/v5.15.4/css/all.css"];
            
            for (const url of urls) {
                
                var link = document.createElement("link");

                link.type = "text/css";
                link.rel = "stylesheet";
                link.href = url;

                document.head.appendChild(link);
            }
        
            return [figure_icon];
        }
        """,
    Output(ids.icons_sun_moon(MATCH), "icon"),
    Output(ids.dummy_div(MATCH), "role"),
    Input(ids.switch(MATCH), "checked"),
    Input(ids.store(MATCH), "data"),
)
    