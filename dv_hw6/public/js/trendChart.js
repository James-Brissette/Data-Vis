/** Class implementing the trendChart. */
class TrendChart {

    /**
     * Initializes the svg elements required for this chart;
     */
    constructor(){

        this.margin = {top: 10, right: 20, bottom: 20, left: 50};

        this.stateNames = d3.select('#shiftChart').classed('sideBar',true).select('#stateList').append('svg').attr('height',800)
        this.d_chart = this.stateNames.append('g')
            .attr('id','d-brushed-states')
            .attr('class','democrat')
        this.r_chart = this.stateNames.append('g')
            .attr('id','r-brushed-states')            
            .attr('class','republican')
        this.i_chart = this.stateNames.append('g')
            .attr('id','i-brushed-states')
            .attr('class','independent')

        this.tip = d3.tip().attr('class', 'd3-tip')
			.direction('w')
			.offset(function() {
				return [0,0];
            });
            
        this.vis = d3.select('#stateList').append('svg')
            .attr('id','tip-vis')
        .append('rect').attr('id','vis')
            .attr('x',0)
            .attr('y',0)
            .attr('height',50)
            .attr('width',50)
            .attr('fill', '#abc');
    };

    /**
     * Creates a list of states that have been selected by brushing over the Electoral Vote Chart
     *
     * @param selectedStates data corresponding to the states selected on brush
     */
    update(selectedStates){
    
    // ******* TODO: PART V *******
    //Display the names of selected states in a list
    //selectedStates = {'name': stateName, 'party': 'd'}
    if (selectedStates[0] == null) {
        d3.select('#' + selectedStates[1] + '-brushed-states').selectAll('text').text('');
        resizeLists();
        return;
    }
    let x = d3.select('#vis')
    console.log(x._groups[0]) 
    this.tip.html((d) => { 
           return '<svg>' + d3.select('#vis')._groups[0][0].outerHTML + '</svg>'
        
    });
    d3.select('#stateList').select('svg').call(this.tip);

    let party = selectedStates[0].party;
    let nameList = d3.select('#' + party + '-brushed-states').selectAll('text').data(selectedStates);
    let nameListEnter = nameList.enter().append('text');
    nameList.exit().remove();
    nameList = nameListEnter.merge(nameList);
    nameList
        .text(d => d.name)
        .attr('x',this.margin.left)
        .attr('y', (d,i) => i*15 + 15)
        .on('mouseenter', this.tip.show)
        .on('mouseleave', this.tip.hide)

    resizeLists();

    

    

    
    
    function resizeLists() {
        d3.select('#r-brushed-states').attr('transform','translate(0,' + d3.select('#d-brushed-states').node().getBoundingClientRect().height + ')');
        d3.select('#i-brushed-states').attr('transform','translate(0,' + (d3.select('#r-brushed-states').node().getBoundingClientRect().height + 
                                                                         d3.select('#d-brushed-states').node().getBoundingClientRect().height) + ')');
    }


    //******** TODO: PART VI*******
    //Use the shift data corresponding to the selected years and sketch a visualization
    //that encodes the shift information



    //******** TODO: EXTRA CREDIT I*******
    //Handle brush selection on the year chart and sketch a visualization
    //that encodes the shift informatiomation for all the states on selected years



    //******** TODO: EXTRA CREDIT II*******
    //Create a visualization to visualize the shift data
    //Update the visualization on brush events over the Year chart and Electoral Vote Chart

    };

}