// Functions

function submit(){
    document.getElementById("submit__hidden").click()
}

function f(){
    let scroll_to_bottom = document.getElementById('message__area');
    scroll_to_bottom.scroll({ top: scroll_to_bottom.scrollHeight})
}

function send_message(){
    const message = $("#msg").val()
    socket.send(message)
}

// Socket

socket.on("connect", (Socket)=>{
    socket.send("CONNECTED!")
})

socket.on("message", (data)=>{

    let div = document.getElementById("start__chat")
    if(div){
        div.style.display = "none"
    }

    $("#message__area").append(`<span class="message" title="{{ msg.date_created }}" ><h1 class="text-1">${data.user}</h1><p class="message__text">${data.msg}</p></span>`)
    f()
})

socket.on("typing", (is_typing) => {
    if(is_typing){
        $("#is__typing").text("Somebody is typing...")
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


// HTML

$("#message__form").on("submit", (event)=>{

    event.preventDefault()
    
    send_message()
    
    $("#message__form")[0].reset()
})


$(document).ready(()=>{
    f()
})
