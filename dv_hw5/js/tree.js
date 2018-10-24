/** Class implementing the tree view. */
class Tree {
    /**
     * Creates a Tree Object
     */
    constructor() {
        
    }

    /**
     * Creates a node/edge structure and renders a tree layout based on the input data
     *
     * @param treeData an array of objects that contain parent/child information.
     */
    createTree(treeData) {

        // ******* TODO: PART VI *******

        let shift = 60;
        //Create a tree and give it a size() of 800 by 300. 
        let treemap = d3.tree().size([800,300])
        let stratify = d3.stratify()
            .id(d => {return d.id})
            .parentId(function(d) {
                if (d.ParentGame == '') {
                    return ''
                }
                let node = treeData[d.ParentGame];
                return node.id;
            });

        //Create a root for the tree using d3.stratify(); 
        let root = stratify(treeData);
        let tree = treemap(root);
        
        //Add nodes and links to the tree. 
        let i = 0;
        let nodes = tree.descendants(),
            links = tree.descendants().slice(1);
        //nodes.forEach(function(d){ d.y = d.depth * 180});

        /***************************************/
        function diagonal(s, d) {

            let path = `M ${s.y} ${s.x}
                    C ${(s.y + d.y) / 2} ${s.x},
                      ${(s.y + d.y) / 2} ${d.x},
                      ${d.y} ${d.x}`
        
            return path
        }
        // *************** Links ***************
        
        let link = d3.select('#tree').selectAll('path.link')
            .data(links, d => d.id);

        let linkEnter = link.enter().append('path')
            .attr('class','link')
            .attr('d', d => {
                return diagonal(d.parent, d)
            });

        let linkUpdate = linkEnter.merge(link);
        linkUpdate
            .attr('transform', d => 'translate(' + shift + ',0)');

        link.exit().remove();

        // *************** Nodes  ***************

        let node = d3.select('#tree').selectAll('g.node')
            .data(nodes, d => d.id || (d.id = ++i));

        let nodeEnter = node.enter().append('g')
            .attr('class', 'node');

        nodeEnter.append('circle')
            .attr('r', 5)
            .style('fill', d => 
                d.parent === null ? '#034e7b' :
                d.data.Team === d.parent.data.Team ? '#034e7b' : '#cb181d');

        nodeEnter.append('text')
            .attr('y', 5)
            .attr('x', d => d.children ? -10 : 10)
            .attr('text-anchor', d => d.children ? 'end' : 'start')
            .text(d => d.data.Team);
      
        // UPDATE
        let nodeUpdate = nodeEnter.merge(node);
        nodeUpdate.attr('transform', d => 'translate(' + (d.y + shift) + ',' + d.x + ')');

        node.exit().remove()
    }

    /**
     * Updates the highlighting in the tree based on the selected team.
     * Highlights the appropriate team nodes and labels.
     *
     * @param row a string specifying which team was selected in the table.
     */
    updateTree(row) {
        // ******* TODO: PART VII *******
        if (row.value.type == 'aggregate') {
            let id = row.key;
                     
            let nodes = d3.selectAll('.node').filter((d) => {
                return (d.data.Team == id)
            });
            let links = d3.selectAll('.link').filter((d) => {
                return (d.data.Team == id && d.parent.data.Team == id)
            });

            nodes.selectAll('text').classed('selectedLabel',true);
            links.classed('selected',true);
        } else {
            let id = row.key;
            let op = row.value.Opponent;
            
            let nodes = d3.selectAll('.node').filter((d) => {
                return (d.data.Team == id && d.data.Opponent == op || d.data.Team == op && d.data.Opponent == id)
            });
            let links = d3.selectAll('.link').filter((d) => {
                return (d.data.Team == id && d.data.Opponent == op || d.data.Team == op && d.data.Opponent == id)
            });

            nodes.selectAll('text').classed('selectedLabel',true);
            links.classed('selected',true);
        }
    }

    /**
     * Removes all highlighting from the tree.
     */
    clearTree() {
        // ******* TODO: PART VII *******

        d3.selectAll('.selected').classed('selected', false);
        d3.selectAll('.selectedLabel').classed('selectedLabel', false); 
    }
}
