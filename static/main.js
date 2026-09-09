/*
 * main.js
 *
 * Runs in the browser. When the form is submitted, it asks the Flask API for
 * matching dishes and writes them into the page -- without a full reload.
 */

// Look up the two elements we work with, by the ids set in index.html.
// document.getElementById returns the matching element (or null if the id
// doesn't exist -- a common source of "why is my script silently broken").
const form = document.getElementById("search-form");
const resultsDiv = document.getElementById("results");


// addEventListener("submit", ...) runs the given function every time the form
// is submitted (button click, or Enter in a field).
//
// "async" lets us use "await" inside -- await pauses until a slow thing (the
// network request) finishes, without freezing the page.
form.addEventListener("submit", async (event) => {
    // By default, submitting a form makes the browser leave and load a new
    // page. We want to stay here and update in place, so cancel that.
    event.preventDefault();

    // --- TODO 1: read the three input values ---
    // Each input has an id ("restrictions", "preferences", "location").
    // getElementById(...).value gives you what the user typed, as a string.
    // Put them in three variables named restrictions, preferences, location.
    const restrictions = document.getElementById("restrictions").value;  // <-- replace
    const preferences = document.getElementById("preferences").value;   // <-- replace
    const location = document.getElementById("location").value;      // <-- replace

    // Build the query string. URLSearchParams turns an object into
    // "restrictions=...&preferences=...&location=..." and escapes special
    // characters (spaces, etc.) for us.
    const params = new URLSearchParams({ restrictions, preferences, location });

    try {
        // Send GET /api/search?<params> and wait for the response.
        const response = await fetch("/api/search?" + params.toString());
        // Parse the response body from JSON text into a real JS array.
        const items = await response.json();
        renderResults(items);
    } catch (err) {
        // Network failed, server errored, bad JSON -- show something rather
        // than failing silently.
        resultsDiv.innerHTML = '<p class="empty">Something went wrong.</p>';
        console.error(err);
    }
});


/*
 * Turn the array of result objects into HTML and put it on the page.
 *
 * Each item looks like:
 *   { restaurant, name, description, tags: [...], score }
 */
function renderResults(items) {
    // Handle "no matches" first.
    if (items.length === 0) {
        resultsDiv.innerHTML = '<p class="empty">No dishes match.</p>';
        return;
    }

    // --- TODO 2: build the results HTML ---
    // Goal: one card per item. A card looks like:
    //
    //   <div class="result">
    //     <h3>Duck Soup — Naveen's Fork</h3>
    //     <p>Brown lentils, roasted duck, herbs, spices</p>
    //     <p class="tags">dairy-free, gluten-free, halal, nut-free, spicy</p>
    //   </div>
    //
    // Approach:
    //   items.map(item => `...template string using ${item.name} etc...`)
    //   gives you an array of HTML strings; .join("") glues them into one.
    //   item.tags is an array -- item.tags.join(", ") makes it a string.
    //   Assign the final string to resultsDiv.innerHTML.
    // resultsDiv.innerHTML = items.map(item => '    <div class="result">
    //      <h3>${item.name} — ${item.restaurant}</h3>
    //      <p>${item.description}</p>
    //      <p class="tags">${item.tags.join(", ")}</p>
    // </div>' );  // <-- replace

    resultsDiv.innerHTML = items.map(item => `
        <div class="result">
            <h3>${item.name} — ${item.restaurant}</h3>
            <p>${item.description}</p>
            <p class="tags">${item.tags.join(", ")}</p>
        </div>
    `).join("");


    

    return;
}
