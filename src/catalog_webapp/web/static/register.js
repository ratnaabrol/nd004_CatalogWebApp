var googleUser = {};

var startApp = function(state) {
  gapi.load('auth2', function(){
    // Retrieve the singleton for the GoogleAuth library and set up the client.
    auth2 = gapi.auth2.init({
      client_id: '103412510527-l53qc3670gg7tved63dvqer4c0ldr4go.apps.googleusercontent.com',
      cookie_policy: 'single_host_origin',
      scope: "openid email"
    }).then(function(auth){
              attachRegisterAction(auth, state);});
  });
};

function attachRegisterAction(auth, state) {
  element = document.getElementById("customBtn")
  console.log(element.id);
  element.onclick = function() {
    grantPromise = auth.grantOfflineAccess();
    grantPromise.then(
      function(resp){processAccessGrant(resp, state);},
      function(err){ console.log("Error granting access: " + err.error)});
  };
};

function processAccessGrant(resp, state) {
  onGoogleRegister(resp, state, onRegisterSuccess, onAlreadyRegistered, onRegisterError);
};

function onRegisterSuccess() {
  console.log("Registration added");
  window.location.replace("/login");
}

function onAlreadyRegistered() {
  document.getElementById('name').innerText = "Already registered";
  console.log("Already registered")
}

function onRegisterError(err) {
  document.getElementById('name').innerText = "Error registering user.";
  console.log("Unexpected error: " + err)
}

function onGoogleRegister(resp, state, registeredCb, alreadyRegisteredCb, errorCb) {
  console.log(resp);
  // TODO: check for resp containing "code" field, if it doesn't check for "error"
  // field
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/googleOneTimeCode/register?state=' + state);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 /* DONE */) {
      if (xhr.status === 200) {
        registeredCb();
      }
      else if (xhr.status === 409 /* conflict -> already registered */) {
        alreadyRegisteredCb();
      }
      else {
        errorCb(xhr.status);
      }
    }
  };
  xhr.send('code=' + resp.code);
};
