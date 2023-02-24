import time
import importlib
import ipyvuetify as v
# Our packages
import get_noaa
import get_sun_data as gsd
import ipywidgets as widgets
importlib.reload(get_noaa)

# ---------- GUI Functions ----------

R = {0: 0, 1: 0, 2: 0}
P = {0: 0, 1: 0, 2: 0}
SC = {0: 0, 1: 0, 2: 0}
N = {0: 0, 1: 0, 2: 0}


# Change back-end indices values
def refresh_states():
    noaa_scales = get_noaa.NoaaScales()
    global R, P, SC, N
    noaa_indices = get_noaa.calculate_indices(noaa_scales)
    R, P = noaa_indices["R"], noaa_indices["P"]
    change_index("R", R[0])
    change_index("P", P[0])
    change_index("SC", SC[0])
    change_index("N", N[0])
    # TODO initialize SC and N


# Refresh all shown indices values
def refresh(widget, event, data):
    refresh_btn.loading = True
    refresh_states()
    change_index("R", R[0])
    change_index("P", P[0])
    change_index("SC", SC[0])
    change_index("N", N[0])
    # TODO Refresh in function of predicted values
    gsd.get_sun_img()
    refresh_btn.loading = False


# --- Show data pages ---
# Show HF page
def r_click(widget, event, data):
    hf_page.v_model = True


# Show space operations page
def p_click(widget, event, data):
    space_op_page.v_model = True


# Show HF page
def sc_click(widget, event, data):
    satcom_page.v_model = True


# Show HF page
def n_click(widget, event, data):
    gnss_page.v_model = True


# --- Show info pages ---
# Show HF page
def r_info_click(widget, event, data):
    hf_info_page.v_model = True


# Show space operations page
def p_info_click(widget, event, data):
    space_op_info_page.v_model = True


# Show HF page
def sc_info_click(widget, event, data):
    satcom_info_page.v_model = True


# Show HF page
def n_info_click(widget, event, data):
    gnss_info_page.v_model = True


# Show bulletin
def bulletin_click(widget, event, data):
    bulletin_dialog.v_model = True


# Show sources
def sources_click(widget, event, data):
    sources_dialog.v_model = True


# Switch between current and predicted index values
def prediction_click(widget, event, data):
    if data == 0:
        # TODAY
        change_index("R", 0)
        change_index("P", 1)
        change_index("SC", 2)
        change_index("N", 3)
        # TODO actually change to today's data
    elif data == 1:
        # J + 1
        change_index("R", 4)
        change_index("P", 5)
        change_index("SC", 0)
        change_index("N", 1)
        # TODO actually change to J+1 data
    else:
        # J + 2
        change_index("R", 2)
        change_index("P", 3)
        change_index("SC", 4)
        change_index("N", 5)
        # TODO actually change to J+2 data


# Change index to new index value
def change_index(index, index_value):
    # index should be R, P, SC, N -> it is R by default
    if index == "R":
        widget = R_widget
    elif index == "P":
        widget = P_widget
    elif index == "SC":
        widget = SC_widget
    else:
        widget = N_widget

    if index_value == 0:
        widget.children = [index + "0"]
        widget.color = "green"
    if index_value == 1:
        widget.children = [index + "1"]
        widget.color = "#ADFF2F"
    if index_value == 2:
        widget.children = [index + "2"]
        widget.color = "yellow"
    if index_value == 3:
        widget.children = [index + "3"]
        widget.color = "orange lighten-2"
    if index_value == 4:
        widget.children = [index + "4"]
        widget.color = "orange"
    if index_value == 5:
        widget.children = [index + "5"]
        widget.color = "red"


# ---------- GUI Widgets ----------
# Main title

title = v.CardTitle(class_="d-flex align-start m-2 title font-weight-medium white--text",
                    children=["TAMAGI: a space weather tool"])

# --- Data pages ---
# HF Radio page
muf_north_img = v.Card(children=[], img="muf_north_pole.png", width=675, height=595, class_="my-2 mx-2")
muf_south_img = v.Card(children=[], img="muf_south_pole.png", width=675, height=595, class_="my-2 mx-2")

hf_page = v.Dialog(children=[v.Card(children=[v.CardTitle(children=["HF Radio"]),
                                              v.CardText(children=["Maximum usable frequency (MUF):\n"
                                                                   ]
                                                         ),
                                              muf_north_img,
                                              muf_south_img
                                              ],
                                    )
                             ], width=1000, height=1200)
hf_page.v_model = False

# Space Operations page
space_op_page = v.Dialog(children=[v.Card(children=[v.CardTitle(children=["Space Operations"]),
                                                    v.CardText(children=["Particle flux:\n"
                                                                         ]
                                                               )
                                                    ],
                                          )
                                   ], width=800, height=400)
space_op_page.v_model = False

# Satellite Communications page
satcom_page = v.Dialog(children=[v.Card(children=[v.CardTitle(children=["Satellite Communications"]),
                                                  v.CardText(children=["S4 data:\n"
                                                                       ]
                                                             )
                                                  ],
                                        )
                                 ], width=800, height=400)
satcom_page.v_model = False

# GNSS page
gnss_page = v.Dialog(children=[v.Card(children=[v.CardTitle(children=["GNSS"]),
                                                v.CardText(children=["Map:\n"
                                                                     ]
                                                           )
                                                ],
                                      )
                               ], width=800, height=400)
gnss_page.v_model = False

# --- Info pages ---
# Info HF Radio page
hf_info_page = v.Dialog(children=[v.Card(children=[v.CardTitle(children=["R index info"]),
                                              v.CardText(children=["R0:\n"
                                                                   ]
                                                         )
                                              ],
                                    )
                             ], width=600, height=400)
hf_info_page.v_model = False

# Info Space Operations page
space_op_info_page = v.Dialog(children=[v.Card(children=[v.CardTitle(children=["P index info"]),
                                                    v.CardText(children=["P0:\n"
                                                                         ]
                                                               )
                                                    ],
                                          )
                                   ], width=600, height=400)
space_op_info_page.v_model = False

# Info Satellite Communications page
satcom_info_page = v.Dialog(children=[v.Card(children=[v.CardTitle(children=["SC info"]),
                                                  v.CardText(children=["SC0:\n"
                                                                       ]
                                                             )
                                                  ],
                                        )
                                 ], width=600, height=400)
satcom_info_page.v_model = False

# Info GNSS page
gnss_info_page = v.Dialog(children=[v.Card(children=[v.CardTitle(children=["N index info"]),
                                                v.CardText(children=["N0:\n"
                                                                     ]
                                                           )
                                                ],
                                      )
                               ], width=600, height=400)
gnss_info_page.v_model = False

# Indices
indices_size = 80

R_widget = v.Btn(children=["R0"], class_="ml-4", width=indices_size, height=indices_size, color="green")
R_widget.on_event('click', r_click)
P_widget = v.Btn(children=["P0"], class_="ml-12", width=indices_size, height=indices_size, color="green")
P_widget.on_event('click', p_click)
SC_widget = v.Btn(children=["SC0"], class_="ml-4", width=indices_size, height=indices_size, color="green")
SC_widget.on_event('click', sc_click)
N_widget = v.Btn(children=["N0"], class_="ml-1", width=indices_size, height=indices_size, color="green")
N_widget.on_event('click', n_click)

R_title = v.CardTitle(class_="font-weight-small white--text", children=["HF Radio"])
P_title = v.CardTitle(class_="font-weight-small white--text", children=["Space Operation"])
SC_title = v.CardTitle(class_="font-weight-small white--text", children=["SatCom"])
N_title = v.CardTitle(class_="font-weight-small white--text", children=["GNSS"])

R_info = v.Btn(children=[v.Icon(children=["mdi-information-outline"])], height=40, width=indices_size)
R_info.on_event('click', r_info_click)
R_info_row = v.Row(children=[R_info, hf_info_page], class_="ml-4 mt-2")

P_info = v.Btn(children=[v.Icon(children=["mdi-information-outline"])], height=40, width=indices_size)
P_info.on_event('click', p_info_click)
P_info_row = v.Row(children=[P_info, space_op_info_page], class_="ml-12 mt-2")

SC_info = v.Btn(children=[v.Icon(children=["mdi-information-outline"])], height=40, width=indices_size)
SC_info.on_event('click', sc_info_click)
SC_info_row = v.Row(children=[SC_info, satcom_info_page], class_="ml-4 mt-2")

N_info = v.Btn(children=[v.Icon(children=["mdi-information-outline"])], height=40, width=indices_size)
N_info.on_event('click', n_info_click)
N_info_row = v.Row(children=[N_info, gnss_info_page], class_="ml-1 mt-2")

R_col = v.Col(children=[R_title, R_widget, R_info_row, hf_page], class_="mx-2")
P_col = v.Col(children=[P_title, P_widget, P_info_row, space_op_page], class_="mx-2")
SC_col = v.Col(children=[SC_title, SC_widget, SC_info_row, satcom_page], class_="mx-2")
N_col = v.Col(children=[N_title, N_widget, N_info_row, gnss_page], class_="mx-2")

indices_row = v.Row(children=[R_col, P_col, SC_col, N_col],
                    class_="d-flex align-center justify-center mx-5")

# Today, J + 1, J + 2 buttons
time_btn_width = 80
time_btn_height = 40

today_btn = v.Btn(children=["Today"], width=time_btn_width, height=time_btn_height, color="grey lighten-3")
j1_btn = v.Btn(children=["J + 1"], width=time_btn_width, height=time_btn_height, color="grey lighten-3")
j2_btn = v.Btn(children=["J + 2"], width=time_btn_width, height=time_btn_height, color="grey lighten-3")

prediction_col = v.BtnToggle(v_model="toggle_exclusive", children=[today_btn, j1_btn, j2_btn], class_="mx-2")
prediction_col.on_event('change', prediction_click)

# Refresh button

refresh_btn = v.Btn(children=[v.Icon(children=["mdi-refresh"])], v_on="tooltip.on", height=40, rounded=True,
                    class_="mx-2")

refresh_btn.on_event('click', refresh)

tool_refresh = v.Tooltip(bottom=True, v_slots=[{
    'name': 'activator',
    'variable': 'tooltip',
    'children': refresh_btn,
}], children=["Refresh"])

# Bulletin button

bulletin_btn = v.Btn(children=[v.Icon(children=["mdi-clipboard-text"])], height=40, rounded=True, class_="mx-5")

bulletin_btn.on_event('click', bulletin_click)


# Sources button

sources_btn = v.Btn(children=["Sources"], width=80, height=60, color="grey lighten-2", class_="mx-5")
sources_btn.on_event('click', sources_click)


# Last sun image (171 Angstrom)

sun_img = v.Card(children=[], img="sun_last_img.jpg", width=350, height=350)

# Sunspot number

sunspot_img = v.Card(children=[], img="sunspot.jpg", width=800, height=350)

# Dialog boxes
                      
bulletin_dialog = v.Dialog(children=[v.Card(children=[v.CardTitle(children=["Space weather bulletin"]),
                                     widgets.HTML((get_noaa.get_bulletin()))]
                          )], width=600, height=400)
bulletin_dialog.v_model = False

sources_dialog = v.Dialog(children=[v.Card(children=[v.CardTitle(children=["Sources"]),
                                                     v.CardText(children=["Sources are:\n"
                                                     "https://www.swpc.noaa.gov/\n"
                                                     "http://www.eswua.ingv.it/\n"
                                                     "https://impc.dlr.de/\n"
                                                     "https://ionospheric-prediction.jrc.ec.europa.eu/"])],
                          )], width=500, height=400)
sources_dialog.v_model = False

# Main rows

upper_row = v.Row(children=[tool_refresh, prediction_col, v.Spacer(),bulletin_dialog, bulletin_btn], class_="mx-2")
middle_row = v.Row(children=[indices_row], class_="my-6")
lower_row = v.Row(children=[sources_btn, sources_dialog, sun_img, sunspot_img],
                  class_="d-flex align-end justify-space-between my-6 mx-4")

# Main widget

main = v.Card(children=[title, upper_row, middle_row, lower_row], img="background.jpg", height=750)
