#TP
import pandas as pd
import calendar as cal
import plotly.express as px
import plotly.graph_objects as go

## Etape 2 préparation des données 

df = pd.read_csv("data.csv")


cols = ['CustomerID', 'Gender', 'Location', 'Product_Category', 
        'Quantity', 'Avg_Price', 'Transaction_Date', 'Month', 'Discount_pct']
df = df[cols]


df['CustomerID'] = df['CustomerID'].fillna(0).astype(int)


df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])


df['Total_price'] = df['Quantity'] * df['Avg_Price'] * (1 - df['Discount_pct'] / 100)

print(df.head())
## Etape 3 Ecrire les fonctions métier 

def chiffre_affaire(data):
    return data['Total_price'].sum()



def frequence_meilleure_vente(data, top=10, ascending=False):

    resultat = data.groupby('Product_Category')['Quantity'].sum().reset_index(name='Nombre_Ventes')
    
    
    resultat = resultat.sort_values(by='Nombre_Ventes', ascending=ascending)
    
    
    return resultat.head(top)



def indicateur_du_mois(data, current_month=12):
    """
    Calcule le CA et les quantités du mois actuel avec la variation 
    par rapport au mois précédent.
    """
    # Filtrer les données
    data_current_month = data[data['Month'] == current_month]
    # Astuce : le mois précédent de Janvier (1) est Décembre (12)
    previous_month = 12 if current_month == 1 else current_month - 1
    data_previous_month = data[data['Month'] == previous_month]

    # Calculs Actuels
    ca_current_month = data_current_month['Total_price'].sum()
    quantity_current_month = data_current_month['Quantity'].sum()

    # Calculs Précédents
    ca_previous_month = data_previous_month['Total_price'].sum()
    quantity_previous_month = data_previous_month['Quantity'].sum()

    # Calculer la différence en pourcentage
    ca_diff_percent = ((ca_current_month - ca_previous_month) / ca_previous_month * 100) if ca_previous_month != 0 else 0
    quantity_diff_percent = ((quantity_current_month - quantity_previous_month) / quantity_previous_month * 100) if quantity_previous_month != 0 else 0

    # Affichage corrigé (tout sur la même ligne pour éviter le SyntaxError)
    print(f"Chiffre d'affaires du mois {current_month}: {ca_current_month:.2f}€")
    print(f"Quantité vendue du mois {current_month}: {quantity_current_month}")
    print(f"Différence CA vs mois précédent: {ca_diff_percent:.2f}%")
    print(f"Différence Quantité vs mois précédent: {quantity_diff_percent:.2f}%")
    
    return ca_current_month, ca_diff_percent, quantity_current_month, quantity_diff_percent

          

   
    


print(chiffre_affaire(df))


print(frequence_meilleure_vente(df, top=10))


print(indicateur_du_mois(df, current_month=12))
## Etape 4 graphique 
def barplot_top_10_ventes(data):
    
    top_10_categories = data.groupby('Product_Category')['Quantity'].sum().sort_values(ascending=False).head(10).index
    
    
    df_plot = data[data['Product_Category'].isin(top_10_categories)]
    
    
    df_plot = df_plot.groupby(['Product_Category', 'Gender'])['Quantity'].sum().reset_index()

    
    fig = px.bar(
        df_plot,
        x='Quantity',
        y='Product_Category',
        color='Gender',
        orientation='h',
        barmode='group', 
        title="Fréquence des 10 meilleures ventes",
        labels={'Quantity': 'Total vente', 'Product_Category': 'Catégorie du produit'},
        category_orders={"Product_Category": list(top_10_categories)},
        color_discrete_map={'F': '#5D6DFF', 'M': '#FF5D43'} 
    )

    
    fig.update_layout(
        plot_bgcolor='rgba(240,244,250,1)', 
        paper_bgcolor='white',
        xaxis_title="Total vente",
        yaxis_title="",
        legend_title="Sexe"
    )
    
    return fig


fig_top10 = barplot_top_10_ventes(df)
fig_top10.show()
def plot_evolution_chiffre_affaire(data):
    
    df_evolution = (
        data.groupby('Month')['Total_price']
        .sum()
        .reset_index()
        .sort_values('Month')
    )
    
    fig = px.line(
        df_evolution,
        x='Month',
        y='Total_price',
        title="Évolution du chiffre d'affaires",
        labels={
            'Month': 'Mois',
            'Total_price': "Chiffre d'affaires (€)"
        }
    )
    
    fig.update_traces(
        line_color='#5D6DFF',
        line_width=2
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(240,244,250,1)',
        paper_bgcolor='white',
        xaxis_title="Mois",
        yaxis_title="Chiffre d'affaires (€)"
    )
    
    return fig


fig_evolution = plot_evolution_chiffre_affaire(df)
fig_evolution.show()
def plot_chiffre_affaire_mois(data):
    
    data_dec = data[data['Month'] == 12]
    data_nov = data[data['Month'] == 11]
    
    ca_mois_courant = data_dec['Total_price'].sum()
    ca_mois_precedent = data_nov['Total_price'].sum()
    qty_mois_courant = data_dec['Quantity'].sum()
    qty_mois_precedent = data_nov['Quantity'].sum()

    fig = go.Figure()

    # Indicateur CA
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=ca_mois_courant,
        delta={
            'reference': ca_mois_precedent,
            'valueformat': '.0f',
            'suffix': '€',
            'increasing': {'color': '#2ecc71'},
            'decreasing': {'color': '#e74c3c'},
        },
        title={
            "text": "Décembre<br><span style='font-size:0.8em;color:gray'>Chiffre d'affaires</span>",
            "font": {"size": 18}
        },
        number={
            'suffix': '€',
            'valueformat': '.0f',
            'font': {'size': 48, 'color': '#2c3e6b'}
        },
        domain={'x': [0, 0.5], 'y': [0, 1]}
    ))

    # Indicateur Quantité
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=qty_mois_courant,
        delta={
            'reference': qty_mois_precedent,
            'valueformat': '.0f',
            'increasing': {'color': '#2ecc71'},
            'decreasing': {'color': '#e74c3c'},
        },
        title={
            "text": "Décembre<br><span style='font-size:0.8em;color:gray'>Quantités vendues</span>",
            "font": {"size": 18}
        },
        number={
            'valueformat': '.0f',
            'font': {'size': 48, 'color': '#2c3e6b'}
        },
        domain={'x': [0.5, 1], 'y': [0, 1]}
    ))

    fig.update_layout(
        paper_bgcolor='white',
        height=200,
        margin=dict(t=60, b=20, l=20, r=20),
    )

    return fig


fig_ca_mois = plot_chiffre_affaire_mois(df)
fig_ca_mois.show()
def plot_vente_mois(data, abbr=True):
    df_vente = (
        data.groupby(['Month', 'Gender'])['Quantity']
        .sum()
        .reset_index()
        .sort_values('Month')
    )
    df_vente['Mois'] = df_vente['Month'].apply(
        lambda x: calendar.month_abbr[x] if abbr else calendar.month_name[x]
    )
    fig = px.bar(
        df_vente, x='Mois', y='Quantity', color='Gender',
        barmode='group',
        title="Ventes par mois",
        labels={'Quantity': 'Quantités vendues', 'Mois': 'Mois', 'Gender': 'Sexe'},
        color_discrete_map={'F': '#5D6DFF', 'M': '#FF5D43'},
        category_orders={'Mois': [calendar.month_abbr[i] for i in range(1, 13)]}
    )
    fig.update_layout(
        plot_bgcolor='rgba(240,244,250,1)', paper_bgcolor='white',
        xaxis_title="Mois", yaxis_title="Quantités vendues", legend_title="Sexe",
        margin=dict(t=40, b=20)
    )
    return fig
fig_vente_mois = plot_vente_mois(df, abbr=True)
fig_vente_mois.show()
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import calendar
from dash import Dash, dcc, html, dash_table, Input, Output

# ── 1. Chargement & préparation ───────────────────────────────────────────────
df = pd.read_csv('data.csv')

cols = ['CustomerID', 'Gender', 'Location', 'Product_Category',
        'Quantity', 'Avg_Price', 'Transaction_Date', 'Month', 'Discount_pct']
df = df[cols]
df['CustomerID'] = df['CustomerID'].fillna(0).astype(int)
df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])
df['Total_price'] = df['Quantity'] * df['Avg_Price'] * (1 - df['Discount_pct'] / 100)

# ── 2. Fonctions graphiques ───────────────────────────────────────────────────
def barplot_top_10_ventes(data):
    top_10 = data.groupby('Product_Category')['Quantity'].sum()\
                 .sort_values(ascending=False).head(10).index
    df_plot = data[data['Product_Category'].isin(top_10)]
    df_plot = df_plot.groupby(['Product_Category', 'Gender'])['Quantity'].sum().reset_index()
    fig = px.bar(
        df_plot, x='Quantity', y='Product_Category', color='Gender',
        orientation='h', barmode='group',
        title="Fréquence des 10 meilleures ventes",
        labels={'Quantity': 'Total vente', 'Product_Category': 'Catégorie du produit'},
        category_orders={"Product_Category": list(top_10)},
        color_discrete_map={'F': '#5D6DFF', 'M': '#FF5D43'}
    )
    fig.update_layout(
        plot_bgcolor='rgba(240,244,250,1)', paper_bgcolor='white',
        xaxis_title="Total vente", yaxis_title="", legend_title="Sexe",
        margin=dict(t=40, b=20)
    )
    return fig


def plot_evolution_chiffre_affaire(data):
    df_evo = data.groupby('Month')['Total_price'].sum().reset_index().sort_values('Month')
    df_evo['Mois'] = df_evo['Month'].apply(lambda x: calendar.month_abbr[x])
    fig = px.line(
        df_evo, x='Mois', y='Total_price',
        title="Évolution du chiffre d'affaires par mois",
        labels={'Mois': 'Mois', 'Total_price': "Chiffre d'affaires (€)"}
    )
    fig.update_traces(line_color='#5D6DFF', line_width=2, fill='tozeroy',
                      fillcolor='rgba(93,109,255,0.1)')
    fig.update_layout(
        plot_bgcolor='rgba(240,244,250,1)', paper_bgcolor='white',
        margin=dict(t=40, b=20)
    )
    return fig


def plot_chiffre_affaire_mois(data):
    ca_dec  = data[data['Month'] == 12]['Total_price'].sum()
    ca_nov  = data[data['Month'] == 11]['Total_price'].sum()
    qty_dec = data[data['Month'] == 12]['Quantity'].sum()
    qty_nov = data[data['Month'] == 11]['Quantity'].sum()

    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number+delta", value=ca_dec,
        delta={'reference': ca_nov, 'valueformat': '.0f', 'suffix': '€',
               'increasing': {'color': '#2ecc71'}, 'decreasing': {'color': '#e74c3c'}},
        title={"text": "December<br><span style='font-size:0.8em;color:gray'>Chiffre d'affaires</span>",
               "font": {"size": 16}},
        number={'suffix': '€', 'valueformat': '.3s', 'font': {'size': 48, 'color': '#2c3e6b'}},
        domain={'x': [0, 0.5], 'y': [0, 1]}
    ))
    fig.add_trace(go.Indicator(
        mode="number+delta", value=qty_dec,
        delta={'reference': qty_nov, 'valueformat': '.0f',
               'increasing': {'color': '#2ecc71'}, 'decreasing': {'color': '#e74c3c'}},
        title={"text": "December<br><span style='font-size:0.8em;color:gray'>Quantités vendues</span>",
               "font": {"size": 16}},
        number={'valueformat': '.0f', 'font': {'size': 48, 'color': '#2c3e6b'}},
        domain={'x': [0.5, 1], 'y': [0, 1]}
    ))
    fig.update_layout(paper_bgcolor='white', height=160, margin=dict(t=30, b=10, l=10, r=10))
    return fig


def table_100_dernieres_ventes(data):
    df_last = data.sort_values('Transaction_Date', ascending=False).head(100)
    df_last = df_last[['Transaction_Date', 'Gender', 'Location',
                        'Product_Category', 'Quantity', 'Avg_Price', 'Discount_pct']].copy()
    df_last['Transaction_Date'] = df_last['Transaction_Date'].dt.strftime('%Y-%m-%d')
    df_last.columns = ['Date', 'Gender', 'Location', 'Product Category',
                       'Quantity', 'Avg Price', 'Discount Pct']
    return df_last

# ── 3. Layout ─────────────────────────────────────────────────────────────────
app = Dash(__name__)
server = app.server

locations = ['Toutes'] + sorted(df['Location'].dropna().unique().tolist())

app.layout = html.Div(style={
    'fontFamily': 'Segoe UI, sans-serif',
    'backgroundColor': '#f4f6fb',
    'minHeight': '100vh'
}, children=[

    # ── Header ──
    html.Div(style={
        'backgroundColor': '#2c3e6b',
        'padding': '14px 24px',
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center'
    }, children=[
        html.H2("ECAP Store", style={'color': 'white', 'margin': 0}),
        dcc.Dropdown(
            id='dropdown-location',
            options=[{'label': l, 'value': l} for l in locations],
            value='Toutes',
            clearable=False,
            placeholder="Choisissez des zones",
            style={'width': '220px', 'fontSize': '14px'}
        )
    ]),

    # ── Ligne 1 : KPI (gauche) + Evolution CA (droite) ──
    html.Div(style={
        'display': 'flex',
        'gap': '16px',
        'padding': '16px 24px 8px 24px'
    }, children=[

        # Colonne gauche : KPI
        html.Div(style={
            'flex': '1',
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'padding': '8px',
            'boxShadow': '0 1px 4px rgba(0,0,0,0.1)'
        }, children=[
            dcc.Graph(id='graph-kpi', config={'displayModeBar': False},
                      style={'height': '160px'})
        ]),

        # Colonne droite : Evolution CA
        html.Div(style={
            'flex': '1.3',
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'padding': '8px',
            'boxShadow': '0 1px 4px rgba(0,0,0,0.1)'
        }, children=[
            dcc.Graph(id='graph-evolution', config={'displayModeBar': False},
                      style={'height': '300px'})
        ]),
    ]),

    # ── Ligne 2 : Top 10 (gauche) + Table (droite) ──
    html.Div(style={
        'display': 'flex',
        'gap': '16px',
        'padding': '8px 24px 24px 24px'
    }, children=[

        # Colonne gauche : Top 10
        html.Div(style={
            'flex': '1',
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'padding': '8px',
            'boxShadow': '0 1px 4px rgba(0,0,0,0.1)'
        }, children=[
            dcc.Graph(id='graph-top10', config={'displayModeBar': False},
                      style={'height': '450px'})
        ]),

        # Colonne droite : Table
        html.Div(style={
            'flex': '1.3',
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'padding': '16px',
            'boxShadow': '0 1px 4px rgba(0,0,0,0.1)'
        }, children=[
            html.H4("Table des 100 dernières ventes",
                    style={'marginTop': 0, 'color': '#2c3e6b', 'fontSize': '15px'}),
            dash_table.DataTable(
                id='table-ventes',
                page_size=7,
                filter_action='none',
                sort_action='native',
                style_table={
                    'overflowX': 'auto',
                    'maxHeight': '350px',
                    'overflowY': 'auto'
                },
                style_header={
                    'backgroundColor': '#f4f6fb', 'fontWeight': 'bold',
                    'fontSize': '13px', 'color': '#2c3e6b'
                },
                style_cell={
                    'fontSize': '13px', 'padding': '8px',
                    'textAlign': 'left', 'color': '#333'
                },
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#fafbff'}
                ]
            )
        ]),
    ]),
])

# ── 4. Callbacks ──────────────────────────────────────────────────────────────
@app.callback(
    Output('graph-kpi',       'figure'),
    Output('graph-evolution', 'figure'),
    Output('graph-top10',     'figure'),
    Output('table-ventes',    'data'),
    Output('table-ventes',    'columns'),
    Input('dropdown-location', 'value')
)
def update_dashboard(location):
    filtered = df if location == 'Toutes' else df[df['Location'] == location]
    df_table = table_100_dernieres_ventes(filtered)
    columns  = [{'name': c, 'id': c} for c in df_table.columns]
    return (
        plot_chiffre_affaire_mois(filtered),
        plot_evolution_chiffre_affaire(filtered),
        barplot_top_10_ventes(filtered),
        df_table.to_dict('records'),
        columns
    )

# ── 5. Lancement ──────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=False, port=8050, jupyter_mode="external")
