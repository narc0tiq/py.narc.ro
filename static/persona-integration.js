// Support for Mozilla Persona

$(function() { // $().ready() handler
    var signinLink = document.getElementById("signin");
    if (signinLink) {
        signinLink.onclick = function(event) {
            navigator.id.request({
                siteName:"Narc Dot Ro",
                oncancel: function() { window.location = signinLink.href; }
            });
            event.preventDefault(); event.stopPropagation(); };
    }

    var signoutLink = document.getElementById("signout");
    if (signoutLink) {
        signoutLink.onclick = function(event) { navigator.id.logout(); event.preventDefault(); event.stopPropagation(); };
    }

    navigator.id.watch({loggedInUser: currentUser,
        onlogin: function(assertion) {
            $.ajax({
                type: "POST",
                url: "/ajax-endpoint/login",
                data: {assertion: assertion, csrf: csrf_token},
                success: function(res, status, xhr) { window.location.reload(); },
                error: function(xhr, status, err) { alert("Login failure: " + err); }
            });
        },
        onlogout: function() {
            $.ajax({
                type: "POST",
                url: "/ajax-endpoint/logout",
                success: function(res, status, xhr) { window.location.reload(); },
                error: function(xhr, status, err) { alert("Logout failure: " + err); }
            });
        }
    });
});

