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
                var netInfo = {}
                for(var i=0; i < data.length; i++) {
                    var iface = data[i];
                    if (iface.is_default) {
                        netInfo.ip4_address = iface.ip4_address;
                        netInfo.mac_address = iface.mac_address;
                        netInfo.gateway = iface.gateway;
                    }
                }
                console.log(netInfo);
                $('#dynamic').html(tNetInfo(netInfo));
            })
            .fail(function(data) {
                $('#dynamic').html('<h1>Failed</h1>' + data);
            })
    }

    function findRouter() {
        $.get("/find_router")
            .done(function(data) {
                console.log(data);
                $('#dynamic').html(data);
            })
            .fail(function(data) {
                $('#dynamic').html('<h1>Failed</h1>' + data);
            })
    }

    startPing();
    setTimeout(getNetInfo, 1000);
    $('#btn-find-router').click(findRouter);
});
