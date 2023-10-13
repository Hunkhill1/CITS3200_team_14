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
              updateYearsAndSemesters(data.num_years, data.new_plan, () => {
                  // This will be called after the DOM is updated
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

function updateYearsAndSemesters(numYears, newPlan) {
  const container = document.querySelector('.container.text-center');
  const submitButton = document.querySelector('.submit-button');
  // Find the existing number of years
  const existingYears = container.querySelectorAll('h2').length;

  let content = "";

  // Iterate only over the new years
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
            
            // Get the unit code for this unit number from new_plan
            const unitCode = newPlan[`year_${year}`][`semester_${semester}`][unit_num - 1];
            
            content += `
                  <td>
                      <div class="select-wrapper">
                          <select name="unit${unit_num}_${year}_${semester}" id="${selectId}" class="unit-select">

                          </select>
                          <span class="close-icon" onclick="removeSelect(this)">&#10006;</span>
                          <div class="form-check">
                              <input class="form-check-input check-prereq-btn" type="radio" name="prereqOption" id="checkPrereq${unit_num}_year${year}_semester${semester}" data-unit-id="${selectId}">
                          </div>                                
                      </div>
                  </td>`;
          }
          content += `
                      </tr>
                  </table>
              </div>`;
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
