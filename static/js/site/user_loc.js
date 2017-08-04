$(document).ready(function() {
    $(".deleteLoc").click(function() {
        $.$urlDelete$ = $(".deleteLoc").attr('data-href');
        $("#sureDelete").modal();
    });
    $("#yesDelete").click(function() {
        window.location.href = $.$urlDelete$;
    });
});
