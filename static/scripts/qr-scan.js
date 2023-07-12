/* envia el codigo del asistente via POST */
function sendPostRequest(id) {
    console.log(id);
    stopScan();
    /* Robado de: https://stackoverflow.com/a/133997 */
    var form = document.createElement('form');
    form.method = 'post';
    form.action = '';
    var field = document.createElement('input');
    field.type = 'hidden';
    field.name = 'asistente';
    field.value = id;
    form.appendChild(field);
    document.body.appendChild(form);
    form.submit();
}

var button = document.getElementById('qr-button');
var video = document.getElementById('qr-video');
var scanner = new QrScanner(video,
    result => sendPostRequest(result.data),
    { highlightScanRegion: true });

function startScan() {
    /* mostramos el video*/
    video.style.width = '100%';
    scanner.start();
    button.onclick = stopScan
    button.innerText = 'Detener escaneo';
}

function stopScan() {
    /* escondemos el video */
    video.style.width = '0';
    scanner.stop();
    button.onclick = startScan
    button.innerText = 'Escanear código QR'
}
