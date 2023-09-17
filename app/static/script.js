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
    
    selectElement.disabled = false;

    console.log("Selected Units: ", selectedUnits);
}

document.addEventListener("DOMContentLoaded", () => {
    const selectElements = document.querySelectorAll(".unit-select");
    selectElements.forEach((select) => {
        selectedUnits.push(select.value);
    });
});

