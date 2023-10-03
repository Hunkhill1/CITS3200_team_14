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

      select.style.fontWeight = '';

      if (unitCode === selectedUnitCode) {
          select.style.fontWeight = 'bold';
      }

      if (prerequisites.includes(unitCode)) {
          select.style.boxShadow = '0 0 2rem orange';
      }

      const postreqsForUnit = await fetchAndCachePrerequisites(unitCode);
      if (postreqsForUnit.includes(selectedUnitCode)) {
          select.style.boxShadow = '0 0 2rem blue';
      }
  });
}

document.addEventListener("DOMContentLoaded", function () {
  const unitCodeDropdown = document.getElementById("unitCode");
  const showPrerequisitesButton = document.getElementById("showPrerequisites");
  const unitInfo = document.querySelector(".unit-info");
  const prerequisitesList = document.getElementById("prerequisitesList");

  showPrerequisitesButton.addEventListener("click", async () => {
    const selectedUnitCode = unitCodeDropdown.value;
    const prerequisites = await fetchAndCachePrerequisites(selectedUnitCode);

    unitInfo.innerHTML = `
            <h2>Unit Information</h2>
            <p>Selected Unit: ${selectedUnitCode}</p>
        `;

    prerequisitesList.innerHTML = `
            <h2>Prerequisites</h2>
            <ul>
                ${prerequisites
                  .map((prerequisite) => `<li>${prerequisite}</li>`)
                  .join("")}
            </ul>
        `;
  });
});

// Existing jQuery-based dropdown code
document.addEventListener("DOMContentLoaded", function () {
  $(".dropdown-item").click(function () {
    var dropdownButton = $(this).closest(".dropdown").find(".dropdown-toggle");
    var selectedValue = $(this).attr("data-value");
    dropdownButton.text(selectedValue);
  });
});

function removeSelect(element) {
  const selectElement = element.previousElementSibling;
  const value = selectElement.value;

  const index = selectedUnits.indexOf(value);

    if (index === -1) {
        selectedUnits.push(value);
        selectElement.style.borderColor = 'red';
        selectElement.style.backgroundColor = '#ffcccc';
    } else {
        selectedUnits.splice(index, 1);
        selectElement.style.borderColor = 'green';
        selectElement.style.backgroundColor = '#71f086';
    }
    
    // Push the removed unit into the unselectedUnits array
    unselectedUnits.push(value);

    
    selectElement.disabled = false;

  console.log("Selected Units: ", selectedUnits);
  console.log("Unselected Units: ", unselectedUnits);
}
document.addEventListener("DOMContentLoaded", () => {
  // Add an event listener to the submit button
  const submitButton = document.querySelector(".submit-button button");
  submitButton.addEventListener("click", () => {
    // Create a JSON object with unit codes, statuses, and starting year/semester
    const unitStatuses = {};
        
        // Get the selected starting year and semester
        const startYearSelect = document.getElementById('startYear');
        const selectedStartYearSemester = startYearSelect.value;
        
        // Include the selected starting year and semester in the JSON object
        unitStatuses.startYearSemester = selectedStartYearSemester;

    // Populate the JSON object with selected units as "complete"
    for (const unit of selectedUnits) {
      unitStatuses[unit] = "complete";
    }

    // Populate the JSON object with unselected units as "incomplete"
    for (const unit of unselectedUnits) {
      unitStatuses[unit] = "incomplete";
    }

    // Send the JSON data to the Python script using fetch
    fetch("/process_json", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(unitStatuses),
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response from the Python script if needed
        console.log("Response from Python script:", data);
      })
      .catch((error) => {
        console.error("Error sending data to Python script:", error);
      });

    // Find unselected units by comparing with all possible unit values
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const selectElements = document.querySelectorAll(".unit-select");

  selectElements.forEach((select) => {
    selectedUnits.push(select.value); // Initial selected units

    select.addEventListener("change", function () {
      // Clear all existing highlights
      selectElements.forEach((select) => {
        select.style.boxShadow = "";
      });

      // Re-check and highlight prerequisites and post-requisites
      checkAndHighlightPrerequisitesAndPostreqs(this.value);
    });
  });
});

$('#submit-button').click(function(e) {
    e.preventDefault(); // Prevent the default form submission
    
    setTimeout(function() {
        $.ajax({
            url: '/fetch-database',
            type: 'GET',
            success: function(data) {
                updatePlanner(data.new_plan);
            },
            error: function(error) {
                console.error('Error fetching the new plan', error);
            }
        });
    }, 2000); // 2000 milliseconds (2 seconds) delay
});

function updatePlanner(newPlan) {
    for (const [yearKey, semesters] of Object.entries(newPlan)) {
        for (const [semesterKey, units] of Object.entries(semesters)) {
            units.forEach((unit, index) => {
                // Extract year and semester number from the keys
                const year = yearKey.split('_')[1];
                const semester = semesterKey.split('_')[1];
                const unitNum = index + 1; // index is 0-based, unitNum is 1-based
                
                // Construct the ID of the select element
                const selectId = `unit${unitNum}_year${year}_semester${semester}`;
                
                // Find the select element by ID and update its value
                const selectElement = document.getElementById(selectId);
                if (selectElement) {
                    selectElement.value = unit;
                }
            });
        }
    }
}

