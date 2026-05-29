const socket = io();

function send(){
    const input = document.getElementById("msg");
    if(!input.value.trim()) return;

    socket.emit("message",{
        to:selectedUser,
        msg:input.value
    });

    input.value="";
}

socket.on("message",(data)=>{
    const box=document.getElementById("messages");

    const div=document.createElement("div");
    div.className="msg recv";
    div.innerText=data.msg;

    box.appendChild(div);
    box.scrollTop=box.scrollHeight;
});

/* AUTO SCROLL */
setInterval(()=>{
    const box=document.getElementById("messages");
    if(box) box.scrollTop=box.scrollHeight;
},300);
