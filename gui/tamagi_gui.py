import ipywidgets as widgets
import ipyvuetify as v

# Main title

title = v.CardTitle(class_="title font-weight-medium white--text", children=["TAMAGI: a space weather tool"])

# Indices

indices_size = 70

R_widget = v.Btn(children=["R0"], width=indices_size, height=indices_size, color="green", class_="mx-2")
P_widget = v.Btn(children=["P0"], width=indices_size, height=indices_size, color="green", class_="mx-2")
SC_widget = v.Btn(children=["SC0"], width=indices_size, height=indices_size, color="green", class_="mx-2")
N_widget = v.Btn(children=["N0"], width=indices_size, height=indices_size, color="green", class_="mx-2")

indices_row = v.Row(children=[R_widget, P_widget, SC_widget, N_widget], class_="mx-2")
indices_row.layout.justify_content = "space-between"

# Today, J + 1, J + 2 buttons
time_btn_width = 80
time_btn_height = 40

today_btn = v.Btn(children=["Today"], width=time_btn_width, height=time_btn_height, color="grey lighten-2")
j1_btn = v.Btn(children=["J + 1"], width=time_btn_width, height=time_btn_height, color="grey lighten-2")
j2_btn = v.Btn(children=["J + 2"], width=time_btn_width, height=time_btn_height, color="grey lighten-2")

prediction_col = v.BtnToggle(v_model="toggle_exclusive", children=[today_btn, j1_btn, j2_btn],
                             style_="margin: 10px 10px 10px 10px")

# Sources button

sources_btn = v.Btn(children=["Sources"], width=80, height=60, color="grey lighten-2", class_="mx-2")

# Sunspot number

sunspot_img = v.Card(children=[], img="sunspot.jpg", width=700, height=400)

# Main rows

middle_row = v.Row(children=[indices_row], class_="my-2", style_="margin: 10px 10px 10px 10px")
lower_row = v.Row(children=[sources_btn, sunspot_img], class_="my-2", style_="margin: 10px 10px 10px 10px")

# Main widget

main = v.Card(children=[title, prediction_col, middle_row, lower_row], img="background.jpg", height=700)
