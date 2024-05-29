const roomName = JSON.parse(document.getElementById('room-name').textContent)
const user = JSON.parse(document.getElementById("user").textContent)
const first_user = JSON.parse(document.getElementById("first_user").textContent)
const second_user_status = JSON.parse(document.getElementById("second_user_status").textContent)
const first_user_status = JSON.parse(document.getElementById("first_user_status").textContent)
const second_user = JSON.parse(document.getElementById("second_user").textContent)
// var user_status = JSON.parse(document.getElementById("user_status").textContent)
const conversation = document.getElementById("conversation")
const chatSocket = new WebSocket('ws://'+ window.location.host+ '/ws/chat/'+ roomName+ '/');
const statusSocket = new WebSocket('ws://'+ window.location.host+ '/ws/status/');
const inputField = document.getElementById("comment")
const sendButton  = document.getElementById("send")
const online_text = document.querySelector(".heading-online")

document.getElementById("hiddeninput").addEventListener('change', handleFileSelect, false)

var isRecord = false
var mic = false

function handleFileSelect() {
  var file = document.getElementById('hiddeninput').files[0]
  getBase64(file, file.type)

}

function getBase64(file, file_type) {
  var type = file_type.split("/")[0]
  var reader = new FileReader()
  reader.readAsDataURL(file)

  reader.onload=function() {
    chatSocket.send(JSON.stringify({
      "type_of": type,
      "message":reader.result
    }))
  }
}
const startStop = document.getElementById("record")

startStop.onclick=()=>{

  if (isRecord) {
    stopRecord()
    startStop.style=""
    isRecord=false
  } else {
    startRecord()
    startStop.style="color:red"
    isRecord=true
  }


}

function startRecord() {
  navigator.mediaDevices.getUserMedia({audio:true})
  .then(stream=>{
    mediaRecorder = new MediaRecorder(stream)
    mediaRecorder.start()
    dataArray = []
    mediaRecorder.ondataavailable=function(e) {
      dataArray.push(e.data)
    }
    mediaRecorder.onstop=function(e) {
      audioData = new Blob(dataArray, {'type':"audio/mp3"})
      dataArray.lenght = 0
      getBase64(audioData,audioData.type)

      stream.getTracks().forEach(function(track){
        if(track.readyState==="live" && track.kind === "audio"){
          track.stop()
        }
      })
    }
  })
}
function stopRecord() {
  mediaRecorder.stop()

}

// navigator.mediaDevices.getUserMedia({audio:true})
//   .then(function (mediaStreamObject) {
//     const startStop = document.getElementById("record")
//     const mediaRecorder = new MediaRecorder(mediaStreamObject)

//     startStop.addEventListener("click", function (e) {
//       if (isRecord) {
//         startStop.style = ""
//         isRecord = false
//         mediaRecorder.stop()
//       } else {
//         startStop.style = "color:red"
//         isRecord = true
//         mediaRecorder.start()
//       }
//     })
//     mediaRecorder.ondataavailable=function(e) {
//       dataArray.push(e.data)
//     }
//     var dataArray = []

//     mediaRecorder.onstop=function (e) {
//       let audioData = new Blob(dataArray, {'type': 'audio/mp3'})
//       dataArray.length = 0
//       console.log(audioData)
//       getBase64(audioData,audioData.type)
//     }

//   })




window.onload = function() {
  console.log(user)
  console.log(first_user,first_user_status)
  console.log(second_user,second_user_status)
  conversation.scrollTop = conversation.scrollHeight
  if (user === first_user && second_user_status === true) {
    online_text.style.display = 'block'
  } else {
    if (user === second_user && first_user_status === true) {
      online_text.style.display = 'block'   
    }
  }
}


statusSocket.onmessage = function(e) {
  const data = JSON.parse(e.data)
  console.log(data.user, "data")
  if (data.user === first_user || data.user === second_user) {
    console.log(user,first_user)
    if (user === first_user) {
      console.log(second_user, data.user, data.online_status)
      if (second_user === data.user && data.online_status == true) {
        online_text.style.display = 'block'
      } else {
        online_text.style.display = 'none'
      }
    } else {
      if (first_user === data.user && data.online_status == true) {
        online_text.style.display = 'block'
      } else {
        online_text.style.display = 'none'
      }
    }
  }
}





chatSocket.onopen = function(event) {
  
};


chatSocket.onmessage = function(e) {


    const data = JSON.parse(e.data)
    console.log(data.user)
    console.log(data.message)
    const message_type = data.type_of
    if (message_type === "text") {
      var message = data.message
    } else if(message_type === "image"){
      var message = `<img src="${data.message}" class="image_message">`
    }else if (message_type === "audio"){
      var message = `<audio style="width: 250px;" controls>
      <source src="${data.message}">
    </audio>`
    }else if (message_type === "video"){
      var message = `<video width="250" height="400" controls>
      <source src="${data.message}">
    </video>`
    }



    if (data.message !== "undefined") {
    if (user === data.user) {

      
        
  
      var message = `<div class="row message-body">
    <div class="col-sm-12 message-main-sender">
      <div class="sender">
        <div class="message-text">
          ${message}
        </div>
        <span class="message-time pull-right">
          ${data.created_date}
        </span>
      </div>
    </div>
  </div>`
    }else {
      var message = `<div class="row message-body">
    <div class="col-sm-12 message-main-receiver">
      <div class="receiver">
        <div class="message-text">
        ${message}
        </div>
        <span class="message-time pull-right">
        ${data.created_date}
        </span>
      </div>
    </div>
  </div>`
    }
  
  
    
    conversation.innerHTML += message
    conversation.scrollTop = conversation.scrollHeight
  }



}
chatSocket.onclose = function(e) {
    console.error("Socket closed unexpectedly")
}
inputField.focus()
inputField.onkeyup = function(e) {
    if (e.keyCode === 13) {
        if (inputField.value !== '') {
            sendButton.click()
            inputField.value = ''
        }
        
        
    }
}
sendButton.onclick= function(e) {
    const message = inputField.value
    chatSocket.send(JSON.stringify({
        "type_of": "text",
        "message": message
    }))
    
}