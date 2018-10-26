/** Class implementing the tileChart. */
class TileChart {

    /**
     * Initializes the svg elements required to lay the tiles
     * and to populate the legend.
     */
    constructor(){
        // Follow the constructor method in yearChart.js
        // assign class 'content' in style.css to tile chart

        // Legend
        let legendHeight = 150;
        //add the svg to the div
        let legend = d3.select("#legend").classed("tile_view",true);

        this.margin = {top: 10, right: 20, bottom: 20, left: 50};

        // Initializes the svg elements required for this chart
        let tileChart = d3.select("#tiles").classed("content", true);

        //fetch the svg bounds
        this.svgBounds = tileChart.node().getBoundingClientRect();
        this.svgWidth = this.svgBounds.width - this.margin.left - this.margin.right;
        this.svgHeight = this.svgWidth * .5;

        //add the svg to the div
        this.svg = tileChart.append("svg")
            .attr("width", this.svgWidth)
            .attr("height", this.svgHeight)

        // creates svg elements within the div
        this.legendSvg = legend.append("svg")
                            .attr("width",this.svgWidth)
                            .attr("height",legendHeight)
                            .attr("transform", "translate(" + this.margin.left + ",0)");
        
        // Intialize tool-tip
        this.tip = d3.tip().attr('class', 'd3-tip')
            .direction('se')
            .offset(function() {
                return [0,0];
            })
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
        else if (party== "D"){
            return "democrat";
        }
        else if (party == "I"){
            return "independent";
        }
    }

    /**
     * Renders the HTML content for tool tip.
     *
     * @param tooltip_data information that needs to be populated in the tool tip
     * @return text HTML content for tool tip
     */
    tooltip_render(tooltip_data) {
        let text = "<h2 class ="  + this.chooseClass(tooltip_data.winner) + " >" + tooltip_data.state + "</h2>";
        text +=  "Electoral Votes: " + tooltip_data.electoralVotes;
        text += "<ul>"
        tooltip_data.result.forEach((row)=>{
            text += "<li class = " + this.chooseClass(row.party)+ ">" + row.nominee+":\t\t"+row.votecount+"\t("+row.percentage+"%)" + "</li>"
        });
        text += "</ul>";

        return text;
    }

    /**
     * Creates tiles and tool tip for each state, legend for encoding the color scale information.
     *
     * @param electionResult election data for the year selected
     * @param colorScale global quantile scale based on the winning margin between republicans and democrats
     */
    update (electionResult, colorScale){
        let that = this;
        //for reference:https://github.com/Caged/d3-tip
        //Use this tool tip element to handle any hover over the chart
            this.tip.html((d)=>{
                     //populate data in the following format
                     let tooltip_data = {
                        "state": d.State,
                        "winner": d.State_Winner,
                        "electoralVotes" : d.Total_EV,
                        "result":[
                                {"nominee": d.D_Nominee_prop,"votecount": d.D_Votes,"percentage": d.D_Percentage,"party":"D"} ,
                                {"nominee": d.R_Nominee_prop,"votecount": d.R_Votes,"percentage": d.R_Percentage,"party":"R"} ,
                                {"nominee": d.I_Nominee_prop,"votecount": d.I_Votes,"percentage": d.I_Percentage,"party":"I"}
                        ]
                     }
                     //pass this as an argument to the tooltip_render function then,
                     return that.tooltip_render(tooltip_data)
                    });

        this.svg.call(this.tip)
        // ******* TODO: PART IV *******
        // Transform the legend element to appear in the center 
        // make a call to this element for it to display.

        // Lay rectangles corresponding to each state according to the 'row' and 'column' information in the data.
        // column is coded as 'Space' in the data.

        // Display the state abbreviation and number of electoral votes on each of these rectangles

        // Use global color scale to color code the tiles.

        // HINT: Use .tile class to style your tiles;
        // .tilestext to style the text corresponding to tiles

        //Call the tool tip on hover over the tiles to display stateName, count of electoral votes
        //then, vote percentage and number of votes won by each party.
        //HINT: Use the .republican, .democrat and .independent classes to style your elements.
        //Creates a legend element and assigns a scale that needs to be visualized
        
        let legendQuantile = d3.legendColor()
            .shapeWidth((this.svgWidth - 2*this.margin.left - this.margin.right)/12)
            .cells(10)
            .orient('horizontal')
            .labelFormat(d3.format('.1r'))
            .scale(colorScale);

        this.legendSvg.append('g').call(legendQuantile);

        let xScale = d3.scaleLinear()
                        .domain([0,12])
                        .range([0,this.svgWidth]);
        let yScale = d3.scaleLinear()
                        .domain([0,8])
                        .range([0,this.svgHeight]);

        d3.select('#tiles').select('svg').selectAll('g').remove()               
        let chart = d3.select('#tiles').select('svg').selectAll('g').data(electionResult);
        let chartEnter = chart.enter().append('g')
        chart.exit().remove()
        chart = chartEnter.merge(chart)

        //Filter the split states from the non split ones

        //non split
        let nonSplitTile = chart.filter(d => {
            let test = [d.Total_EV, d.D_EV, d.R_EV, d.I_EV]
            return (test[1] == test[0] || test[2] == test[0] || test[3] == test[0])
        })
        nonSplitTile.append('rect').classed('tile',true)
            .attr('x', (d) => xScale(+d['Space']))
            .attr('y', (d) => yScale(+d['Row']))
            .attr('width', this.svgWidth/12)
            .attr('height', this.svgHeight/8)
            .attr('fill', d => colorScale(+d['RD_Difference']))
            .on('mouseenter', this.tip.show)
            .on('mouseleave', this.tip.hide)
        
        nonSplitTile.append('text').classed('tilestext',true)
            .text(d => d.Abbreviation)
            .attr('x', (d) => xScale(+d['Space'] + .5))
            .attr('y', (d) => yScale(+d['Row'] + .45))
            .attr('pointer-events','none');

        
        nonSplitTile.append('text').classed('tilestext',true)
            .text(d => d.Total_EV)
            .attr('x', (d) => xScale(+d['Space'] + .5))
            .attr('y', (d) => yScale(+d['Row'] + .75))
            .attr('pointer-events','none');


        
        //split
        let splitTile = chart.filter(d => {
            let test = [d.Total_EV, d.D_EV, d.R_EV, d.I_EV]
            return (test[1] != test[0] && test[2] != test[0] && test[3] != test[0])
        })
        splitTile.append('rect').classed('tile',true)
            .attr('x', (d) => xScale(+d['Space']))
            .attr('y', (d) => yScale(+d['Row']))
            .attr('width', d => (this.svgWidth/12) * (d.D_EV / d.Total_EV))
            .attr('height', this.svgHeight/8)
            .attr('fill', d => colorScale(-Math.abs(+d['RD_Difference'] * (d.D_EV / d.Total_EV))))
            .on('mouseenter', this.tip.show)
            .on('mouseleave', this.tip.hide);

        splitTile.append('rect').classed('tile',true)
            .attr('x', (d) => xScale(+d['Space'] + (d.D_EV / d.Total_EV)))
            .attr('y', (d) => yScale(+d['Row']))
            .attr('width', d => (this.svgWidth/12) * (d.R_EV / d.Total_EV))
            .attr('height', this.svgHeight/8)
            .attr('fill', d => colorScale(Math.abs(+d['RD_Difference'] * (d.R_EV / d.Total_EV))))
            .on('mouseenter', this.tip.show)
            .on('mouseleave', this.tip.hide);

        splitTile.append('rect').classed('tile independent',true)
            .attr('x', (d) => xScale(+d['Space']) + (d.D_EV / d.Total_EV) + (d.R_EV / d.Total_EV))
            .attr('y', (d) => yScale(+d['Row']))
            .attr('width', d => (this.svgWidth/12) * (d.I_EV / d.Total_EV))
            .attr('height', this.svgHeight/8)
            .on('mouseenter', this.tip.show)
            .on('mouseleave', this.tip.hide);
        
        splitTile.append('text').classed('tilestext',true)
            .text(d => d.Abbreviation)
            .attr('x', (d) => xScale(+d['Space'] + .5))
            .attr('y', (d) => yScale(+d['Row'] + .45))
            .attr('pointer-events','none');

        
        splitTile.append('text').classed('tilestext',true)
            .text(d => d.Total_EV)
            .attr('x', (d) => xScale(+d['Space'] + .5))
            .attr('y', (d) => yScale(+d['Row'] + .75))
            .attr('pointer-events','none');

            
    };


}