from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from games import Games
import pandas as pd
import numpy as np
import base64
import io
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
plt.style.use('fivethirtyeight')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        elo_range = request.form['content']
        opening = request.form['content2']
        
        g = Games('/data/lichess.db', elo=elo_range, opening=opening)
        plot_popularity(g.df, elo=elo_range)

        try:
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

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
    return render_template('/', name = plt.show())

if __name__ == "__main__":
    app.run(debug=True)