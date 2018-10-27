/** Class implementing the trendChart. */
class TrendChart {

    /**
     * Initializes the svg elements required for this chart;
     */
    constructor(){
        this.electoralVoteChart = 0;
        this.margin = {top: 10, right: 20, bottom: 20, left: 50};

        this.stateNames = d3.select('#shiftChart').classed('sideBar',true).select('#stateList').append('svg').classed('.stateList',true).attr('height',800)
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
				return ([200,-20]);
            });
            

        this.trendData = [];
        let years = ['1940','1944','1948','1952','1956','1960','1964','1968','1972','1976','1980','1984', '1988','1992','1996','2000','2004','2008','2012','2016']
        years.forEach(year => {
            d3.csv('data/Year_Timeline_' + year + '.csv').then(electionResult => {
                let val = {'year': year, 'MaxRD': Math.max(...electionResult.map(a=>+a.RD_Difference)), 'MinRD': Math.min(...electionResult.map(a=>+a.RD_Difference)), 'raw': electionResult}
                this.trendData.push(val);
            });
        })

        this.svgHeight = 400
        this.svgWidth = 400
        this.beta = d3.select('#beta').append('svg')
        this.beta.append('g').classed('pointsTitle', true).append('text')
        this.beta.append('g').classed('barsTitle', true).append('text')
        this.beta.append('g').classed('stateName', true).append('text')
        this.beta.append('g').classed('typeText', true).append('text')
        this.beta.append('g').classed('xAxis', true)
        this.beta.append('g').classed('yAxis', true)
        this.beta.append('g').classed('shiftPoints', true)
        this.beta.append('g').classed('shiftBars', true)
        this.beta.append('g').classed('xShiftAxis', true)
        this.beta.append('g').classed('yShiftAxis', true)

        let domain = [-60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60];
        let range = ["#063e78", "#08519c", "#3182bd", "#6baed6", "#9ecae1", "#c6dbef", "#fcbba1", "#fc9272", "#fb6a4a", "#de2d26", "#a50f15", "#860308"];
        this.colorScale = d3.scaleQuantile()
            .domain(domain)
            .range(range);

        this.yearList = [];
        this.pinned = false;
        this.activeCountry = 0;
        this.selectedStates = [];
        this.pinText = this.stateNames.append('text').classed('.pin-text', true).text('(pinned)').attr('opacity',0)
    };

    chooseClass (party) {
        if (party == "R"){
            return "republican";
        }
        else if (party== "D"){
            return "democrat";
        }
        else if (party == "I"){
            return "independent";
        }
    }

    linkElectoralVoteChart(chart) {
        this.electoralVoteChart = chart;
    }
    updateActiveYears(yearList) {
        this.yearList = yearList;
    }

    removeTip() {
        return this.tip.hide
    }
    /**
     * Creates a list of states that have been selected by brushing over the Electoral Vote Chart
     *
     * @param selectedStates data corresponding to the states selected on brush
     */
    update(selectedStates){
        this.selectedState = selectedStates;
    // ******* TODO: PART V *******
    //Display the names of selected states in a list
    //selectedStates = {'name': stateName, 'party': 'd'}
    let that = this;
    if (selectedStates[0] == null) {
        d3.select('#' + selectedStates[1] + '-brushed-states').selectAll('text').text('');
        resizeLists();
        this.removeTip()
        return;
    }
    
    generateChart(this,selectedStates[0]);
    let x = d3.select('#vis')
    this.tip.html((d) => { 
           return generateChart(that,d);
    });
    let listSpan = d3.select('#stateList').select('svg').call(this.tip);

    let party = selectedStates[0].party;
    let nameList = d3.select('#' + party + '-brushed-states').selectAll('text').data(selectedStates);
    let nameListEnter = nameList.enter().append('text');
    nameList.exit().remove();
    nameList = nameListEnter.merge(nameList);
    nameList
        .text(d => d.name)
        .attr('x',this.margin.left)
        .attr('y', (d,i) => i*15 + 15)
        .attr('cursor','pointer')
        .on('click', function(d,i) { 
                let count = d3.selectAll('.pinned')._groups[0].length;
                let e = nameList.filter((d,index) => { return index == i })
                if (count == 0) {
                    that.pinned = true;
                    d3.selectAll('.pinned').classed('pinned',false)
                    e.classed('pinned',true)
                    that.pinText
                        .attr('x', e._groups[0][0].x.baseVal[0].value + e._groups[0][0].textLength.baseVal.value + 15)
                        .attr('y', e._groups[0][0].y.baseVal[0].value)
                    that.pinText.attr('opacity','1')
                    that.update(selectedStates)

                    return
                }
                
                if (e._groups[0][0].className.baseVal.indexOf('pinned') == 0) {
                    //Clicked element has class pinned
                    that.pinned = false;
                    e.classed('pinned',false)
                    that.pinText.attr('opacity','0')
                    
                    that.update(selectedStates)
                    return
                }
        })
        .on('mouseenter', this.pinned ? 
                            (d3.select('.d3-tip.w').select('svg').select('.stateName').select('text')._groups[0][0].textContent == this.activeCountry ? 
                            function() {return console.log('butter')} : null ) : this.tip.show)
        .on('mouseout', this.pinned ? null : this.tip.hide)

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
    
    function generateChart(that, stateData) {
        console.log(stateData)
        let xMax = 550;
        let yMax = 350;

        let topY = 175;        
        let botY = 175;
        let chartshiftY = 220;
        let chartshiftX = 75;
        that.beta.attr('width',xMax).attr('height',yMax + 50)

        let pointData = []
        that.trendData.forEach(year => {
            pointData.push(year.raw[year.raw.map(a => a.State).indexOf(stateData.name)]);
        });
        while(pointData[0] == undefined) { pointData.shift(); }
        pointData.sort(function(a, b) {
            return a.Year - b.Year
        } );
        
        let domain = Math.max(Math.max(...pointData.map(a => a.RD_Difference)),Math.abs(Math.min(...pointData.map(a => a.RD_Difference))))
        let yScale = d3.scaleLinear()
                    .domain([domain,-domain])
                    .range([0,topY]);
        let xScale = d3.scaleLinear()
                    .domain([1940,2016])
                    .range([0,xMax - 150])
                    .nice()

        let xAxis = d3.axisBottom()
                    .scale(xScale)
                    .tickSize(0)
                

        let yAxis = d3.axisLeft()
                    .scale(yScale);


        that.beta.select('.xAxis').attr('transform','translate(' + chartshiftX + ',' + ((topY / 2) + 15) + ')').call(xAxis).selectAll('text').remove();
        that.beta.select('.yAxis').attr('transform','translate(' + chartshiftX + ',15)').call(yAxis);


        let connections = that.beta.select('.shiftPoints').selectAll('line').data(pointData)
        let connectionsEnter = connections.enter().append('line')
        connections.exit().remove()
        connections = connectionsEnter.merge(connections)
        connections 
            .attr('x1', (d,i) => i == 0  ? xScale(d.Year) + chartshiftX + 35 : xScale(d.Year - 1) + chartshiftX + 20)
            .attr('y1', (d,i) => i == 0 ? yScale(d.RD_Difference) + 15 : yScale(+connections._groups[0][i-1].__data__.RD_Difference) + 15)
            .attr('x2', d => xScale(d.Year) + chartshiftX + 35)
            .attr('y2', d => yScale(d.RD_Difference) + 15)
            .attr('class', d=> 'line' + d.Year)
            .attr('stroke', d => that.colorScale(d.RD_Difference))

        let points = that.beta.select('.shiftPoints').selectAll('circle').data(pointData)
        let pointsEnter = points.enter().append('circle')
        points.exit().remove()
        points = pointsEnter.merge(points)
        points 
            .attr('cx', d => xScale(d.Year) + chartshiftX + 35)
            .attr('cy', d => yScale(d.RD_Difference) + 15)
            .attr('r', 7)
            .attr('fill', d => that.colorScale(d.RD_Difference))
            .attr('class', d=> 'circle' + d.Year)
        points.append('title')
            .text(d => d.RD_Difference)

        if (that.yearList.length != 0) {
            points.filter(d => {
                return that.yearList.indexOf(d.Year) == -1
            }).attr('fill','#aaa');
            connections.filter(d => {
                return that.yearList.indexOf(d.Year) == -1
            }).attr('stroke','#aaa')
        }



        let barData = []
        that.trendData.forEach(year => {
            barData.push(year.raw[year.raw.map(a => a.State).indexOf(stateData.name)]);
        });
        while(barData[0] == undefined) { barData.shift(); }
        
        domain = Math.max(Math.max(...barData.map(a => a.Shift)),Math.abs(Math.min(...barData.map(a => a.Shift))))
        let yShiftScale = d3.scaleLinear()
                    .domain([domain,-domain])
                    .range([0,botY]);
        let xShiftScale = d3.scaleLinear()
                    .domain([1940,2016])
                    .range([0,xMax - 150])
                    .nice()
        let heightScale = d3.scaleLinear()
                    .domain([0, domain])
                    .range([0,botY / 2])

        let xShiftAxis = d3.axisBottom()
                    .scale(xShiftScale)
                    .tickSize(0)
                

        let yShiftAxis = d3.axisLeft()
                    .scale(yShiftScale);


        that.beta.select('.xShiftAxis').attr('transform','translate(' + chartshiftX + ',' + ((botY / 2) + chartshiftY) + ')').call(xShiftAxis).selectAll('text').remove();
        that.beta.select('.yShiftAxis').attr('transform','translate(' + chartshiftX + ',' + (chartshiftY) + ')').call(yShiftAxis);

        let shiftBars = that.beta.select('.shiftBars').selectAll('rect').data(barData)
        let shiftBarsEnter = shiftBars.enter().append('rect')
        shiftBars.exit().remove()
        shiftBars = shiftBarsEnter.merge(shiftBars)
        shiftBars 
            .attr('x', d => xShiftScale(+d.Year) + chartshiftX + 30)
            .attr('y', d => d.Direction == 'Right' ? (botY / 2) + chartshiftY - heightScale(+d.Shift) : (botY / 2) + chartshiftY)
            .attr('width', 15)
            .attr('height', d => heightScale(+d.Shift))
            .attr('class', d=> 'bar' + d.Year)
            .attr('fill', d => d.Direction == 'Right' ? that.colorScale(+d.Shift) : that.colorScale(-d.Shift))
        shiftBars.append('title')
            .text(d => d.Shift + '% to the ' + d.Direction)
            
        if (that.yearList.length != 0) {
            shiftBars.filter(d => {
                return that.yearList.indexOf(d.Year) == -1
            }).attr('fill','#aaa')
        }

        that.beta.select('.pointsTitle').select('text')
            .attr('x', 0)
            .attr('y', 0)
            .attr('text-anchor', 'middle')
            .attr('transform','translate(40,100) rotate(270)')
            .text('RD_Difference')
            .attr('class','tilestext');

        that.beta.select('.barsTitle').select('text')
            .attr('x', 0)
            .attr('y', 0)
            .attr('text-anchor', 'middle')
            .attr('transform','translate(40,300) rotate(270)')
            .text('Voter Shift')
            .attr('class','tilestext');

        that.beta.select('.stateName').select('text')
            .attr('x', 450)
            .attr('y', 40)
            .attr('text-anchor', 'middle')
            .text(stateData.name)
            .attr('class','votesPercentageText ' + (stateData.party == 'd' ? 'democrat' : (stateData.party == 'r' ? 'republican' : 'independent')));

        that.beta.select('.typeText').select('text')
            .attr('x', 470)
            .attr('y', 380)
            .attr('text-anchor', 'middle')
            .text('Trend Chart')
            .attr('class','votesPercentageText')
            .attr('fill','#eee')

        
        that.beta.style('border','1px solid')
        return(that.beta._groups[0][0].outerHTML)
    }

    //******** TODO: EXTRA CREDIT II*******
    //Create a visualization to visualize the shift data
    //Update the visualization on brush events over the Year chart and Electoral Vote Chart

    };

}