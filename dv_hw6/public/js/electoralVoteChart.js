class ElectoralVoteChart {
    /**
     * Constructor for the ElectoralVoteChart
     *
     * @param trendChart an instance of the ShiftChart class
     */
    constructor (trendChart){

        // Follow the constructor method in yearChart.js
        // assign class 'content' in style.css to electoral-vote chart

        //Creating YearChart instance
        this.trendChart = trendChart;
        // the data
        
        // Initializes the svg elements required for this chart
        this.margin = {top: 10, right: 20, bottom: 20, left: 50};
        let divVoteChart = d3.select("#electoral-vote").classed("sub_content", true);

        //fetch the svg bounds
        this.svgBounds = divVoteChart.node().getBoundingClientRect();
        this.svgWidth = this.svgBounds.width - this.margin.left - this.margin.right;
        this.svgHeight = 180;

        //add the svg to the div
        this.svg = divVoteChart.append("svg")
            .attr("width", this.svgWidth)
            .attr("height", this.svgHeight)
       
        this.svg.append('g').classed('d-chart',true).append('text')
        this.svg.append('g').classed('brush',true).attr('id','d-brush');
        this.svg.append('g').classed('r-chart',true).append('text')
        this.svg.append('g').classed('brush',true).attr('id','r-brush');
        this.svg.append('g').classed('i-chart',true).append('text')
        this.svg.append('g').classed('brush',true).attr('id','i-brush');
        this.svg.append('text').attr('id','votesToWinText')
        this.svg.append('line').attr('id','votesToWinLine')

        this.d_brushed = false;
        this.r_brushed = false;
        this.i_brushed = false;
    };

    /**
     * Returns the class that needs to be assigned to an element.
     *
     * @param party an ID for the party that is being referred to.
     */
    chooseClass (party) {
        if (party == "R"){
            return "republican";
        }
        else if (party == "D"){
            return "democrat";
        }
        else if (party == "I"){
            return "independent";
        }
    }

    /**
     * Creates the stacked bar chart, text content and tool tips for electoral vote chart
     *
     * @param electionResult election data for the year selected
     * @param colorScale global quantile scale based on the winning margin between republicans and democrats
     */

   update (electionResult, colorScale){
       
       // ******* TODO: PART II *******
       // Group the states based on the winning party for the state;
       // then sort them based on the margin of victory
       
       // Create the stacked bar chart.
       let that = this;
        let barHeight = 20;
        let buffer = 25;

        
        let i_data = electionResult.filter(item => item.RD_Difference == 0)
        let d_data = electionResult.filter(item => item.RD_Difference < 0).sort(function(a,b){return +a.RD_Difference - +b.RD_Difference})
        let r_data = electionResult.filter(item => item.RD_Difference > 0).sort(function(a,b){return +b.RD_Difference - +a.RD_Difference})
        

        function reduce_sum(a,b) {
            return +a + +b;
        }

        let D_EV = d_data.map(a => a.D_EV).reduce(reduce_sum)
        let R_EV = r_data.map(a => a.R_EV).reduce(reduce_sum)
        console.log(D_EV)
        let I_EV = i_data.map(a => a.I_EV).length == 0 ? 0 : i_data.map(a => a.I_EV).reduce(reduce_sum)

        let voteScale = d3.scaleLinear()
                            .domain([0,Math.max(R_EV,D_EV)])
                            .range([0,this.svgWidth - 100])

        let d_brush = d3.brushX().extent([[0,25], [voteScale(+D_EV), 45  + barHeight]]).on("brush end", d_brushed);
        let r_brush = d3.brushX().extent([[0,80], [voteScale(+R_EV), 100  + barHeight]]).on("brush end", r_brushed);
        let i_brush = d3.brushX().extent([[0,135],[voteScale(+I_EV), 155 + barHeight]]).on("brush end", i_brushed);
        
        console.log(r_data.map(a => a.R_EV).reduce(reduce_sum),d_data.map(a => a.D_EV).reduce(reduce_sum))

        let chart = d3.select('#electoral-vote').select('svg')

        //Removes brushing on yearChange provided the brushes have been initialized at least once
        if (this.d_brushed) {
            d3.select('#d-brush').call(d_brush.move,null);
        }
        if (this.r_brushed) {
            d3.select('#r-brush').call(r_brush.move,null);
        }
        if (this.i_brushed) {
            d3.select('#i-brush').call(i_brush.move,null);
        }

        //Democrat
        let d_chart = chart.select('.d-chart').selectAll('rect').data(d_data);
        let d_chartEnter = d_chart.enter().append('rect');
        d_chart.exit().remove();

        d_chart = d_chartEnter.merge(d_chart);
        d_chart
            .attr('y', this.margin.top + buffer)
            .attr('x', (d,i) => i - 1 == -1 ? 0 : d3.select(d_chart.nodes()[i-1])._groups['0']['0'].x.baseVal.value + voteScale(d3.select(d_chart.nodes()[i-1])._groups['0']['0'].__data__.D_EV))
            .attr('width', d => voteScale(d.D_EV))
            .attr('height',barHeight)
            .attr('fill', d => colorScale(d.RD_Difference))
            .attr('class','electoralVotes')

        chart.select('.d-chart').select('text')
            .text(D_EV)
            .attr('x', 0)
            .attr('y', 30)
            .attr('class','electoralVoteText democrat')
        chart.select('#d-brush').call(d_brush)
        this.d_brushed = true;

        //Republican
        let r_chart = chart.select('.r-chart').selectAll('rect').data(r_data);
        let r_chartEnter = r_chart.enter().append('rect');
        r_chart.exit().remove();
        r_chart = r_chartEnter.merge(r_chart);
        console.log('r_chart:')
        console.log(electionResult.filter(item => item.RD_Difference > 0).sort(function(a,b){return +b.RD_Difference - +a.RD_Difference}))
        r_chart
            .attr('y', 90)
            .attr('x', (d,i) => i - 1 == -1 ? 0 : d3.select(r_chart.nodes()[i-1])._groups['0']['0'].x.baseVal.value + voteScale(d3.select(r_chart.nodes()[i-1])._groups['0']['0'].__data__.R_EV))
            .attr('width', d => voteScale(d.R_EV))
            .attr('height',barHeight)
            .attr('fill', d => colorScale(d.RD_Difference))
            .attr('class','electoralVotes');

        chart.select('.r-chart').select('text')
            .text(R_EV)
            .attr('x', 0)
            .attr('y', 85)
            .attr('class','electoralVoteText republican');
        chart.select('#r-brush').call(r_brush);
        this.r_brushed = true;


        //Independent
        if (I_EV > 0) {

            let i_chart = chart.select('.i-chart').selectAll('rect').data(i_data);
            let i_chartEnter = i_chart.enter().append('rect');
            i_chart.exit().remove();
        
            i_chart = i_chartEnter.merge(i_chart);
            i_chart
                .attr('y', 145)
                .attr('x', (d,i) => i - 1 == -1 ? 0 : d3.select(i_chart.nodes()[i-1])._groups['0']['0'].x.baseVal.value + voteScale(d3.select(i_chart.nodes()[i-1])._groups['0']['0'].__data__.I_EV))
                .attr('width', d => voteScale(d.I_EV))
                .attr('height',barHeight)
                .attr('class','electoralVotes independent');

            chart.select('.i-chart').select('text')
                .text(I_EV)
                .attr('x', 0)
                .attr('y', 140)
                .attr('class','electoralVoteText independent');
            chart.select('#i-brush').call(i_brush);
            this.i_brushed = true;
        } else {
            chart.select('.i-chart').select('text')
                .text('')
            chart.select('.i-chart').selectAll('rect').remove()
        }


        d3.select('#votesToWinText')
            .attr('text-anchor','middle')
            .attr('x', voteScale(270))
            .attr('y', 20)
            .text('270 needed to win')

        d3.select('#votesToWinLine')
            .attr('x1', voteScale(270))
            .attr('y1', 25)
            .attr('x2', voteScale(270))
            .attr('y2', 130)
            .attr('stroke','black')
            .attr('stroke-width',2)
                            

       // Use the global color scale to color code the rectangles for Democrates and Republican.
       // Use #089c43 to color Independent party.
       // HINT: Use .electoralVotes class to style your bars.

       // Display total count of electoral votes won by the Democrat, Republican and Independent party(if there's candidate).
       // on top of the corresponding groups of bars.
       // HINT: Use the .electoralVoteText class to style your text elements; Use this in combination with
       // Use chooseClass method to get a color based on the party wherever necessary
       
       // Display a bar with minimal width in the center of the bar chart to indicate the 50% mark
       // HINT: Use .middlePoint class to style this bar.
       
       // Just above this, display the text mentioning the total number of electoral votes required
       // to win the elections throughout the country
       // HINT: Use .electoralVotesNote class to style this text element
       // HINT: Use the chooseClass method to style your elements based on party wherever necessary.










       //******* TODO: PART V *******
       
       //Implement brush on the bar chart created above.
       //Implement a call back method to handle the brush end event.
       //Call the update method of shiftChart and pass the data corresponding to brush selection.
       //HINT: Use the .brush class to style the brush.

       function d_brushed() {
        let s = d3.event.selection;
        console.log(s);
        if (s === null) {
            that.trendChart.update([null, 'd']);
            return;
        }
        let states = Array.prototype.slice.call(d3.select(".d-chart").selectAll('rect')._groups[0])
        
        states = states.filter(state => {
            let x = state.x.baseVal.value
            let width = state.width.baseVal.value
            return (x >= s[0] && x < s[1]) ||
                    (x + width > s[0] && x <= s[1]) ||
                    (x <= s[0] && x + width >= s[1])
        })
        
        let d = []
        states.forEach(state => {
            d.push({'name': state.__data__.State,'party':'d', 'Abbreviation':state.__data__.Abbreviation})
        });
        console.log(d);
        that.trendChart.update(d)
    }

    function r_brushed() {
        let s = d3.event.selection;
        if (s === null) {
            that.trendChart.update([null, 'r']);
            return;
        }
        let states = Array.prototype.slice.call(d3.select(".r-chart").selectAll('rect')._groups[0])
        
        states = states.filter(state => {
            let x = state.x.baseVal.value
            let width = state.width.baseVal.value
            return (x >= s[0] && x < s[1]) ||
                    (x + width > s[0] && x <= s[1]) ||
                    (x <= s[0] && x + width >= s[1])
        })
        
        let d = []
        states.forEach(state => {
            d.push({'name': state.__data__.State,'party':'r', 'Abbreviation':state.__data__.Abbreviation})
        });
        console.log(d);
        that.trendChart.update(d)
    }

    function i_brushed() {
        let s = d3.event.selection;
        if (s === null) {
            that.trendChart.update([null, 'i']);
            return;
        }
        let states = Array.prototype.slice.call(d3.select(".i-chart").selectAll('rect')._groups[0])
        states = states.filter(state => {
            let x = state.x.baseVal.value
            let width = state.width.baseVal.value
            return (x >= s[0] && x < s[1]) ||
                    (x + width > s[0] && x <= s[1]) ||
                    (x <= s[0] && x + width >= s[1])
        })
        
        let d =[]
        states.forEach(state => {
            d.push({'name': state.__data__.State,'party':'i', 'Abbreviation':state.__data__.Abbreviation})
        });
        console.log(d);
        that.trendChart.update(d)
    }









    };

    
}