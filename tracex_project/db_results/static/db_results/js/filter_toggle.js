$(document).ready(function () {
    $("#toggleButton1").click(function () {
        $("#contentWrapper1").toggle();
    });

    $("#toggleButton2").click(function () {
        $("#contentWrapper2").toggle();
    });

    const ageSlider = document.getElementById('age-slider');
    const minAgeField = document.getElementById('min-age');
    const maxAgeField = document.getElementById('max-age');

    const minAgeInitial = minAgeField.value || 0;
    const maxAgeInitial = maxAgeField.value || 100;

    const ageValues = [minAgeInitial, maxAgeInitial];

    noUiSlider.create(ageSlider, {
        start: ageValues,
        connect: true,
        range: {
            'min': 0,
            'max': 100
        }
    });

    minAgeField.addEventListener('change', function () {
        ageSlider.noUiSlider.set([this.value, null]);
    });
    maxAgeField.addEventListener('change', function () {
        ageSlider.noUiSlider.set([null, this.value]);
    });

    ageSlider.noUiSlider.on('update', function (values, handle) {
        minAgeField.value = Math.round(values[0]);
        maxAgeField.value = Math.round(values[1]);
    });

    document.getElementById('toggleAll').addEventListener('change', function() {
        const checkboxes = document.querySelectorAll('.origin-checkbox input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
        });
    });
    document.getElementById('toggleGender').addEventListener('change', function () {
        const checkboxes = document.querySelectorAll('input[name="gender"]');
        checkboxes.forEach(checkbox => checkbox.checked = this.checked);
    });

    document.getElementById('toggleCondition').addEventListener('change', function () {
        const checkboxes = document.querySelectorAll('input[name="condition"]');
        checkboxes.forEach(checkbox => checkbox.checked = this.checked);
    });

    document.getElementById('togglePreexistingCondition').addEventListener('change', function () {
        const checkboxes = document.querySelectorAll('input[name="preexisting_condition"]');
        checkboxes.forEach(checkbox => checkbox.checked = this.checked);
    });
});
