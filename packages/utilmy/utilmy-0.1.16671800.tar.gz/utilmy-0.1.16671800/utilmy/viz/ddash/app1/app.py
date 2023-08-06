# -*- coding: utf-8 -*-
"""  Launch app
Doc::
   
   ### pip install fire
    cd folder
    python app.py  main   --dir_html0  assets/html


 
"""
from dash import Dash, html
from dash_treeview_antd import TreeView
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Simple render html'

### Main page ressource
page_default = 'assets/html/main.html'
dir_html     = "assets/html/"



###################################################################
######  Utils #####################################################
def sidebar_add_v1():
    """ Add sidebar style arguments for the sidebar.

    Returns:
        _type_: _description_
    """
    SIDEBAR_STYLE = {
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'bottom': 0,
        'width': '20%',
        'padding': '20px 10px',
        'backgroundColor': '#f8f9fa',
        'verticalAlign': 'middle',
        'alignItems': 'center'
    }


    treeview = {
                'title': 'Parent', 'key':'0',
                'children': [{
                    'title': 'Child',   'key': '01',
                    'children': [
                        {'title': 'Subchild1', 'key': 'page1.html'},
                        {'title': 'Subchild2', 'key': 'page2.html'},
                    ],
                },
                {   'title': 'Child2',   'key': '02',
                    'children': [
                        {'title': 'Subchild2-1', 'key': 'page2_1.html'},
                        {'title': 'Subchild2-2', 'key': 'page2_2.html'},
                        {'title': 'Subchild2-3', 'key': 'page2_3.html'},
                    ],
                }]
            }

    sidebar_content = html.Div([
        dbc.Row([   dbc.Col([  TreeView(
                            id='input',
                            multiple=False,
                            checkable=False,
                            checked=False,
                            selected=[],
                            expanded=[],
                            data=treeview
                        )  ])  ])
    ], style=SIDEBAR_STYLE)
    return sidebar_content



@app.callback(Output('output', 'src'), [Input('input', 'selected')])
def iframe_render(selected):
    global page_default, dir_html

    if selected == []:
        return f'{page_default}'

    elif selected[0].endswith('.html'):
            page_default = selected[0]
            return f'{dir_html}/{selected[0]}'
    else:
        return f'{page_default}'



###################################################################
def main_page():

    sidebar_content = sidebar_add_v1()


    ###### the style arguments for the main content page.
    CONTENT_STYLE = {
        'marginLeft': '25%',
        'marginRight': '5%',
        'top': '10px',
        'padding': '20px 10px'
    }
    main_content = html.Div([
        dbc.Row([  html.Iframe(id="output")])], style=CONTENT_STYLE)



    app.layout = html.Div([sidebar_content, main_content])






def main(dir_html0="", dir_log=""):
    """ Run main app

    Args:
        dir_html0 (str, optional): _description_. Defaults to "assets/html/".

    """
    global dir_html
    dir_html = dir_html0 if dir_html0 != "" else dir_html


    main_page()
    app.run_server(debug=True)




if __name__ == '__main__':
     import fire
     fire.Fire()


