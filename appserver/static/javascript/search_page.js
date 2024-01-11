"use strict";

// Require jQuery and Splunk modules
require(["jquery", "splunkjs/splunk"], function($) {

    // Log that the require function has been called
    console.log("search_page.js require(...) called");

    // Attach click event handler to the element with id "search"
    $("#search").click(search_page);

    // Function to handle the search functionality
    async function search_page() {
        try {
            // Construct the URL for fetching data based on the search input
            const baseURI = "https://laptop-ujm3ivrg:8021/servicesNS/-";
            const appName = "splunk-app";
            const endpoint = "search_entity";
            const searchInput = document.getElementById('search_input').value;
            const url = `${baseURI}/${appName}/${endpoint}?query=${searchInput}`;

            // Fetch data from the constructed URL using the Fetch API
            const response = await fetch(url, {
                method: "GET", mode: "cors", credentials: "include"
            });

            // Parse the JSON response
            const responseData = await response.json();

            // Display the retrieved data in the HTML element with id 'searchResults'
            const outputElement = document.getElementById('searchResults');
            outputElement.innerHTML = '';  // Clear previous results

            // Display each item in a formatted way
            responseData.forEach(item => {
                outputElement.innerHTML += JSON.stringify(item, null, 2) + '<br>';
            });

            console.log('Success:', responseData);
        } catch (error) {
            // Handle errors and display a message in the HTML element with id 'searchResults'
            console.error('Error fetching search results:', error);
            const outputElement = document.getElementById('searchResults');
            outputElement.innerHTML = 'Error fetching search results. Check the console for details.';
        }
    }
});
