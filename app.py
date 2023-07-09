from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort

import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zchoumalx'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log')
def log():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('log.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('result.html', post=post, p1=post['player1'], p2=post['player2'], c=post['chance'], w=post['winner'])

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        p1 = request.form['player1']
        p2 = request.form['player2']

        if not p1 or not p2:
            flash('Both players are required!')
        else:
            # calculate prediction
            (c, w) = predict(p1, p2)

            # add data to database
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (player1, player2, chance, winner) VALUES (?, ?, ?, ?)',
                         (p1, p2, c, w))
            conn.commit()
            conn.close()
            return render_template('result.html', p1=p1, p2=p2, c=str(c), w=w)

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        p1 = request.form['player1']
        p2 = request.form['player2']

        if not p1 or not p2:
            flash('Both players are required!')
        else:
            # recalculate prediction
            (c, w) = predict(p1, p2)
            
            conn = get_db_connection()
            conn.execute('UPDATE posts SET player1 = ?, player2 = ?, chance = ?, winner = ?'
                         ' WHERE id = ?',
                         (p1, p2, c, w, id))
            conn.commit()
            conn.close()
            return redirect("url_for('log')")

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{} vs. {}" was successfully deleted!'.format(post['player1'], post['player2']))
    return redirect(url_for('log'))

@app.route('/about')
def about():
    return render_template('about.html')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def getStats(p1, p2):
    one = p1.split()
    two = p2.split()
    one_code = two_code = age1 = rank1 = points1 = age2 = rank2 = points2 = 0

    # scrape info for 2 players from rankings
    html_text = requests.get('https://www.atptour.com/en/rankings/singles?rankRange=1-5000').text
    soup = BeautifulSoup(html_text, 'html.parser')
    players = soup.find_all('tr', class_='')
    for player in players:
        rank = player.find('td', class_='rank-cell border-left-4 border-right-dash-1').text.strip()
        points = player.find('td', class_='points-cell border-right-dash-1').text.replace(',', '').strip()
        age = player.find('td', class_='age-cell border-left-dash-1 border-right-4').text.strip()
        name = re.sub(r"(\w)([A-Z])", r"\1 \2", player.find('span', class_='player-cell-wrapper').text.strip())
        profile = player.find('span', class_='player-cell-wrapper').a['href'].split('/')
        if p1 in name:
            one_code = profile[4]
            age1, rank1, points1 = age, rank, points
        if p2 in name:
            two_code = profile[4]
            age2, rank2, points2 = age, rank, points
        if one_code != 0 and two_code != 0:
            break

    # scrape info from head 2 head
    url = "https://www.atptour.com/en/players/atp-head-2-head/" + \
          one[0] + "-" + one[1] + "-vs-" + two[0] + "-" + two[1] + "/" + str(one_code) + "/" + str(two_code)
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    h2h = soup.find('table', class_='h2h-table h2h-table-ytd').text.split()
    # events = soup.find('table', class_="modal-event-breakdown-table").text.split()

    # get profile and h2h stats
    wins1 = soup.find('div', class_='player-left-wins').find('div', class_="players-head-rank").text.strip()
    wins2 = soup.find('div', class_='player-right-wins').find('div', class_="players-head-rank").text.strip()
    i = h2h.index("YTD")
    ytd_wl1, ytd_wl2 = h2h[i-1].split('/'), h2h[i+2].split('/')
    ytd_titles1, ytd_titles2 = h2h[i+3], h2h[i+6]
    wl1, wl2 = h2h[i+7].split('/'), h2h[i+10].split('/')
    career_titles1, career_titles2 = h2h[i+11], h2h[i+14]

    return url

def predict(p1, p2):
    c, w = 0, "Novak Djokovic"
    one = p1.split()
    two = p2.split()
    one_code = two_code = age1 = rank1 = points1 = age2 = rank2 = points2 = 0

    # scrape info for 2 players from rankings
    html_text = requests.get('https://www.atptour.com/en/rankings/singles?rankRange=1-5000').text
    soup = BeautifulSoup(html_text, 'html.parser')
    players = soup.find_all('tr', class_='')
    for player in players:
        rank = player.find('td', class_='rank-cell border-left-4 border-right-dash-1').text.strip()
        points = player.find('td', class_='points-cell border-right-dash-1').text.replace(',', '').strip()
        age = player.find('td', class_='age-cell border-left-dash-1 border-right-4').text.strip()
        name = re.sub(r"(\w)([A-Z])", r"\1 \2", player.find('span', class_='player-cell-wrapper').text.strip())
        profile = player.find('span', class_='player-cell-wrapper').a['href'].split('/')
        if p1 in name:
            one_code = profile[4]
            age1, rank1, points1 = age, rank, points
        if p2 in name:
            two_code = profile[4]
            age2, rank2, points2 = age, rank, points
        if one_code != 0 and two_code != 0:
            break

    # scrape info from head 2 head
    url = "https://www.atptour.com/en/players/atp-head-2-head/" + \
          one[0] + "-" + one[1] + "-vs-" + two[0] + "-" + two[1] + "/" + str(one_code) + "/" + str(two_code)
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    h2h = soup.find('table', class_='h2h-table h2h-table-ytd').text.split()
    events = soup.find('table', class_="modal-event-breakdown-table").text.split()

    # get profile and h2h stats
    player = [p1, p2]
    wins1 = soup.find('div', class_='player-left-wins').find('div', class_="players-head-rank").text.strip()
    wins2 = soup.find('div', class_='player-right-wins').find('div', class_="players-head-rank").text.strip()
    wins = [wins1, wins2]
    i = h2h.index("YTD")
    ytd_wl1, ytd_wl2 = h2h[i-1].split('/'), h2h[i+2].split('/')
    ytd_wl = [ytd_wl1, ytd_wl2]
    ytd_titles1, ytd_titles2 = h2h[i+3], h2h[i+6]
    ytd_titles = [ytd_titles1, ytd_titles2]
    wl1, wl2 = h2h[i+7].split('/'), h2h[i+10].split('/')
    wl = [wl1, wl2]
    career_titles1, career_titles2 = h2h[i+11], h2h[i+14]
    career_titles = [career_titles1, career_titles2]

    # convert data to csv
    dict = {'Player': player, 'Wins': wins, 'YTD Win/Loss': ytd_wl, 'YTD Titles': ytd_titles, 'Career Win/Loss': wl, 'Career Titles': career_titles}

    # calculate each player's score for this match-up
    win_value1 = int(points1) + (int(wins1))*8000 + (int(ytd_titles1))*70 + (int(career_titles1))*50 + int(wl1[0]) + \
        (int(ytd_wl1[0]))*1000 - (int(age1))*10 - (int(rank1)*50)
    win_value2 = int(points2) + (int(wins2))*8000 + (int(ytd_titles2))*70 + (int(career_titles2))*50 + int(wl2[0]) + \
        (int(ytd_wl2[0]))*1000 - (int(age2))*10 - (int(rank2)*50)
    
    total = win_value1 + win_value2
    win_pct = win_value1 / total

    # calculate prediction value
    if win_pct < .50:
        c = int(round(float((1 - win_pct) * 100), 0))
        w = p2
    else:
        c = int(round(float(win_pct * 100), 0))
        w = p1

    return (c, w)