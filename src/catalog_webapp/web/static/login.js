var googleUser = {};

var startApp = function(state) {
  gapi.load("auth2", function(){
    // Retrieve the singleton for the GoogleAuth library and set up the client.
    auth2 = gapi.auth2.init({
      client_id: "103412510527-l53qc3670gg7tved63dvqer4c0ldr4go.apps.googleusercontent.com",
      cookie_policy: "single_host_origin",
      access_type: "offline",
      scope: "openid email"
    }).then(function(auth){attachSignInAction(auth, state);});
  });
};

function onSignInSuccess() {
  console.log("Logged in.");
  window.location.replace("/");
};

function onSignInError(err) {
  console.log("Unable to log in: " + err);
  msg = "";
  if (err === 403) {
    msg = "Unknown or deactivated user."
  }
  else if (err === 401) {
    msg = "Error with log in request."
  }
  else {
    msg = "Unable to login (" + err + ")."
  }
  document.getElementById("gMsg").innerText = msg;
};

function processAccessGrant(resp, state) {
  onGoogleSignIn(resp, state, onSignInSuccess, onSignInError);
};

function attachSignInAction(auth, state) {
  element = document.getElementById("customBtn")
  console.log(element.id);
  element.onclick = function() {
    auth.grantOfflineAccess().then(
      function(resp){processAccessGrant(resp, state);},
      function(err){ console.log("Error granting access: " + err.error)});
  };
};

function onGoogleSignIn(resp, state, loggedInCb, errorCb) {
  console.log(resp);
  // TODO: check for resp containing "code" field, if it doesn't check for "error"
  // field
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/googleOneTimeCode/login?state=' + state);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 /* DONE */) {
      if (xhr.status === 200) {
        loggedInCb();
      }
      else {
        errorCb(xhr.status);
      }
    }
  };
  xhr.send('code=' + resp.code);
};
