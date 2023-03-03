# Foreign packages
import ipyvuetify as v
import ipywidgets as widgets
from datetime import datetime
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns

# Our packages
import get_noaa
import get_sun_data as gsd

# ---------- Tool Functions ----------


def get_index():
    return str(datetime.now()).replace(":", "_").replace(" ", "_").replace(".", "_", 1)


def delete_sun_img(cur_index):
    for filename in glob.glob("./sun_last_img_*"):
        if filename != ".\\sun_last_img_" + cur_index + ".jpg":
            os.remove(filename)


def delete_muf_img(cur_index):
    for filename in glob.glob("./muf_north_pole_*"):
        if filename != ".\\muf_north_pole_" + cur_index + ".png":
            os.remove(filename)
    for filename in glob.glob("./muf_south_pole_*"):
        if filename != ".\\muf_south_pole_" + cur_index + ".png":
            os.remove(filename)


# ---------- GUI Functions ----------

R = {0: 0, 1: 0, 2: 0}
P = {0: 0, 1: 0, 2: 0}
SC = {0: 0, 1: 0, 2: 0}
N = {0: 0, 1: 0, 2: 0}
Day = 0  # 0 -> Today, 1 -> J+1, 2 -> J+2


# Initialize data
def initialize():
    prediction_col.v_model = Day
    noaa_scales = get_noaa.NoaaScales()
    global R, P, SC, N
    noaa_indices = get_noaa.calculate_indices(noaa_scales)
    R, P = noaa_indices["R"], noaa_indices["P"]
    change_index("R", R[0])
    change_index("P", P[0])
    change_index("SC", SC[0])
    change_index("N", N[0])
    bulletin_dialog.children[0].children[1].value = get_noaa.get_bulletin(R, P, SC, N)
    ssn_data = get_noaa.get_sunspot()
    with sunspot_img:
        sns.set(rc={'figure.figsize': (9, 3.3)})
        sns.set_style('darkgrid')
        sns.lineplot(x='time-tag', y='ssn', data=ssn_data).set(title="Sunspot number (indicator of solar cycle)")
        plt.xlabel("Date")
        plt.ylabel("Monthly average sunspot number")
        plt.xticks([12*i for i in range(11)])
        plt.show()
    index = get_index()
    gsd.get_sun_img(index)
    get_noaa.get_muf(index)
    sun_img.img = "sun_last_img_" + index + ".jpg"
    muf_north_img.img = "muf_north_pole_" + index + ".png"
    muf_south_img.img = "muf_south_pole_" + index + ".png"
    delete_sun_img(index)
    delete_muf_img(index)
    # TODO initialize SC and N


# Refresh all shown indices values
def refresh(widget, event, data):
    refresh_btn.loading = True
    today_btn.disabled = True
    j1_btn.disabled = True
    j2_btn.disabled = True
    if type(prediction_col.v_model) is int:
        change_index("R", R[prediction_col.v_model])
        change_index("P", P[prediction_col.v_model])
        change_index("SC", SC[prediction_col.v_model])
        change_index("N", N[prediction_col.v_model])
    else:
        change_index("R", R[0])
        change_index("P", P[0])
        change_index("SC", SC[0])
        change_index("N", N[0])
    bulletin_dialog.children[0].children[1].value = get_noaa.get_bulletin(R, P, SC, N)
    index = get_index()
    gsd.get_sun_img(index)
    get_noaa.get_muf(index)
    sun_img.img = "sun_last_img_" + index + ".jpg"
    muf_north_img.img = "muf_north_pole_" + index + ".png"
    muf_south_img.img = "muf_south_pole_" + index + ".png"
    delete_sun_img(index)
    delete_muf_img(index)
    today_btn.disabled = False
    j1_btn.disabled = False
    j2_btn.disabled = False
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
    global Day
    if type(prediction_col.v_model) is int:
        Day = prediction_col.v_model
    else:
        prediction_col.v_model = Day
    change_index("R", R[Day])
    change_index("P", P[Day])
    change_index("SC", SC[Day])
    change_index("N", N[Day])


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
muf_north_img = v.Card(children=[], width=675, height=595, class_="my-2 mx-2")
muf_south_img = v.Card(children=[], width=675, height=595, class_="my-2 mx-2")

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
            widgets.HTML("""<table style="border:1px solid black">
              <colgroup>
                <col width="5%">
                <col width="7%">
                <col width="65%">
                <col width="8%">
                <col width="15%">  </colgroup>
              <tbody><tr>
                <th><strong>Scale</strong></th>
                <th><strong>Description</strong></th>
                <th><strong>Effect</strong></th>
                <th><strong>Physical measure</strong></th>
                <th><strong>Average Frequency</strong><br>
                        (1 cycle = 11 years)</th>
              </tr>
              <tr>
                <td class="noaa_scale_bg_5 numeric_scale">R 5</td>
                <td class="scale_description">Extreme</td>
                <td><p><b>HF Radio:</b> Complete HF (high frequency) radio blackout on the entire sunlit side of the Earth lasting for a number of hours. This results in no HF radio contact with mariners and en route aviators in this sector.</p>
                  <p><b>Navigation:</b> Low-frequency navigation signals used by maritime and general aviation systems experience outages on the sunlit side of the Earth for many hours, causing loss in positioning. Increased satellite navigation errors in positioning for several hours on the sunlit side of Earth, which may spread into the night side.</p></td>
                <td>X20<br> (2 x 10<sup>-3</sup>)</td>
                <td>Less than 1 per cycle</td>
              </tr>
              <tr>
                <td class="noaa_scale_bg_4 numeric_scale">R 4</td>
                <td class="scale_description">Severe</td>
                <td><p><b>HF Radio:</b> HF radio communication blackout on most of the sunlit side of Earth for one to two hours. HF radio contact lost during this time.</p>
                  <p><b>Navigation:</b> Outages of low-frequency navigation signals cause increased error in positioning for one to two hours. Minor disruptions of satellite navigation possible on the sunlit side of Earth.</p></td>
                <td>X10<br> (10<sup>-3</sup>)</td>
                <td>8 per cycle<br> (8 days per cycle)</td>
              </tr>
              <tr>
                <td class="noaa_scale_bg_3 numeric_scale">R 3</td>
                <td class="scale_description">Strong</td>
                <td><p><b>HF Radio:</b> Wide area blackout of HF radio communication, loss of radio contact for about an hour on sunlit side of Earth.</p>
                  <p><b>Navigation:</b> Low-frequency navigation signals degraded for about an hour.</p></td>
                <td>X1<br> (10<sup>-4</sup>) </td>
                <td>175 per cycle<br> (140 days per cycle)</td>
              </tr>
              <tr>
                <td class="noaa_scale_bg_2 numeric_scale">R 2</td>
                <td class="scale_description">Moderate</td>
                <td><p><b>HF Radio:</b> Limited blackout of HF radio communication on sunlit side, loss of radio contact for tens of minutes.</p>
                  <p><b>Navigation:</b> Degradation of low-frequency navigation signals for tens of minutes.</p></td>
                <td>M5<br> (5 x 10<sup>-5</sup>)</td>
                <td>350 per cycle<br> (300 days per cycle)</td>
              </tr>
              <tr>
                <td class="noaa_scale_bg_1 numeric_scale">R 1</td>
                <td class="scale_description">Minor</td>
                <td>
                  <p><b>HF Radio:</b> Weak or minor degradation of HF radio communication on sunlit side, occasional loss of radio contact.</p>
                  <p><b>Navigation:</b> Low-frequency navigation signals degraded for brief intervals.</p></td>
                <td>M1<br> (10<sup>-5</sup>)</td>
                <td>2000 per cycle<br> (950 days per cycle)</td>
              </tr>
             </tbody></table>""",
             layout=widgets.Layout(margin='0px 20px 0px 20px'))
                                              ],
                                    )
                             ], width=1000, height=600)
hf_info_page.v_model = False

# Info Space Operations page
space_op_info_page = v.Dialog(children=[v.Card(children=[v.CardTitle(children=["P index info"]),
    widgets.HTML("""<table style="border:1px solid black">
              <colgroup>
                <col width="7%">
                <col width="9%">
                <col width="67%">
                <col width="17%">  </colgroup>
              <tbody><tr>
                <th><strong>Scale</strong></th>
                <th><strong>Description</strong></th>
                <th><strong>Effect</strong></th>
                <th><strong>Average Frequency</strong><br>
                        (1 cycle = 11 years)</th>
              </tr>
              <tr>
                <td class="noaa_scale_bg_5 numeric_scale">P 5</td>
                <td class="scale_description">Extreme</td>
                <td><p><b>Space Operation:</b> Satellites may be rendered useless, memory impacts can cause loss of 
                control, may cause serious noise in image data, star-trackers may be unable to locate sources; 
                permanent damage to solar panels possible. Extensive surface charging likely as well as uplink/downlink
                problems.</p>
                <td>4 days per cycle</td>
              </tr>
              <tr>
                <td class="noaa_scale_bg_4 numeric_scale">P 4</td>
                <td class="scale_description">Severe</td>
                <td><p><b>Space Operation:</b>May experience surface charging, memory device problems and noise on 
                imaging systems; star-tracker problems may cause orientation problems and require corrections, and 
                solar panel efficiency can be degraded</p>
                <td>100 per cycle<br> (8 days per cycle)</td>
              </tr>
              <tr>
                <td class="noaa_scale_bg_3 numeric_scale">P 3</td>
                <td class="scale_description">Strong</td>
                <td><p><b>Space Operation:</b>Surface charging may occur on satellite components, drag may increase on 
                low-Earth-orbit satellites, and corrections may be needed for orientation problems. Single-event upsets,
                 noise in imaging systems, and slight reduction of efficiency in solar panel are likely.</p>
                <td>200 per cycle<br> (140 days per cycle)</td>
              </tr>
              <tr>
                <td class="noaa_scale_bg_2 numeric_scale">P 2</td>
                <td class="scale_description">Moderate</td>
                <td><p><b>Space Operation:</b>Corrective actions to orientation may be required by ground control; 
                possible changes in drag affect orbit predictions. Infrequent single-event upsets possible.</p>
                <td>600 per cycle<br> (300 days per cycle)</td>
              </tr>
              <tr>
                <td class="noaa_scale_bg_1 numeric_scale">P 1</td>
                <td class="scale_description">Minor</td>
                <td>
                  <p><b>Space Operation:</b>Minor impact on satellite operations possible.</p>
                <td>1700 per cycle<br> (900 days per cycle)</td>
              </tr>
             </tbody></table>""",
             layout=widgets.Layout(margin='0px 20px 0px 20px'))

                                                    ],
                                          )
                                   ], width=1000, height=600)
space_op_info_page.v_model = False

# Info Satellite Communications page
satcom_info_page = v.Dialog(children=[v.Card(children=[v.CardTitle(children=["SC index info"]),
                                                  v.CardText(children=["SC0:\n"
                                                                       ]
                                                             )
                                                  ],
                                        )
                                 ], width=1000, height=600)
satcom_info_page.v_model = False

# Info GNSS page
gnss_info_page = v.Dialog(children=[v.Card(children=[v.CardTitle(children=["N index info"]),
                                                v.CardText(children=["N0:\n"
                                                                     ]
                                                           )
                                                ],
                                      )
                               ], width=1000, height=600)
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
sun_img = v.Card(children=[], width=350, height=350)

# Sunspot number
sunspot_img = widgets.Output()  # v.Card(children=[], img="sunspot.jpg", width=800, height=350)

# Dialog boxes
bulletin_dialog = v.Dialog(children=[v.Card(children=[v.CardTitle(children=["Space weather bulletin"]),
                                     widgets.HTML(layout=widgets.Layout(margin='0px 20px 0px 20px'))])
                                     ], width=700, height=500)
bulletin_dialog.v_model = False

sources_dialog = v.Dialog(children=[v.Card(children=[v.CardTitle(children=["Sources"]),
                                                     v.CardText(children=[widgets.HTML(value='Sources are:<br>'
                                                     '<a href="https://www.swpc.noaa.gov/">www.swpc.noaa.gov</a><br>'
                                                     '<a href="http://www.eswua.ingv.it/">www.eswua.ingv.it</a><br>'
                                                     '<a href="https://impc.dlr.de/">impc.dlr.de</a><br>'
                                                     '<a href="https://ionospheric-prediction.jrc.ec.europa.eu/">'
                                                     'ionospheric-prediction.jrc.ec.europa.eu</a><br>')])
                                                     ],
                                           )], width=500, height=400)
sources_dialog.v_model = False

# Main rows
upper_row = v.Row(children=[tool_refresh, prediction_col, v.Spacer(), bulletin_dialog, bulletin_btn], class_="mx-2")
middle_row = v.Row(children=[indices_row], class_="my-6")
lower_row = v.Row(children=[sources_btn, sources_dialog, sun_img, sunspot_img],
                  class_="d-flex align-end justify-space-between my-6 mx-4")

# Main widget
main = v.Card(children=[title, upper_row, middle_row, lower_row], img="background.jpg", height=750)
