function fbbgchange1(el) {
    el.style.color = "#FF87FF";
}
function fbbgchange2(el) {
    el.style.color = "#2D2D32";
}
function fbcolorchangename1() {
    $('#id_name').css('background-color', '#FFEBEF')
}
$('#id_name').focus(fbcolorchangename1);
function fbcolorchangename2() {
    $('#id_name').css('background-color', 'white')
}
$('#id_name').blur(fbcolorchangename2);
function fbcolorchangeemail1() {
    $('#id_email').css('background-color', '#FFEBEF')
}
$('#id_email').focus(fbcolorchangeemail1);
function fbcolorchangeemail2() {
    $('#id_email').css('background-color', 'white')
}
$('#id_email').blur(fbcolorchangeemail2);
function fbcolorchangemsg1() {
    $('#id_msg').css('background-color', '#FFEBEF')
}
$('#id_msg').focus(fbcolorchangemsg1);
function fbcolorchangemsg2() {
    $('#id_msg').css('background-color', 'white')
}
$('#id_msg').blur(fbcolorchangemsg2);