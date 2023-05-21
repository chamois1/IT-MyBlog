// modal window for edit post
var openModalBtn = document.getElementById("editPost");
var modal = document.getElementById("modalEdit");
var closeBtn = document.getElementsByClassName("close")[0];

openModalBtn.onclick = function() {
  modal.style.display = "block";
};

closeBtn.onclick = function() {
  modal.style.display = "none";
};


window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};


// show field reply
function replyBtn(authorId) {
    var replyContainer = document.getElementById("reply-container-" + authorId);
    if (replyContainer.style.display === "none") {
        replyContainer.style.display = "block";
    } else {
        replyContainer.style.display = "none";
    }
}        
    

// show block replys
function ShowReplys(id_main_comment) {
    var replysBlock = document.getElementById("block-replys-" + id_main_comment);
    if (replysBlock.style.display === "none") {
        replysBlock.style.display = "block";
    } else {
        replysBlock.style.display = "none";
    }
}      


// window edit comment
function showWindowEdiоt(userId) {
    var window = document.getElementById("WindowEdit");
    var text_edit = document.getElementById("text_edit");
    text_edit.value = userId;
    window.style.display = "block";
}

function hideWindowEdit() {
    var window = document.getElementById("WindowEdit");
    window.style.display = "none";
}


function showWindowEditReply(userId) {
    var window = document.getElementById("WindowEdit");
    var text_edit = document.getElementById("text_edit");
    text_edit.value = userId;
    window.style.display = "block";
}

function hideWindowEdit() {
    var window = document.getElementById("WindowEdit");
    window.style.display = "none";
}      