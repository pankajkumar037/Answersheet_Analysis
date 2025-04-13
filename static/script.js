document.getElementById("upload-form").addEventListener("submit", async function(e) {
    e.preventDefault();

    const answerSheet = document.getElementById("answer_sheet").files[0];
    const questionPaper = document.getElementById("question_paper").files[0];

    if (!answerSheet && !questionPaper) {
        alert("Please upload at least one file!");
        return;
    }

    const formData = new FormData();
    if (answerSheet) {
        formData.append("answer_sheet", answerSheet);
        document.getElementById("answer-preview").src = URL.createObjectURL(answerSheet);
    }

    if (questionPaper) {
        formData.append("question_paper", questionPaper);
        document.getElementById("question-preview").src = URL.createObjectURL(questionPaper);
    }

    document.getElementById("preview").classList.remove("d-none");

    const resultSection = document.getElementById("result-section");
    const spinner = document.getElementById("spinner");

    resultSection.style.display = "none";
    spinner.style.display = "block"; 

    const res = await fetch("/api/upload", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    spinner.style.display = "none";
    document.getElementById("result").textContent = JSON.stringify(data, null, 2);
    resultSection.style.display = "block";
});