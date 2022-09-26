
function submit(){
    document.getElementById("submit__hidden").click()
}

function openNav() {

    document.getElementById("mySidebar").style.width = "70vw"; 
    document.getElementById("mySidebar").style.paddingLeft = "1vw"; 
    document.getElementById("mySidebar").style.paddingRight = "1vw"; 

}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("mySidebar").style.paddingLeft = "0"; 
    document.getElementById("mySidebar").style.paddingRight = "0"; 
}

function f(){
    let scroll_to_bottom = document.getElementById('message__area');
    scroll_to_bottom.scroll({ top: scroll_to_bottom.scrollHeight})
}

function send_message(){
    const message = $("#msg").val()
    socket.send(message)
}


socket.on("connect", (Socket)=>{
    socket.send("CONNECTED!")
})

socket.on("user_action", (online_users) => {
    if(online_users === 1){
        $("#online__users").text(`${online_users} user online`)
    }
    else{
        $("#online__users").text(`${online_users} users online`)
    }
})

socket.on("message", (data)=>{

    let div = document.getElementById("start__chat")
    if(div){
        div.style.display = "none"
    }

    $("#message__area").append(`<span class="message" title="${data.date}" ><h1 class="text">${data.user}</h1><p class="message__text">${data.msg}</p></span>`)
    f()
})

socket.on("typing", (typer) => {
    const is_typing = typer.is_typing
    const user = typer.user
    if(is_typing){
        $("#is__typing").text(`${user} is typing...`)
    }
    else{
        $("#is__typing").text("")
    }
})

document.getElementById("msg").addEventListener("input", ()=>{
    const message = $("#msg").val()

    if(!(message && message.length > 0 && message.trim().length > 0)){
        socket.emit("typing__signal", false)
        return;
    }
    
    $('#msg').keypress((e)=>{
    
        if(e.which!=13){
            socket.emit("typing__signal", true)
        }
    
        else{
            socket.emit("typing__signal", false)
        }
    
    })
})


$("#message__form").on("submit", (event)=>{

    event.preventDefault()
    
    send_message()
    
    $("#message__form")[0].reset()
})


$(document).ready(()=>{
    f()
})

$('.message__text a').each(function(){
    $(this).attr('target', '_BLANK');
});