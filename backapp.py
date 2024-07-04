#!/usr/bin/python
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room
from uuid import uuid4
from collections import Counter

app = Flask(__name__)
socketio = SocketIO(app)

fullsession = []
playes = {}
players = {}
pl_names = []
playerss = {
    'X': [],
    'O': []
}
allmoves = []



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game')
def game():
    
    uid = str(uuid4())
    username = request.args.get('username')
    session_id = request.args.get('session_id')

    return render_template('game.html', username=username, session_id=session_id, uid=uid)


count = 0
@socketio.on('join_room')
def handle_join_room(data):
    global count
    global fullsession
    
    
    username = data['username']
    session_id = data['session_id']
    uid = data['ids']

    # if username in pl_names:

            
    # pl_names.append(username)

    # if session_id in fullsession:
    #      socketio.emit('session_full', {'session_id': session_id}, room=request.sid)
    #      return
   
    # res = 'X'
    # turn = True
    # if len(players) > 0:
    #     turn = False
    #     res = 'O'
    if len(players) % 2 == 0:
        turn = True
        res = 'X'
    else:
        turn = False
        res = 'O'
    count += 1
    player = {
        'username': username,
        'session_id': session_id,
        'res': res,
        'turn': turn,
        'move': [],
        'attr': '',
        'uid': uid
    }

    join_room(session_id)
    

    players['player' + str(count)] = player
    
    playes[session_id] = players

    socketio.emit('joined_single', {'player': player}, room=request.sid)
    socketio.emit('joined', {'player': players}, room=session_id)
    if len(players) == 2:
        
        fullsession.append(players['player2']['session_id'])
        socketio.emit('start', {'player': players}, room=session_id)

@socketio.on('picked')
def handle_picked(data):
    picked = data['player']['player1']['turn']
    if picked:
        win = CheckWinner(data['player']['player1']['res'] , data['mv'])
        data['player']['player1']['turn'] = False
        data['player']['player2']['turn'] = True
    else:
        win = CheckWinner(data['player']['player2']['res'] , data['mv'])
        data['player']['player2']['turn'] = False
        data['player']['player1']['turn'] = True
    if win:
        socketio.emit('winner', {'win': win}, room=data['player']['player1']['session_id'])
    
    socketio.emit('picked_change', {'data': data, 'attr': data['attr'], 'ids': data['ids']}, room=data['player']['player1']['session_id'])


def CheckWinner(player, data):
    playerss[player].append(data)
    allmoves.append(data)
    cols = []
    rows = []
    diagR = []
    diagL = []
    if len(playerss[player]) >= 3:
        for i in playerss[player]:
            cols.append(i[1])
            rows.append(i[0])
            if int(i[0]) - int(i[1]) == 0:
                diagR.append(int(i[0]) - int(i[1]))
            if int(i[0]) + int(i[1]) == 2:
                diagL.append(int(i[0]) + int(i[1]))
        counter1 = Counter(cols)
        counter2 = Counter(rows)

        most_cols = counter1.most_common(1)
        most_rows = counter2.most_common(1)
        if most_rows[0][1] >= 3 or most_cols[0][1] >= 3 or len(diagR) >= 3:
            return player
        elif len(allmoves) >= 9:
            return 'draw'





if __name__ == '__main__':
    socketio.run(app, debug=1)