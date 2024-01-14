var table = document.getElementById("mapTable");

function createGrid() {
    // Get the user input for grid size
    var gridSize = parseInt(document.getElementById("gridSize").value);

    // Clear existing table content
    table.innerHTML = "";

    // Create rows and cells for the new grid
    for (var i = 0; i < gridSize; i++) {
        var tr = document.createElement("tr");
        for (var j = 0; j < gridSize; j++) {
            var td = document.createElement("td");
            td.textContent = "";
            td.onclick = function () {
                // Remove existing color classes
                this.classList.remove('water', 'highland', 'lowland', 'desert');

                // Change the value when a cell is clicked
                this.textContent = document.getElementById("cellType").value;

                // Apply different colors based on cell type
                applyColor(this);
            };

            // Set initial type for left, right, top, and bottom-most cells
            if (i === 0 || j === 0 || i === gridSize - 1 || j === gridSize - 1) {
                td.textContent = 'W';
            }

            // Apply different colors based on cell type
            applyColor(td);

            tr.appendChild(td);
        }
        table.appendChild(tr);
    }
}

function applyColor(cell) {
    switch (cell.textContent) {
        case 'W':
            cell.classList.add('water');
            break;
        case 'H':
            cell.classList.add('highland');
            break;
        case 'L':
            cell.classList.add('lowland');
            break;
        case 'D':
            cell.classList.add('desert');
            break;
        default:
            break;
    }
}

function createRandomMap() {
    var cellTypes = ['W', 'H', 'L', 'D'];
    for (var i = 1; i < table.rows.length - 1; i++) {
        for (var j = 1; j < table.rows[i].cells.length - 1; j++) {
            // Set a random cell type
            var randomType = cellTypes[Math.floor(Math.random() * cellTypes.length)];
            table.rows[i].cells[j].textContent = randomType;

            // Remove existing color classes
            table.rows[i].cells[j].classList.remove('water', 'highland', 'lowland', 'desert');

            // Apply different colors based on cell type
            applyColor(table.rows[i].cells[j]);
        }
    }
}

function generateString() {
    var finalString = "";
    for (var i = 0; i < table.rows.length; i++) {
        for (var j = 0; j < table.rows[i].cells.length; j++) {
            finalString += table.rows[i].cells[j].textContent;
        }
        finalString += '\n';
    }
    alert(finalString);
}