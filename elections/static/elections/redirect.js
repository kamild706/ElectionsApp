let field = $("#time");
let time = Number(field.text());

setTimeout(function () {
    window.location.href = "/";
}, 10000);

setInterval(function () {
    field.text(--time);
}, 1000);
