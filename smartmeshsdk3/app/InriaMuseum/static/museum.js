var uiReady = false;

//=========================== initialization ==================================

function loadSvg() {
    d3.xml('/static/museum.svg')
        .then(data => {
            document.body.append(data.documentElement);
            buildPage();
        })
}

function buildPage() {
    
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