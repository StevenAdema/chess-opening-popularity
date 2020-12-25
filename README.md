# chess-opening-popularity
chess-opening-explorer is a Flask-Python app that reads a pgn database of chess games to map the popularity of a provided opening against a set of ELOs.

## Sample

![Queen's Gambit Popularity](/conf/showcase.gif?raw=true)

## Insipiration and Example
Online chess traffic has increased nearly 40% month-over-month since the release of Netflix's The Queen's Gambit on Oct. 23, 2020. In Beth Harmon's final match, she opens with the series' namesake: The Queen's Gambit (1. d4 d5 2. c4).  There have been numerous articles covering the recent rise in chess. This project was built to determine if the influx of new players from the popular series also led to a similar boost in the relative use of the opening.

By analyzing all games played on lichess.org over the past two months(~150 million), we can compare the popularity of an opening. A PGN (Portable Game Notation) is a plain text record of of both game metadata (date, player ELOs, winner, time control, etc) as well as the moves made in the game.  Running the app against lichess.org's Oct and Nov databases against the opening 1. d4 d5 2. c4, we see the following:

<br/>

![Queen's Gambit Popularity](/conf/queens_gambit.PNG?raw=true)

Wow! A 40% relative increase from the pre-release October average to it's peak in mid November among players in the 800-1000 ELO range.

<br/>

![King's Pawn Popularity](/conf/e4e5Nf3.PNG?raw=true)

Similarly, the impact of a large new player base has lead to an increase in the popularity of the King's Pawn Opening.  This opening leads to the Italian Game and Guico Piano, two very common lines for beginners to study.



## Installation
1. Clone the repo.
2. Download the full record of games for Oct, Nov from https://database.lichess.org/. Unzip the files to ./data
3. Run the requirements script to install the required packages.
4. '''pip install -r requirements.txt'''
5. '''env\scripts\activate'''
6. '''python app.py'''
7. Open http://127.0.0.1:5000/

