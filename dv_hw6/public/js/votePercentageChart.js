/** Class implementing the votePercentageChart. */
class VotePercentageChart {

    /**
     * Initializes the svg elements required for this chart;
     */
    constructor(){
		// Follow the constructor method in yearChart.js
		// assign class 'content' in style.css to vote percentage chart
        
        // Initializes the svg elements required for this chart
        this.margin = {top: 10, right: 20, bottom: 20, left: 50};
        let divVotePercentageChart = d3.select("#votes-percentage").classed("fullview", true);

        //fetch the svg bounds
        this.svgBounds = divVotePercentageChart.node().getBoundingClientRect();
        this.svgWidth = this.svgBounds.width - this.margin.left - this.margin.right;
        this.svgHeight = 180;

        //add the svg to the div
        this.svg = divVotePercentageChart.append("svg")
            .attr("width", this.svgWidth)
            .attr("height", this.svgHeight)
       
		let d = this.svg.append('g').classed('d-chart',true)
		d.append('text').attr('id','d-percent')
		d.append('text').attr('id','d-candidate')
			
        let r = this.svg.append('g').classed('r-chart',true)
		r.append('text').attr('id','r-percent')
		r.append('text').attr('id','r-candidate')

		let i = this.svg.append('g').classed('i-chart',true)
		i.append('text').attr('id','i-percent')
		i.append('text').attr('id','i-candidate')

        this.svg.append('text').attr('id','popVotesToWinText')
        this.svg.append('line').attr('id','popVotesToWinLine')


		//for reference: https://github.com/Caged/d3-tip
		//Use this tool tip element to handle any hover over the chart
		this.tip = d3.tip().attr('class', 'd3-tip')
			.direction('s')
			.offset(function() {
				return [0,0];
			});
    }


	/**
	 * Returns the class that needs to be assigned to an element.
	 *
	 * @param party an ID for the party that is being referred to.
	 */
	chooseClass(data) {
	    if (data == "R"){
	        return "republican";
	    }
	    else if (data == "D"){
	        return "democrat";
	    }
	    else if (data == "I"){
	        return "independent";
	    }
	}

	/**
	 * Renders the HTML content for tool tip
	 *
	 * @param tooltip_data information that needs to be populated in the tool tip
	 * @return text HTML content for toop tip
	 */
	tooltip_render (tooltip_data) {
	    let text = "<ul>";
	    tooltip_data.result.forEach((row)=>{
			text += "<li class = " + this.chooseClass(row.party)+ ">" 
				 + row.nominee+":\t\t"+row.votecount+"\t("+row.percentage+")" + 
				 "</li>"
	    });
	    return text;
	}

	/**
	 * Creates the stacked bar chart, text content and tool tips for Vote Percentage chart
	 *
	 * @param electionResult election data for the year selected
	 */
	update (electionResult){

			this.tip.html((d)=> {
	                /* populate data in the following format
	                 * tooltip_data = {
	                 * "result":[
	                 * {"nominee": D_Nominee_prop,"votecount": D_Votes_Total,"percentage": D_PopularPercentage,"party":"D"} ,
	                 * {"nominee": R_Nominee_prop,"votecount": R_Votes_Total,"percentage": R_PopularPercentage,"party":"R"} ,
	                 * {"nominee": I_Nominee_prop,"votecount": I_Votes_Total,"percentage": I_PopularPercentage,"party":"I"}
	                 * ]
	                 * }
	                 * pass this as an argument to the tooltip_render function then,
	                 * return the HTML content returned from that method.
	                 * */








	            });

   			  // ******* TODO: PART III *******

		    //Create the bar chart.
		    //Use the global color scale to color code the rectangles.
		    //HINT: Use .votesPercentage class to style your bars.

		    //Display the total percentage of votes won by each party
		    //on top of the corresponding groups of bars.
		    //HINT: Use the .votesPercentageText class to style your text elements;  Use this in combination with
		    // chooseClass to get a color based on the party wherever necessary

		    //Display a bar with minimal width in the center of the bar chart to indicate the 50% mark
		    //HINT: Use .middlePoint class to style this bar.

		    //Just above this, display the text mentioning details about this mark on top of this bar
		    //HINT: Use .votesPercentageNote class to style this text element

		    //Call the tool tip on hover over the bars to display stateName, count of electoral votes.
		    //then, vote percentage and number of votes won by each party.

			//HINT: Use the chooseClass method to style your elements based on party wherever necessary.















			
	};


}