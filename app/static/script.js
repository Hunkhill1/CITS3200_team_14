// Dictionary to cache fetched prerequisites for each unit code
const fetchedPrerequisites = {};
const selectedUnits = [];
const unselectedUnits = [];

// Fetch and cache prerequisites
async function fetchAndCachePrerequisites(unitCode) {
    if (!fetchedPrerequisites[unitCode]) {
        const response = await fetch(`/unit/${unitCode}`);
        const data = await response.json();
        fetchedPrerequisites[unitCode] = data.prerequisites;
    }
    return fetchedPrerequisites[unitCode];
}

// Check and highlight prerequisites
async function checkAndHighlightPrerequisitesAndPostreqs(selectedUnitCode) {
    const prerequisites = await fetchAndCachePrerequisites(selectedUnitCode);
  
    const selectElements = document.querySelectorAll(".unit-select");
    selectElements.forEach(async (select) => {
        const unitCode = select.value;

        if (prerequisites.includes(unitCode)) {
            select.style.boxShadow = '0 0 2rem orange';
        }

        const postreqsForUnit = await fetchAndCachePrerequisites(unitCode);
        if (postreqsForUnit.includes(selectedUnitCode)) {
            select.style.boxShadow = '0 0 2rem blue';
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const unitCodeDropdown = document.getElementById('unitCode');
    const showPrerequisitesButton = document.getElementById('showPrerequisites');
    const unitInfo = document.querySelector('.unit-info');
    const prerequisitesList = document.getElementById('prerequisitesList');

    showPrerequisitesButton.addEventListener('click', async () => {
        const selectedUnitCode = unitCodeDropdown.value;
        const prerequisites = await fetchAndCachePrerequisites(selectedUnitCode);
        
        unitInfo.innerHTML = `
            <h2>Unit Information</h2>
            <p>Selected Unit: ${selectedUnitCode}</p>
        `;
        
        prerequisitesList.innerHTML = `
            <h2>Prerequisites</h2>
            <ul>
                ${prerequisites.map(prerequisite => `<li>${prerequisite}</li>`).join('')}
            </ul>
        `;
    
    
    });
});

// Existing jQuery-based dropdown code
document.addEventListener("DOMContentLoaded", function () {
    $('.dropdown-item').click(function () {
        var dropdownButton = $(this)
        .closest('.dropdown')
        .find('.dropdown-toggle');
        var selectedValue = $(this).attr('data-value');
        dropdownButton.text(selectedValue);
    });
});

function removeSelect(element) {
    const selectElement = element.previousElementSibling;
    const value = selectElement.value;
    
    const index = selectedUnits.indexOf(value);

    if (index === -1) {
        selectedUnits.push(value);
        selectElement.style.borderColor = 'green';
        selectElement.style.backgroundColor = '#71f086';
    } else {
        selectedUnits.splice(index, 1);
        selectElement.style.borderColor = 'red';
        selectElement.style.backgroundColor = '#ffcccc';
    }
    
    // Push the removed unit into the unselectedUnits array
    unselectedUnits.push(value);

    
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


// Logic for the second page
document.addEventListener("DOMContentLoaded", () => {
    const selectElements = document.querySelectorAll(".unit-select");
  
    selectElements.forEach((select) => {
        selectedUnits.push(select.value); // Initial selected units
        
        select.addEventListener('change', function() {
            // Clear all existing highlights
            selectElements.forEach((select) => {
                select.style.boxShadow = '';
            });
            
            // Re-check and highlight prerequisites and post-requisites
            checkAndHighlightPrerequisitesAndPostreqs(this.value);
        });
    });
});


