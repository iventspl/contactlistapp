document.querySelectorAll('form[data-validate]').forEach((form) => {
    // Done here, not in HTML. Without JavaScript the browser native validation still works
    form.noValidate = true;

    form.addEventListener('submit', (e) => {
        const fields = [...form.elements].filter((field) => field.willValidate);
        fields.forEach(showFieldValidity);

        if (!form.checkValidity()) {
            e.preventDefault();
            fields.find((field) => !field.validity.valid)?.focus();
        }
    });

    // Recheck a field while the user is fixing it.
    form.addEventListener('input', (e) => {
        if (e.target.classList.contains('is-invalid')) {
            showFieldValidity(e.target);
        }
    });
});

function showFieldValidity(field) {
    const feedback = getFeedbackElement(field);

    if (field.validity.valid) {
        field.classList.remove('is-invalid');
        feedback.textContent = '';
        return;
    }

    field.classList.add('is-invalid');
    feedback.textContent = field.validity.patternMismatch && field.dataset.patternMessage
        ? field.dataset.patternMessage
        : field.validationMessage;
}

function getFeedbackElement(field) {
    let feedback = field.parentElement.querySelector('.js-invalid-feedback');
    if (!feedback) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback js-invalid-feedback';
        field.insertAdjacentElement('afterend', feedback);
    }
    return feedback;
}
