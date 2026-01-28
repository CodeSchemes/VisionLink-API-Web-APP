


document.addEventListener("input", () => {
    document.querySelectorAll(".search-input").forEach(inputField => {
        const tableRows = inputField.closest("table").querySelectorAll("tbody tr");
        const headerCell = inputField.closest("th");
        const otherHeaderCells = inputField.closest("tr").querySelectorAll("th");
        const colIndex = Array.from(otherHeaderCells).indexOf(headerCell);
        const searchableCells = Array.from(tableRows)
                .map(row => row.querySelectorAll("td")[colIndex]);
        
                inputField.addEventListener("input", () => {
                    const searchQuery = inputField.value.toLowerCase();

                    for(const tableCell of searchableCells){
                        const row = tableCell.closest("tr");
                        const value = tableCell.textContent
                            .toLowerCase()
                            .replace(",", " ");

                        row.style.visibility = null;

                        if (value.search(searchQuery) === -1){
                            row.style.visibility = "collapse";
                        };
                    };

                })




        console.log(colIndex)
        console.log(searchableCells)

    })
})


async function loadData(url, table){
    /**
     * Loads data from a backend API and populates an HTML table with formatted results
     * @async
     * @function loadData
     * @param {string} url - The backend API endpoint URL to fetch data from (e.g., "http://localhost:5000/data")
     * @param {HTMLTableElement} table - The HTML table element to populate with the fetched data
     * 
     * @returns {Promise<void>}
     * 
     * @throws {Error} Throws an error if the fetch response is not ok or if JSON parsing fails
     * 
     * @description
     * This function fetches data from a Python backend API, parses the response, and inserts
     * formatted data into an HTML table. The table structure (headers and row data) is determined
     * by the provided URL using a switch statement. If thead or tbody elements don't exist,
     * they are created automatically.
     * 
     * @assumptions
     * - The backend API returns a JSON response with two properties: `columns` (array) and `data` (array of arrays)
     * - The `data` array contains rows where each row is an array of values indexed by column position
     * - The table parameter is a valid HTMLTableElement or has similar querySelector capabilities
     * - The URL parameter matches one of the cases defined in the switch statement; unmapped URLs will result in an empty table
     * - Missing or null values in the data should be replaced with placeholder strings ('---' or 'Null')
     * - The backend is running locally on http://localhost:5000
     * - Search input fields will be added to each header for filtering functionality (handled elsewhere)
     * - The provided indices in `indexToAdd` arrays correctly correspond to the column positions in the backend response
     */

    try {
        let tableHead = table.querySelector("thead");
        let tablebody = table.querySelector("tbody");


        
        // ensure thead and tbody exist so we don't try to set properties on null
        if (!tableHead) {
            tableHead = document.createElement("thead");
            table.insertBefore(tableHead, table.firstChild);
        };
        if (!tablebody) {
            tablebody = document.createElement("tbody");
            table.appendChild(tablebody);
        };
 
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        };
        let { columns, data } = await response.json();
        let dataFormatted = []; //will be used to format selected data from fetch call
        let headersFormatted = [] //Will be assigned during formatting 
        console.log(columns)
        console.log(data)
        
        let rows = []
        let indexToAdd = [] 
            switch(url){
                case "http://localhost:5000/data":
                    headersFormatted = ["Asset ID", "Make", "Model", "Serial Number", "Hours"];
                    rows = [];
                    indexToAdd = [15,11,13,14,24];


                    for (const row of data) {
                        const v0 = row[indexToAdd[0]];
                        const v1 = row[indexToAdd[1]];
                        const v2 = row[indexToAdd[2]];
                        const v3 = row[indexToAdd[3]];
                        const v4 = row[indexToAdd[4]];
                        rows.push([
                            v0 != null ? v0 : '---',
                            v1 != null ? v1 : '---',
                            v2 != null ? v2 : 'Null',
                            v3 != null ? v3 : '---',
                            v4 != null ? v4 : 'Null'
                        ]);
                    } 
                    dataFormatted = rows
                    console.log(rows)  
                    break;
                
                case "http://localhost:5000/data/faults":
                    headersFormatted = ["Asset ID", "Serial Number", "Fault Description", "Fault Mid"];
                    rows = [];
                    indexToAdd = [7,6,15,16];

                    
                    for (const row of data) {
                        const v0 = row[indexToAdd[0]];
                        const v1 = row[indexToAdd[1]];
                        const v2 = row[indexToAdd[2]];
                        const v3 = row[indexToAdd[3]];
                        rows.push([
                            v0 != null ? v0 : '---',
                            v1 != null ? v1 : '---',
                            v2 != null ? v2 : 'Null',
                            v3 != null ? v3 : 'Null'
                        ]);
                    }  
                    dataFormatted = rows
                    console.log(rows)  
                    break;

                case "http://localhost:5000/data/hours":
                    headersFormatted = ["Asset ID", "Serial Number", "Hours"];
                    rows = [];
                    indexToAdd = [15,14,24];


                    for (const row of data) {
                        const v0 = row[indexToAdd[0]];
                        const v1 = row[indexToAdd[1]];
                        const v2 = row[indexToAdd[2]];
                        rows.push([
                            v0 != null ? v0 : '---',
                            v1 != null ? v1 : '---',
                            v2 != null ? v2 : 'Null',
                        ]);
                    } 
                    dataFormatted = rows
                    console.log(rows)  
                    break;
                
            }
        

        // Clear the table 
        tableHead.innerHTML = "<tr></tr>";
        tablebody.innerHTML = "";

        //Populate Headers
        for (const headerText of headersFormatted){
            const headerEl = document.createElement("th");
            const searchField = document.createElement("input");
            searchField.classList.add("search-input");
            
            
            searchField.placeholder = headerText;
            headerEl.appendChild(searchField);
            tableHead.querySelector("tr").appendChild(headerEl);
            
        }
        //Populate rows of data
        for (const row of dataFormatted){
            const rowEl = document.createElement("tr");

            for(const cellText of row){
                const cellEl = document.createElement("td");
                cellEl.textContent = cellText;

                rowEl.appendChild(cellEl);
            };

            tablebody.appendChild(rowEl);
        }
    } catch (error){
        console.error(error.message);
    };
};




