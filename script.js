document.addEventListener('DOMContentLoaded', function() {
    const healthForm = document.getElementById('health-form');
    const heartRateInput = document.getElementById('heart-rate');
    const stepsInput = document.getElementById('steps');

    healthForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const heartRate = heartRateInput.value;
        const steps = stepsInput.value;

        fetch('/health_metrics', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                heart_rate: heartRate,
                steps: steps
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Health metric added successfully!');
                heartRateInput.value = '';
                stepsInput.value = '';
            } else {
                alert('Error adding health metric.');
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
