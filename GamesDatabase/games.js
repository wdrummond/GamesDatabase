
var title = document.getElementById("titleField");
var genre = document.getElementById("genreField");
var platform = document.getElementById("consoleField");
var rating = document.getElementById("ratingField");
var multiplayer = document.getElementById("multiplayerField");
var online = document.getElementById("onlineField");


var storeBtn = document.getElementById("storeBtn");
var loadBtn = document.getElementById("loadBtn");
var clrBtn = document.getElementById("clrBtn");
var delBtn = document.getElementById("delBtn");
var editBtn = document.getElementById("editBtn");
var updateBtn = document.getElementById("updateBtn");

var putID;

var index = function () {
  console.log("load button clicked");
  var request = new XMLHttpRequest();
  request.onreadystatechange = function () {
    if (request.readyState == XMLHttpRequest.DONE) 
    {
      if (request.status >= 200 && request.status <= 400) 
      {
        var responses = JSON.parse(request.responseText);
        var elements = document.getElementsByClassName("tableRow");
        while(elements.length > 0) 
        {
          elements[0].parentNode.removeChild(elements[0]);
        }
        for(var i = 0; i<responses.length; i++) 
        {
          tableHandler(responses[i]);  
        }
      } else {
        alert("you have failed.");
      }
    }
  };
request.open("GET", "http://localhost:8080/games");
request.withCredentials = true;
request.send();
};

var tableHandler = function (message) {
  var confirmed = false;
  var table = document.getElementById("displayTable");
  var template = document.getElementById("rowTemplate");
  //loop over the existing rows and remove/re add everything

  var tableItem = template.content.cloneNode(true);
  tableItem.id = message["id"];
  //console.log(tableItem.id);
  tableItem.querySelector('.titleRow').innerHTML = message.title;
  tableItem.querySelector('.consoleRow').innerHTML = message.console;
  tableItem.querySelector('.ratingRow').innerHTML = message.rating;
   
    tableItem.querySelector('.delBtn').onclick = function() {
      confirmed = confirm('Are you absolutely sure you want to get rid of ' + message.title + '?');
      if (confirmed) 
      {
        var request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (request.readyState == XMLHttpRequest.DONE) 
            {
              if (request.status >= 200 && request.status < 400) 
              {
                //responses = JSON.parse(request.responseText); 
                index();
              } else {
                alert("you have failed at deleting.");
              }
            }
          };
        request.open("DELETE", "http://localhost:8080/games/"+tableItem.id);
        //request.withCredentials = true;
        request.send();    
      };
    } 

    tableItem.querySelector('.editBtn').onclick = function() {
      //alert(message.title);
      title.value = message.title;
      genre.value = message.genre;
      platform.value = message.console;
      rating.value = message.rating;
      multiplayer.value = message.multiplayer;
      online.value = message.online;
      console.log(tableItem.id);
      putID = tableItem.id;

    };
      table.appendChild(tableItem); 
};

// var tableUpdateHandler = function(message) {
//   //var tableItem = template.content.cloneNode(true);
//   console.log(message)

// };

storeBtn.onclick = function () {
  console.log("store button clicked");
  var request = new XMLHttpRequest();
  request.onreadystatechange = function () {
    if (request.readyState == XMLHttpRequest.DONE) {
      if (request.status >= 200 && request.status <= 400) {
        //responses = JSON.parse(request.responseText);
      } else {
        alert("you have failed.");
      }
    }
  };
request.open("POST", "http://localhost:8080/games");
request.withCredentials = true;
request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
request.send( "title=" + encodeURIComponent(title.value)
			+ "&genre=" + encodeURIComponent(genre.value)
			+ "&console=" + encodeURIComponent(platform.value)
			+ "&rating=" + encodeURIComponent(rating.value)
			+ "&multiplayer=" + encodeURIComponent(multiplayer.value)
			+ "&online=" + encodeURIComponent(online.value));
};

loadBtn.onclick = index;


updateBtn.onclick = function () {
  console.log("edit button clicked");
  var request = new XMLHttpRequest();
  request.onreadystatechange = function () {
    if (request.readyState == XMLHttpRequest.DONE) {
      if (request.status >= 200 && request.status <= 400) {
        console.log(request.responseText)
        // responses = JSON.parse(request.responseText);
        // tableUpdateHandler(responses);  
      } else {
        alert("you have failed.");
      }
    }
  };
  //tableItem.id = message["id"];
  request.open("PUT", "http://localhost:8080/games/" + putID);
  //request.withCredentials = true;
  request.send("title=" + encodeURIComponent(title.value)
            + "&genre=" + encodeURIComponent(genre.value)
            + "&console=" + encodeURIComponent(platform.value)
            + "&rating=" + encodeURIComponent(rating.value)
            + "&multiplayer=" + encodeURIComponent(multiplayer.value)
            + "&online=" + encodeURIComponent(online.value));
  var table = document.getElementById('displayTable');
};

clrBtn.onclick = function () {
  console.log("clear button clicked");
  
  title.value = ''
  genre.value = ''
  platform.value = ''
  rating.value = ''
  multiplayer.value = ''
  online.value = ''
};
