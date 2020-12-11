# chess-opening-popularity
chess-opening-explorer is a python app that reads a pgn database of chess games to map the popularity of a provided opening.

## Insipiration and Example
Online chess traffic has increased nearly 40% month-over-month since the release of Netflix's The Queen's Gambit on Oct. 23, 2020. In Beth Harmon's final match, she opens with the series' namesake: The Queen's Gambit (1. d4 d5 2. c4).  There have been numerous articles covering the recent rise in chess. This project was built to determine if the influx of new players from the popular series also led to a similar boost in the relative use of the opening.

By analyzing all games played on lichess.org over the past two months(~150 million), we can compare the popularity of an opening. A PGN (Portable Game Notation) is a plain text record of of both game metadata (date, player ELOs, winner, time control, etc) as well as the moves made in the game.  Running the app against lichess.org's Oct and Nov databases against the opening 1. d4 d5 2. c4, we see the following:


![Queen's Gambit Popularity](../conf/d4d5c4.PNG "Queen's Gambit Popularity")

Approx. a 7% relative increase from the pre-release October average to it's peak in mid November. The King's Knight, a very beginner friendly opening, also saw a similar bump in popularity.

![King's Pawn Popularity](../conf/e4e5Nf4.PNG "King's Pawn Popularity")

The French Defense, an opening less likely to be studied by beginners in their first week, saw a decrease in popularity.

![French Defense Popularity](../conf/e4e6d4.PNG "French Defense Popularity")



## Installation
1. Dowlnoad the full record of games for Oct, Nov from https://database.lichess.org/. Unzip the files to ./data
2. Clone the repo.
3. Run the requirements script to install any required packages.
4. Run the code from cmd or the IDE of you choice.
