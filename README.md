# Tennis Match Predictor
*Author: [Malchu Pascual](https://github.com/malchu)*<br />
*Link: [Tennis Match Predictor](https://tennismatchpredictor.malchupascual.repl.co/)*
## Introduction
Tennis is a sophisticated sport. It can often be extremely difficult to predict who will win a tennis match due to many deciding factors, such as form, rank, head-to-head, and win-loss record. This program accounts for many of those factors to solve this problem by being able to predict who will win in an ATP tennis match between 2 men's professional players. Given 2 names of ATP players as input for a tennis match between them, a winner is predicted along with percent probabilities of how likely each player could win that match.
## Description
### Background
The user interface consists of the title, 2 text boxes to input each player's name, 2 photos for the profile pictures of each of those respective players, and the "Predict!" button. Once you click "Predict!", a donut graph will appear with the probabilities of winning for both players along with a prediction statement at the bottom. The photos, graph, and prediction statement change depending on which players are inputted, and you can continuously input different players after each prediction.<br /><br />
**Copyright Disclaimer**<br />
I do not own any of the photos used in the application. All player media used are owned by the [ATP Tour](https://www.atptour.com/en/).
## Installation
### Prerequisites
To run the application locally, you must have installed:
* [Python 3.9 (or higher)](https://www.python.org/downloads/)
* [pip](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/)
* [Beautifulsoup](https://www.geeksforgeeks.org/beautifulsoup-installation-python/)
* [Matplotlib](https://matplotlib.org/stable/users/installing/index.html)
### Running Application
To run the application locally, first clone this repository.
## How to Use
1. Input an ATP player's full name in each of the 2 text boxes. Make sure to spell their full names correctly.
2. Click "Predict!" and wait for the results to come up.
3. Voila! You can now see who will win that match and the likelihood.
### Walkthrough
![](https://github.com/malchu/tennismatchpredictor/blob/master/examples/usage.gif)
## Example Output
### Default
![Alt text](examples/win.jpg?raw=true "")
### Close Match
![Alt text](examples/close.jpg?raw=true "")
### Rout
![Alt text](examples/crush.jpg?raw=true "")
### Toss-up
![Alt text](examples/idk.jpg?raw=true "")
