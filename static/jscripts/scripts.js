document.addEventListener("DOMContentLoaded", function () {
    const actionInput = document.getElementById("action");

    actionInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevent the default form submission
            document.querySelector("form").submit(); // Submit the form
        }
    });
});
