/**
 * script.js
 * 
 * This JavaScript file contains client-side functionality for the Study Planner web application.
 * It manages user interactions, form submissions, and dynamic updates of the user interface.
 * 
 * Contents:
 * - Caching and fetching of unit prerequisites.
 * - Highlighting prerequisites and post-requisites.
 * - Setup of event listeners for checking prerequisites.
 * - Handling the display of unit information and prerequisites.
 * - Updating the unit selection interface.
 * - Managing user actions, such as editing and deleting units.
 * - Sending JSON data to the server for processing.
 * 
 * Usage:
 * 1. This script handles various client-side features, including the display of prerequisites,
 *    unit selection, highlighting, and user actions.
 * 2. It interacts with the server to retrieve unit data and make updates.
 * 3. Event listeners are set up to respond to user interactions and form submissions.
 * 
 * Important Notes:
 * - This script interacts with specific HTML elements and assumes the structure of the web application.
 * - Ensure that this script is linked to your HTML templates correctly.
 * - Server-side routes and endpoints are expected to be available for data retrieval and processing.
 * - The script uses asynchronous functions and fetch requests to communicate with the server.
 * - Verify that the script works in the context of your web application and make adjustments as needed.
 * 
 * For more details on specific functions and actions, refer to the code comments below.
 */


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

function setupCheckPrereqButtons() {
  const checkPrereqButtons = document.querySelectorAll(".check-prereq-btn");
  let lastChecked = null;

  checkPrereqButtons.forEach((button) => {
      button.addEventListener("change", async function() {
          const unitSelectId = this.getAttribute("data-unit-id");
          const unitSelect = document.getElementById(unitSelectId);
          const selectedUnitCode = unitSelect.value;

          const selectElements = document.querySelectorAll(".unit-select");
          selectElements.forEach((select) => {
              select.style.boxShadow = "";
          });

          if (this.checked) {
              if (lastChecked === this) {
                  this.checked = false;
                  lastChecked = null;
              } else {
                  lastChecked = this;
                  await checkAndHighlightPrerequisitesAndPostreqs(selectedUnitCode);
              }
          } else {
              lastChecked = null;
          }
      });

      button.addEventListener("click", function() {
          if (button === lastChecked) {
              button.checked = false;
              lastChecked = null;

              const selectElements = document.querySelectorAll(".unit-select");
              selectElements.forEach((select) => {
                  select.style.boxShadow = "";
              });
          }
      });
  });
};

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

function setupDropdownClick() {
  $(".dropdown-item").click(function () {
    var dropdownButton = $(this).closest(".dropdown").find(".dropdown-toggle");
    var selectedValue = $(this).attr("data-value");
    dropdownButton.text(selectedValue);
  });
};

function removeSelect(element) {
  const selectElement = element.previousElementSibling;
  const value = selectElement.value;

  const selectedIndex = selectedUnits.indexOf(value);
  const unselectedIndex = unselectedUnits.indexOf(value);

  if (selectedIndex === -1) { // if the unit is not already in the selectedUnits
    selectedUnits.push(value);
    if (unselectedIndex !== -1) { // remove from unselectedUnits if present
      unselectedUnits.splice(unselectedIndex, 1);
    }
    selectElement.style.borderColor = 'red';
    selectElement.style.backgroundColor = '#ffcccc';
  } else { // if the unit is in the selectedUnits
    selectedUnits.splice(selectedIndex, 1);
    if (unselectedIndex === -1) { // only add to unselectedUnits if not already present
      unselectedUnits.push(value);
    }
    selectElement.style.borderColor = 'blue';
    selectElement.style.backgroundColor = '#87CEEB';
  }

  selectElement.disabled = false;

  console.log("Selected Units: ", selectedUnits);
  console.log("Unselected Units: ", unselectedUnits);
}

function setupUnitSelectChange() {
  const selectElements = document.querySelectorAll(".unit-select");
  selectElements.forEach((select) => {
      select.addEventListener("change", function () {
      // Clear all existing highlights
      selectElements.forEach((select) => {
        select.style.boxShadow = "";
      });

      // Re-check and highlight prerequisites and post-requisites
      checkAndHighlightPrerequisitesAndPostreqs(this.value);
    });
  });
};

document.addEventListener("DOMContentLoaded", () => {
  const selectElements = document.querySelectorAll(".unit-select");
  selectElements.forEach((select) => {
    selectedUnits.push(select.value);
  });
  setupCheckPrereqButtons();
  setupDropdownClick();
  setupUnitSelectChange();
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

$('#submit-button').click(function(e) {
  e.preventDefault();
  setTimeout(function() {
      $.ajax({
          url: '/fetch-database',
          type: 'GET',
          success: function(data) {
              // First call to updatePlanner
              updatePlanner(data.new_plan);

              // Call to updateYearsAndSemesters
              updateYearsAndSemesters(data.num_years, data.new_plan, data.all_units, () => {
                  // Second call to updatePlanner inside the callback to ensure it runs after updateYearsAndSemesters
                  updatePlanner(data.new_plan);
              });
          },
          error: function(error) {
              console.error('Error fetching the new plan', error);
          }
      });
  }, 2000);
});

function updatePlanner(newPlan) {
  for (const [yearKey, semesters] of Object.entries(newPlan)) {
      for (const [semesterKey, units] of Object.entries(semesters)) {
          units.forEach((unit, index) => {
              const year = yearKey.split('_')[1];
              const semester = semesterKey.split('_')[1];
              const unitNum = index + 1;
              
              const selectId = `unit${unitNum}_year${year}_semester${semester}`;
              const selectElement = document.getElementById(selectId);
              
              if (selectElement) {
                selectElement.value = (unit && unit !== "None") ? unit : "OPTION";
              }
          });
      }
  }
}

function updateYearsAndSemesters(numYears, newPlan, all_units) {
  const container = document.querySelector('.container.text-center');
  const submitButton = document.querySelector('.submit-button');
  const existingYears = container.querySelectorAll('h2').length;

  let content = "";

  for (let year = existingYears + 1; year <= numYears; year++) {
      content += `<div><h2>Year ${year}</h2>`;
      for (let semester = 1; semester <= 2; semester++) {
          content += `
              <div class="semester">
                  <h3>Semester ${semester}</h3>
                  <table class="table">
                      <tr>
                          <th>Unit 1</th>
                          <th>Unit 2</th>
                          <th>Unit 3</th>
                          <th>Unit 4</th>
                      </tr>
                      <tr>`;

          for (let unit_num = 1; unit_num <= 4; unit_num++) {
              const selectId = `unit${unit_num}_year${year}_semester${semester}`;
              const unitCode = newPlan[`year_${year}`][`semester_${semester}`][unit_num - 1];

              content += `
  <td>
      <div class="select-wrapper">
          <select name="unit${unit_num}_${year}_${semester}" id="${selectId}" class="unit-select">`;
              
          // Add the selected unit as the first option
          content += `<option value="${unitCode}" selected>${unitCode}</option>`;

          for (const unit of all_units) {
              const currentUnitCode = unit[0];
              const unitSemester = unit[2]; 

              // Applying the condition from your template in JavaScript
              if (currentUnitCode !== unitCode && (unitSemester === semester || unitSemester === 12)) {
                  content += `<option value="${currentUnitCode}">${currentUnitCode}</option>`;
              }
          }

          content += `</select>
                      <span class="close-icon" onclick="removeSelect(this)">&#10006;</span>
                      <div class="form-check">
                          <input class="form-check-input check-prereq-btn" type="radio" name="prereqOption" id="checkPrereq${unit_num}_year${year}_semester${semester}" data-unit-id="${selectId}">
                      </div>                                
                  </div>
              </td>`;

          }

          content += `</tr></table></div>`;
      }
      content += '</div>';
  }

  // Create a temporary container to hold the content
  const tempContainer = document.createElement('div');
  tempContainer.innerHTML = content;

  // Insert each year's content before the submit button
  while (tempContainer.firstChild) {
      container.insertBefore(tempContainer.firstChild, submitButton);
  }

  // Apply setup functions after all new content has been added
  setupCheckPrereqButtons();
  setupDropdownClick();
  setupUnitSelectChange();
}

function toggleLegend() {
    var legend = document.getElementById("legend");
    if (legend.style.display === "none" || legend.style.display === "") {
        legend.style.display = "block";
    } else {
        legend.style.display = "none";
    }
}

function closeLegend() {
    var legend = document.getElementById("legend");
    legend.style.display = "none";
}


// Function to handle the edit button click
// console.log('{{ units | tojson | safe }}');
// var unitsData = JSON.parse('{{ units | tojson | safe }}');

// function updateUnitInfo() {
//     var selectedUnitCode = document.getElementById("unitCode").value;
//     var selectedUnit = unitsData.find(function(unit) {
//         return unit[0] === selectedUnitCode;
//     });

//     if (selectedUnit) {
//         document.getElementById("unitCodePlaceholder").textContent = selectedUnit[0];
//         document.getElementById("unitNamePlaceholder").textContent = selectedUnit[1];
//         document.getElementById("unitPointsPlaceholder").textContent = selectedUnit[2];
//         document.getElementById("semesterPlaceholder").textContent = selectedUnit[3];
//         document.getElementById("categoryIdPlaceholder").textContent = selectedUnit[4];
//     }
// }

// function saveUnit() {
//   var editedCode = document.getElementById("editUnitCode").value;
//   var editedName = document.getElementById("editUnitName").value;
//   var editedPoints = document.getElementById("editUnitPoints").value;
//   var editedSemester = document.getElementById("editUnitSemester").value;
//   var editedCategory = document.getElementById("editUnitCategory").value;

//   var selectedUnit = unitsData.find(function(unit) {
//       return unit[0] === editedCode;
//   });

//   if (selectedUnit) {
//       selectedUnit[1] = editedName;
//       selectedUnit[2] = editedPoints;
//       selectedUnit[3] = editedSemester;
//       selectedUnit[4] = editedCategory;
//       console.log("Unit information edited and saved:", selectedUnit);

//       window.location.href = "{{ url_for('staff_editing') }}";
//   }
// }


// // document.getElementById("showUnitInfo1").addEventListener("click", updateUnitInfo);
// document.getElementById("submitEdit").addEventListener("click", saveUnit);
function saveUnit() {
  var editedCode = document.getElementById("editUnitCode").value;
  var editedName = document.getElementById("editUnitName").value;
  var editedPoints = document.getElementById("editUnitPoints").value;
  var editedSemester = document.getElementById("editUnitSemester").value;
  var editedCategory = document.getElementById("editUnitCategory").value;

  var selectedUnit = unitsData.find(function(unit) {
      return unit[0] === editedCode;
  });

  if (selectedUnit) {
      selectedUnit[1] = editedName;
      selectedUnit[2] = editedPoints;
      selectedUnit[3] = editedSemester;
      selectedUnit[4] = editedCategory;
      console.log("Unit information edited and saved:", selectedUnit);

      // Redirect to the staff editing page
      window.location.href = "{{ url_for('staff_editing') }}";
  }
}


document.addEventListener('DOMContentLoaded', function () {
  const editUnitForm = document.getElementById('editUnitForm');
  const saveButton = document.getElementById('submitEdit');

  saveButton.addEventListener('click', function (event) {
      event.preventDefault();

      const unitCode = document.getElementById('editUnitCode').value;
      const unitName = document.getElementById('editUnitName').value;
      const unitPoints = document.getElementById('editUnitPoints').value;
      const unitSemester = document.getElementById('editUnitSemester').value;
      const unitCategory = document.getElementById('editUnitCategory').value;

      const jsonData = {
          unitCode: unitCode,
          unitName: unitName,
          unitPoints: unitPoints,
          unitSemester: unitSemester,
          unitCategory: unitCategory
      };

      // Send the JSON data to the server using a POST request
      fetch('/process_unit_edit', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(jsonData)
      });
      window.location.href = "/staff_editing";
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const addUnitForm = document.getElementById('addUnitForm');
  const saveButton = document.getElementById('submitAdd');

  saveButton.addEventListener('click', function (event) {
      event.preventDefault();

      const unitCode = document.getElementById('addUnitCode').value;
      const unitName = document.getElementById('addUnitName').value;
      const unitPoints = document.getElementById('addUnitPoints').value;
      const unitSemester = document.getElementById('addUnitSemester').value;
      const unitCategory = document.getElementById('addUnitCategory').value;

      const jsonData = {
          unitCode: unitCode,
          unitName: unitName,
          unitPoints: unitPoints,
          unitSemester: unitSemester,
          unitCategory: unitCategory
      };

      // Send the JSON data to the server using a POST request
      fetch('/process_unit_add', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(jsonData)
      });
      window.location.href = "/staff_editing";

  });
});

document.addEventListener('DOMContentLoaded', function () {
  const deleteUnitForm = document.getElementById('deleteUnitForm');
  const deleteButton = document.getElementById('submitDelete');

  deleteButton.addEventListener('click', function (event) {
      event.preventDefault();

      const unitCode = document.getElementById('deleteUnitCode').value;

      const jsonData = {
          unitCode: unitCode
      };

      // Send the JSON data to the server using a POST request
      fetch('/process_unit_delete', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(jsonData)
      });
      window.location.href = "/staff_editing";

  });
});



// document.addEventListener('DOMContentLoaded', function () {
//   // Handle the "Add" button click
//   document.getElementById("addUnitButton").addEventListener("click", function () {
//       // Redirect to staff_editing_new.html
//       window.location.href = "{{ url_for('staff_editing_new') }}";

//       // Sample data to send for unit addition
//       const jsonData = {
//           unitCode: "NEW123",
//           unitName: "New Unit",
//           unitPoints: "4",
//           unitSemester: "Spring",
//           unitCategory: "Category 1"
//       };

//       // Send a POST request to process the addition
//       fetch('/process_unit_add', {
//           method: 'POST',
//           headers: {
//               'Content-Type': 'application/json'
//           },
//           body: JSON.stringify(jsonData)
//       });
//       window.location.href = "/staff_editing";
//   });
// });

