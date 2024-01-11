"use strict";

// Require jQuery and Splunk modules
require([
    "jquery", "splunkjs/splunk"
], function($, splunk) {
    console.log("display_page.js require(...) called");

    // Handle click events on elements with the class "clickable_button"
    $(".clickable_button").click(display_page);
    async function display_page() {
        try {
            // Construct the URL for fetching data based on the clicked element's id
            const baseURI = "https://laptop-ujm3ivrg:8021/servicesNS/-";
            const appName = "splunk-app";
            const endpoint = "view_entity";
            const entity = this.id;
            const url = `${baseURI}/${appName}/${endpoint}?entity=${entity}`;
            console.log(url);

            // Fetch data from the constructed URL using the Fetch API
            const response = await fetch(url, {
                method: "GET", mode: "cors", credentials: "include"
            });

            // Parse the JSON response
            const responseData = await response.json();
            console.log('Success:', responseData);

            // Display the retrieved data in a table
            displayTable(responseData);
        } catch (error) {
            console.error('Error fetching aggregated data:', error);

            // Display an error message in the HTML element with id 'displayEntities'
            const outputElement = document.getElementById('displayEntities');
            outputElement.innerHTML = 'Error fetching aggregated data. Check the console for details.';
        }
    }


    // Function to display the data in a table
    function displayTable(entities) {
        // Create a table element
        const table = document.createElement("table");

        // Create the header row of the table
        const headerRow = table.insertRow();
        for (const key in entities[0]) {
            const th = document.createElement("th");
            th.textContent = key;
            headerRow.appendChild(th);
        }

        // Create table rows and cells for each item in the data
        entities.forEach(item => {
            const row = table.insertRow();
            for (const key in item) {
                const cell = row.insertCell();
                cell.textContent = item[key];
            }
        });

        // Get the HTML element with id 'displayEntities'
        const outputElement = document.getElementById('displayEntities');

        // Clear any previous content and append the table to the output element
        outputElement.innerHTML = '';
        outputElement.appendChild(table);
    }
});
