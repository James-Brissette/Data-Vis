
let votePercentageChart = new VotePercentageChart();

let tileChart = new TileChart();

let shiftChart = new TrendChart();

let electoralVoteChart = new ElectoralVoteChart(shiftChart);

//load the data corresponding to all the election years
//pass this data and instances of all the charts that update on year selection to yearChart's constructor
d3.csv("data/yearwiseWinner.csv").then(electionWinners => {
    let yearChart = new YearChart(electoralVoteChart, tileChart, votePercentageChart, electionWinners, shiftChart);
    yearChart.update();
});

document.addEventListener('click', function(e) {
    console.log(e)
    if (e.path.map(a => a.id).indexOf('stateList') == -1) {
        d3.selectAll('.d3-tip')
            .style('opacity',0)
            .attr('pointer-events','none').select('svg').attr('opacity',0);
        shiftChart.pinned = false;
        shiftChart.pinText.attr('opacity',0)
        d3.selectAll('.pinned').classed('pinned',false)
        
        if (electoralVoteChart.d_brushed && d3.select('#d-brush')._groups[0][0].__brush.selection != null) {
            let min = d3.select('#d-brush')._groups[0][0].__brush.selection[0][0]
            let max = d3.select('#d-brush')._groups[0][0].__brush.selection[1][0]
            d3.select('#d-brush').call(electoralVoteChart.d_brush.move,[min,max]);
        }
        if (electoralVoteChart.r_brushed && d3.select('#r-brush')._groups[0][0].__brush.selection != null) {
            let min = d3.select('#r-brush')._groups[0][0].__brush.selection[0][0]
            let max = d3.select('#r-brush')._groups[0][0].__brush.selection[1][0]
            d3.select('#r-brush').call(electoralVoteChart.r_brush.move,[min,max]);
        }
        if (electoralVoteChart.i_brushed && d3.select('#i-brush')._groups[0][0].__brush.selection != null) {
            let min = d3.select('#i-brush')._groups[0][0].__brush.selection[0][0]
            let max = d3.select('#i-brush')._groups[0][0].__brush.selection[1][0]
            d3.select('#i-brush').call(electoralVoteChart.i_brush.move,[min,max]);
        }
    }
});

window.addEventListener('mousedown', function(e) {
    console.log(e)
    d3.selectAll('.selection').attr('pointer-events','all')
    if (e.path.map(a => a.id).indexOf('selected') != -1) {
        d3.selectAll('.d3-tip')
            .style('opacity',0)
            .attr('pointer-events','none').select('svg').attr('opacity',0);
        shiftChart.pinned = false;
        shiftChart.pinText.attr('opacity',0)
        d3.selectAll('.pinned').classed('pinned',false)
    }
});
