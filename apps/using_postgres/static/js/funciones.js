$(document).ready( function() {

    $("#email").focusout( function(){
        checkEmail();
    })

    $('#email').focusin( function(){
        $("#errorEmail").text("");
    })
    $('#boton01').click(function(event){
        $('usuario').remove();

    });


    // $('#password').click( function(){
    //     $

    // })
});

function checkEmail(){
    let data = $('#email').serialize();
    console.log('Data es ', data);
    $.ajax({
        method: "GET",
        // method: "POST",
        url: '/verificarEmail',
        data: data
    })

    .done(function(respuesta){
        console.log('la respuesta es ', respuesta);
        if (respuesta['respuesta'] == 'Existe'){
            $('#errorEmail').text('El email ya se encuentra registrado')
        }
    })

    .fail(function(){
        // alert('error');
    })

}

let idUsuario = null;

function establecerId(id){
    idUsuario = id;
    alert('El usuario a eliminar es el ' + idUsuario)
}

function eliminarUsuario(){
    window.location.href = "/eliminar/"+idUsuario
}