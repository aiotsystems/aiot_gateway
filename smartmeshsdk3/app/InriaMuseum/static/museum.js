var uiReady = false;

//=========================== defines =========================================

//=========================== globals =========================================

//=========================== helpers =========================================

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