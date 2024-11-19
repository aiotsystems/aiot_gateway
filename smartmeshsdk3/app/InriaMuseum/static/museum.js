var uiReady = false;

//=========================== initialization ==================================

function getCmd() {
    $.getJSON('cmd.json', function(cmd) {
        handleCmd(cmd);
    })
}

function handleCmd(cmd) {
    
    console.log(cmd);
    
    switch(cmd.cmdName) {
        case 'loadsvg':
            d3.xml('/static/'+cmd.svgName+'.svg')
                .then(data => {
                    $("#svgdiv").html(data.documentElement);;
                    armButtons(cmd.svgName);
                })
    }
}

function armButtons(svgName) {
    
    switch (svgName) {
        case 'page01_welcome':
            d3.select("#button_start_fr")        // "DEBUT"
                .on('click', function(d,i){
                    window.location = 'page02_introduction';
                });
            break;
        case 'page02_introduction':
            d3.select("#button_active")          // "SUITE"
                .on('click', function(d,i){
                    window.location = 'map';
                });
            d3.select("#button_start_fr")        // "DEBUT"
                .on('click', function(d,i){
                    window.location = 'page01_welcome';
                });
            d3.select("#button_credits")         // "C"
                .on('click', function(d,i){
                    window.location = 'credits';
                });
            break;
        case 'map':
            d3.select("#button_suite_group")     // "SUITE"
                .on('click', function(d,i){
                    window.location = 'page03_defi';
                });
            d3.select("#button_start_fr_label")  // "DEBUT"
                .on('click', function(d,i){
                    window.location = 'page01_welcome';
                });
            d3.select("#button_credits")         // "C"
                .on('click', function(d,i){
                    window.location = 'credits';
                });
            break;
        case 'page03_defi':
            d3.select("#button_start_fr_label")  // "DEBUT"
                .on('click', function(d,i){
                    window.location = 'page01_welcome';
                });
            d3.select("#button_credits")         // "C"
                .on('click', function(d,i){
                    window.location = 'credits';
                });
            break;
    }
    
    /*
    d3.select("#button_lowpower")
        .on('click', function(d,i){
            $.post('museum', 'button_lowpower');
        });
    d3.select("#button_active")
        .on('click', function(d,i){
            $.post('museum', 'button_active');
        });
    d3.select("#button_music1")
        .on('click', function(d,i){
            $.post('museum', 'button_music1');
        });
    d3.select("#button_music2")
        .on('click', function(d,i){
            $.post('museum', 'button_music2');
        });
    */
    
    uiReady = true;
}

//=========================== periodic ========================================

function getData() {
    
    $.getJSON('museum.json', function(data) {
        updateUI(data);
    })
}

function updateUI(data) {
    
    // abort if UI not ready
    if (uiReady==false) {
        return;
    }
    
    // motes
    for (const [key,value] of Object.entries(data.motes)) {
        d3.select('#'+key)
            .style("fill",         value.fill)
            .style("stroke",       value.stroke)
            .style("stroke-width", 3);
    }
}
