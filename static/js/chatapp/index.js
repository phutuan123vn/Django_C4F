$(document).ready(function () {
  $(".roomItem").hover(
    function () {
      $(this).css("box-shadow", "0 0.5rem 0.2rem rgba(0, 0, 0, 0.3)");
    },
    function () {
      $(this).css("box-shadow", "");
    }
  );
});
function initWebSocket(id) {
  const chatSocket = new WebSocket(
    "ws://" + window.location.host + "/ws/chat/" + id + "/"
  );
  chatSocket.onopen = function (e) {
    console.log("Chat socket opened");
  };
  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);
    const messageDiv = `
                        <div class="row card p-4 m-4">
                            <div class="card-header">
                                <h3>${data.user}</h3>
                            </div>
                            <div class="card-body">
                                <p>${data.message}</p>
                            </div>
                            <div class="card-footer"><span>${data.date}</span></div>
                        </div>
                        `;
    $("div.container.messages").append(messageDiv);
    var container = document.getElementById("scroll-container");
    container.scrollTop = container.scrollHeight - container.clientHeight;
  };
  chatSocket.onclose = function (e) {
    console.error("Chat socket closed unexpectedly");
  };
  return {
    close: function () {
      chatSocket.close();
    },
    send: function (data) {
      chatSocket.send(
        JSON.stringify({
          message: data,
        })
      );
    }
  };
}
let instanceWS = null;
if ($(".roomName")) {
  instanceWS = initWebSocket($(".roomName").attr("roomID"));
}
function reloadMsg(id) {
  const id_form = $("form#formMessage").attr("roomID");
  if (id_form == id) return;
  $("form#formMessage").attr("roomID", id);
  console.log("Reloading messages Room ID: ", id);
  if (instanceWS) {
    instanceWS.close();
  }
  instanceWS = initWebSocket(id);
  $.ajax({
    url: `get-msg/`,
    type: "GET",
    data: {
      room_id: id,
    },
    success: function (response) {
      console.log(response);
      if (response.status === "success") {
        $("div.container.messages").html("");
        response.messages.forEach((message) => {
          username = message.user__username;
          const messageDiv = `
                        <div class="row card p-4 m-4">
                            <div class="card-header">
                                <h3>${username}</h3>
                            </div>
                            <div class="card-body">
                                <p>${message.value}</p>
                            </div>
                            <div class="card-footer"><span>${message.date}</span></div>
                        </div>
                        `;
          $("div.container.messages").append(messageDiv);
        });
        var container = document.getElementById("scroll-container");
        container.scrollTop = container.scrollHeight - container.clientHeight;
      }
    },
    error: function (error) {
      console.log(error);
    },
  });
  // $("form#formMessage").attr("action", `/chat/sendmsg/${id}/`);
}

$(".btnSendMsg").click(function () {
  const value = $("#message").val();
  if (!value) return;
  if (!instanceWS) return;
  instanceWS.send(value);
  $("#message").val("");
})



// $('form#formMessage').on('submit', function(e) {
//     e.preventDefault();
//     const form = $(this);
//     const roomID = form.attr('roomID')
//     message = $("#message").val();
//     console.log(form.serialize());
//     if (message) {
//         $.ajax({
//             url: form.attr("action"),
//             type: "POST",
//             data: form.serialize(),
//             success: function (response) {
//             if (response.status === "success") {
//                 form.find("input#message").val("");
//                 const message = response.message;
//                 username = message.username;
//                 const messageDiv = `
//                         <div class="card my-2 row">
//                             <div class="card-header">
//                                 <h5>${username}</h5>
//                             </div>
//                             <div class="card-body">
//                                 <p>${message.value}</p>
//                             </div>
//                             <div class="card-footer"><span>${message.date}</span></div>
//                         </div>
//                         `;
//                 $("div.container.messages").append(messageDiv);
//                 var container = document.getElementById("scroll-container");
//                 container.scrollTop = container.scrollHeight - container.clientHeight;
//             }
//             },
//             error: function (error) {
//             console.log(error);
//             },
//         });
//     }
// })
