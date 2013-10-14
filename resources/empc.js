$(function em() {

    var pingInterval = null;
    function startPing() {
        pingInterval = setInterval($.get("/ping"), 10000);
    }

    function getNetInfo() {
        $.get("/netinfo")
            .done(function(data) {
                $('#dynamic').html('<h1>Got It!</h1>' + data);
            })
            .fail(function(data) {
                $('#dynamic').html('<h1>Failed</h1>' + data);
            })
    }

    startPing();
    setTimeout(getNetInfo, 1000);
});
