var firebaseConfig = {
    apiKey: "AIzaSyDMbl0549XQXckH-bkqkZrZgnN-3C4DJEs",
    authDomain: "eduall-d42d8.firebaseapp.com",
    projectId: "eduall-d42d8",
    storageBucket: "eduall-d42d8.appspot.com",
    messagingSenderId: "173044320418",
    appId: "1:173044320418:web:8205dddd73788c415c2ffb"
};
firebase.initializeApp(firebaseConfig);

// Google Sign-In Function
function googleSignIn() {
    var provider = new firebase.auth.GoogleAuthProvider();
    firebase.auth().signInWithPopup(provider).then(function(result) {
        var user = result.user;
        // Resolve the ID token before sending it
        user.getIdToken().then(function(idToken) {
            // Send the ID token to the backend
            fetch('/google-login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ idToken: idToken })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/dashboard';
                } else {
                    console.error('Google Sign-In failed:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }).catch(function(error) {
        console.error('Error during Google Sign-In:', error);
    });
}