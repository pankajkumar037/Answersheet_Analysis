document.getElementById("upload-form").addEventListener("submit", async function(e) {
    e.preventDefault();

    const questionPaper = document.getElementById("question_paper").files[0];
    const answerSheets = document.getElementById("answer_sheets").files;

    const formData = new FormData();

    if (questionPaper) {
        formData.append("question_paper", questionPaper);
        document.getElementById("question-preview").classList.remove("d-none");
        document.getElementById("pdf-preview").src = URL.createObjectURL(questionPaper);
    } else {
        document.getElementById("question-preview").classList.add("d-none");
        document.getElementById("pdf-preview").src = "";
    }

    const answersPreviewDiv = document.getElementById("answers-preview");
    answersPreviewDiv.innerHTML = ""; 
    if (answerSheets.length > 0) {
        document.getElementById("answers-preview").classList.remove("d-none");
        for (const file of answerSheets) {
            formData.append("answer_sheets", file);
            const img = document.createElement("img");
            img.src = URL.createObjectURL(file);
            img.classList.add("img-thumbnail");
            answersPreviewDiv.appendChild(img);
        }
    } else {
        document.getElementById("answers-preview").classList.add("d-none");
    }

    const spinner = document.getElementById("spinner");
    const resultsSection = document.getElementById("results-section");
    const chartsContainer = document.getElementById("charts-container");
    const resultsText = document.getElementById("results-text");
    const downloadLink = document.getElementById("download-link");

    resultsSection.style.display = "none";
    spinner.style.display = "block";
    chartsContainer.innerHTML = ""; 
    resultsText.textContent = "";
    downloadLink.classList.add("d-none");

    const res = await fetch("/api/upload", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    spinner.style.display = "none";
    resultsSection.style.display = "block";
    downloadLink.classList.remove("d-none");
    resultsText.textContent = JSON.stringify(data.insights, null, 2);

    // Render charts if data.charts is available as base64 images
    if (data.charts && data.charts.length > 0) {
        chartsContainer.innerHTML = ""; 
        data.charts.forEach(chartData => {
            const img = document.createElement('img');
            img.src = chartData.image;
            img.alt = chartData.id; 
            img.classList.add('img-fluid', 'mb-3'); 
            chartsContainer.appendChild(img);
        });
    } else {
        chartsContainer.innerHTML = "<p class='text-muted'>No charts to display.</p>";
    }
});