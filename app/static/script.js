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
