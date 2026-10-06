// event delegation for all forms with data-confirm
document.body.addEventListener('submit', (e) => {
    const submittedForm = e.target.closest('form[data-confirm]');
    if (submittedForm) {
        const confirmMessage = submittedForm.dataset.confirm;
        const userDecision = window.confirm(confirmMessage);
        if (!userDecision) e.preventDefault();
    }
});