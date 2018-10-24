    /**
     * Loads in the table information from fifa-matches-2018.json
     */
//d3.json('data/fifa-matches-2018.json').then( data => {
//
//    /**
//     * Loads in the tree information from fifa-tree-2018.csv and calls createTree(csvData) to render the tree.
//     *
//     */
//    d3.csv("data/fifa-tree-2018.csv").then(csvData => {
//
//        //Create a unique "id" field for each game
//        csvData.forEach( (d, i) => {
//            d.id = d.Team + d.Opponent + i;
//        });
//
//         //Create Tree Object
//        let tree = new Tree();
//        tree.createTree(csvData);
//
//        //Create Table Object and pass in reference to tree object (for hover linking)
//
//        let table = new Table(data,tree);
//
//        table.createTable();
//        table.updateTable(); */
//    });
//});



// // ********************** HACKER VERSION ***************************
/**
 * Loads in fifa-matches-2018.csv file, aggregates the data into the correct format,
 * then calls the appropriate functions to create and populate the table.
 *
 */
function labelToValue(l) {
    out = 0;
    switch (l) {
        case 'Round of Sixteen':
            out = 1;
            break;
        case 'Quarter Finals':
            out = 2;
            break;
        case 'Semi Finals':
            out = 3;
            break;
        case 'Fourth Place':
            out = 4;
            break;
        case 'Third Place':
            out = 5;
            break;
        case 'Runner-Up':
            out = 6;
            break;
        case 'Winner':
            out = 7;
            break;
    }

    return out;
 }

 d3.csv("data/fifa-matches-2018.csv").then( matchesCSV => {
     /**
      * Loads in the tree information from fifa-tree-2018.csv and calls createTree(csvData) to render the tree.
      *
      */
    d3.csv("data/fifa-tree-2018.csv").then( treeCSV => {

     // ******* TODO: PART I *******
     

     hackerData = d3.nest()
        .key(d => d.Team
        )
        .rollup( leaves =>{
            let goalsmade =     d3.sum(leaves,function(l){return l['Goals Made']});
            let goalsconceded = d3.sum(leaves,function(l){return l['Goals Conceded']});
            let deltagoals =    d3.sum(leaves,function(l){return l['Delta Goals']});
            let wins =          d3.sum(leaves,function(l){return l['Wins']});
            let losses =        d3.sum(leaves,function(l){return l['Losses']});


            leaves = leaves.sort(function compare(a,b) {
                let x = labelToValue(a.Result)
                let y = labelToValue(b.Result)
                
                return d3.descending(x,y);

            });

            let label = leaves[0].Result;

            let games = d3.nest()
                //Creating unique keys to allow for multiple games against the same opponent
                //Example: England played Belgium twice
                .key(leaves => leaves.Opponent + '' + leaves['Goals Conceded'])
                .rollup ( leaf => {
                    /* console.log(leaf); */
                    let made = leaf[0]['Goals Made'];
                    let conceded = leaf[0]['Goals Conceded'];
                    let opponent = leaf[0].Team;
                    let rank = labelToValue(leaf[0].Result);

                    let result = {'label': leaf[0].Result, 'ranking': rank};

                    return {'Delta Goals' : '',
                    'Goals Conceded' : conceded,
                    'Goals Made' : made,
                    'Losses' : '',
                    'Opponent' : opponent,
                    'Result' : result,
                    'Wins' : '',
                    'type' : 'game'}
                })
                .entries(leaves)
                //removing the unique identifier used above
                games.forEach(function(game) { game.key = game.key.slice(0,-1) });

            let total = leaves.length;
            let rank = labelToValue(label);
            let result = {'label': label, 'ranking': rank}

            
            return {'Goals Made' : goalsmade,
            'Goals Conceded' : goalsconceded,
            'Delta Goals' : deltagoals,
            'Wins' : wins,
            'Losses' : losses,
            'Result' : result,
            'TotalGames' : total,
            'type' : 'aggregate',
            'games' : games}
        })
        .entries(matchesCSV)

        
        //Create a unique "id" field for each game
        treeCSV.forEach( (d, i) => {
            d.id = d.Team + d.Opponent + i;
        });

        //Create Tree Object
        let hackerTree = new Tree();
        hackerTree.createTree(treeCSV);
        //Create Table Object
        let hackerTable = new Table(hackerData,hackerTree);

        hackerTable.createTable();
        hackerTable.updateTable();

       });

 });
// ********************** END HACKER VERSION ***************************
