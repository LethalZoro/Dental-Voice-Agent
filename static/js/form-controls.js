// Form controls for the patient data and call form

document.addEventListener("DOMContentLoaded", function () {
  // Elements
  const dataCards = document.querySelectorAll(".data-card");
  const collapseAllBtn = document.getElementById("collapseAllBtn");
  const expandAllBtn = document.getElementById("expandAllBtn");
  const callForm = document.getElementById("callForm");
  const verifyDataCheck = document.getElementById("verifyDataCheck");
  const submitBtn = document.querySelector(".call-btn");
  const progressBar = document.querySelector(
    "#dataCompletionBar .progress-bar"
  );
  const requiredInputs = document.querySelectorAll(
    "input[required], select[required]"
  );

  // Initialize form validation state
  updateFormValidationState();

  // Data cards toggle
  dataCards.forEach((card) => {
    const header = card.querySelector(".data-card-header");
    const body = card.querySelector(".collapse");
    const icon = header.querySelector(".fas.fa-chevron-down");

    // Use Bootstrap's collapse events instead of direct click handler
    $(body).on("show.bs.collapse", function () {
      icon.style.transform = "rotate(0deg)";
    });

    $(body).on("hide.bs.collapse", function () {
      icon.style.transform = "rotate(-90deg)";
    });
  });

  // Collapse/Expand all sections
  collapseAllBtn.addEventListener("click", function () {
    dataCards.forEach((card) => {
      const body = card.querySelector(".collapse");
      const icon = card.querySelector(".fas.fa-chevron-down");
      body.classList.remove("show");
      icon.style.transform = "rotate(-90deg)";
    });
  });

  expandAllBtn.addEventListener("click", function () {
    dataCards.forEach((card) => {
      const body = card.querySelector(".collapse");
      const icon = card.querySelector(".fas.fa-chevron-down");
      body.classList.add("show");
      icon.style.transform = "rotate(0deg)";
    });
  });

  // Form validation
  requiredInputs.forEach((input) => {
    input.addEventListener("input", updateFormValidationState);
    input.addEventListener("change", updateFormValidationState);
  });

  verifyDataCheck.addEventListener("change", updateSubmitButton);

  // Form submission
  callForm.addEventListener("submit", function (e) {
    if (!isFormValid() || !verifyDataCheck.checked) {
      e.preventDefault();
      alert(
        "Please complete all required fields and verify your data before making a call."
      );
      highlightEmptyFields();
    }
  });

  // Functions
  function updateFormValidationState() {
    const totalFields = requiredInputs.length;
    let filledFields = 0;

    requiredInputs.forEach((input) => {
      if (input.value.trim() !== "") {
        filledFields++;
        input.classList.remove("is-invalid");
      }
    });

    const percentage = Math.round((filledFields / totalFields) * 100);
    progressBar.style.width = percentage + "%";
    progressBar.setAttribute("aria-valuenow", percentage);

    // Update color based on completion
    if (percentage < 50) {
      progressBar.classList.remove("bg-warning", "bg-success");
      progressBar.classList.add("bg-danger");
    } else if (percentage < 100) {
      progressBar.classList.remove("bg-danger", "bg-success");
      progressBar.classList.add("bg-warning");
    } else {
      progressBar.classList.remove("bg-danger", "bg-warning");
      progressBar.classList.add("bg-success");
    }

    updateSubmitButton();
  }

  function updateSubmitButton() {
    if (isFormValid() && verifyDataCheck.checked) {
      submitBtn.disabled = false;
      submitBtn.classList.remove("btn-secondary");
      submitBtn.classList.add("btn-primary");
    } else {
      submitBtn.disabled = true;
      submitBtn.classList.remove("btn-primary");
      submitBtn.classList.add("btn-secondary");
    }
  }

  function isFormValid() {
    let valid = true;
    requiredInputs.forEach((input) => {
      if (input.value.trim() === "") {
        valid = false;
      }
    });
    return valid;
  }

  function highlightEmptyFields() {
    requiredInputs.forEach((input) => {
      if (input.value.trim() === "") {
        input.classList.add("is-invalid");

        // Find the parent data-card and expand it
        let parent = input.closest(".collapse");
        if (parent) {
          parent.classList.add("show");
          const icon = parent.previousElementSibling.querySelector(
            ".fas.fa-chevron-down"
          );
          if (icon) {
            icon.style.transform = "rotate(0deg)";
          }
        }
      }
    });
  }

  // Initial check
  updateSubmitButton();
});
