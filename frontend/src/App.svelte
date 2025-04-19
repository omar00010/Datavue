<script>
    let message = "Loading...";

    // Fetch the message from the API
    fetch("/api/health") // Updated to match the backend's CORS configuration
        .then((response) => response.json())
        .then((data) => {
            message = data.message;
        })
        .catch((error) => {
            console.error("Error fetching API:", error);
            message = "Failed to load message. Error: " + error;
        });
</script>

<main>
    <h1>Welcome to the Svelte App!</h1>
    <h2>Message from the API:</h2>
    <h1>{message}</h1>
</main>

<style>
    main {
        text-align: center;
        padding: 1em;
        font-family: Arial, sans-serif;
    }
</style>