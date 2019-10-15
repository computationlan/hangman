function updateGameState(response) {
  var jsonResponse = JSON.parse(response);
  console.log(jsonResponse);
  refreshTree(jsonResponse["wrong_guesses_left"]);
  document.getElementById("challenge").innerHTML = jsonResponse["guessed"].join(" ");
  drawAlphabet(jsonResponse["wrong_guesses"], jsonResponse["guessed"], jsonResponse["game_over"]);
  document.getElementById("game_over").innerHTML = jsonResponse["game_over_message"];
  if (jsonResponse["game_over"]) {
    document.getElementById("challenge").innerHTML = jsonResponse["challenge"];
    getLeaderboard();
  }
}

function refreshTree(wrong_guesses_left) {
  var img = document.getElementById("tree");
  img.src = "/static/tree-image-" + (6 - wrong_guesses_left).toString() + ".png";
}

function drawAlphabet(wrong_guesses, guessed, game_over) {
  var alphabet = document.getElementById("alphabet");
  alphabet.innerHTML = "";
  for (letter of "ABCDEFGHIJKLMNOPQRSTUVWXYZ") {
    var element = document.createElement("input");
    element.setAttribute("type", "button");
    element.setAttribute("value", letter);
    element.setAttribute("name", letter);
    element.disabled = game_over;
    if (wrong_guesses.includes(letter)) {
      element.style.color = "red";
      element.disabled = true;
    } else if (guessed.includes(letter)) {
      element.style.color = "green";
      element.disabled = true;
    }
    element.onclick = function() {
      letterGuessed = this.value;
      var xhttp = new XMLHttpRequest();
      xhttp.open("GET", "/guess_handler?letterGuessed=" + letterGuessed, true);
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
          if (this.status == 200) {
            updateGameState(xhttp.responseText);
          } else {
            alert("Internal server error, please try again later");
          }
        }
      };
      xhttp.send();
    };
    alphabet.appendChild(element);
  }
}

function gameInit() {
  const form = document.querySelector("form");
  const data = new URLSearchParams(new FormData(form).entries());
  console.log(data);
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/game_init?" + data, true);
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      if (this.status == 200) {
        updateGameState(xhttp.responseText);
      } else {
        alert("Internal server error, please try again later");
      }
    }
  };
  xhttp.send();
}

function getLeaderboard() {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/leaderboard", true);
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var jsonResponse = JSON.parse(xhttp.responseText);
      console.log(jsonResponse);
      var leaderboard = document.getElementById("leaderboard");
      leaderboard.innerHTML = "";
      for (row of jsonResponse) {
        var tr = document.createElement("tr");
        for (field of ["difficulty", "score", "username"]) {
          var td = document.createElement("td");
          td.appendChild(document.createTextNode(row[field]));
          tr.appendChild(td);
        }
        leaderboard.appendChild(tr);
      }
    }
  };
  xhttp.send();
}
