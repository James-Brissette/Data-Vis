/** Data structure for the data associated with an individual country. */
class PlotData {
    /**
     *
     * @param country country name from the x data object
     * @param xVal value from the data object chosen for x at the active year
     * @param yVal value from the data object chosen for y at the active year
     * @param id country id
     * @param region country region
     * @param circleSize value for r from data object chosen for circleSizeIndicator
     */
    constructor(country, xVal, yVal, id, region, circleSize) {
        this.country = country;
        this.xVal = xVal;
        this.yVal = yVal;
        this.id = id;
        this.region = region;
        this.circleSize = circleSize;
    }
}

/** Class representing the scatter plot view. */
class GapPlot {

    /**
     * Creates an new GapPlot Object
     *
     * For part 2 of the homework, you only need to worry about the first parameter.
     * You will be updating the plot with the data in updatePlot,
     * but first you need to draw the plot structure that you will be updating.
     *
     * Set the data as a variable that will be accessible to you in updatePlot()
     * Call the drawplot() function after you set it up to draw the plot structure on GapPlot load
     *
     * We have provided the dimensions for you!
     *
     * @param updateCountry a callback function used to notify other parts of the program when the selected
     * country was updated (clicked)
     * @param updateYear a callback function used to notify other parts of the program when a year was updated
     * @param activeYear the year for which the data should be drawn initially
     */
    constructor(data, updateCountry, updateYear, activeYear) {

        // ******* TODO: PART 2 *******

        this.margin = { top: 20, right: 20, bottom: 60, left: 80 };
        this.width = 810 - this.margin.left - this.margin.right;
        this.height = 500 - this.margin.top - this.margin.bottom;
        this.activeYear = activeYear;

        this.data = data;
        this.countries = data["life-expectancy"].map(a => a.country);
        this.indicators = [];
        //TODO - Your code goes here - 
        
        this.drawPlot();
        this.updateYear = updateYear;
        this.activeCountry = 0;
        
        // ******* TODO: PART 3 *******
        /**
         For part 4 of the homework, you will be using the other 3 parameters.
         * assign the highlightUpdate function as a variable that will be accessible to you in updatePlot()
         * assign the dragUpdate function as a variable that will be accessible to you in updatePlot()
         */


        //TODO - Your code goes here - 

    }

    /**
     * Sets up the plot, axes, and slider,
     */

    drawPlot() {
        // ******* TODO: PART 2 *******
        /**
         You will be setting up the plot for the scatterplot.
         Here you will create axes for the x and y data that you will be selecting and calling in updatePlot
         (hint): class them.

         Main things you should set up here:
         1). Create the x and y axes
         2). Create the activeYear background text


        //TODO - Your code goes here - 
        

         The dropdown menus have been created for you!

         */

         let xScale = d3.scaleLinear()
            .domain([0,1000])
            .range([0,this.width])
            .nice();

        let yScale = d3.scaleLinear()
            .domain([1000,0])
            .range([0,this.height])
            .nice();

            
        let xmargin = 35;
        let ymargin = 10;
        
        let xAxis = d3.axisBottom().scale(xScale);
        let yAxis = d3.axisLeft().scale(yScale);


        d3.select('#scatter-plot')
            .append('div').attr('id', 'chart-view');

        d3.select('#scatter-plot')
            .append('div').attr('id', 'activeYear-bar');

        d3.select('#chart-view')
            .append('div')
            .attr("class", "tooltip")
            .style("opacity", 0);

        d3.select('#chart-view')
            .append('svg').classed('plot-svg', true)
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom);

        let svgGroup = d3.select('#chart-view').select('.plot-svg').append('g').classed('wrapper-group', true);
        svgGroup.append('g').classed('background-text', true).append('text')
            .text(this.activeYear)
            .attr('x',this.width / 5)
            .attr('y',this.height / 3)
            .attr('font-size',90)
            .attr('fill', '#999999');
        svgGroup.append('g').classed('y axis', true)
            .attr('transform','translate(' + xmargin + ',' + ymargin + ')')
            .call(yAxis);
        svgGroup.append('g').classed('x axis', true)
            .attr('transform','translate(' + xmargin + ',' + (this.height + ymargin) + ')')
            .call(xAxis.tickFormat(d3.format('.3s')));
        svgGroup.append('g').classed('circles', true)
            .attr('transform','translate(' + (xmargin + 10) + ',' + (ymargin) + ') scale(1,1)');
        
        this.drawYearBar();

        /* This is the setup for the dropdown menu- no need to change this */

        let dropdownWrap = d3.select('#chart-view').append('div').classed('dropdown-wrapper', true);

        let cWrap = dropdownWrap.append('div').classed('dropdown-panel', true);

        cWrap.append('div').classed('c-label', true)
            .append('text')
            .text('Circle Size');

        cWrap.append('div').attr('id', 'dropdown_c').classed('dropdown', true).append('div').classed('dropdown-content', true)
            .append('select');

        let xWrap = dropdownWrap.append('div').classed('dropdown-panel', true);

        xWrap.append('div').classed('x-label', true)
            .append('text')
            .text('X Axis Data');

        xWrap.append('div').attr('id', 'dropdown_x').classed('dropdown', true).append('div').classed('dropdown-content', true)
            .append('select');

        let yWrap = dropdownWrap.append('div').classed('dropdown-panel', true);

        yWrap.append('div').classed('y-label', true)
            .append('text')
            .text('Y Axis Data');

        yWrap.append('div').attr('id', 'dropdown_y').classed('dropdown', true).append('div').classed('dropdown-content', true)
            .append('select');

        d3.select('#chart-view')
            .append('div')
            .classed('circle-legend', true)
            .append('svg')
            .append('g')
            .attr('transform', 'translate(10, 0)');
    }

    /**
     * Renders the plot for the parameters specified
     *
     * @param activeYear the year for which to render
     * @param xIndicator identifies the values to use for the x axis
     * @param yIndicator identifies the values to use for the y axis
     * @param circleSizeIndicator identifies the values to use for the circle size
     */
    updatePlot(activeYear, xIndicator, yIndicator, circleSizeIndicator) {
        
        // ******* TODO: PART 2 *******

        /*
        You will be updating the scatterplot from the data. hint: use the #chart-view div

        *** Structuring your PlotData objects ***
        You need to start by mapping the data specified by the parameters to the PlotData Object
        Your PlotData object is specified at the top of the file
        You will need get the data specified by the x, y and circle size parameters from the data passed
        to the GapPlot constructor

        *** Setting the scales for your x, y, and circle data ***
        For x and y data, you should get the overall max of the whole data set for that data category,
        not just for the activeYear.

        ***draw circles***
        draw the circles with a scaled area from the circle data, with cx from your x data and cy from y data
        You need to size the circles from your circleSize data, we have provided a function for you to do this
        called circleSizer. Use this when you assign the 'r' attribute.

        ***Tooltip for the bubbles***
        You need to assign a tooltip to appear on mouse-over of a country bubble to show the name of the country.
        We have provided the mouse-over for you, but you have to set it up
        Hint: you will need to call the tooltipRender function for this.

        *** call the drawLegend() and drawDropDown()
        These will draw the legend and the drop down menus in your data
        Pay attention to the parameters needed in each of the functions
        
        */
        this.indicators = [xIndicator, yIndicator, circleSizeIndicator];
        
        let ind = [];
        let counter = 0;
        let data_keys = Object.keys(this.data);
        let data = this.data;

        data_keys.map(a => new Set(this.data[a].map(b => b.indicator))).forEach(function(e) {
            ind[Array.from(e)[0]] = data_keys[counter];
            ++counter;
        })
        console.log(ind);

        let plot_data = [];
        this.countries.forEach(function(c) {
            
            let xidx = data[ind[xIndicator]].map(a => a.country).indexOf(c);
            
            let yidx = data[ind[yIndicator]].map(a => a.country).indexOf(c);
            let cidx = data[ind[circleSizeIndicator]].map(a => a.country).indexOf(c);

            let id = data['life-expectancy'].map(a => a.geo)[data['life-expectancy'].map(a => a.country).indexOf(c)];
            let region = data['population'].map(a => a.region)[data['population'].map(a => a.country).indexOf(c)];
            let xVal = (xidx === -1) ? 0 : data[ind[xIndicator]][xidx][activeYear];
            let yVal = (yidx === -1) ? 0 : data[ind[yIndicator]][yidx][activeYear];
            let circleSize = (cidx === -1) ? 0 : data[ind[circleSizeIndicator]][cidx][activeYear];
            
            plot_data[c] = new PlotData(c, xVal, yVal, id, region, circleSize);
        });

        
        let xmargin = 45;
        let ymargin = 10;

        //Determines the appropriate scale for the X and Y axes
        let xMax = 0;
        this.data[ind[xIndicator]].forEach(function(e) {
            for (let i = 1800; i<=2020; i++) {
                xMax = Math.max(xMax, e[i]);
            }
        });
        let xScale = d3.scaleLinear()
            .domain([0,xMax])
            .range([0,this.width])
            .nice();
        d3.select('.x.axis')
            .attr('transform','translate(' + xmargin + ',' + (this.height + ymargin) + ')')
            .call(d3.axisBottom().scale(xScale)); 
        
        let yMax = 0;
        this.data[ind[yIndicator]].forEach(function(e) {
            for (let i = 1800; i<=2020; i++) {
                yMax = Math.max(yMax, e[i]);
            }
        });
        let yScale = d3.scaleLinear()
            .domain([yMax,0])
            .range([0,this.height])
            .nice();
        d3.select('.y.axis')
            .attr('transform','translate(' + xmargin + ',' + ymargin + ')')
            .call(d3.axisLeft().scale(yScale).tickFormat(d3.format('.3s')));

        //Calculate the min and max circle size for the circle sizer function
        let minSize = 10000000;
        this.data[ind[circleSizeIndicator]].forEach(function(e) {
            for (let i = 1800; i<=2020; i++) {
                minSize = Math.min(minSize, e[i]);
            }
        });
        let maxSize = 0;
        this.data[ind[circleSizeIndicator]].forEach(function(e) {
            for (let i = 1800; i<=2020; i++) {
                maxSize = Math.max(maxSize, e[i]);
            }
        });

        //Update the plot activeYear text
        d3.select(".background-text").select('text').text(activeYear);


        /**
         *  Function to determine the circle radius by circle size
         *  This is the function to size your circles, you don't need to do anything to this
         *  but you will call it and pass the circle data as the parameter.
         * 
         * @param d the data value to encode
         * @returns {number} the radius
         */
        let circleSizer = function(d) {
            let cScale = d3.scaleSqrt().range([3, 20]).domain([minSize, maxSize]);
            return d.circleSize ? cScale(d.circleSize) : 3;
        };

        let circles = d3.select('.circles').selectAll('circle')
            .data(Object.values(plot_data));
        let circlesEnter = circles.enter().append('circle');
        circles.exit().remove();
        circles = circlesEnter.merge(circles);
    
        let thisGapPlot = this;
        circles
            .attr('cx', d => xScale(d.xVal))
            .attr('cy', d => yScale(d.yVal))
            .attr('r', d => circleSizer(d))
            .attr('class', d => 
                d.id.toLowerCase() === thisGapPlot.activeCountry[0] ? 
                d.region + ' selected-country' : 
                d.region === thisGapPlot.activeCountry[1] ? d.region : 
                thisGapPlot.activeCountry === 0 ? d.region : d.region + ' hidden')
            .attr('id', d => d.id)
            .on('mouseenter', d => {
                d3.select('.tooltip')
                .style('opacity',1)
                .style('background', 'none').append('div').classed('tooltip', true)
                .style('left', (xScale(d.xVal)-30) +'px')
                .style('top', (yScale(d.yVal)-30) +'px')
                .style('border','1px solid grey')
                .html(thisGapPlot.tooltipRender(d));
            })
           .on('mouseleave', function(d,i) {
                d3.select('.tooltip').style('opacity',0).selectAll('.tooltip').remove();
           });

        this.drawDropDown(circleSizeIndicator, xIndicator, yIndicator);
        this.drawLegend(minSize,maxSize);
    }

    /**
     * Setting up the drop-downs
     * @param sizeData data used to size the circles
     * @param xData data used for x attribute
     * @param yData data used for y attribute
     */
    drawDropDown(sizeData, xData, yData) {

        let that = this;
        let dropDownWrapper = d3.select('.dropdown-wrapper');
        let dropData = [];

        for (let key in this.data) {
            dropData.push({
                indicator: this.data[key][0].indicator,
                indicator_name: this.data[key][0].indicator_name
            });
        }

        /* CIRCLE DROPDOWN */
        let dropC = dropDownWrapper.select('#dropdown_c').select('.dropdown-content').select('select');

        let optionsC = dropC.selectAll('option')
            .data(dropData);


        optionsC.exit().remove();

        let optionsCEnter = optionsC.enter()
            .append('option')
            .attr('value', (d, i) => d.indicator);

        optionsCEnter.append('text')
            .text((d, i) => d.indicator_name);

        optionsC = optionsCEnter.merge(optionsC);

        let selectedC = optionsC.filter(d => d.indicator === sizeData[0].indicator)
            .attr('selected', true);

        dropC.on('change', function(d, i) {
            let cValue = this.options[this.selectedIndex].value;
            let xValue = dropX.node().value;
            let yValue = dropY.node().value;
            that.updatePlot(that.activeYear, xValue, yValue, cValue);
        });

        /* X DROPDOWN */
        let dropX = dropDownWrapper.select('#dropdown_x').select('.dropdown-content').select('select');

        let optionsX = dropX.selectAll('option')
            .data(dropData);

        optionsX.exit().remove();

        let optionsXEnter = optionsX.enter()
            .append('option')
            .attr('value', (d, i) => d.indicator);

        optionsXEnter.append('text')
            .text((d, i) => d.indicator_name);

        optionsX = optionsXEnter.merge(optionsX);

        let selectedX = optionsX.filter(d => d.indicator === xData[0].indicator)
            .attr('selected', true);

        dropX.on('change', function(d, i) {
            let xValue = this.options[this.selectedIndex].value;
            let yValue = dropY.node().value;
            let cValue = dropC.node().value;
            that.updatePlot(that.activeYear, xValue, yValue, cValue);
        });

        /* Y DROPDOWN */
        let dropY = dropDownWrapper.select('#dropdown_y').select('.dropdown-content').select('select');

        let optionsY = dropY.selectAll('option')
            .data(dropData);

        optionsY.exit().remove();

        let optionsYEnter = optionsY.enter()
            .append('option')
            .attr('value', (d, i) => d.indicator);

        optionsY = optionsYEnter.merge(optionsY);

        optionsYEnter.append('text')
            .text((d, i) => d.indicator_name);

        let selectedY = optionsY.filter(d => d.indicator === yData[0].indicator)
            .attr('selected', true);

        dropY.on('change', function(d, i) {
            let yValue = this.options[this.selectedIndex].value;
            let xValue = dropX.node().value;
            let cValue = dropC.node().value;
            that.updatePlot(that.activeYear, xValue, yValue, cValue);
        });

    }

    /**
     * Draws the year bar and hooks up the events of a year change
     */
    drawYearBar() {

        // ******* TODO: PART 2 *******
        //The drop-down boxes are set up for you, but you have to set the slider to updatePlot() on activeYear change

        // Create the x scale for the activeYear;
        // hint: the domain should be max and min of the years (1800 - 2020); it's OK to set it as numbers
        // the plot needs to update on move of the slider

        /* ******* TODO: PART 3 *******
        You will need to call the updateYear() function passed from script.js in your activeYear slider
        */
        let that = this;

        //TODO - Your code goes here - 
        
        let xScale = d3.scaleLinear().domain([1800, 2020]).range([0,1]);
        let colorScale = d3.scaleLinear().domain([1800,1900, 2000,2020]).range(['red','blue','black','orange']);

        //Slider to change the activeYear of the data
        let yearScale = d3.scaleLinear().domain([1800, 2020]).range([30, 730]);

        let yearSlider = d3.select('#activeYear-bar')
            .append('div').classed('slider-wrap', true)
            .append('input').classed('slider', true)
            .attr('type', 'range')
            .attr('min', 1800)
            .attr('max', 2020)
            .attr('value', this.activeYear)

        let sliderLabel = d3.select('.slider-wrap')
            .append('div').classed('slider-label', true)
            .append('svg');

        let sliderText = sliderLabel.append('text').text(this.activeYear);

        sliderText.attr('x', yearScale(this.activeYear));
        sliderText.attr('y', 25);

        let slider = d3.select('.slider').node()
        yearSlider.on('input', function() {
            that.updateYear(slider.value);
            sliderText.attr('x', yearScale(slider.value));
            sliderText.text(slider.value);
            d3.selectAll('.info').style('color',colorScale(slider.value));
        });

    }

    /**
     * Draws the legend for the circle sizes
     *
     * @param min minimum value for the sizeData
     * @param max maximum value for the sizeData
     */
    drawLegend(min, max) {
        // ******* TODO: PART 2*******
        //This has been done for you but you need to call it in updatePlot()!
        //Draws the circle legend to show size based on health data
        let scale = d3.scaleSqrt().range([3, 20]).domain([min, max]);

        let circleData = [min, max];

        let svg = d3.select('.circle-legend').select('svg').select('g');

        let circleGroup = svg.selectAll('g').data(circleData);
        circleGroup.exit().remove();

        let circleEnter = circleGroup.enter().append('g');
        circleEnter.append('circle').classed('neutral', true);
        circleEnter.append('text').classed('circle-size-text', true);

        circleGroup = circleEnter.merge(circleGroup);

        circleGroup.attr('transform', (d, i) => 'translate(' + ((i * (5 * scale(d))) + 20) + ', 25)');

        circleGroup.select('circle').attr('r', (d) => scale(d));
        circleGroup.select('circle').attr('cx', '0');
        circleGroup.select('circle').attr('cy', '0');
        let numText = circleGroup.select('text').text(d => new Intl.NumberFormat().format(d));

        numText.attr('transform', (d) => 'translate(' + ((scale(d)) + 10) + ', 0)');
    }

    /**
     * Reacts to a highlight/click event for a country; draws that country darker
     * and fades countries on other continents out
     * @param activeCountry
     */
    updateHighlightClick(activeCountry) {
        /* ******* TODO: PART 3*******
        //You need to assign selected class to the target country and corresponding region
        // Hint: If you followed our suggestion of using classes to style
        // the colors and markers for countries/regions, you can use
        // d3 selection and .classed to set these classes on here.
        // You will not be calling this directly in the gapPlot class,
        // you will need to call it from the updateHighlight function in script.js
        */

        let activeClass = d3.select('circle#' + activeCountry).attr('class').split(' ')[0];
        d3.select('#chart-view').selectAll('circle').classed('hidden',true);
        d3.select('#chart-view').selectAll('circle.' + activeClass).classed('hidden',false);
        d3.select('#chart-view').selectAll('circle.neutral').classed('hidden',false);

    }

    /**
     * Clears any highlights
     */
    clearHighlight() {
        // ******* TODO: PART 3*******
        // Clear the map of any colors/markers; You can do this with inline styling or by
        // defining a class style in styles.css

        // Hint: If you followed our suggestion of using classes to style
        // the colors and markers for hosts/teams/winners, you can use
        // d3 selection and .classed to set these classes off here.

        d3.select('#chart-view').selectAll('circle').classed('hidden',false)
    }

    /**
     * Returns html that can be used to render the tooltip.
     * @param data 
     * @returns {string}
     */
    tooltipRender(data) {
        let text = "<h2>" + data['country'] + "</h2>";
        return text;
    }

}