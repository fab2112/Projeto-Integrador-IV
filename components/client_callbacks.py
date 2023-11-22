# Imports
from dash import clientside_callback, Input, Output
from utils.theme_switch import ThemeSwitch


# Theme - tabs | bg_container | tab_style
clientside_callback(
    """
    function(themeValue) {
        var tab = "text-info";
        var bg_container_1 = {"background-color": "#F0F0F0"};
        var tab_style = {"background-color": "#F0F0F0", "color": "grey"};
        
        if (!themeValue) {
            tab = "text-primary";
            bg_container_1 = {"background-color": "#181818"};
            tab_style = {"background-color": "#181818", "color": "grey"};
        }
        
        return [
            bg_container_1,
            tab,
            tab,
            tab,
            tab_style,
            tab_style,
            tab_style
            ];
    }
    """,
    [
        Output('container', 'style'),
        Output('tab-1', 'active_label_class_name'),
        Output('tab-2', 'active_label_class_name'),
        Output('tab-3', 'active_label_class_name'),
        Output('tab-1', 'label_style'),
        Output('tab-2', 'label_style'),
        Output('tab-3', 'label_style'),
        
        ], 
    [Input(ThemeSwitch.ids.switch('theme-2'), 'checked')])

# Update Button
clientside_callback(
    """
    function (n_clicks) {
        return true
    }
    """,
    Output("loading-button", "loading", allow_duplicate=True),
    Input("loading-button", "n_clicks"),
    prevent_initial_call=True)

# Theme - Notificação de update 
clientside_callback(
    """
    function(themeValue) {
        var datepicker_theme = {"colorScheme": "light"};
        
        if (!themeValue) {
            datepicker_theme = {"colorScheme": "dark"};
        }       
        return [datepicker_theme];
    }
    """,
    [Output('note-1', 'theme')],
    [Input(ThemeSwitch.ids.switch('theme-2'), 'checked')],)

# Theme - Datepicker-group 
clientside_callback(
    """
    function(themeValue) {
        var datepicker_theme = {"colorScheme": "light"};
        
        if (!themeValue) {
            datepicker_theme = {"colorScheme": "dark"};
        }       
        return [datepicker_theme];
    }
    """,
    [Output('dp-theme', 'theme')],
    [Input(ThemeSwitch.ids.switch('theme-2'), 'checked')],)

# Card-Title-1
clientside_callback(
    """
    function(ano) {
        var value = "Movimentações financeiras por período";
        return value;
    }
    """,
    Output("card-title-1", "children"),
    [Input("date-picker-1", "value")]
)
