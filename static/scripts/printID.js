var url = new URL(window.location.href); 
var id = url.searchParams.get('id');

// comprueba que id no sea null y que exista un elemento
// html con la misma id de la url, y lo imprime
if (!!id && $('#' + id).length) {
    $('#' + id).printThis();
} else {
    console.error("ID de inscrito no encontrado");
}
