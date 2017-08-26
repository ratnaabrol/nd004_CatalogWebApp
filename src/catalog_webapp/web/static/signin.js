var googleUser = {};

var startApp = function(state) {
  gapi.load('auth2', function(){
    // Retrieve the singleton for the GoogleAuth library and set up the client.
    auth2 = gapi.auth2.init({
      client_id: '103412510527-l53qc3670gg7tved63dvqer4c0ldr4go.apps.googleusercontent.com',
      cookie_policy: 'single_host_origin',
      scope: "profile email"
    });
    attachSignin(document.getElementById('customBtn'), state);
  });
};

function attachSignin(element, state) {
  console.log(element.id);
  auth2.attachClickHandler(element, {},
    function(googleUser) {
      onGoogleSignIn(googleUser, state,
                     function() {
                       document.getElementById('name').innerText = "Created registration as: " +
                           googleUser.getBasicProfile().getName();
                       console.log("Registration added");
                     },
                     function() {
                       document.getElementById('name').innerText = "Already registered as: " +
                           googleUser.getBasicProfile().getName();
                       console.log("Already registered")
                     },
                     function(http_status) {
                       document.getElementById('name').innerText = "Error registering user.";
                       console.log("Unexpected error: " + http_status)
                     });
    }, function(error) {
      document.getElementById('name').innerText = "Error registering user.";
      console.log(JSON.stringify(error, undefined, 2));
    });
}

function onGoogleSignIn(googleUser, state, registered, alreadyRegistered, error) {
  var authResponse = googleUser.getAuthResponse(true);
  var id_token = authResponse.id_token;
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/googleTokenRegister?state=' + state);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 /* DONE */) {
      if (xhr.status === 200) {
        registered();
      }
      else if (xhr.status === 409 /* conflict -> already registered */) {
        alreadyRegistered();
      }
      else {
        error(xhr.status);
      }
    }
  };
  xhr.send('idtoken=' + id_token);
};
