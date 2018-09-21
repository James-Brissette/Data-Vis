/** Data structure for the data associated with an individual country. */
class InfoBoxData {
    /**
     *
     * @param country name of the active country
     * @param region region of the active country
     * @param indicator_name the label name from the data category
     * @param value the number value from the active year
     */
    constructor(country, region, indicator_name, value) {
        this.country = country;
        this.region = region;
        this.indicator_name = indicator_name;
        this.value = value;
    }
}

/** Class representing the highlighting and selection interactivity. */
class InfoBox {
    /**
     * Creates a InfoBox Object
     * @param data the full data array
     */
    constructor(data) {
        this.data = data;
        this.countries = data["life-expectancy"].map(a => a.country);
        d3.select('#country-detail').append('g').classed('info-box', true);
    }

    /**
     * Renders the country description
     * @param activeCountry the IDs for the active country
     * @param activeYear the year to render the data for
     */
    updateTextDescription(activeCountry, activeYear) {
        // ******* TODO: PART 4 *******
        // Update the text elements in the infoBox to reflect:
        // Selected country, region, population and stats associated with the country.
        /*
         * You will need to get an array of the values for each category in your data object
         * hint: you can do this by using Object.values(this.data)
         * you will then need to filter just the activeCountry data from each array
         * you will then pass the data as paramters to make an InfoBoxData object for each category
         *
         */

        //TODO - Your code goes here - 
        let countryData = []
        this.countries.forEach(function(c) {
            let idx = data[ind[xIndicator]].map(a => a.country).indexOf(c);

            let id = data['life-expectancy'].map(a => a.geo)[data['life-expectancy'].map(a => a.country).indexOf(c)];
            let region = data['population'].map(a => a.region)[data['population'].map(a => a.country).indexOf(c)];
            let xVal = (xidx === -1) ? 0 : data[ind[xIndicator]][xidx][activeYear];
            let yVal = (yidx === -1) ? 0 : data[ind[yIndicator]][yidx][activeYear];
            let circleSize = (cidx === -1) ? 0 : data[ind[circleSizeIndicator]][cidx][activeYear];
            
            plot_data[c] = new PlotData(c, xVal, yVal, id, region, circleSize);
        });


        Object.keys(this.data).forEach(function(key) {
            let idx = this.data[key].map(a => a.country).indexOf(activeCountry);
            countryData[key] =  this.data[key][idx][activeYear];
        });
        console.log(countryData);

        d3.select('.info-box').append('text').text('Population');
        d3.select('.info-box').append('text').text('Population');
        

    }

    /**
     * Removes or makes invisible the info box
     */
    clearHighlight() {

        //TODO - Your code goes here - 
    }

}