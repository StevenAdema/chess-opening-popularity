from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from games import Games
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from bokeh.resources import CDN
from bokeh.models import DatetimeTickFormatter


app = Flask(__name__)
app.debug = True

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':  
        print('if')
        elo_range = request.form['service']
        opening_original = request.form['name']
        opening = "['" + opening_original.replace(",", "', '") + "']"
        g = Games('/data/lichess.db', elo=elo_range, opening=opening)
        x = g.df.date.tolist()
        x = [datetime.strptime(d, '%Y.%m.%d') for d in x]
        y = g.df.opening_percentage_played.tolist()
        chart_title = "Popularity of " + opening_original + " by " + elo_range + " ELOs"
        p = figure(title=chart_title, x_axis_type="datetime")
        p.xaxis.formatter = DatetimeTickFormatter(days="%d-%b")
        p.line(x, y, color="darkorange", line_width=3)
        p.yaxis.axis_label = "% of games beginning with " + opening_original
        p.yaxis.axis_label_text_color = "#662900"
        p.xaxis.axis_label = "Date"
        p.xaxis.axis_label_text_color = "#662900"
        script1, div1 = components(p)
        cdn_js = CDN.js_files
        cdn_css = CDN.css_files

        return render_template('index.html', script1=script1, div1=div1, cdn_css=cdn_css, cnd_js=cdn_js)
    else:
        print('else')
        g = Games('/data/lichess.db', elo='ALL', opening="['d4', 'd5', 'c4']")
        x = g.df.date.tolist()
        x = [datetime.strptime(d, '%Y.%m.%d') for d in x]
        y = g.df.opening_percentage_played.tolist()
        chart_title = "Popularity of 1. d4 d5 2. c4 by All ELOs"
        p = figure(title=chart_title, x_axis_type="datetime")
        p.xaxis.formatter = DatetimeTickFormatter(days="%d-%b")
        p.line(x, y, color="darkorange", line_width=3)
        p.yaxis.axis_label = "% of games beginning with 1. d4 d5 2. c4 "
        p.yaxis.axis_label_text_color = "#662900"
        p.xaxis.axis_label = "Date"
        p.xaxis.axis_label_text_color = "#662900"

        script1, div1 = components(p)
        cdn_js = CDN.js_files
        cdn_css = CDN.css_files

        return render_template('index.html', script1=script1, div1=div1, cdn_css=cdn_css, cnd_js=cdn_js)


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