/**
 * Data structure for the data associated with an individual country.
 * the CountryData class will be used to keep the data for drawing your map.
 * You will use the region to assign a class to color the map!
 */
class CountryData {
    /**
     *
     * @param type refers to the geoJSON type- countries are considered features
     * @param properties contains the value mappings for the data
     * @param geometry contains array of coordinates to draw the country paths
     * @param region the country region
     */
    constructor(type, id, properties, geometry, region) {

        this.type = type;
        this.id = id;
        this.properties = properties;
        this.geometry = geometry;
        this.region = region;
    }
}

/** Class representing the map view. */
class Map {

    /**
     * Creates a Map Object
     *
     * @param data the full dataset
     * @param updateCountry a callback function used to notify other parts of the program when the selected
     * country was updated (clicked)
     */
    constructor(data, updateCountry) {
        // ******* TODO: PART I *******
        this.projection = d3.geoWinkel3().scale(140).translate([365, 225]);
        this.nameArray = data.population.map(d => d.geo.toUpperCase());
        this.populationData = data.population;
        this.updateCountry = updateCountry;
        this.data = data;
    }

    /**
     * Renders the map
     * @param world the json data with the shape of all countries and a string for the activeYear
     */
    drawMap(world) {
        console.log(world.feature);
        //note that projection is global!

        // ******* TODO: PART I *******

        // Draw the background (country outlines; hint: use #map-chart)
        // Make sure to add a graticule (gridlines) and an outline to the map

        // Hint: assign an id to each country path to make it easier to select afterwards
        // we suggest you use the variable in the data element's id field to set the id

        // Make sure and give your paths the appropriate class (see the .css selectors at
        // the top of the provided html file)

        // You need to match the country with the region. This can be done using .map()
        // We have provided a class structure for the data called CountryData that you should assign the paramters to in your mapping

        //TODO - Your code goes here -


        let countries = []; 
        world.features.forEach(country => {
            let region_idx = this.data['population'].map(a => a.geo).indexOf(country.id.toLowerCase());
            let region = this.data['population'].map(a => a.region)[region_idx];
            let c = new CountryData(country.type,country.id,country.properties,country.geometry,region);
            countries[country.id] = c;
        });
        console.log(countries);

        let path = d3.geoPath().projection(this.projection);
        let thisMap = this;
        let map = d3.select('#map').selectAll('path')
            .data(world.features)
            .enter()
            .append('path')
            .attr('d', path)
            .attr('class', d => (d.id === 'undefined') ? 'unassigned' : countries[d.id].region)
            .attr('id', d => (d.id === 'undefined') ? 'unassigned' : d.id.toLowerCase());
            //.on('click', d => thisMap.updateCountry(d.id));

        let graticule = d3.geoGraticule();
        d3.select('#map').append('path')
            .datum(graticule)
            .attr('class','graticule')
            .attr('d', path);

        d3.select('#map').append('path')
            .datum(graticule.outline)
            .attr('class','graticule outline')
            .attr('d', path);
    }

    /**
     * Highlights the selected conutry and region on mouse click
     * @param activeCountry the country ID of the country to be rendered as selected/highlighted
     */
    updateHighlightClick(activeCountry) {
        // ******* TODO: PART 3*******
        // Assign selected class to the target country and corresponding region
        // Hint: If you followed our suggestion of using classes to style
        // the colors and markers for countries/regions, you can use
        // d3 selection and .classed to set these classes on here.
        //

        d3.selectAll('#' + activeCountry).classed('selected-country',true);
        console.log(activeCountry);
    }

    /**
     * Clears all highlights
     */
    clearHighlight() {
        // ******* TODO: PART 3*******
        // Clear the map of any colors/markers; You can do this with inline styling or by
        // defining a class style in styles.css

        // Hint: If you followed our suggestion of using classes to style
        // the colors and markers for hosts/teams/winners, you can use
        // d3 selection and .classed to set these classes off here.

        //TODO - Your code goes here - 
        d3.selectAll('.selected-country').classed('selected-country', false);
        console.log("removing");
    }
}