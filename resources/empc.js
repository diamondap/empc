$(function em() {

    var pingInterval = null;
    var lastPing = null;
    function startPing() {
        pingInterval = setInterval(
            function() {
                $.get("/ping")
                .done(function (data) {
                    lastPing = data.last_ping;
                });
            }, 10000);
    }


    var tNetInfo = Mustache.compile($('#t-netinfo').html());
    function getNetInfo() {
        $.get("/netinfo")
            .done(function(data) {
                console.log(data);
                $('#dynamic').html(tNetInfo(data));
            })
            .fail(function(data) {
                $('#dynamic').html('<h1>Request Failed</h1>' + data);
            })
    }


    startPing();
    setTimeout(getNetInfo, 1000);
});
