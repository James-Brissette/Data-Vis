/**
 * Makes the first bar chart appear as a staircase.
 *
 * Note: use only the DOM API, not D3!
 */
function staircase() {
    // ****** TODO: PART II ******
    
    charta = document.getElementById("aBarChart").children;
    length = 10;
    for (let i = 0; i < charta.length; i++) {
        charta[i].setAttribute('width',length);
        length += 10;
    }
}

window.onload = function (e) {
    changeData().then(bindColorEvent);
}

function bindColorEvent() {
    let bars = document.getElementsByClassName('bar');
    for (let i = 0; i < bars.length; i++) {
        color = bars[i].style.fill
        
        bars[i].addEventListener("mouseover", function(e) {
            bars[i].style.fill = "#000000"
        });
        bars[i].addEventListener("mouseleave", function(e) {
            bars[i].style.fill = color
        });
    }
}
d3.select('#aBarChart').selectAll('rect')

/**
 * Render the visualizations
 * @param data
 */
function update(data) {
    /** 
     * D3 loads all CSV data as strings. While Javascript is pretty smart
     * about interpreting strings as numbers when you do things like
     * multiplication, it will still treat them as strings where it makes
     * sense (e.g. adding strings will concatenate them, not add the values
     * together, or comparing strings will do string comparison, not numeric 
     * comparison).
     *
     * We need to explicitly convert values to numbers so that comparisons work
     * when we call d3.max()
     **/
    
    for (let d of data) {
        d.a = +d.a; //unary operator converts string to number
        d.b = +d.b; //unary operator converts string to number
    }

    // Set up the scales
    let aScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.a)])
        .range([0, 140]);
    let bScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.b)])
        .range([0, 140]);
    let iScale = d3.scaleLinear()
        .domain([0, data.length])
        .range([10, 120]);


    // ****** TODO: PART III (you will also edit in PART V) ******

    // TODO: Select and update the 'a' bar chart bars

    let aBars = d3.select('#aBarChart').selectAll('rect')
        .classed('bar', true).data(data);
    aBarsEnter = aBars.enter().append('rect').classed('bar', true);

    aBars.exit().remove();
    aBars = aBars.merge(aBarsEnter);
    console.log(aBars);
    aBars
        .attr('width', d => aScale(d.a))
        .attr('height', 10)
        .attr('x', 0)
        .attr('y', (d,i) => 10*(i+1));
        

    // TODO: Select and update the 'b' bar chart bars
    let bBars = d3.select('#bBarChart').selectAll('rect').data(data);
    bBarsEnter = bBars.enter().append('rect').classed('bar',true);
    
    bBars.exit().remove();
    bBars = bBars.merge(bBarsEnter)
        .attr('width', d => bScale(d.b))
        .attr('height', 10)
        .attr('x', 0)
        .attr('y', (d,i) => 10*(i+1))

    bindColorEvent();
    // TODO: Select and update the 'a' line chart path using this line generator

    let aLineGenerator = d3.line()
        .x((d, i) => iScale(i))
        .y((d) => aScale(d.a));

    let aPath = d3.select('#linesA > path')
        .attr('d', d => aLineGenerator(data))

    // TODO: Select and update the 'b' line chart path (create your own generator)
    let bLineGenerator = d3.line()
    .x((d, i) => iScale(i))
    .y((d) => bScale(d.b));

    let bPath = d3.select('#linesB > path')
    .attr('d', d => bLineGenerator(data))

    // TODO: Select and update the 'a' area chart path using this area generator
    let aAreaGenerator = d3.area()
        .x((d, i) => iScale(i))
        .y0(0)
        .y1(d => aScale(d.a));

    let aChart = d3.select('#aAreaChart')
        .attr('d', d => aAreaGenerator(data))

    // TODO: Select and update the 'b' area chart path (create your own generator)
    let bAreaGenerator = d3.area()
        .x((d,i) => iScale(i))
        .y0(0)
        .y1(d => bScale(d.b));
    
    let bChart = d3.select('#bAreaChart')
        .attr('d', d => bAreaGenerator(data));

    // TODO: Select and update the scatterplot points
    let tooltip = d3.select('#scatterplot').select('.tooltip')
    let points = d3.select('#scatterplot').selectAll('circle').data(data);
    pointsEnter = points.enter().append('circle');
    points.exit().remove()
    points = pointsEnter.merge(points);
    
    
    
    points
        .attr('cx', d => aScale(d.a))
        .attr('cy', d => bScale(d.b))
        .attr('r', 5)
        .on('mouseover', function(d) {
            d3.select('.tooltip')
            .text('(' + d.a + ', ' + d.b + ')')
            .attr('opacity',1)
        })
        .on('mouseout', function(d) {
            d3.select('.tooltip')
            .attr('opacity',0)
        })
        .on('click', d => console.log('(' + d.a + ',' + d.b + ')'));

    // ****** TODO: PART IV ******
    function updateToolTip(d) {
       
    }
}

/**
 * Update the data according to document settings 
 */
async function changeData() {
    //  Load the file indicated by the select menu
    let dataFile = document.getElementById('dataset').value;
    try{
        const data = await d3.csv('data/' + dataFile + '.csv'); 
        if (document.getElementById('random').checked) { // if random
            update(randomSubset(data));                  // update w/ random subset of data
        } else {                                         // else
            update(data);
            console.log("Hit")                                // update w/ full data
        }
    } catch (error) {
        alert('Could not load the dataset!');
    }
}

/**
 *  Slice out a random chunk of the provided in data
 *  @param data
 */
function randomSubset(data) {
    return data.filter( d => (Math.random() > 0.5));
}