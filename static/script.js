// ==========================================
// GET ELEMENTS
// ==========================================

const home = document.getElementById("home");
const researchPage = document.getElementById("researchPage");

const researchTopic = document.getElementById("researchTopic");

const bottomInput = document.getElementById("bottomInput");
const bottomResearchTopic =
    document.getElementById("bottomResearchTopic");

const userQuestion =
    document.getElementById("userQuestion");

const researchStatus =
    document.getElementById("researchStatus");

const planSection =
    document.getElementById("planSection");

const researchPlan =
    document.getElementById("researchPlan");

const resultsSection =
    document.getElementById("resultsSection");

const researchResults =
    document.getElementById("researchResults");


// ==========================================
// SET EXAMPLE TOPIC
// ==========================================

function setTopic(topic) {

    researchTopic.value = topic;

    researchTopic.focus();
}


// ==========================================
// NEW RESEARCH
// ==========================================

function newResearch() {

    home.classList.remove("hidden");

    researchPage.classList.add("hidden");

    bottomInput.classList.add("hidden");

    researchTopic.value = "";

    userQuestion.innerText = "";

    researchStatus.innerText =
        "🔎 Starting research...";

    researchPlan.innerHTML = "";

    researchResults.innerHTML = "";

    planSection.classList.add("hidden");

    resultsSection.classList.add("hidden");

    researchTopic.focus();
}


// ==========================================
// START RESEARCH
// ==========================================

async function startResearch() {

    const topic =
        researchTopic.value.trim();

    if (!topic) {

        alert(
            "Please enter a research topic."
        );

        researchTopic.focus();

        return;
    }


    // Show research page

    home.classList.add("hidden");

    researchPage.classList.remove("hidden");

    bottomInput.classList.remove("hidden");


    // Display user's question

    userQuestion.innerText = topic;


    // Reset previous results

    researchPlan.innerHTML = "";

    researchResults.innerHTML = "";

    planSection.classList.add("hidden");

    resultsSection.classList.add("hidden");


    // Show status

    researchStatus.innerText =
        "🧠 Creating research plan...";


    try {

        const response =
            await fetch("/research", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    question: topic
                })

            });


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Research request failed."
            );

        }


        // Display research plan

        displayResearchPlan(
            data.plan
        );


        // Display research results

        displayResearchResults(
            data.results
        );


        researchStatus.innerText =
            "✅ Research completed";


    } catch (error) {

        console.error(error);

        researchStatus.innerText =
            "❌ Research failed";

        researchResults.innerHTML = `
            <div class="result-card">
                <p>
                    ${escapeHtml(error.message)}
                </p>
            </div>
        `;

        resultsSection.classList.remove(
            "hidden"
        );
    }
}


// ==========================================
// DISPLAY RESEARCH PLAN
// ==========================================

function displayResearchPlan(plan) {

    if (!plan) {

        return;
    }


    const areas =
        plan.research_areas || [];


    researchPlan.innerHTML = "";


    areas.forEach(
        (area, index) => {

            const item =
                document.createElement("div");

            item.className =
                "plan-item";


            item.innerHTML = `

                <strong>
                    ${index + 1}. ${escapeHtml(area.title)}
                </strong>

                <span>
                    ${escapeHtml(area.question)}
                </span>

            `;


            researchPlan.appendChild(
                item
            );
        }
    );


    planSection.classList.remove(
        "hidden"
    );
}


// ==========================================
// DISPLAY RESEARCH RESULTS
// ==========================================

function displayResearchResults(
    results
) {

    if (!results ||
        results.length === 0) {

        researchResults.innerHTML = `
            <div class="result-card">
                <p>
                    No research results were returned.
                </p>
            </div>
        `;

        resultsSection.classList.remove(
            "hidden"
        );

        return;
    }


    researchResults.innerHTML = "";


    results.forEach(
        (result, index) => {

            const card =
                document.createElement("div");

            card.className =
                "result-card";


            card.innerHTML = `

                <h3>
                    ${index + 1}.
                    ${escapeHtml(result.title)}
                </h3>

                <p>
                    ${formatResearchText(
                        result.result
                    )}
                </p>

            `;


            researchResults.appendChild(
                card
            );
        }
    );


    resultsSection.classList.remove(
        "hidden"
    );
}


// ==========================================
// BOTTOM INPUT
// ==========================================

function startResearchFromBottom() {

    const topic =
        bottomResearchTopic.value.trim();


    if (!topic) {

        bottomResearchTopic.focus();

        return;
    }


    researchTopic.value = topic;

    bottomResearchTopic.value = "";


    startResearch();
}


// ==========================================
// ENTER KEY
// ==========================================

researchTopic.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            startResearch();
        }

    }
);


bottomResearchTopic.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            startResearchFromBottom();
        }

    }
);


// ==========================================
// FORMAT RESEARCH TEXT
// ==========================================

function formatResearchText(text) {

    if (!text) {

        return "";
    }


    return escapeHtml(text)
        .replace(/\n/g, "<br>");
}


// ==========================================
// HTML SAFETY
// ==========================================

function escapeHtml(text) {

    if (text === null ||
        text === undefined) {

        return "";
    }


    const div =
        document.createElement("div");

    div.textContent =
        String(text);

    return div.innerHTML;
}