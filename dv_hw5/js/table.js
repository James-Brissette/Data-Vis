/** Class implementing the table. */
class Table {
    /**
     * Creates a Table Object
     */
    constructor(teamData, treeObject) {

        // Maintain reference to the tree object
        this.tree = null;

        /**List of all elements that will populate the table.*/
        // Initially, the tableElements will be identical to the teamData
        this.tableElements = teamData;

        ///** Store all match data for the 2018 Fifa cup */
        this.teamData = teamData;
        console.log(teamData);
        this.tableHeaders = ["Delta Goals", "Result", "Wins", "Losses", "TotalGames"];

        /** letiables to be used when sizing the svgs in the table cells.*/
        this.cell = {
            "width": 70,
            "height": 20,
            "buffer": 15
        };

        this.bar = {
            "height": 20
        };

        this.treeObject = treeObject;
        this.sortOrder = false;
        /** Set variables for commonly accessed data columns*/
        this.goalsMadeHeader = 'Goals Made';
        this.goalsConcededHeader = 'Goals Conceded';

        /** Setup the scales*/
        this.goalScale = null;


        /** Used for games/wins/losses*/
        this.gameScale = null;

        /**Color scales*/
        /**For aggregate columns*/
        /** Use colors '#feebe2' and '#690000' for the range*/
        this.aggregateColorScale = null;


        /**For goal Column*/
        /** Use colors '#cb181d' and '#034e7b' for the range */
        this.goalColorScale = null;
    }


    /**
     * Creates a table skeleton including headers that when clicked allow you to sort the table by the chosen attribute.
     * Also calculates aggregate values of goals, wins, losses and total games as a function of country.
     *
     */
    createTable() {
        let leftPad = 10;
        // ******* TODO: PART II *******

        //Update Scale Domains
        let maxGoals = Math.max(...Object.values(this.teamData).map(a => Math.max(...[a.value['Goals Made'],a.value['Goals Conceded'],a.value['Delta Goals']])));
        this.goalScale = d3.scaleLinear()
            .domain([0,maxGoals])
            .range([0,(this.cell.width + 40)]);
        this.aggregateColorScale = d3.scaleLinear()
            .domain([0,maxGoals])
            .range(['#cb181d','#034e7b']);
        let maxGames = Math.max(...Object.values(this.teamData).map(a => a.value['TotalGames']))
        this.gameScale = d3.scaleLinear()
            .domain([0,maxGames])
            .range([0,this.cell.width]).nice();
        this.aggregateColorScale = d3.scaleLinear()
            .domain([0,maxGames])
            .range(['#feebe2','#690000']);

        // Create the axes
        let goalAxis = d3.axisTop().scale(this.goalScale).ticks(7);
        
        //add GoalAxis to header of col 1.
        let goalHeader = d3.select('#goalHeader').append('svg')
            .attr('width', (this.cell.width + 50))
            .attr('height', 5)
            .style('padding-top',this.cell.buffer + 5)
            .style('padding-left',leftPad)
            .call(goalAxis);
        
        this.tableElements = this.teamData;
        // ******* TODO: PART V *******

        // Set sorting callback for clicking on headers
        

        //Set sorting callback for clicking on Team header
        //Clicking on headers should also trigger collapseList() and updateTable().

    }


    /**
     * Updates the table contents with a row for each element in the global variable tableElements.
     */
    updateTable() {
        // ******* TODO: PART III *******
        //Create table rows
        let that = this;        
        let leftPad = 10;
        
        let tableRows = d3.select('tbody').selectAll('tr').data(this.tableElements);
        let tableRowsEnter = tableRows.enter().append('tr')
        
        tableRows.exit().remove();

        tableRows = tableRowsEnter.merge(tableRows);
        tableRows
            .attr('id', d => d.key)
            .attr('height',this.cell.height)
            .on('click', function(d,i) {
                console.log(d)
                that.updateList(i);
            })
            .on('mouseenter', function(d) {
                that.treeObject.updateTree(d);
            })
            .on('mouseleave', function(d) {
                that.treeObject.clearTree();
            });

        //Append th elements for the Team Names
        let th = tableRows.selectAll('th').data(d => [{'type':d.value['type'], 'vis':'text', 'value':d.key}]);
        let thEnter = th.enter().append('th');
        th.exit().remove();

        th = thEnter.merge(th);
        

        //Append td elements for the remaining columns. 
        let td = tableRows.selectAll('td').data(d => 
            [{'type':d.value['type'], 'vis':'goals', 'value':{'Delta Goals':d.value['Delta Goals'],
                                                    'Goals Conceded':d.value['Goals Conceded'],
                                                    'Goals Made':d.value['Goals Made']}},
            {'type':d.value['type'], 'vis':'text', 'value':d.value['Result']['label']},
            {'type':d.value['type'], 'vis':'bars', 'value':d.value['Wins']},
            {'type':d.value['type'], 'vis':'bars', 'value':d.value['Losses']},
            {'type':d.value['type'], 'vis':'bars', 'value':d.value['TotalGames']}]);
        let tdEnter = td.enter().append('td');
        td.exit().remove();
        td = tdEnter.merge(td);

            
            td.selectAll('svg').remove();
            //Barcharts
            let barCharts = td.filter((d) => {
                return d.type == 'aggregate'
            }).filter((d) => {
                return d.vis == 'bars'
            });

            barCharts.append('svg')
            .attr('height', this.cell.height)
            .attr('width', this.cell.width);
            
            barCharts.select('svg').append('rect')
            .attr('height', this.cell.height)
            .attr('width', d => this.gameScale(d.value))
            .attr('fill', d => this.aggregateColorScale(d.value));
            barCharts.select('svg').append('text')
            .text(d => d.value)
            .style('fill', 'white')
            .attr('transform',d => 'translate(' + (this.gameScale(d.value) - 10) +',14)');

            
            let aggregateGoalChart = td.filter((d) => {
                return d.vis == 'goals'
            }).filter((d) => {
                return d.type == 'aggregate'
            });
            let gameGoalChart = td.filter((d) => {
                return d.vis == 'goals'
            }).filter((d) => {
                return d.type == 'game'
            });

            aggregateGoalChart.append('svg')
            .attr('height', this.cell.height)
            .attr('width', this.cell.width + 55);
            gameGoalChart.append('svg')
            .attr('height', this.cell.height)
            .attr('width', this.cell.width + 55);

            
            
            //goal bars
            aggregateGoalChart.select('svg').append('rect').classed('goalBar',true)
            .attr('x', function(d) {
                let min = Math.min(...[d.value['Goals Made'],d.value['Goals Conceded']]);
                return that.goalScale(min)+leftPad;
            })
            .attr('y', this.cell.height/4)
            .attr('height',this.cell.height/2)
            .attr('width', d => this.goalScale(Math.abs(d.value['Delta Goals'])))
            .attr('fill', d => d.value['Delta Goals'] > 0 ? '#034e7b' : '#cb181d')
            .append('title').text(d => 'Goals Scored: ' + d.value['Goals Made'] + ' Goals Conceded: ' + d.value['Goals Conceded']);

            gameGoalChart.select('svg').append('rect').classed('goalBar',true)
            .attr('y', 2*this.cell.height/5)
            .attr('height',this.cell.height/5)
            .attr('width', d => this.goalScale(Math.max(d.value['Goals Made'],d.value['Goals Conceded']) - Math.min(d.value['Goals Made'],d.value['Goals Conceded'])))
            .attr('fill', d => d.value['Goals Made'] > d.value['Goals Conceded'] ? '#034e7b' : '#cb181d')
            .attr('x', function(d) {
                let min = Math.min(...[d.value['Goals Made'],d.value['Goals Conceded']]);
                return that.goalScale(min)+leftPad;
            })
            .append('title').text(d => 'Goals Scored: ' + d.value['Goals Made'] + ' Goals Conceded: ' + d.value['Goals Conceded']);

            //made goals
            aggregateGoalChart.select('svg').append('circle').classed('goalCircle',true)
            .attr('cx', d => this.goalScale(d.value['Goals Made'])+leftPad)
            .attr('cy',this.cell.height/2)
            .attr('fill', d => d.value['Goals Made'] == d.value['Goals Conceded'] ? '#808080' : '#034e7b')
            .append('title').text(d => d.value['Goals Made']);
            gameGoalChart.select('svg').append('circle').classed('goalCircle',true)
            .attr('cx', d => this.goalScale(d.value['Goals Made'])+leftPad)
            .attr('cy',this.cell.height/2)
            .attr('fill', d => d.value['Goals Made'] == d.value['Goals Conceded'] ? '#808080' : '#034e7b')
            .append('title').text(d => d.value['Goals Made']);
            gameGoalChart.select('svg').append('circle').classed('fillerCirlce',true)
            .attr('cx', d => this.goalScale(d.value['Goals Made'])+leftPad)
            .attr('cy',this.cell.height/2)
            .append('title').text(d => d.value['Goals Made']);

            //conceded goals
            aggregateGoalChart.select('svg').append('circle').classed('goalCircle',true)
            .attr('cx', d => this.goalScale(d.value['Goals Conceded'])+leftPad)
            .attr('cy',this.cell.height/2)
            .attr('fill', d =>  d.value['Goals Made'] == d.value['Goals Conceded'] ? '#808080' :'#cb181d')
            .append('title').text(d => d.value['Goals Conceded']);
            gameGoalChart.select('svg').append('circle').classed('goalCircle',true)
            .attr('cx', d => this.goalScale(d.value['Goals Conceded'])+leftPad)
            .attr('cy',this.cell.height/2)
            .attr('fill', d =>  d.value['Goals Made'] == d.value['Goals Conceded'] ? '#808080' :'#cb181d')
            .append('title').text(d => d.value['Goals Conceded']);
            gameGoalChart.select('svg').append('circle').classed('fillerCirlce',true)
            .attr('cx', d => this.goalScale(d.value['Goals Conceded'])+leftPad)
            .attr('cy',this.cell.height/2)
            .append('title').text(d => d.value['Goals Conceded']);
            

            //Team Names
            th.selectAll('text').remove();
            th.append('text')
                .attr('class', d => d.type)
                .text(d => d.type == 'aggregate' ? d.value : 'x'+ d.value);
            //Round/Results
            let textLabels = td.filter((d) => {
                return d.vis == 'text'
            });

            textLabels.append('svg')
            .attr('height', this.cell.height)
            .attr('width', this.cell.width + 55)

            textLabels.select('svg').append('text')
                .text(d => d.value)
                .attr('x',0)
                .attr('y',10)
                .style('font-weight','bold');


            let sortCriteria = ['Delta Goals','Round','Wins','Losses','TotalGames'];
            let headers = d3.select('thead').select('tr').selectAll('td');
            let thHeader = d3.select('thead').select('tr').select('th');

            headers.data(sortCriteria)
                .on('click', function(d) {
                    that.collapseList();
                    that.tableElements = that.tableElements.sort(function compare(a,b) {
                        
                        switch (d) {
                            case 'Wins':
                                if (d == that.sortOrder) {
                                    return d3.ascending(a.value[d],b.value[d]);
                                } else {
                                    return d3.descending(a.value[d],b.value[d]);
                                }
                            case 'Losses':
                                if (d == that.sortOrder) {
                                    return d3.ascending(a.value[d],b.value[d]);
                                } else {
                                    return d3.descending(a.value[d],b.value[d]);
                                }
                            case 'TotalGames':
                                if (d == that.sortOrder) {
                                    return d3.ascending(a.value[d],b.value[d]);
                                } else {
                                    return d3.descending(a.value[d],b.value[d]);
                                }
                            case 'Delta Goals':
                                if (d == that.sortOrder) {
                                    return d3.ascending(a.value[d],b.value[d]);
                                } else {
                                    return d3.descending(a.value[d],b.value[d]);
                                }
                            case 'Round':
                                let x = a.value.Result.ranking
                                let y = b.value.Result.ranking

                                if (d == that.sortOrder) {
                                    if (x < y) {
                                        return -1;
                                    } else if (x > y) {
                                        return 1;
                                    } else {
                                        return 0;
                                    };
                                } else {
                                    if (x > y) {
                                        return -1;
                                    } else if (x < y) {
                                        return 1;
                                    } else {
                                        return 0;
                                    };
                                }                                
                        } 
                    });
                    if (that.sortOrder == d) {
                        that.sortOrder = false;
                    } else {
                        that.sortOrder = d;
                    }
                    that.updateTable();
                });
            thHeader.data(['Team'])
                .on('click', function(d) {
                    that.collapseList();
                    that.tableElements = that.tableElements
                        .sort(function compare(a,b) {
                            if (d == that.sortOrder) {
                                if (a.key > b.key) {
                                    return -1;
                                } else if (a.key < b.key) {
                                    return 1;
                                } else {
                                    return 0;
                                };
                            } else {
                                if (a.key < b.key) {
                                    return -1;
                                } else if (a.key > b.key) {
                                    return 1;
                                } else {
                                    return 0;
                                };
                            };
                        });
                    if (that.sortOrder == d) {
                        that.sortOrder = false;
                    } else {
                        that.sortOrder = d;
                    }
                    that.updateTable();
                });
    };

    /**
     * Updates the global tableElements variable, with a row for each row to be rendered in the table.
     *
     */
    updateList(i) {
        // ******* TODO: PART IV *******
       
        //Only update list for aggregate clicks, not game clicks
        if (this.tableElements[i].value['type'] == 'aggregate') {
            if (i < this.tableElements.length - 1 && this.tableElements[i + 1].value['type'] == 'game') {
                    let count = 0;
                    while (this.tableElements[i+count+1].value['type'] == 'game') {
                        ++count;
                        if ((i+count+1) >= this.tableElements.length) {
                            break;
                        }
                    }
                    this.tableElements.splice((i+1),count)
            } else {
                let games = this.tableElements[i].value['games'];
                let a = this.tableElements.slice(0,(i+1));
                let b = this.tableElements.slice((i+1), this.tableElements.length);

                games.forEach(element => {
                    a = a.concat(element);
                });
                this.tableElements = a.concat(b);
            }
        }

        this.updateTable();

    }

    /**
     * Collapses all expanded countries, leaving only rows for aggregate values per country.
     *
     */
    collapseList() {
        
        // ******* TODO: PART IV *******
        let i = 0;
        while (i < this.tableElements.length -1) {
            if (this.tableElements[i + 1].value['type'] == 'game') {
                let count = 1;
                while (this.tableElements[i+count+1].value['type'] == 'game') {
                    ++count;
                }
                this.tableElements.splice((i+1),count)
            }
            ++i;
        }
        this.updateTable();

    }


}
