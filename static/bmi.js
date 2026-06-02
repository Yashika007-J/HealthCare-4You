document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('bmi-form');
    const result = document.getElementById('result');

    if (!form || !result) {
        return;
    }

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const weight = parseFloat(document.getElementById('weight').value);
        const heightCm = parseFloat(document.getElementById('height').value);

        if (!weight || !heightCm || weight <= 0 || heightCm <= 0) {
            result.textContent = 'Please enter valid positive values for weight and height.';
            result.style.color = 'red';
            return;
        }

        const heightM = heightCm / 100;
        const bmi = weight / (heightM * heightM);
        const category = getBmiCategory(bmi);

        result.innerHTML = `Your BMI is <strong>${bmi.toFixed(1)}</strong> (${category}).`;
        result.style.color = '#111';
    });
});

function getBmiCategory(bmi) {
    if (bmi < 18.5) {
        return 'Underweight';
    }
    if (bmi < 25) {
        return 'Normal weight';
    }
    if (bmi < 30) {
        return 'Overweight';
    }
    return 'Obese';
}

