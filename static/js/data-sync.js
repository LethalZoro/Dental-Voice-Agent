// Sync patient data between forms
document.addEventListener("DOMContentLoaded", function () {
  // Sync fields between insured and patient when relationship is SELF
  const relationshipSelect = document.getElementById("relationship_to_patient");
  const insuredName = document.getElementById("insured_name");
  const insuredDob = document.getElementById("insured_dob");
  const patientName = document.getElementById("patient_name");
  const patientDob = document.getElementById("patient_dob");

  if (
    relationshipSelect &&
    insuredName &&
    insuredDob &&
    patientName &&
    patientDob
  ) {
    relationshipSelect.addEventListener("change", function () {
      if (this.value === "SELF") {
        // Set up two-way sync
        syncFields(insuredName, patientName);
        syncFields(insuredDob, patientDob);
      } else {
        // Remove sync
        removeSync(insuredName, patientName);
        removeSync(insuredDob, patientDob);
      }
    });

    // Initialize sync if relationship is SELF
    if (relationshipSelect.value === "SELF") {
      syncFields(insuredName, patientName);
      syncFields(insuredDob, patientDob);
    }
  }

  // Helper functions
  function syncFields(field1, field2) {
    const syncHandler = function () {
      field2.value = field1.value;
    };

    const reverseHandler = function () {
      field1.value = field2.value;
    };

    field1.addEventListener("input", syncHandler);
    field2.addEventListener("input", reverseHandler);

    // Store handlers for later removal
    field1.syncHandler = syncHandler;
    field2.syncHandler = reverseHandler;
  }

  function removeSync(field1, field2) {
    if (field1.syncHandler) {
      field1.removeEventListener("input", field1.syncHandler);
      field1.syncHandler = null;
    }

    if (field2.syncHandler) {
      field2.removeEventListener("input", field2.syncHandler);
      field2.syncHandler = null;
    }
  }
});
