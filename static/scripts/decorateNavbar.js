function rtrim(str, ch) {
    var i = str.length;
    while (i-- && str.charAt(i) === ch);
    return str.substring(0, i + 1);
}

var links = document.getElementsByClassName("navbar-link");
var current_url = window.location.href;
var is_setted = false;

for (var i = 0; i < links.length; ++i) {
    if (current_url.startsWith(links[i].href) && rtrim(links[i].href, '/') !== window.location.origin) {
        links[i].classList.add("active");
        is_setted = true;
        break;
    }
}

if (!is_setted) {
    for (var i = 0; i < links.length; ++i) {
        if (current_url.startsWith(links[i].href)) {
            links[i].classList.add("active");
            is_setted = true;
            break;
        }
    }
}
