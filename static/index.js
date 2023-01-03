function no_help() {
    document.getElementById('help').innerHTML = "?";
    document.getElementById('help').style = "display:block; margin-right:47%;margin-left:47%;margin-top: 15px; border: solid black 3px; text-align: center; background-color:#C0C0C0;"
}

function help() {
    passw = document.getElementById('help')
    if (passw.innerHTML == "?") {
        passw.innerHTML = "<b>The password should contain at least one <em>lowercase letter</em>, one <em>number</em>, one <em>uppercase letter</em> and one <em>special character</em>.</b>";
        passw.style = "margin-left: 80px; margin-right: 80px; border:none;display:block;margin-top: 15px;border: solid black 3px; text-align: center; background-color:#C0C0C0;cursor:none";
    } else if (passw.innerHTML != "?"){
        document.getElementById('help').innerHTML = "?";
        document.getElementById('help').style = "display:block; margin-right:47%;margin-left:47%;margin-top: 15px; border: solid black 3px; text-align: center; background-color:#C0C0C0;"

    }
}
function showp() {
    var x = document.getElementById("pass");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }
function showc() {
        var x = document.getElementById("confirm");
        if (x.type === "password") {
          x.type = "text";
        } else {
          x.type = "password";
        }
      }
function exit() {
    document.getElementById('logout').innerHTML ="<strong>X</strong>"
    document.getElementById('logout').onmouseout = function no_exit(){
        document.getElementById('logout').innerHTML ="Log out"
    }
}
const canvas = document.querySelector('canvas');
const c = canvas.getContext('2d');
