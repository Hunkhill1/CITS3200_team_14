document.addEventListener('DOMContentLoaded', function () {
    const unitCodeDropdown = document.getElementById('unitCode');
    const showPrerequisitesButton = document.getElementById('showPrerequisites');
    const unitInfo = document.querySelector('.unit-info');
    const prerequisitesList = document.getElementById('prerequisitesList');

    showPrerequisitesButton.addEventListener('click', async () => {
        const selectedUnitCode = unitCodeDropdown.value;

        // Fetch prerequisites using AJAX (you can use fetch or jQuery.ajax)
        const response = await fetch(`/unit/${selectedUnitCode}`);
        const data = await response.json();

        // Update the unit information and prerequisites
        unitInfo.innerHTML = `
            <h2>Unit Information</h2>
            <p>Selected Unit: ${selectedUnitCode}</p>
            <!-- You can add more unit information here -->
        `;
        
        prerequisitesList.innerHTML = `
            <h2>Prerequisites</h2>
            <ul>
                ${data.prerequisites.map(prerequisite => `<li>${prerequisite}</li>`).join('')}
            </ul>
        `;
    
    
    });
});

document.addEventListener("DOMContentLoaded", function () {
    $('.dropdown-item').click(function () {
        var dropdownButton = $(this)
        .closest('.dropdown')
        .find('.dropdown-toggle');
        var selectedValue = $(this).attr('data-value');
        dropdownButton.text(selectedValue);
        // Add logic to set this value in a hidden form field or use in other ways.
    });
});

const selectedUnits = [];
const unselectedUnits = [];

function removeSelect(element) {
    const selectElement = element.previousElementSibling;
    const removedValue = selectElement.value;
    
    // Find the index of the removed unit in the array and remove it
    const index = selectedUnits.indexOf(removedValue);
    if (index !== -1) {
        selectedUnits.splice(index, 1);
    }
    
    // Push the removed unit into the unselectedUnits array
    unselectedUnits.push(removedValue);
    
    selectElement.style.borderColor = 'red';
    selectElement.style.backgroundColor = '#ffcccc';
    
    // Enable the select box so it can be changed again
    selectElement.disabled = false;

    console.log("Selected Units: ", selectedUnits);
    console.log("Unselected Units: ", unselectedUnits);

   
}
document.addEventListener("DOMContentLoaded", () => {
    // Add an event listener to the submit button
    const submitButton = document.querySelector('.submit-button button');
    submitButton.addEventListener('click', () => {
        // Create a JSON object with unit codes and statuses
        const unitStatuses = {};

        // Populate the JSON object with selected units as "complete"
        for (const unit of selectedUnits) {
            unitStatuses[unit] = "complete";
        }

        // Populate the JSON object with unselected units as "incomplete"
        for (const unit of unselectedUnits) {
            unitStatuses[unit] = "incomplete";
        }

        // Send the JSON data to the Python script using fetch
        fetch('/process_json', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(unitStatuses),
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the Python script if needed
            console.log('Response from Python script:', data);
        })
        .catch(error => {
            console.error('Error sending data to Python script:', error);
        });

        // Find unselected units by comparing with all possible unit values
    });
});


document.addEventListener("DOMContentLoaded", () => {
    // Add initial select values to the array
    const selectElements = document.querySelectorAll(".unit-select");
    selectElements.forEach((select) => {
        selectedUnits.push(select.value);
    });
});

