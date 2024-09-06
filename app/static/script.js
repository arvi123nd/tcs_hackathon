async function sendQuery() {
    const query = document.getElementById('queryInput').value;
    const responseDiv = document.getElementById('response');

    console.log("Sending query:", query); // Debugging line

    try {
        const response = await fetch('http://127.0.0.1:8001/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }

        const data = await response.json();
        console.log("Response received:", data); // Debugging line
        responseDiv.innerText = data.response;
    } catch (error) {
        console.error("Error occurred:", error); // Debugging line
        responseDiv.innerText = 'An error occurred: ' + error.message;
    }
}
