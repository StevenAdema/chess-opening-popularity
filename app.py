from flask import Flask, render_template, url_for, request, redirect
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
from games import Games
import pandas as pd
import numpy as np
import base64
import json
import io
import plotly
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
plt.style.use('fivethirtyeight')

app = Flask(__name__)
# app.debug = True

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':  
        print('if')
        elo_range = request.form['content']
        opening = request.form['content2']   
        print(elo_range, opening)  
        g = Games('/data/lichess.db', elo=elo_range, opening=opening)
    
        x = g.df['date'].tolist()
        x = [datetime.strptime(d, '%Y.%m.%d') for d in x]
        x = [datetime.strftime(d, '%b-%d') for d in x]

        graph = dict(
            data=[go.Bar(
                x=x,
                y=g.df['opening_percentage_played']
            )],
            layout=dict(
                title='Bar Plot',
                yaxis=dict(
                    title="opening_percentage_played"
                ),
                xaxis=dict(
                    title="date"
                )
            )
        )

        # Convert the figures to JSON
        graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder) 
        return render_template('chart.html', graphJSON=graphJSON)
    else:
        print('else')
        elo_range = '800-1000'
        opening = "['e4','e5','Ke2']" 
        g = Games('/data/lichess.db', elo=elo_range, opening=opening)
        # plot_popularity(g.df, elo=elo_range)
        x = g.df['date'].tolist()
        x = [datetime.strptime(d, '%Y.%m.%d') for d in x]
        x = [datetime.strftime(d, '%b-%d') for d in x]

        graph = dict(
            data=[go.Bar(
                x=x,
                y=g.df['opening_percentage_played']
            )],
            layout=dict(
                title='Bar Plot',
                yaxis=dict(
                    title="opening_percentage_played"
                ),
                xaxis=dict(
                    title="date"
                )
            )
        )

        # Convert the figures to JSON
        graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder) 
        return render_template('index.html', graphJSON=graphJSON)

# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         elo_range = request.form['content']
#         opening = request.form['content2']
        
#         g = Games('/data/lichess.db', elo=elo_range, opening=opening)
#         # plot_popularity(g.df, elo=elo_range)
#         x = g.df['date'].tolist()
#         x = [datetime.strptime(d, '%Y.%m.%d') for d in x]
#         x = [datetime.strftime(d, '%b-%d') for d in x]

#         graph = dict(
#             data=[go.Bar(
#                 x=x,
#                 y=g.df['opening_percentage_played']
#             )],
#             layout=dict(
#                 title='Bar Plot',
#                 yaxis=dict(
#                     title="opening_percentage_played"
#                 ),
#                 xaxis=dict(
#                     title="date"
#                 )
#             )
#         )

#         # Convert the figures to JSON
#         graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder) 
#         return render_template('index.html', graphJSON=graphJSON)
#     else:
#         return render_template('index.html')


def plot_popularity(df, opening_name='unknown', elo=None):
    """ Creates a line plot of the relative popularity of an opening over a defined
    period of time.
    Args:
        df: the DataFrame containing the date axis and column named 'opening' with
            the relative popularity of the move per each day
        opening_name: The plain text name of the opening for use in the legend
        elo: the elo range of the players using the opening for use in the legend
        """
    img = io.BytesIO()

    x = df['date'].tolist()
    x = [datetime.strptime(d, '%Y.%m.%d') for d in x]
    x = [datetime.strftime(d, '%b-%d') for d in x]

    fig, ax = plt.subplots(figsize=(12, 6))
    # fig, ax = plt.subplots()
    plt.xticks(np.arange(0, 62, 7))
    ax.plot(x, df['opening_percentage_played'])
    plt.gca().yaxis.set_major_formatter(PercentFormatter(100, decimals=2))
    if elo is not None:
        plt.legend(labels=['% of games beginning with ' + opening_name + ' for ' + elo + ' ELO players'], loc=2)
    else:
        plt.legend(labels=['% of games beginning with ' + opening_name], loc=2)
    plt.title('Popularity of ' + opening_name + ' on lichess.org')
    # plt.annotate("♕ Release of 'The Queen\'s Gambit'", (22.6, 1.73))
    fig.savefig('/data/img.png')
    plt.close(fig)

if __name__ == "__main__":
    app.run(debug=True)