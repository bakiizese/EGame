$(document).ready(() => {

    const socket = io.connect('http://127.0.0.1:5000')
    const name = username
    let dataPlayer = {}
    let gamewon = false

    // alert(computer)
    socket.on('connect', () => {
        socket.emit('join_room', {
            username: username,
            session_id: session_id,
            ids: ids
            })
    })

    socket.on('joined', (data) => {
        dataPlayer = data;
        $('#info #you').text(`You: ${name}`)

    })
    socket.on('joined_single', (data) => {
        //console.log(data['player']['res'])
        // console.log(data)
        const youare = data['player']['res']
        if (youare === 'O'){ 
            $(`.${ids}`).addClass('disabled')
        }
        $('#youare').text(`You Play As ${youare}`)
    })
    socket.on('start', (data) => {
        // console.log(data)
        const oppName = data.player[session_id]['player1']['username']
        let opp = ''
        if (oppName === username){
            opp = data.player[session_id]['player2']['username']
        }else{
            opp = oppName
        }
        
        $('#info #opp').text(`Opp: ${opp}`)
        exchange(data)
    })

    $('.btn').on('click', function () {
        const attrs = $(this).attr('id')
        const mv = $(this).attr('index')
        // console.log(mv)
        // const ids = ids
        // $('.btn').addClass('disabled')
        // console.log(dataPlayer)

        socket.emit('picked', {
            player: dataPlayer['player'],
            attr: attrs,
            ids: ids,
            mv: mv,
            session_id: session_id
        })
        // exchange(dataPlayer)
        
        
        // $(`#${attrs}`).prop('disabled', true)
    })
    
    socket.on('picked_change', (data) => {
        const attrs = data['attr']
        const cpmove = data['cpmove']
        if (computer){
            // alert(attrs)
            $(`#${attrs}`).text('X')
            $('.btn').addClass('disabled')
            if (cpmove){
                setTimeout(() => {
                $(`#${cpmove}`).text('O')
                $('.btn').removeClass('disabled')
                }, 1000)
            }
            
        }else{
        exchange(data['data'])
       

        $(`#${attrs}`).prop('disabled', true)

        dataPlayer = data['data']
        changeTurn(data['data'])
        }
    })
    
    socket.on('session_full', (data) => {
        alert('this session is full')
    })

    var modal = $("#myModal");

    // modal.css("display", "block");
    // $("#myModal p").text('Its a Draw')
    
    var span = $(".close");
    socket.on('winner', (data) => {
        
        modal.css("display", "block");
        if (data['win'] === 'draw') {
            $("#myModal p").text('Its a Draw')
        }else if (name === data['username']){
            $("#myModal p").text('You Won')
        }else{
            $("#myModal p").text('You Lost')
        }
        gamewon = true
        $('.btn').addClass('disabled')
        $('.fixed-button').addClass('disabled')
    })

    $('.fixed-button').on('click', function() {
        modal.css("display", "block");
        $("#myModal p").text('Playing')
        $(this).addClass('disabled')
    })

    span.click(function() {
        modal.css("display", "none");
        $('.fixed-button').removeClass('disabled')
    });

    $(window).click(function(event) {
        if (event.target == modal[0]) {
            modal.css("display", "block");
        }
    });

    $('#playagain').on('click', () => {
        if (computer){
            window.location.href =  `http://127.0.0.1:5000/game?computer=1&username=${username}&session_id=${session_id}`;
        }else{
            window.location.href =  `http://127.0.0.1:5000/game?username=${username}&session_id=${session_id}`;
        }
    })
    $('#goback').on('click', () => {
        window.history.back()
    })

    function changeTurn(data){
        // console.log(data)
        let ids = data['ids']
        let dt = data['player'][session_id]['player1']['uid']
        let dt2 = data['player'][session_id]['player2']['uid']

        dt = '.' + dt
        dt2 = '.' + dt2
        ids = '.' + ids
        //$(`${ids}`).addClass('disabled')
        if (gamewon){
        }else if(ids === dt){
            //alert('in')
            $(`${dt2}`).removeClass('disabled')
            $(`${dt}`).addClass('disabled')
        }
        else{
            //alert('out')
            $(`${dt}`).removeClass('disabled')
            $(`${dt2}`).addClass('disabled')
        }
    }

    function exchange(data) {
        // console.log(data)
        const turn = data['player'][session_id]['player1']
        const attrs = data['attr']
        if (turn['turn']){
            // console.log(turn['turn'])
            $('#turns').text(`it is ${turn['res']}'s turn`)
            $(`#${attrs}`).text('O')
            
            // $('.btn').addClass('disabled')
        }else{
            const t = data['player'][session_id]['player2']['res']
            $('#turns').text(`it is ${t}'s turn`)
            $(`#${attrs}`).text('X')
        }
    }
})