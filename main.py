import re
import tkinter as tk
import matplotlib
import requests
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
import urllib.request
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def get_prediction():

    # get players
    player_one = entry1.get()
    player_two = entry2.get()
    one = player_one.split()
    two = player_two.split()

    one_code = two_code = age1 = rank1 = points1 = age2 = rank2 = points2 = 0

    # scrape info for 2 players from rankings
    html_text = requests.get('https://www.atptour.com/en/rankings/singles?rankRange=1-5000').text
    soup = BeautifulSoup(html_text, 'lxml')
    players = soup.find_all('tr', class_='')
    for player in players:
        rank = player.find('td', class_='rank-cell border-left-4 border-right-dash-1').text.strip()
        points = player.find('td', class_='points-cell border-right-dash-1').text.replace(',', '').strip()
        age = player.find('td', class_='age-cell border-left-dash-1 border-right-4').text.strip()
        name = re.sub(r"(\w)([A-Z])", r"\1 \2", player.find('span', class_='player-cell-wrapper').text.strip())
        profile = player.find('span', class_='player-cell-wrapper').a['href'].split('/')
        if player_one in name:
            one_code = profile[4]
            age1, rank1, points1 = age, rank, points
        if player_two in name:
            two_code = profile[4]
            age2, rank2, points2 = age, rank, points
        if one_code != 0 and two_code != 0:
            break

    # scrape info from head 2 head
    url = "https://www.atptour.com/en/players/atp-head-2-head/" + \
          one[0] + "-" + one[1] + "-vs-" + two[0] + "-" + two[1] + "/" + one_code + "/" + two_code
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

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

    # calculate each player's score for this match-up
    win_value1 = int(points1) + (int(wins1))*8000 + (int(ytd_titles1))*70 + (int(career_titles1))*50 + int(wl1[0]) + \
        (int(ytd_wl1[0]))*1000 - (int(age1))*10 - (int(rank1)*50)
    win_value2 = int(points2) + (int(wins2))*8000 + (int(ytd_titles2))*70 + (int(career_titles2))*50 + int(wl2[0]) + \
        (int(ytd_wl2[0]))*1000 - (int(age2))*10 - (int(rank2)*50)
    total = win_value1 + win_value2
    win_pct = win_value1 / total

    # print my prediction
    if win_pct < .50:
        prediction.config(text='Malchu predicts ' + player_two + ' will win with a ' +
                               str(int(round(float((1 - win_pct) * 100), 0))) + '% ' + 'chance!', bg='white')
        if 48 > int(round(float(win_pct * 100), 0)) > 40:
            prediction.config(text='Malchu thinks it\'s gonna be close! Slight edge to ' + player_two + "!", bg='white')
        if 20 >= int(round(float(win_pct * 100), 0)) >= 0:
            prediction.config(text='Malchu would bet on this one. ' + player_two + " winning this without a doubt.",
                              bg='white')
    else:
        prediction.config(text='Malchu predicts ' + player_one + ' will win with a ' +
                               str(int(round(float(win_pct * 100), 0))) + '% ' + 'chance!', bg='white')
        if 60 > int(round(float(win_pct * 100), 0)) > 52:
            prediction.config(text='Malchu thinks it\'s gonna be close! Slight edge to ' + player_one + "!", bg='white')
        if 100 >= int(round(float(win_pct * 100), 0)) >= 80:
            prediction.config(text='Malchu would bet on this one. ' + player_one + " winning this without a doubt.",
                              bg='white')
    if 53 > int(round(float(win_pct * 100), 0)) > 47:
        prediction.config(text='Malchu thinks it\'s a toss up! Anybody\'s game!', bg='white')

    # scrape player's profile images
    global img1
    global img2
    img1 = "https://www.atptour.com" + soup.find('div', class_='player-left-image').find('img')['src']
    img2 = "https://www.atptour.com" + soup.find('div', class_='player-right-image').find('img')['src']
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(img1, "left.png")
    urllib.request.urlretrieve(img2, "right.png")

    # add images
    canvas1.delete("left")
    img1 = Image.open("left.png").convert('RGBA')
    img1 = img1.resize((150, 150))
    img1 = ImageTk.PhotoImage(img1)
    canvas1.create_image(140, 150, image=img1, tags="left")
    canvas1.delete("right")
    img2 = Image.open("right.png").convert('RGBA')
    img2 = img2.resize((150, 150))
    img2 = ImageTk.PhotoImage(img2)
    canvas1.create_image(560, 150, image=img2, tags="right")
    canvas1.create_window(350, 330, window=prediction)

    # create predictor graph
    fig = matplotlib.figure.Figure(figsize=(2, 2))
    ax = fig.add_subplot(111)
    ax.pie([win_value1, win_value2], colors=['cyan', 'magenta'], shadow=True, startangle=90)
    circle = matplotlib.patches.Circle((0, 0), 0.7, color='white')
    ax.add_artist(circle)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas = canvas.get_tk_widget()
    canvas.place(x=250, y=50)
    vs2 = tk.Label(root, text='VS', bg='white')
    vs2.config(font=('helvetica', 25))
    canvas.create_window(100, 100, window=vs2)

    # create predictor values
    reset = tk.Label(root, text='100')
    reset.config(font=('helvetica', 25), bg='white', fg='white')
    reset2 = tk.Label(root, text='100')
    reset2.config(font=('helvetica', 25), bg='white', fg='white')
    canvas1.create_window(250, 150, window=reset)
    canvas1.create_window(450, 150, window=reset2)
    pct1 = tk.Label(root, text=str(int(round(float(win_pct*100), 0))))
    pct1.config(font=('helvetica', 25), bg='white')
    pct2 = tk.Label(root, text=str(int(round(float((1-win_pct)*100), 0))))
    pct2.config(font=('helvetica', 25), bg='white')
    canvas1.create_window(250, 150, window=pct1)
    canvas1.create_window(450, 150, window=pct2)


# create window
root = tk.Tk()
root.resizable(False, False)
root.title('Tennis Match Predictor')

# create canvas
canvas1 = tk.Canvas(root, width=700, height=360, relief='raised', bg='white')
canvas1.pack()

# create labels
title = tk.Label(root, text='Tennis Match Predictor')
title.config(font=('helvetica', 20), bg='white')
canvas1.create_window(350, 40, window=title)

p1 = tk.Label(root, text='Player One:')
p1.config(font=('helvetica', 10), bg='white')
canvas1.create_window(140, 250, window=p1)

p2 = tk.Label(root, text='Player Two:')
p2.config(font=('helvetica', 10), bg='white')
canvas1.create_window(560, 250, window=p2)

vs = tk.Label(root, text='VS')
vs.config(font=('helvetica', 25), bg='white')
canvas1.create_window(350, 150, window=vs)

prediction = tk.Label(root, text='', font=('helvetica', 12))

# add default images
img = Image.open("default.png").convert('RGBA')
img = img.resize((150, 150))
img = ImageTk.PhotoImage(img)

tk.Label(root, image=img)
tk.Label(root, image=img)
canvas1.create_image(140, 150, image=img, tags="left")
canvas1.create_image(560, 150, image=img, tags="right")

# create entry boxes
entry1 = tk.Entry(root)
canvas1.create_window(140, 280, window=entry1)
entry2 = tk.Entry(root)
canvas1.create_window(560, 280, window=entry2)

# create button
button1 = tk.Button(text='Predict!', command=get_prediction, bg='black', fg='white',
                    font=('helvetica', 16, 'bold'))
canvas1.create_window(350, 270, window=button1)

# run
root.mainloop()
