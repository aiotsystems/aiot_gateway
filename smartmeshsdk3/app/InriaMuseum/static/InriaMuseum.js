var uiReady = false;

//=========================== initialization ==================================

function getCmd() {
    $.getJSON('cmd.json', function(cmd) {
        handleCmd(cmd);
    })
}

function armButtons(svgName) {
    
    switch (svgName) {
        case 'page01_welcome':
            d3.select("#button_start_fr"      ).on('click', clickHandler('DEBUT'));
            break;
        case 'page02_introduction':
            d3.select("#button_active"        ).on('click', clickHandler('SUITE'));
            d3.select("#button_start_fr"      ).on('click', clickHandler('DEBUT'));
            d3.select("#button_credits"       ).on('click', clickHandler('C'));
            break;
        case 'map':
            d3.select("#button_suite_group"   ).on('click', clickHandler('SUITE'));
            d3.select("#button_start_fr_label").on('click', clickHandler('DEBUT'));
            d3.select("#button_credits"       ).on('click', clickHandler('C'));
            break;
        case 'page03_defi':
            d3.select("#button_start_fr_label").on('click', clickHandler('DEBUT'));
            d3.select("#button_credits"       ).on('click', clickHandler('C'));
            break;
        case 'select_music':
            d3.select("#button_music1"        ).on('click', clickHandler('HARRY_POTTER'));
            d3.select("#button_music2"        ).on('click', clickHandler('STAR_WARS'));
            d3.select("#button_start_fr_label").on('click', clickHandler('DEBUT'));
            d3.select("#button_credits"       ).on('click', clickHandler('C'));
            break;
        case 'num_people':
            d3.select("#button_num_people_1"  ).on('click', clickHandler('BUTTON_1'));
            d3.select("#button_num_people_2"  ).on('click', clickHandler('BUTTON_2'));
            d3.select("#button_num_people_3"  ).on('click', clickHandler('BUTTON_3'));
            d3.select("#button_num_people_4"  ).on('click', clickHandler('BUTTON_4'));
            d3.select("#button_credits"       ).on('click', clickHandler('C'));
            break;
        case 'credits':
            d3.select("#button_leave_credits" ).on('click', clickHandler('CLOSE'));
            break;
        
    }
    
    uiReady = true;
}

function clickHandler(buttonname) {
    return function(d,i) {
        $.post(
            'action',
            buttonname,
            function(cmd) {
                handleCmd(cmd);
            },
            'json'
        );
    }
}

//=========================== handle commands from server =====================

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
