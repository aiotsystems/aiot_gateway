<html>
    <head>
        <meta charset="utf-8">
        <title>Inria Museum</title>
        <link   rel="stylesheet" href="/static/InriaMuseum.css">
        <script src="/static/d3.v7.min.js"></script>
        <script src="/static/jquery-3.7.1.min.js" charset="utf-8"></script>
        <script src="/static/museum.js" charset="utf-8"></script>
        <script id="js">
            $(document).ready(function() {
                getCmd();
                setInterval(function() {
                    getCmd()
                },1000);
            });
        </script>
    </head>
    <body>
        <div id="svgdiv"></div>
    </body>
</html>
