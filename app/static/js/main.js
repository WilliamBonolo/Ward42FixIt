document.addEventListener('DOMContentLoaded', () => {
    
    // ==========================================
    // 1. CLIENT-SIDE VALIDATION (Report Form)
    // ==========================================
    const reportForm = document.getElementById('reportForm');
    if (reportForm) {
        const description = document.getElementById('description');
        const cell = document.getElementById('reporter_cell');
        const descError = document.getElementById('descError');
        const cellError = document.getElementById('cellError');

        reportForm.addEventListener('submit', (e) => {
            let isValid = true;

            // Validate Description length
            if (description.value.length < 10 || description.value.length > 500) {
                descError.textContent = "Description must be between 10 and 500 characters.";
                descError.style.display = "block";
                isValid = false;
            } else {
                descError.style.display = "none";
            }

            // Validate SA Cell Number (10 digits, starting with 0)
            const cellRegex = /^0[0-9]{9}$/;
            if (!cellRegex.test(cell.value)) {
                cellError.textContent = "Please enter a valid 10-digit SA cell number starting with 0.";
                cellError.style.display = "block";
                isValid = false;
            } else {
                cellError.style.display = "none";
            }

            if (!isValid) {
                e.preventDefault(); // Stop form submission if errors exist
            }
        });
    }

    // ==========================================
    // 2. LIVE TABLE FILTER (Dashboard)
    // ==========================================
    const filterCategory = document.getElementById('filterCategory');
    const filterStatus = document.getElementById('filterStatus');
    const tableRows = document.querySelectorAll('.report-row');

    if (filterCategory && filterStatus && tableRows.length > 0) {
        const filterTable = () => {
            const catValue = filterCategory.value.toLowerCase();
            const statValue = filterStatus.value.toLowerCase();

            tableRows.forEach(row => {
                const rowCategory = row.getAttribute('data-category').toLowerCase();
                const rowStatus = row.getAttribute('data-status').toLowerCase();

                const matchesCategory = catValue === "" || rowCategory === catValue;
                const matchesStatus = statValue === "" || rowStatus === statValue;

                if (matchesCategory && matchesStatus) {
                    row.style.display = ""; // Show
                } else {
                    row.style.display = "none"; // Hide
                }
            });
        };

        filterCategory.addEventListener('change', filterTable);
        filterStatus.addEventListener('change', filterTable);
    }

    // ==========================================
    // 3. SAVED DRAFT (localStorage)
    // ==========================================
    // Only apply on the report page
    if (reportForm) {
        const streetInput = document.getElementById('street');
        const categoryInput = document.getElementById('category');
        const descInput = document.getElementById('description');

        // Load draft on page load
        try {
            const savedDraft = JSON.parse(localStorage.getItem('reportDraft'));
            if (savedDraft) {
                if (savedDraft.street) streetInput.value = savedDraft.street;
                if (savedDraft.category) categoryInput.value = savedDraft.category;
                if (savedDraft.description) descInput.value = savedDraft.description;
            }
        } catch (error) {
            console.error("Error loading draft:", error);
        }

        // Save draft as user types (excluding PII like name and cell)
        const saveDraft = () => {
            try {
                const draft = {
                    street: streetInput.value,
                    category: categoryInput.value,
                    description: descInput.value
                };
                localStorage.setItem('reportDraft', JSON.stringify(draft));
            } catch (error) {
                console.error("Error saving draft:", error);
            }
        };

        streetInput.addEventListener('input', saveDraft);
        categoryInput.addEventListener('change', saveDraft);
        descInput.addEventListener('input', saveDraft);

        // Clear draft on successful submit
        reportForm.addEventListener('submit', () => {
            localStorage.removeItem('reportDraft');
        });
    }
});