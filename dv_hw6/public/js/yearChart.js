class YearChart {

    /**
     * Constructor for the Year Chart
     *
     * @param electoralVoteChart instance of ElectoralVoteChart
     * @param tileChart instance of TileChart
     * @param votePercentageChart instance of Vote Percentage Chart
     * @param electionInfo instance of ElectionInfo
     * @param electionWinners data corresponding to the winning parties over mutiple election years
     */
    constructor (electoralVoteChart, tileChart, votePercentageChart, electionWinners, trendChart) {

        //Creating YearChart instance
        this.electoralVoteChart = electoralVoteChart;
        this.tileChart = tileChart;
        this.votePercentageChart = votePercentageChart;
        this.trendChart = trendChart;
        // the data
        this.electionWinners = electionWinners;
        console.log(electionWinners)
        
        // Initializes the svg elements required for this chart
        this.margin = {top: 10, right: 20, bottom: 20, left: 50};
        let divyearChart = d3.select("#year-chart").classed("fullview", true);

        //fetch the svg bounds
        this.svgBounds = divyearChart.node().getBoundingClientRect();
        this.svgWidth = this.svgBounds.width - this.margin.left - this.margin.right;
        this.svgHeight = 150;

        //add the svg to the div
        this.svg = divyearChart.append("svg")
            .attr("width", this.svgWidth)
            .attr("height", this.svgHeight)

        this.svg.append('g').attr('id', 'yearBrush')
        this.svg.append('g').classed('yearPoints', true)
        this.brushed = false;
    };

    /**
     * Returns the class that needs to be assigned to an element.
     *
     * @param party an ID for the party that is being referred to.
     */
    chooseClass (party) {
        if (party == "R") {
            return "yearChart republican";
        }
        else if (party == "D") {
            return "yearChart democrat";
        }
        else if (party == "I") {
            return "yearChart independent";
        }
    }

    /**
     * Creates a chart with circles representing each election year, populates text content and other required elements for the Year Chart
     */
    update () {
        let that = this;
        //Domain definition for global color scale
        let domain = [-60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60];

        //Color range for global color scale
        let range = ["#063e78", "#08519c", "#3182bd", "#6baed6", "#9ecae1", "#c6dbef", "#fcbba1", "#fc9272", "#fb6a4a", "#de2d26", "#a50f15", "#860308"];

        //ColorScale be used consistently by all the charts
        this.colorScale = d3.scaleQuantile()
            .domain(domain)
            .range(range);
        
        // ******* TODO: PART I *******
        // Create the chart by adding circle elements representing each election year

        let chartLine = d3.select('.fullview').select('svg').select('.yearPoints').append('line')
            .attr('x1', 0)
            .attr('y1', 20)
            .attr('x2',this.svgWidth)
            .attr('y2', 20)
            .attr('class', 'lineChart');

        let chart = d3.select('#year-chart').select('svg').select('.yearPoints').selectAll('g').data(this.electionWinners);
        let chartEnter = chart.enter().append('g')
            .attr('transform','translate(0,10)');

        chart.exit().remove()

        chart = chartEnter.merge(chart)

        let yearScale = d3.scaleLinear()
                        .domain([1940,2016])
                        .range([40,this.svgWidth - 40])

        let brush = d3.brushX().extent([[10,0], [this.svgWidth - 10, 40]]).on("brush end", brushed);
        this.svg.select('#yearBrush').call(brush);
        this.brushed = true;

        chart.append('circle')
            .attr('cx', d => yearScale(d.YEAR))
            .attr('cy', 10)
            .attr('r',8)
            .attr('class', d => this.chooseClass(d.PARTY))
            .on('mouseenter', function() {
                d3.select(this).classed('highlighted',true);
            })
            .on('mouseout', function() {
                d3.select(this).classed('highlighted',false);
            })
            .on('click', function(d) {
                d3.selectAll('circle').classed('selected',false);
                d3.select(this).classed('selected',true);


                //Call the update methods of electoralVotesChart, votePercentageChart, and tileChart
                d3.csv('data/Year_Timeline_' + d.YEAR + '.csv').then(electionResult => {
                    console.log('Triggered Update for year ' + d.YEAR);
                    console.log(electionResult);
                    that.electoralVoteChart.update(electionResult, that.colorScale);
                    that.tileChart.update(electionResult, that.colorScale);
                    that.votePercentageChart.update(electionResult);
                });
            });

        chart.append('text').classed('yeartext',true)
            .text(d => d.YEAR)
            .attr('x', d => yearScale(d.YEAR))
            .attr('y', 45)


        // The circles should be colored based on the winning party for that year
        // HINT: Use the .yearChart class to style your circle elements
        // HINT: Use the chooseClass method to choose the color corresponding to the winning party.

        // Append text information of each year right below the corresponding circle
        // HINT: Use .yeartext class to style your text elements
       
        // Style the chart by adding a dashed line that connects all these years.
        // HINT: Use .lineChart to style this dashed line
       
        // Clicking on any specific year should highlight that circle and  update the rest of the visualizations
        // HINT: Use .highlighted class to style the highlighted circle
       
        // Election information corresponding to that year should be loaded and passed to
        // the update methods of other visualizations

        // Note: you may want to initialize other visulaizations using some election from the get go, rather than waiting for a click (the reference solution uses 2012)











       //******* TODO: EXTRA CREDIT *******
       //Implement brush on the year chart created above.
       //Implement a call back method to handle the brush end event.
       //Call the update method of shiftChart and pass the data corresponding to brush selection.
       //HINT: Use the .brush class to style the brush.

       

       function brushed() {
        let s = d3.event.selection
        let years = Array.prototype.slice.call(d3.select(".yearPoints").selectAll('circle')._groups[0])
        
        years = years.filter(state => {
            let x = state.cx.baseVal.value
            let r = state.r.baseVal.value
            return (x >= s[0] && x < s[1]) ||
                    ((x+r) > s[0] && (x-r) <= s[1]) ||
                    ((x-r) <= s[0] && (x+r) >= s[1])
        })
        d3.select(".yearPoints").selectAll('circle').classed('highlighted', false)
        years.forEach(point => {
            point.className.baseVal += ' highlighted';
        });

        that.trendChart.updateActiveYears(years.map(a => a.__data__.YEAR));
       }

      






    };

};