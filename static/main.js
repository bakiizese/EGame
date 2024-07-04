$(document).ready(() => {
    $("#myModal").css("display", "none");
    $('.gamebtn').on('click', () => {
        $("#myModal").css("display", "block");
        //window.location.href =  `http://127.0.0.1:5000/game?username=${username}&session_id=${session_id}`;
    })
    $(".close").on('click', () => {
        $("#myModal").css("display", "none");
    });
    $('#human').on('click', () => {
        window.location.href =  `http://127.0.0.1:5000/game?username=${username}&session_id=${session_id}`;
    })
    $('#computer').on('click', () => {
        window.location.href =  `http://127.0.0.1:5000/game?computer=1&username=${username}&session_id=${session_id}`;
    })
})