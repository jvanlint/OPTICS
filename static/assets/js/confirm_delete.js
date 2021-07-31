document.addEventListener('DOMContentLoaded', () => {
    var buttons = document.querySelectorAll("[data-target='#confirmModal']");
    for (const button of buttons) {
        button.addEventListener("click", function(event) {
            // find the modal and add the caller-id as an attribute
            var modal = document.getElementById("confirmModal");
            modal.setAttribute("caller-id", this.getAttribute("id"));

            // extract texts from calling element and replace the modals texts with it
            if ("message" in this.dataset) {
                document.getElementById("modal-message").innerHTML = this.dataset.message;
            };
            if ("buttontext" in this.dataset) {
                document.getElementById("confirmButtonModal").innerHTML = this.dataset.buttontext;
            };
        })
    }

    document.getElementById("confirmButtonModal").onclick = () => {
        // when the Confirm Button in the modal is clicked
        var button_clicked = event.target
        var caller_id = button_clicked.closest("#confirmModal").getAttribute("caller-id");
        var caller = document.getElementById(caller_id);
        // open the url that was specified for the caller
        window.location = caller.getAttribute("href");
    };
});