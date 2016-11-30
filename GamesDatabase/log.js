//register fields
var uName = document.getElementById("inUName");
var fName = document.getElementById("inFName");
var lName = document.getElementById("inLName");
var pWord = document.getElementById("inPword");
var age = document.getElementById("inAge");

var logName = document.getElementById("userName");
var logPass = document.getElementById("passInput");


//buttons
var regBtn = document.getElementById("registerBtn");
var logBtn = document.getElementById("logBtn");


//methods
logBtn.onclick = function () 
{
	console.log("Log In Button clicked.")
	var request = new XMLHttpRequest();
  	request.onreadystatechange = function () 
  	{
    	if (request.readyState == XMLHttpRequest.DONE) 
    	{
      		if (request.status >= 200 && request.status <= 400) 
      		{
            //var logged = true;
        		console.log(request.responseText)
        		// responses = JSON.parse(request.responseText);
        		alert("welcome " + logName.value)
        		window.location.href = "file:///home/w/wdrummond/Desktop/CS3200/A4/Games.html";

      		} else {
        		alert("Your name or password is invalid. Probably both.");
      		}
    	}
    };

    if (logPass.value == "" || logName.value == "") {
    	alert("Your name or password is invalid. Possibly both.");
    } else{

	    request.open("POST", "http://localhost:8080/session");
	    request.withCredentials = true;
	    request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	  	request.send("userName=" + encodeURIComponent(logName.value)
            + "&password=" + encodeURIComponent(logPass.value));
	  }

	  //window.location.href = "file:///home/w/wdrummond/Desktop/CS3200/A4/Games.html";

};


regBtn.onclick = function () 
{
	console.log("Register Button clicked.")
	var request = new XMLHttpRequest();
  	request.onreadystatechange = function () 
  	{
    	if (request.readyState == XMLHttpRequest.DONE) 
    	{
      		if (request.status >= 200 && request.status <= 400) 
      		{
        		console.log(request.responseText)
        		// responses = JSON.parse(request.responseText);
        		alert("Thanks for registering " + uName.value)

        		uName.value = ""
      			fName.value = ""
      			lName.value = ""
      			pWord.value = ""
      			age.value = ""

      		} else if (request.status >= 400) {
      			console.log(request.responseText)
      			alert("Your name or email has already been taken.")

      		} else {
        		alert("you have failed.");
      		}
    	}
    };

    request.open("POST", "http://localhost:8080/users");
    request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  	request.send("userName=" + encodeURIComponent(uName.value)
            + "&fName=" + encodeURIComponent(fName.value)
            + "&lName=" + encodeURIComponent(lName.value)
            + "&encryptedPassword=" + encodeURIComponent(pWord.value)
            + "&age=" + encodeURIComponent(age.value));

    //alert("Thanks for registering " + uName.value)

    // uName.value = ""
    // fName.value = ""
    // lName.value = ""
    // pWord.value = ""
    // age.value = ""
};
