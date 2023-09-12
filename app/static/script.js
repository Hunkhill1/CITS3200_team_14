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

(document).ready(function () {
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
            
            // Change the border color of the select box to red
            selectElement.style.borderColor = 'red';
            
            // You can also add additional styling as needed
            // For example, change the background color
            selectElement.style.backgroundColor = '#ffcccc';

            // Optionally, you can disable the select box to prevent further changes
            selectElement.disabled = true;

            // Log the selected units (you can do whatever you want with this array)
            console.log("Selected Units: ", selectedUnits);
        }


        document.addEventListener("DOMContentLoaded", () => {
            // Add initial select values to the array
            const selectElements = document.querySelectorAll(".unit-select");
            selectElements.forEach((select) => {
                selectedUnits.push(select.value);
            });
        });