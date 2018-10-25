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
            

        this.trendData = [];
        let years = ['1940','1944','1948','1952','1956','1960','1964','1968','1972','1976','1980','1984', '1988','1992','1996','2000','2004','2008','2012','2016']
        years.forEach(year => {
            d3.csv('data/Year_Timeline_' + year + '.csv').then(electionResult => {
                console.log('Recorded Year ' + year + ' data to trendChart');
                
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
    };

    updateActiveYears(yearList) {
        this.yearList = yearList;
        console.log('Updated!')
    }
    /**
     * Creates a list of states that have been selected by brushing over the Electoral Vote Chart
     *
     * @param selectedStates data corresponding to the states selected on brush
     */
    update(selectedStates){
    console.log(this.trendData)
    // ******* TODO: PART V *******
    //Display the names of selected states in a list
    //selectedStates = {'name': stateName, 'party': 'd'}
    let that = this;
    if (selectedStates[0] == null) {
        d3.select('#' + selectedStates[1] + '-brushed-states').selectAll('text').text('');
        resizeLists();
        return;
    }
    
    generateChart(this,selectedStates[0]);
    let x = d3.select('#vis')
    console.log(x._groups[0]) 
    this.tip.html((d) => { 
           return generateChart(that,d);
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
        .attr('cursor','pointer')
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
    
    
    function generateChart(that, stateData) {
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

        
        console.log(pointData)
        let points = that.beta.select('.shiftPoints').selectAll('circle').data(pointData)
        let pointsEnter = points.enter().append('circle')
        points.exit().remove
        points = pointsEnter.merge(points)
        points 
            .attr('cx', d => xScale(d.Year) + chartshiftX + 35)
            .attr('cy', d => yScale(d.RD_Difference) + 15)
            .attr('r', 7)
            .attr('fill', d => that.colorScale(d.RD_Difference))

        console.log(that.yearList);
        if (that.yearList.length != 0) {
            points.filter(d => {
                return that.yearList.indexOf(d.Year) == -1
            }).attr('fill','#aaa')
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

        
        console.log(barData)
        let shiftBars = that.beta.select('.shiftBars').selectAll('rect').data(barData)
        let shiftBarsEnter = shiftBars.enter().append('rect')
        shiftBars.exit().remove
        shiftBars = shiftBarsEnter.merge(shiftBars)
        shiftBars 
            .attr('x', d => xShiftScale(+d.Year) + chartshiftX + 30)
            .attr('y', d => d.Direction == 'Right' ? (botY / 2) + chartshiftY - heightScale(+d.Shift) : (botY / 2) + chartshiftY)
            .attr('width', 15)
            .attr('height', d => heightScale(+d.Shift))
            .attr('fill', d => d.Direction == 'Right' ? that.colorScale(+d.Shift) : that.colorScale(-d.Shift))

        console.log(that.yearList);
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
            .attr('class','votesPercentageText');

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