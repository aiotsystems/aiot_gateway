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