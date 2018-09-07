/** Class representing a Tree. */
class Tree {
    /**
     * Creates a Tree Object
     * Populates a single attribute that contains a list (array) of Node objects to be used by the other functions in this class
     * note: Node objects will have a name, parentNode, parentName, children, level, and position
     * @param {json[]} json - array of json objects with name and parent fields
     */
    

    constructor(json) {
        let r = new Node();
        let elements = [];
        json.forEach(function(item) {
            let n = new Node(item.name,item.parent);
            if (n.parentName === 'root') {
                r = n;
            }
            let i = elements.findIndex(j => j.name === item.parent);
            if (i > -1) {
                n.parentNode = elements[i];               
            }          
            elements.push(n);
        });
        this.root = r;
        this.elements = elements;
    }

    /**
     * Function that builds a tree from a list of nodes with parent refs
     */
    buildTree() {
    
        // note: in this function you will assign positions and levels by making calls to assignPosition() and assignLevel()
        let elements = this.elements;
        elements.forEach(function(item) {
           if (item.parentNode != null) {
               item.parentNode.children.push(item);
           }
        });
            
        //Handles the root of the tree where there is no parent but d3 will reference the parent
        //to calculate where to draw the line in renderTree()
        if (this.root.parentNode === null) {
            this.root.parentNode = this.root;
        }
                
        this.assignLevel(this.root,0);
        this.assignPosition(this.root,0);
        this.renderTree();
    }

    /**
     * Recursive function that assign levels to each node
     */
    assignLevel(node, level) {
        if (node.children.length != 0) {
            node.children.forEach(n => this.assignLevel(n,level + 1));
        }
        node.level = level;
    }

    /**
     * Recursive function that assign positions to each node
     */
    assignPosition(node, position) {
        node.position = position;
        if (node.children.length === 0) { 
            return position + 1;
        }
        node.children.forEach(n => position = this.assignPosition(n,position));
        return position;     
    }

    /**
     * Function that renders the tree
     */
    renderTree() { 
        let elements = this.elements;       
        let svg = d3.select('body').append('svg');
        let xscale = 150;
        let yscale = 100;
        
        svg
            .attr('height', 1200)
            .attr('width', 1200);
        
        svg.append('g')
            .attr('class', 'lineGroup')
            .attr('transform', 'translate(50, 50)');

        svg.append('g')
            .attr('class', 'nodeGroup')
            .attr('transform', 'translate(50, 50)');
        
        
         svg.selectAll('.lineGroup').selectAll('line')
            .data(elements)
            .enter().append('line')
            .attr('x2', d => d.parentNode.level * xscale)
            .attr('y2', d => d.parentNode.position * yscale)
            .attr('x1', d => d.level * xscale)
            .attr('y1', d => d.position * yscale);
        
        svg.selectAll('.nodeGroup').selectAll("circle")
            .data(elements)
            .enter().append('circle')
            .attr('cx', d => d.level * xscale)
            .attr('cy', d => d.position * yscale)
            .attr('r', 40);

        svg.selectAll('.nodeGroup').selectAll("text")
            .data(elements)
            .enter().append('text')
            .attr('x', d => d.level * xscale)
            .attr('y', d => d.position * yscale)
            .attr('class', 'label')
            .text(d => d.name);
    }

}
