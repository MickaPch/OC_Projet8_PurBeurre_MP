$("#id_user_login").on('keyup', function() {
    var user_login = $(this).val();
    if (user_login != "") {
        $.ajax({
            url: "/user/check_user_login/",
            type: "POST",
            data: {user_login: user_login}
        }).done(function(response) {
            if (response == "True") {
                $("#id_user_login").addClass('is-invalid').removeClass('is-valid');
            } else {
                $("#id_user_login").addClass('is-valid').removeClass('is-invalid');
            }
        }).fail(function() {
            console.log('failed');
        });
    } else {
        $(this).removeClass('is-valid is-invalid');
    }
});

$("#id_email").on('keyup', function() {
    var email = $(this).val();
    if (email != "") {
        $.ajax({
            url: "/user/check_email/",
            type: "POST",
            data: {email: email}
        }).done(function(response) {
            if (response == "email disponible") {
                $("#id_email").addClass('is-valid').removeClass('is-invalid');
            } else if (response == "email pris") {
                console.log('Cet email est déjà pris');
                $("#id_email").addClass('is-invalid').removeClass('is-valid');
            } else {
                console.log('Entrez un format de mail valide.');
                $("#id_email").addClass('is-invalid').removeClass('is-valid');
            }
        }).fail(function() {
            console.log('failed');
        });
    } else {
        $(this).addClass('is-invalid').removeClass('is-valid');
    }
});

$("#form_new").on('submit', function(event) {
    event.preventDefault();
    var form = $(this);
    console.log(form);

    send_post(form);

});

function send_post(form) {
    console.log('Send post is ok');
    console.log(form);
    if ( $("#id_pwd").val() == $("#id_pwd_confirm").val() ) {
        $.ajax({
            url: form.attr("data-new-account"),
            data: form.serialize(),
            dataType: 'json',
            method: "POST",
            success: function (data) {
                if (data.ok) {
                    alert('Le compte a bien été créé')
                } else {
                    alert('Erreur')
                }
            },
            error: function(xhr, errmsg, err) {
                console.log(errmsg);
            }
        });
    } else {
        alert('Les mots de passe de correspondent pas.');
    }
}


