$(document).ready(() => {
    $('.game').on('click', (event) => {
        event.preventDefault();
        let username = $('#play #username').val()
        let session_id = $('#play #session_id').val()

        if (username && session_id){
            window.location.href =  `/game?username=${username}&session_id=${session_id}`;
        }
    })

})