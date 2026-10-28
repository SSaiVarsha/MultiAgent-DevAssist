let generatedTestCode = "";


function extractPythonTests(text) {

    if (!text) {
        return "";
    }

    return text.trim();
}


function getLanguage() {

    return document.getElementById("languageSelect").value;

}


async function runCode() {
    const code = document.getElementById("code").value;
    const language = getLanguage();
    const fileName = document.getElementById("fileName").textContent;
    const terminal = document.getElementById("terminalOutput");
    const button = document.getElementById("runButton");

    if (!code.trim()) {
        terminal.textContent = "Please enter some code first.";
        return;
    }

    button.disabled = true;
    button.textContent = "⏳ Running...";
    terminal.textContent =
        `▶ Saving ${fileName}...\n\n`;

    try {
        // First save the current file
        const saveResponse = await fetch("/project/file", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                file: fileName,
                code: code
            })
        });

        const saveData = await saveResponse.json();

        if (!saveData.success) {
            throw new Error("Could not save file: " + saveData.error);
        }

        terminal.textContent =
            `✓ Saved: ${fileName}\n\n` +
            `▶ Running ${language}...\n\n`;

        // Then execute the code
        const response = await fetch("/execute", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                language: language,
                code: code
            })
        });

        if (!response.ok) {
            throw new Error("Server error: " + response.status);
        }

        const data = await response.json();

        if (data.success) {
            terminal.textContent =
                `✓ Saved: ${fileName}\n\n` +
                `▶ Running ${language}...\n\n` +
                data.output +
                "\nProcess finished successfully.";
        } else {
    terminal.textContent =
        `✓ Saved: ${fileName}\n\n` +
        `▶ Running ${language}...\n\n` +
        "❌ Execution Error\n\n" +
        data.error +
        "\n\n🐛 DevAssist is analyzing the error...";

    await analyzeExecutionError(
        code,
        data.error
    );
}

    } catch (error) {
        terminal.textContent =
            "❌ Could not run code.\n\n" +
            error.message;
    } finally {
        button.disabled = false;
        button.textContent = "▶ Run";
    }
}

function changeLanguage() {

    const language =
        document.getElementById("languageSelect").value;

    const fileName =
        document.getElementById("fileName");

    const code =
        document.getElementById("code");


    if (language === "python") {

        fileName.textContent = "main.py";

        code.value =
`def calculate_total(price, quantity):
    return price * quantity


total = calculate_total(100, 5)

print(total)`;

    }


    else if (language === "java") {

        fileName.textContent = "Main.java";

        code.value =
`public class Main {

    public static void main(String[] args) {

        int result = 10 + 20;

        System.out.println(result);

    }

}`;

    }


    else if (language === "cpp") {

        fileName.textContent = "main.cpp";

        code.value =
`#include <iostream>

using namespace std;

int main() {

    int result = 10 + 20;

    cout << result << endl;

    return 0;
}`;

    }


    else if (language === "javascript") {

        fileName.textContent = "main.js";

        code.value =
`function calculateTotal(price, quantity) {

    return price * quantity;

}

console.log(calculateTotal(10, 20));`;

    }

}

async function loadProjectFiles() {
    const sidebar = document.querySelector(".sidebar");

    try {
        const response = await fetch("/project/files");
        const data = await response.json();

        // Keep the PROJECT title and project name
        sidebar.innerHTML = `
    <div class="panel-title">PROJECT</div>
    <div class="project-name">📁 MyProject</div>
    <button class="new-file-button" onclick="createNewFile()">＋ New File</button>
`;

        if (data.files.length === 0) {
            sidebar.innerHTML += `
                <div class="file">No files</div>
            `;
            return;
        }

        data.files.forEach(fileName => {
    const fileElement = document.createElement("div");

    fileElement.className = "file";

    fileElement.innerHTML = `
        <span class="file-name">📄 ${fileName}</span>
        <span class="file-actions">
            <button onclick="renameFile(event, '${fileName}')">✏️</button>
            <button onclick="deleteFile(event, '${fileName}')">🗑️</button>
        </span>
    `;

    fileElement.querySelector(".file-name").onclick = function () {
        openProjectFile(fileName);
    };

    sidebar.appendChild(fileElement);
});

    } catch (error) {
        console.error("Could not load project files:", error);
    }
}


async function openProjectFile(fileName) {
    try {
        const response = await fetch(
            `/project/file/${encodeURIComponent(fileName)}`
        );

        const data = await response.json();

        if (!data.success) {
            alert(data.error);
            return;
        }

        document.getElementById("fileName").textContent = fileName;
        document.getElementById("code").value = data.code;

        // Change language automatically based on extension
        if (fileName.endsWith(".py")) {
            document.getElementById("languageSelect").value = "python";
        } else if (fileName.endsWith(".java")) {
            document.getElementById("languageSelect").value = "java";
        } else if (fileName.endsWith(".cpp")) {
            document.getElementById("languageSelect").value = "cpp";
        } else if (fileName.endsWith(".js")) {
            document.getElementById("languageSelect").value = "javascript";
        }

    } catch (error) {
        alert("Could not open file: " + error.message);
    }
}


window.addEventListener("load", loadProjectFiles);


async function saveCurrentFile() {
    const fileName = document.getElementById("fileName").textContent;
    const code = document.getElementById("code").value;

    if (!fileName || fileName === "main.py") {
        // main.py is still a valid file, so continue
    }

    try {
        const response = await fetch("/project/file", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                file: fileName,
                code: code
            })
        });

        const data = await response.json();

        if (data.success) {
            const terminal = document.getElementById("terminalOutput");

            terminal.textContent =
                `✓ Saved: ${fileName}\n\n` +
                `Location: workspace/${fileName}`;
        } else {
            alert("Save failed: " + data.error);
        }

    } catch (error) {
        alert("Could not save file: " + error.message);
    }
}

async function createNewFile() {
    const fileName = prompt("Enter the file name:");

    if (!fileName || !fileName.trim()) {
        return;
    }

    const cleanName = fileName.trim();

    try {
        const response = await fetch("/project/file", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                file: cleanName,
                code: ""
            })
        });

        const data = await response.json();

        if (!data.success) {
            alert("Could not create file: " + data.error);
            return;
        }

        await loadProjectFiles();

        await openProjectFile(cleanName);

    } catch (error) {
        alert("Could not create file: " + error.message);
    }
}


async function renameFile(event, oldName) {
    event.stopPropagation();

    const newName = prompt(
        "Enter the new file name:",
        oldName
    );

    if (!newName || !newName.trim()) {
        return;
    }

    const cleanName = newName.trim();

    try {
        const response = await fetch(
            `/project/file/${encodeURIComponent(oldName)}`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    new_name: cleanName
                })
            }
        );

        const data = await response.json();

        if (!data.success) {
            alert("Rename failed: " + data.error);
            return;
        }

        await loadProjectFiles();

        // If the renamed file was currently open
        if (
            document.getElementById("fileName").textContent === oldName
        ) {
            document.getElementById("fileName").textContent = cleanName;
        }

    } catch (error) {
        alert("Could not rename file: " + error.message);
    }
}

async function deleteFile(event, fileName) {
    event.stopPropagation();

    const confirmed = confirm(
        `Are you sure you want to delete "${fileName}"?`
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(
            `/project/file/${encodeURIComponent(fileName)}`,
            {
                method: "DELETE"
            }
        );

        const data = await response.json();

        if (!data.success) {
            alert("Delete failed: " + data.error);
            return;
        }

        await loadProjectFiles();

        // Clear editor if deleted file was open
        if (
            document.getElementById("fileName").textContent === fileName
        ) {
            document.getElementById("fileName").textContent = "No file";
            document.getElementById("code").value = "";
        }

    } catch (error) {
        alert("Could not delete file: " + error.message);
    }
}

async function analyzeWithAgent(agentType) {

    const code =
        document.getElementById("code").value;

    const requirement =
        document.getElementById("requirement").value;

    const resultsSection =
        document.getElementById("results");

    const agentsDiv =
        document.getElementById("agents");

    const reportDiv =
        document.getElementById("report");

    const viewButton =
        document.getElementById("viewAnalysisButton");

    if (!code.trim()) {
        alert("Please enter some code first.");
        return;
    }

    const agents = {
        debug: {
            name: "Debugging Agent",
            icon: "🐛",
            type: "DEBUG"
        },

        review: {
            name: "Code Review Agent",
            icon: "🔍",
            type: "CODE_REVIEW"
        },

        optimization: {
            name: "Optimization Agent",
            icon: "⚡",
            type: "OPTIMIZATION"
        },

        documentation: {
            name: "Documentation Agent",
            icon: "📚",
            type: "DOCUMENTATION"
        },

        test: {
            name: "Test Case Agent",
            icon: "🧪",
            type: "TEST_CASE"
        },

        security: {
            name: "Security Agent",
            icon: "🔐",
            type: "SECURITY"
        },

        complex: {
            name: "Complex Analysis Agent",
            icon: "🧠",
            type: "COMPLEX"
        }
    };

    const selectedAgent = agents[agentType];

    console.log("agentType:", agentType);
    console.log("selectedAgent:", selectedAgent);
    console.log("agent type sent:", selectedAgent?.type);

    if (!selectedAgent) {
        alert("Unknown AI agent.");
        return;
    }

    resultsSection.classList.remove("hidden");

    if (viewButton) {
        viewButton.classList.add("hidden");
    }

    agentsDiv.innerHTML = `

        <div class="analysis-top">

            <div>
                <h3>Selected Agent</h3>
                <p>
                    ${selectedAgent.icon}
                    ${selectedAgent.name}
                </p>
            </div>

        </div>

        <div class="agent-results">

            <div class="agent-card">

                <div class="agent-card-header">

                    <span>
                        ${selectedAgent.icon}
                    </span>

                    <strong>
                        ${selectedAgent.name}
                    </strong>

                </div>

                <div class="loading">
                    🤖 ${selectedAgent.name} is analyzing your code...
                </div>

            </div>

        </div>
    `;

    reportDiv.innerHTML = "";

    try {

        const response = await fetch(
            "/analyze/agent",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
    request: selectedAgent.type,
    code: code,
    requirement: requirement
})
            }
        );

        if (!response.ok) {
            throw new Error(
                "AI server error: " +
                response.status
            );
        }

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error);
        }
        if (selectedAgent.type === "TEST_CASE") {

    generatedTestCode =
        extractPythonTests(data.result);
}
// Extract corrected code from Security Agent output
let securityFixedCode = "";

if (selectedAgent.type === "SECURITY") {
    const result = data.result || "";

    const startMarker = "SECURITY_FIXED_CODE_START";
    const endMarker = "SECURITY_FIXED_CODE_END";

    const startIndex = result.indexOf(startMarker);
    const endIndex = result.indexOf(endMarker);

    if (
        startIndex !== -1 &&
        endIndex !== -1 &&
        endIndex > startIndex
    ) {
        securityFixedCode = result
            .substring(
                startIndex + startMarker.length,
                endIndex
            )
            .trim();

        // Remove Markdown code fences
        securityFixedCode = securityFixedCode.replace(
            /^```[a-zA-Z0-9_+-]*\s*/i,
            ""
        );

        securityFixedCode = securityFixedCode.replace(
            /\s*```$/,
            ""
        );

        securityFixedCode = securityFixedCode.trim();
    }
}
        agentsDiv.innerHTML = `

            <div class="analysis-top">

                <div>
                    <h3>Selected Agent</h3>

                    <p>
                        ${selectedAgent.icon}
                        ${selectedAgent.name}
                    </p>
                </div>

            </div>

            <div class="agent-results">

                <div class="agent-card">

                    <div class="agent-card-header">

                        <span>
                            ${selectedAgent.icon}
                        </span>

                        <strong>
                            ${selectedAgent.name}
                        </strong>

                    </div>

                    <pre>${data.result}</pre>

                    ${
                        selectedAgent.type === "DEBUG"
                        ?
                        `
                        <button
                            class="apply-fix-button"
                            onclick="applyDebugFix()">
                            🔧 Apply Suggested Fix
                        </button>
                        `
                        :
                        ""
                    }

                    ${
    selectedAgent.type === "SECURITY" &&
    securityFixedCode
        ? `
            <button
                class="apply-fix-button"
                onclick="applySecurityFix()">
                🔐 Apply Security Fix
            </button>
        `
        : ""
}

                </div>

            </div>
        `;

       reportDiv.innerHTML = "";

    } catch (error) {

        agentsDiv.innerHTML = `

            <div class="error">

                ❌ AI analysis failed

                <br><br>

                ${error.message}

            </div>

        `;

        reportDiv.innerHTML = "";
    }
}


async function askAI() {
    const code = document.getElementById("code").value;
    const requestBox = document.getElementById("aiRequest");
    const request = requestBox.value.trim();

    const resultsSection = document.getElementById("results");
    const agentsDiv = document.getElementById("agents");
    const reportDiv = document.getElementById("report");

    if (!request) {
        alert("Please enter a question.");
        return;
    }

    if (!code.trim()) {
        alert("Please enter some code first.");
        return;
    }

    resultsSection.classList.remove("hidden");

    agentsDiv.innerHTML = `
        <div class="loading">
            🤖 DevAssist is thinking...
        </div>
    `;

    reportDiv.innerHTML = "";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                request: request,
                code: code
            })
        });

        if (!response.ok) {
            throw new Error("Server error: " + response.status);
        }

        const data = await response.json();

        agentsDiv.innerHTML = `
    <h3>Selected Agents</h3>
    <p>${data.selected_agents}</p>

    <div class="agent-results">
        ${Object.entries(data.agent_results).map(([agent, result]) => `
            <div class="agent-card">
                <div class="agent-card-header">
                    <span>${getAgentIcon(agent)}</span>
                    <strong>${getAgentName(agent)}</strong>
                </div>

                <pre>${result}</pre>
            </div>
        `).join("")}
    </div>
`;

reportDiv.innerHTML = `
    <div class="final-report">
        <h3>📋 DevAssist Final Report</h3>
        <pre>${data.report}</pre>
    </div>
`;

    } catch (error) {

        agentsDiv.innerHTML = `
            <div class="error">
                ❌ AI request failed
            </div>
        `;

        reportDiv.innerHTML = `
            <pre>${error.message}</pre>
        `;
    }
}


function openAI() {
    document.getElementById("aiRequest").focus();
}


function getAgentName(agent) {
    const names = {
        DEBUG: "Debugging Agent",
        CODE_REVIEW: "Code Review Agent",
        OPTIMIZATION: "Optimization Agent",
        DOCUMENTATION: "Documentation Agent",
        TEST_CASE: "Test Case Agent",
        COMPLEX: "Complex Analysis Agent"
    };

    return names[agent] || agent;
}


function getAgentIcon(agent) {
    const icons = {
        DEBUG: "🐛",
        CODE_REVIEW: "🔍",
        OPTIMIZATION: "⚡",
        DOCUMENTATION: "📚",
        TEST_CASE: "🧪",
        COMPLEX: "🧠"
    };

    return icons[agent] || "🤖";
}


async function analyzeExecutionError(code, error) {

    const resultsSection = document.getElementById("results");
    const agentsDiv = document.getElementById("agents");
    const reportDiv = document.getElementById("report");

    resultsSection.classList.remove("hidden");

    agentsDiv.innerHTML = `
        <div class="analysis-header">
            <h3>Selected Agents</h3>
            <p>🐛 DEBUG</p>
        </div>

        <div class="agent-card">
            <div class="agent-card-header">
                <span>🐛</span>
                <strong>Debugging Agent</strong>
            </div>

            <div class="loading">
                🤖 Analyzing execution error...
            </div>
        </div>
    `;

    reportDiv.innerHTML = "";

    const request =
        `The program failed during execution.

Analyze this execution error and identify the exact cause.
Explain why it happened and provide the corrected code.

Execution Error:
${error}`;

    try {

        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                request: request,
                code: code,
                execution_error: error
            })
        });

        if (!response.ok) {
            throw new Error(
                "AI server error: " + response.status
            );
        }

        const data = await response.json();

        agentsDiv.innerHTML = `
            <div class="analysis-top">
    <div>
        <h3>Selected Agents</h3>
        <p>${data.selected_agents}</p>
    </div>
</div>

            <div class="agent-results">

                ${Object.entries(data.agent_results).map(
                    ([agent, result]) => `
                        <div class="agent-card">

                            <div class="agent-card-header">
                                <span>${getAgentIcon(agent)}</span>
                                <strong>${getAgentName(agent)}</strong>
                            </div>

                            <pre>${result}</pre>

                            ${
                                agent === "DEBUG"
                                ?
                                `<button
                                    class="apply-fix-button"
                                    onclick="applyDebugFix()">
                                    🔧 Apply Suggested Fix
                                </button>`
                                :
                                ""
                            }

                        </div>
                    `
                ).join("")}

            </div>
        `;

        reportDiv.innerHTML = `
            <div class="final-report">

                <h3>📋 DevAssist Final Report</h3>

                <pre>${data.report}</pre>

            </div>
        `;

    } catch (error) {

        agentsDiv.innerHTML = `
            <div class="error">
                ❌ Automatic AI debugging failed
            </div>
        `;

        reportDiv.innerHTML = `
            <pre>${error.message}</pre>
        `;
    }
}

async function applyDebugFix() {

    const cards =
        document.querySelectorAll("#agents .agent-card pre");

    let correctedCode = "";

    for (const card of cards) {

        const text = card.textContent;

        const startMarker = "CORRECTED_CODE_START";
        const endMarker = "CORRECTED_CODE_END";

        const startIndex = text.indexOf(startMarker);
        const endIndex = text.indexOf(endMarker);

        if (
            startIndex !== -1 &&
            endIndex !== -1 &&
            endIndex > startIndex
        ) {

            correctedCode = text.substring(
                startIndex + startMarker.length,
                endIndex
            ).trim();

            break;
        }
    }

    if (!correctedCode) {
        alert("No corrected code was found.");
        return;
    }

    // Remove Markdown code fences
    correctedCode = correctedCode.replace(
        /```[a-zA-Z0-9_+-]*\s*/g,
        ""
    );

    // Remove Markdown bold markers
    correctedCode = correctedCode.replace(
        /\*\*/g,
        ""
    );

    // Remove any remaining standalone backticks
    correctedCode = correctedCode.replace(
        /`/g,
        ""
    );

    correctedCode = correctedCode.trim();

    // Put clean corrected code into editor
    document.getElementById("code").value =
        correctedCode;

    // Save corrected code
    try {

        const file = "main.py";

        const response =
            await fetch(
                "/project/file",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        file: file,
                        code: correctedCode
                    })
                }
            );

        const data =
            await response.json();

        if (!data.success) {

            alert(
                "Code was corrected in the editor, but saving failed."
            );

            return;
        }

        alert(
            "✅ Corrected code applied and saved successfully."
        );

    } catch (error) {

        alert(
            "Code was corrected, but saving failed: " +
            error.message
        );
    }
}
function closeAIAnalysis() {

    const resultsSection =
        document.getElementById("results");

    const viewButton =
        document.getElementById("viewAnalysisButton");

    resultsSection.classList.add("hidden");

    viewButton.classList.remove("hidden");

    document.getElementById("code").focus();
}

function openLastAnalysis() {

    const resultsSection =
        document.getElementById("results");

    const viewButton =
        document.getElementById("viewAnalysisButton");

    resultsSection.classList.remove("hidden");

    viewButton.classList.add("hidden");
}


function extractPythonTests(result) {
    if (!result) {
        return "";
    }

    let code = result.trim();

    // Remove ```python ... ``` or ``` ... ```
    code = code.replace(/^```(?:python|py)?\s*/i, "");
    code = code.replace(/\s*```$/i, "");

    return code.trim();
}



async function runTests() {

    const terminal =
        document.getElementById("terminalOutput");

    const testButton =
        document.getElementById("testButton");

    const sourceCode =
        document.getElementById("code").value;

    if (!sourceCode.trim()) {
        alert("Please enter some code first.");
        return;
    }

    if (!generatedTestCode) {
        alert(
            "Please generate test cases first using 🧪 Generate Tests."
        );
        return;
    }

    testButton.disabled = true;
    testButton.textContent = "⏳ Testing...";

    terminal.textContent =
        "🧪 Running generated tests against your code...\n\n";

    try {

        const response = await fetch(
            "/test",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    source_code: sourceCode,
                    test_code: generatedTestCode
                })
            }
        );

        if (!response.ok) {
            throw new Error(
                "Test server error: " +
                response.status
            );
        }

        const data =
            await response.json();

        // Display professional test dashboard
        displayTestResults(data);

        if (data.success) {

            terminal.textContent =
                "🧪 Test Execution\n\n" +
                "✅ ALL TESTS PASSED\n\n" +
                data.output;

        } else {

            terminal.textContent =
                "🧪 Test Execution\n\n" +
                "❌ TESTS FAILED\n\n" +
                data.output +
                "\n" +
                data.error +
                "\n\n" +
                "🐛 DevAssist is analyzing the failure...";

            // Automatic debugging remains unchanged
            await analyzeTestFailure(
                sourceCode,
                data.output,
                data.error
            );
        }

    } catch (error) {

        terminal.textContent =
            "❌ Could not run tests.\n\n" +
            error.message;

    } finally {

        testButton.disabled = false;
        testButton.textContent = "🧪 Run Tests";
    }
}

async function analyzeTestFailure(
    sourceCode,
    testOutput,
    testError
) {

    const agentsDiv =
        document.getElementById("agents");

    const reportDiv =
        document.getElementById("report");

    agentsDiv.innerHTML += `
        <div class="agent-card">

            <div class="agent-card-header">
                <span>🐛</span>
                <strong>Automatic Failure Analysis</strong>
            </div>

            <div class="loading">
                🤖 Debugging Agent is analyzing the test failure...
            </div>

        </div>
    `;

    try {

        const response = await fetch(
            "/test/analyze-failure",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    source_code: sourceCode,
                    test_output: testOutput,
                    test_error: testError
                })
            }
        );

        if (!response.ok) {
            throw new Error(
                "Failure analysis server error: " +
                response.status
            );
        }

        const data =
            await response.json();

        if (!data.success) {
            throw new Error(data.error);
        }

        const cards =
            agentsDiv.querySelectorAll(".agent-card");

        const lastCard =
            cards[cards.length - 1];

        lastCard.innerHTML = `
            <div class="agent-card-header">
                <span>🐛</span>
                <strong>Automatic Failure Analysis</strong>
            </div>

            <pre>${data.result}</pre>

            <button
                class="apply-fix-button"
                onclick="applyDebugFix()">
                🔧 Apply Suggested Fix
            </button>
        `;

    } catch (error) {

        agentsDiv.innerHTML += `
            <div class="error">
                ❌ Automatic failure analysis failed
                <br><br>
                ${error.message}
            </div>
        `;
    }
}


function displayTestResults(data) {

    const resultsSection =
        document.getElementById("results");

    const agentsDiv =
        document.getElementById("agents");

    const reportDiv =
        document.getElementById("report");

    resultsSection.classList.remove("hidden");

    const output =
        data.output || "";

    const error =
        data.error || "";

    /*
     * Extract pytest summary.
     *
     * Example:
     * 4 passed
     * 2 failed, 2 passed
     */

    let totalTests = 0;
    let passedTests = 0;
    let failedTests = 0;

    const passedMatch =
        output.match(/(\d+)\s+passed/);

    const failedMatch =
        output.match(/(\d+)\s+failed/);

    if (passedMatch) {
        passedTests =
            parseInt(passedMatch[1]);
    }

    if (failedMatch) {
        failedTests =
            parseInt(failedMatch[1]);
    }

    totalTests =
        passedTests + failedTests;

    let passPercentage = 0;

    if (totalTests > 0) {
        passPercentage =
            Math.round(
                (passedTests / totalTests) * 100
            );
    }

    /*
     * Extract individual test results
     */

    const testLines =
        output.split("\n");

    let testResultsHTML = "";

    testLines.forEach(line => {

        const passed =
            line.match(
                /test_[^\s:]+.*PASSED/
            );

        const failed =
            line.match(
                /test_[^\s:]+.*FAILED/
            );

        if (passed) {

            const testName =
                passed[0]
                    .replace(/\s+PASSED.*$/, "")
                    .trim();

            testResultsHTML += `
                <div class="individual-test passed">
                    <span>✅</span>
                    <span>${testName}</span>
                    <strong>PASSED</strong>
                </div>
            `;
        }

        if (failed) {

            const testName =
                failed[0]
                    .replace(/\s+FAILED.*$/, "")
                    .trim();

            testResultsHTML += `
                <div class="individual-test failed">
                    <span>❌</span>
                    <span>${testName}</span>
                    <strong>FAILED</strong>
                </div>
            `;
        }
    });

    /*
     * Status
     */

    const status =
        data.success
            ? "ALL TESTS PASSED"
            : "TESTS FAILED";

    const statusIcon =
        data.success
            ? "✅"
            : "❌";

    /*
     * Dashboard
     */

    agentsDiv.innerHTML = `

        <div class="analysis-top">

            <div>
                <h3>Test Results</h3>

                <p>
                    🧪 Pytest
                </p>
            </div>

        </div>

        <div class="test-dashboard">

            <div class="test-status
                ${data.success ? "success" : "failure"}">

                <div class="test-status-icon">
                    ${statusIcon}
                </div>

                <div>
                    <h2>${status}</h2>

                    <p>
                        ${passPercentage}% test success rate
                    </p>
                </div>

            </div>


            <div class="test-statistics">

                <div class="test-stat">

                    <div class="test-stat-number">
                        ${totalTests}
                    </div>

                    <div class="test-stat-label">
                        Total Tests
                    </div>

                </div>


                <div class="test-stat">

                    <div class="test-stat-number">
                        ${passedTests}
                    </div>

                    <div class="test-stat-label">
                        Passed
                    </div>

                </div>


                <div class="test-stat">

                    <div class="test-stat-number">
                        ${failedTests}
                    </div>

                    <div class="test-stat-label">
                        Failed
                    </div>

                </div>


                <div class="test-stat">

                    <div class="test-stat-number">
                        ${passPercentage}%
                    </div>

                    <div class="test-stat-label">
                        Success Rate
                    </div>

                </div>

            </div>


            ${
                testResultsHTML
                ?
                `
                <div class="individual-tests">

                    <h3>
                        Test Case Details
                    </h3>

                    ${testResultsHTML}

                </div>
                `
                :
                ""
            }


            <details class="pytest-details">

                <summary>
                    📄 View Full Pytest Output
                </summary>

                <pre>${output}</pre>

                ${
                    error
                    ?
                    `<pre>${error}</pre>`
                    :
                    ""
                }

            </details>

        </div>
    `;

    reportDiv.innerHTML = "";
}


async function applySecurityFix() {
    const codeEditor = document.getElementById("code");
    const agentsDiv = document.getElementById("agents");

    const cards = agentsDiv.querySelectorAll(".agent-card pre");

    let correctedCode = "";

    for (const card of cards) {
        const result = card.textContent;

        const startMarker = "SECURITY_FIXED_CODE_START";
        const endMarker = "SECURITY_FIXED_CODE_END";

        const startIndex = result.indexOf(startMarker);
        const endIndex = result.indexOf(endMarker);

        if (
            startIndex !== -1 &&
            endIndex !== -1 &&
            endIndex > startIndex
        ) {
            correctedCode = result
                .substring(
                    startIndex + startMarker.length,
                    endIndex
                )
                .trim();

            correctedCode = correctedCode.replace(
                /^```[a-zA-Z0-9_+-]*\s*/i,
                ""
            );

            correctedCode = correctedCode.replace(
                /\s*```$/,
                ""
            );

            correctedCode = correctedCode.trim();

            break;
        }
    }

    if (!correctedCode) {
        alert("No corrected code was found.");
        return;
    }

    const confirmed = confirm(
        "Apply the AI-generated security fix to the editor? Review the code before running it."
    );

    if (!confirmed) {
        return;
    }

    codeEditor.value = correctedCode;

    try {
        const response = await fetch("/project/file", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                file: "main.py",
                code: correctedCode
            })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            alert(
                "The code was updated in the editor, but saving failed."
            );
            return;
        }

        alert(
            "Security fix applied and saved to main.py. Review it before running."
        );
    } catch (error) {
        alert(
            "The code was updated in the editor, but saving failed: " +
            error.message
        );
    }
}

