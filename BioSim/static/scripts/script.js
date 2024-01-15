var table = document.getElementById("mapTable");

var map_str=""

function createGrid() {
    // Get the user input for grid size
    var gridSize = parseInt(document.getElementById("gridSize").value);
    if (gridSize > 16){
        gridSize = 16;
    }
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
    
    createGrid();

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
    // map_str = finalString
    alert(finalString);
    return finalString
}

function saveCarnivoreParams() {

}

function runSimulation() {
        mapValue = generateString();
        nYearsValue =  document.querySelector("#sim_years").value;
        prjNameValue =  document.querySelector("#prj_name").value;
        // Validate if any of the values are null
        if (mapValue == null || nYearsValue == null || prjNameValue == null) {
            // Show a warning message
            alert("Please fill in all required fields.");
            return;  // Stop further processing if validation fails
        }

        var dataToSend = {
            'map': mapValue,
            'n_years': nYearsValue,
            'prj_name' : prjNameValue,
        };
        

        fetch('run-simulation/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dataToSend),
        })
        .then((response) => response.json())
        .then(data => {
            console.log(window.location)
            var loc = window.location
            var wsStart = "ws://"
            if (loc.protocol == 'https:') {
                wsStart = "wss://"
            }
            var sim_id = data.sim_id
            
            console.log(sim_id);

            var endpoint = wsStart + window.location.host + `/ws/task_status/${sim_id}/`
            // var endpoint = `ws://localhost:8000/ws/task_status/`
            // Establish WebSocket connection
            console.log(endpoint)

            var socket = new WebSocket(endpoint);

            // Send the task ID to the server
            socket.onopen = event => {
                console.log('WebSocket connection opened!');
                socket.send(JSON.stringify({ 'task_id': data.task_id }));
            };

            // Handle messages from the server
            socket.onmessage = event => {
                const receivedData = JSON.parse(event.data);
                console.log('Received message from server:', receivedData);

                // Update the user based on the task status
                if (receivedData.status === 'SUCCESS') {
                    console.log(`task : completed`)
                    // alert('Task completed!');
                    createFetchButton(sim_id);

                } else {
                    // Update the user interface based on the task status
                    console.log(`Task status: ${receivedData.status}`);
                }
            };

            socket.onclose = event => {
                console.log('WebSocket connection closed:', event);
            };

            socket.onerror = error => {
                console.error('WebSocket error:', error);
            };
        });
};

function createFetchButton(sim_id) {
    var result_area = document.querySelector(".result");

    // Check if there is already a button in the result area
    var existingButton = result_area.querySelector("button");
    if (existingButton) {
        // Remove the existing button
        existingButton.remove();
    }

    // Create a new button element
    var fetchResultButton = document.createElement("button");
    fetchResultButton.textContent = "Download Results";
    fetchResultButton.onclick = function() {
        fetchAnotherEndpoint(sim_id);
    };

    // Append the new button to the result area
    result_area.appendChild(fetchResultButton);
}

function fetchAnotherEndpoint(sim_id) {
    // Logic to fetch another endpoint when the button is clicked
    fetch(`download-result/${sim_id}/`)
}


function toggleCollapsible() {
    var content = document.getElementById('inputContent');
    var icon = document.getElementById('toggleIcon');
    if (content.style.display === 'none' || content.style.display === '') {
        content.style.display = 'block';
        icon.innerText = '-';
    } else {
        content.style.display = 'none';
        icon.innerText = '+';
    }
}

function generateJSON() {
    var form = document.getElementById('userInputForm');
    var formData = new FormData(form);
    var jsonObject = {};

    formData.forEach(function(value, key){
        jsonObject[key] = value;
    });

    var jsonString = JSON.stringify(jsonObject, null, 2);
    var formattedJson = jsonString.replace(/"([^"]+)":/g, "'$1':");
    
    document.getElementById('jsonOutput').innerText = formattedJson;
}