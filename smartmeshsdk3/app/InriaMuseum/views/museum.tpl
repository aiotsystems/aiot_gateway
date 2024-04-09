<!doctype html>

<meta charset="utf-8">
<title>Inria Museum</title>

<link   rel="stylesheet" href="/static/museum.css">
<script src="/static/d3.v7.min.js"></script>
<script src="/static/jquery-3.7.1.min.js" charset="utf-8"></script>
<script src="/static/museum.js" charset="utf-8"></script>

<script id="js">
    $(document).ready(function() {
        loadSvg();
        getData();
        // periodically refresh
        setInterval(function() {
            getData()
        },500);
    });
</script>