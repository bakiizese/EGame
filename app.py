from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room
from uuid import uuid4
from collections import Counter
from ai import Caller

app = Flask(__name__)
socketio = SocketIO(app)

board = [
    [' ',' ',' '],
    [' ',' ',' '],
    [' ',' ',' ']
    ]

fullsession = []
computer = None
playes = {}
players = {}
pl_names = []
playerss = {
    'X': [],
    'O': []
}
all_moves = {}



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game')
def game():
    global computer

    uid = str(uuid4())
    username = request.args.get('username')
    session_id = request.args.get('session_id')
    computer = request.args.get('computer')

    return render_template('game.html', username=username, session_id=session_id, uid=uid, computer=computer)


count = 0
@socketio.on('join_room')
def handle_join_room(data):
    global count
    global fullsession
    global players
    global computer
    # print(computer)
    username = data['username']
    session_id = data['session_id']
    uid = data['ids']

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
    socketio.emit('joined', {'player': playes}, room=session_id)
    if computer:
        player = {
            'username': 'Computer',
            'session_id': session_id,
            'res': 'O',
            'turn': False,
            'move': [],
            'attr': '',
            #'uid': uid
        }
        players['player' + str(count + 1)] = player
        playes[session_id] = players
        # num_session = {}
        # num_session.setdefault(session_id, []).append(session_id)
        # with open('pl.json', 'a') as file:
        #     json.dump(num_session, file, indent=4)

    if len(playes[session_id]) == 2:
        players = {}
        count = 0
        # fullsession.append(players['player2']['session_id'])
        socketio.emit('start', {'player': playes}, room=session_id)
        

@socketio.on('picked')
def handle_picked(data):
    session_id = data['session_id']
    if computer:
        username = data['player'][session_id]['player1']['username']
        rs = data['player'][session_id]['player1']['res']
        mv = data['mv']
        win1 = CheckWinner('X', data['mv'], session_id)
        board[int(mv[0])][int(mv[1])] = rs
        
        if win1:
            clear()
            socketio.emit('picked_change', {'data': data, 'attr': data['attr'], 'ids': data['ids']}, room=session_id)
            socketio.emit('winner', {'win': win1, 'username': username}, room=session_id)
            return

        cpmove = Caller(board, 'O', rs)
        board[int(cpmove[1][0])][int(cpmove[1][1])] = 'O'
        win2 = CheckWinner('O', cpmove[1], session_id)

        if win2:
            clear()
            socketio.emit('picked_change', {'data': data, 'attr': data['attr'], 'ids': data['ids'], 'cpmove': cpmove[0]}, room=session_id)
            socketio.emit('winner', {'win': win2, 'username': 'Computer'}, room=session_id)
            return
            
        socketio.emit('picked_change', {'data': data, 'attr': data['attr'], 'ids': data['ids'], 'cpmove': cpmove[0]}, room=session_id)
        return
        
    picked = data['player'][session_id]['player1']['turn']
    if picked:
        username = data['player'][session_id]['player1']['username']
        win = CheckWinner(data['player'][session_id]['player1']['res'] , data['mv'], session_id)
        data['player'][session_id]['player1']['turn'] = False
        data['player'][session_id]['player2']['turn'] = True
    else:
        username = data['player'][session_id]['player2']['username']
        win = CheckWinner(data['player'][session_id]['player2']['res'] , data['mv'], session_id)
        data['player'][session_id]['player2']['turn'] = False
        data['player'][session_id]['player1']['turn'] = True
    if win:
        clear()
        socketio.emit('winner', {'win': win, 'username': username}, room=session_id)
    
    socketio.emit('picked_change', {'data': data, 'attr': data['attr'], 'ids': data['ids']}, room=session_id)


def CheckWinner(player, data, session_id):
    global playerss
    global all_moves

    playerss.setdefault(session_id, {}).setdefault(player, []).append(data)
    all_moves.setdefault(session_id, {}).setdefault('allmoves', []).append(data)
    cols = []
    rows = []
    diagR = []
    diagL = []
    print(playerss)
    print(all_moves)
    print(board)
    if len(playerss[session_id][player]) >= 3:
        for i in playerss[session_id][player]:
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
        if most_rows[0][1] >= 3 or most_cols[0][1] >= 3 or len(diagR) >= 3 or len(diagL) >= 3:
            playerss = {}
            all_moves = {}
            return player
        elif len(all_moves[session_id]['allmoves']) >= 9:
            playerss = {}
            all_moves = {}
            return 'draw'

def clear():
    global board, computer, all_moves, playerss
    computer = None
    playerss = {
        'X': [],
        'O': []
    }
    all_moves = {}
    board = [
    [' ',' ',' '],
    [' ',' ',' '],
    [' ',' ',' ']
    ]
    




if __name__ == '__main__':
    socketio.run(app, debug=1)