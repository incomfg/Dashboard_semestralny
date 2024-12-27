from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Wczytanie danych
file_path = (r'C:\Users\nz7039\PycharmProjects\WD\Superstore_Sales.xlsx')
data = pd.ExcelFile(file_path)
orders_data = data.parse("Orders")

# Lista unikalnych miast, posortowanych alfabetycznie
unique_cities = sorted(orders_data["City"].unique())

# Lista unikalnych kategorii sprzedaży
unique_categories = sorted(orders_data["Category"].unique())

# Funkcja do generowania wykresu sprzedaży według kategorii produktów
def generate_category_sales_fig(filtered_data):
    return px.bar(
        filtered_data.groupby("Category")["Sales"].sum().reset_index(),
        x="Category", y="Sales", title="Sprzedaż według kategorii produktów",
        labels={"Sales": "Sprzedaż", "Category": "Kategoria"},
        color="Sales", text_auto=True
    )

# Tworzenie aplikacji Dash z Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# 1. Sprzedaż według kategorii produktów
category_sales_fig = generate_category_sales_fig(orders_data)

# 2. Rozkład sprzedaży w regionach
region_sales_fig = px.pie(
    orders_data, names="Region", values="Sales",
    title="Rozkład sprzedaży w regionach"
)

# 3. Proporcja sposobów wysyłki
ship_mode_fig = px.pie(
    orders_data, names="Ship Mode",
    title="Proporcja sposobów wysyłki"
)

# 4. Relacja zysku i sprzedaży
profit_sales_fig = px.scatter(
    orders_data, x="Sales", y="Profit", color="Category",
    title="Relacja zysku i sprzedaży",
    labels={"Sales": "Sprzedaż", "Profit": "Zysk"}
)

# 5. Analiza segmentów klientów
segment_sales_fig = px.bar(
    orders_data.groupby("Segment")["Sales"].sum().reset_index(),
    x="Segment", y="Sales", title="Sprzedaż według segmentu klientów",
    labels={"Sales": "Sprzedaż", "Segment": "Segment"},
    color="Sales", text_auto=True
)

# 6. 10 najlepszych miast pod względem sprzedaży
top_cities = orders_data.groupby("City")["Sales"].sum().nlargest(10).reset_index()
city_sales_fig = px.bar(
    top_cities, x="City", y="Sales", title="10 najlepszych miast pod względem sprzedaży",
    labels={"Sales": "Sprzedaż", "City": "Miasto"},
    text_auto=True,
    color="Sales"
)

# 7. 5 najlepszych stanów pod względem sprzedaży
top_states = orders_data.groupby("State")["Sales"].sum().nlargest(5).reset_index()
state_sales_fig = px.bar(
    top_states, x="State", y="Sales", title="5 najlepszych stanów pod względem sprzedaży",
    labels={"Sales": "Sprzedaż", "State": "Stan"},
    text_auto=True,
    color="Sales"
)

# Layout aplikacji
app.layout = dbc.Container(
    [
        # Nagłówek z gradientowym tłem
        html.Div(
            children=[
                html.H1("Dashboard Sprzedaży Superstore", className="text-center text-light mb-4"),
                html.P(
                    "Dane pochodzą z fikcyjnego sklepu Superstore i zawierają informacje o sprzedaży, "
                    "zyskach, segmentach klientów, kategoriach produktów oraz regionach. Zadanie semestralen Wizualizacja danych UŚ.",
                    className="text-center text-light"
                ),
            ],
            style={
                "background": "linear-gradient(to right, #141E30, #243B55)",
                "padding": "20px",
                "border-radius": "10px"
            }
        ),

        # Dropdown do wyboru miasta
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="city-dropdown",
                        options=[{"label": city, "value": city} for city in unique_cities],
                        placeholder="Wybierz miasto",
                        className="mb-4"
                    ),
                    width=6
                ),
                # Dropdown do wyboru kategorii sprzedaży
                dbc.Col(
                    dcc.Dropdown(
                        id="category-dropdown",
                        options=[{"label": category, "value": category} for category in unique_categories],
                        placeholder="Wybierz kategorię",
                        className="mb-4"
                    ),
                    width=6
                ),
            ]
        ),

        # Pierwszy wiersz z wykresami
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="category-sales-graph", figure=category_sales_fig), width=6),
                dbc.Col(dcc.Graph(id="region-sales-graph", figure=region_sales_fig), width=6),
            ]
        ),

        # Drugi wiersz z wykresami
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="ship-mode-graph", figure=ship_mode_fig), width=6),
                dbc.Col(dcc.Graph(id="profit-sales-graph", figure=profit_sales_fig), width=6),
            ]
        ),

        # Trzeci wiersz z jednym dużym wykresem
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="segment-sales-graph", figure=segment_sales_fig), width=12),
            ]
        ),

        # Czwarty wiersz z nowymi wykresami
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=city_sales_fig), width=6),
                dbc.Col(dcc.Graph(figure=state_sales_fig), width=6),
            ]
        ),
    ],
    fluid=True,
    style={
        "backgroundColor": "#2C3E50",  # Ciemne tło
        "color": "#ECF0F1"  # Jasny tekst
    }
)

# Callbacki do aktualizacji wykresów w zależności od wybranego miasta i kategorii

@app.callback(
    Output("category-sales-graph", "figure"),
    [Input("city-dropdown", "value"),
     Input("category-dropdown", "value")]
)
def update_category_graph(selected_city, selected_category):
    filtered_data = orders_data
    if selected_city:
        filtered_data = filtered_data[filtered_data["City"] == selected_city]
    if selected_category:
        filtered_data = filtered_data[filtered_data["Category"] == selected_category]
    return generate_category_sales_fig(filtered_data)

@app.callback(
    Output("region-sales-graph", "figure"),
    [Input("city-dropdown", "value"),
     Input("category-dropdown", "value")]
)
def update_region_graph(selected_city, selected_category):
    filtered_data = orders_data
    if selected_city:
        filtered_data = filtered_data[filtered_data["City"] == selected_city]
    if selected_category:
        filtered_data = filtered_data[filtered_data["Category"] == selected_category]
    return px.pie(filtered_data, names="Region", values="Sales", title="Rozkład sprzedaży w regionach")

@app.callback(
    Output("ship-mode-graph", "figure"),
    [Input("city-dropdown", "value"),
     Input("category-dropdown", "value")]
)
def update_ship_mode_graph(selected_city, selected_category):
    filtered_data = orders_data
    if selected_city:
        filtered_data = filtered_data[filtered_data["City"] == selected_city]
    if selected_category:
        filtered_data = filtered_data[filtered_data["Category"] == selected_category]
    return px.pie(filtered_data, names="Ship Mode", title="Proporcja sposobów wysyłki")

@app.callback(
    Output("profit-sales-graph", "figure"),
    [Input("city-dropdown", "value"),
     Input("category-dropdown", "value")]
)
def update_profit_sales_graph(selected_city, selected_category):
    filtered_data = orders_data
    if selected_city:
        filtered_data = filtered_data[filtered_data["City"] == selected_city]
    if selected_category:
        filtered_data = filtered_data[filtered_data["Category"] == selected_category]
    return px.scatter(
        filtered_data, x="Sales", y="Profit", color="Category",
        title="Relacja zysku i sprzedaży", labels={"Sales": "Sprzedaż", "Profit": "Zysk"}
    )

@app.callback(
    Output("segment-sales-graph", "figure"),
    [Input("city-dropdown", "value"),
     Input("category-dropdown", "value")]
)
def update_segment_sales_graph(selected_city, selected_category):
    filtered_data = orders_data
    if selected_city:
        filtered_data = filtered_data[filtered_data["City"] == selected_city]
    if selected_category:
        filtered_data = filtered_data[filtered_data["Category"] == selected_category]
    return px.bar(
        filtered_data.groupby("Segment")["Sales"].sum().reset_index(),
        x="Segment", y="Sales", title="Sprzedaż według segmentu klientów",
        labels={"Sales": "Sprzedaż", "Segment": "Segment"},
        color="Sales", text_auto=True
    )

# Uruchomienie aplikacji
if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
