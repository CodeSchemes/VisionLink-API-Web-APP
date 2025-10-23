

async function loadData(url, table){

    try {
        let tableHead = table.querySelector("thead");
        let tablebody = table.querySelector("tbody");


        
        // ensure thead and tbody exist so we don't try to set properties on null
        if (!tableHead) {
            tableHead = document.createElement("thead");
            table.insertBefore(tableHead, table.firstChild);
        }
        if (!tablebody) {
            tablebody = document.createElement("tbody");
            table.appendChild(tablebody);
        }
 
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
        let { columns, data } = await response.json();

        console.log(columns)
        console.log(data)
        //Filter data into usable format by trimming empty fields. Check for empy fields in console.log in browser dev tool
        if (url == "http://localhost:5000/"){
            const headersToRemove = ['customAssetState', 'source', 'customUtilizationType'];
            const dataToRemove = []

            const removalSet = new Set(headersToRemove)
            columns = columns.filter(header => !removalSet.has(header));
            /*for(const header of columns){
                for(const headerR of headersToRemove)
                    if(header === headerR){
                        let removalIndex = columns.indexOf(header)
                        columns.splice(removalIndex, 1)
                    }
            }*/
        }

        // Clear the table 
        tableHead.innerHTML = "<tr></tr>";
        tablebody.innerHTML = "";

        //Populate Headers
        for (const headerText of columns){
            const headerEl = document.createElement("th");
            
            headerEl.textContent = headerText;
            tableHead.querySelector("tr").appendChild(headerEl);
        }
        //Populate rows of data
        for (const row of data){
            const rowEl = document.createElement("tr");

            for(const cellText of row){
                const cellEl = document.createElement("td");
                cellEl .textContent = cellText

                rowEl.appendChild(cellEl)
            }

            tablebody.appendChild(rowEl)
        }
    } catch (error){
        console.error(error.message);
    }
}


