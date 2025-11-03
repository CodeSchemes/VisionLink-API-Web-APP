


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
                case "http://localhost:5000/":
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
                            v2 != null ? v2 : 'Null'
                        ]);
                    }  
                    dataFormatted = rows
                    console.log(rows)  
                    break;
                
                case "http://localhost:5000/faults":
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
                
            }
            /*for(const header of columns){
                for(const headerR of headersToRemove)
                    if(header === headerR){
                        let removalIndex = columns.indexOf(header)
                        columns.splice(removalIndex, 1)
                    };
            };*/
        

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
            //tableHead.querySelector("th").appendChild(inputField)
        }
        //Populate rows of data
        for (const row of dataFormatted){
            const rowEl = document.createElement("tr");

            for(const cellText of row){
                const cellEl = document.createElement("td");
                cellEl .textContent = cellText;

                rowEl.appendChild(cellEl);
            };

            tablebody.appendChild(rowEl);
        }
    } catch (error){
        console.error(error.message);
    };
};




