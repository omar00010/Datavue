<script>
    import { onMount } from 'svelte';
  
    let messages = [];
    let input = '';
    let loading = false;
    let messagesEnd;
  
    const sendMessage = async () => {
      if (!input.trim()) return;
      messages = [...messages, { sender: 'user', text: input }];
      loading = true;

      if (input.toLowerCase() === 'list tables') {
        try {
          const res = await fetch('/api/list/tables', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
          });
          const data = await res.json();
          const tables = data.tables.join(', '); 
          messages = [...messages, { sender: 'bot', text: `Tables: ${tables}` }];

        } catch (error) {
          messages = [...messages, { sender: 'bot', text: 'Failed to fetch tables.' }];
          scrollToBottom(); 
        }
      } else {
        try {
          const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: input })
          });
          const data = await res.json();
          messages = [...messages, { sender: 'bot', text: data.response }];
          scrollToBottom(); 
        } catch (error) {
          messages = [...messages, { sender: 'bot', text: 'Failed to fetch response.' }];
          scrollToBottom(); 
        }
      }

      input = '';
      loading = false;
    };
  
    const scrollToBottom = () => {
      messagesEnd?.scrollIntoView({ behavior: 'smooth' });
    };

    // Automatically scroll to the bottom when the component is mounted
    onMount(() => {
      scrollToBottom();
    });

    // Reactive statement to scroll to the bottom whenever messages or loading changes
    $: {
      if (messages.length || loading) {
        scrollToBottom();
      }
    }

    const handleKey = (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    };
</script>
  
  <style>
    :global(body) {
      margin: 0;
      font-family: system-ui, sans-serif;
      background-color: #0d0d0d;
      color: #e0e0e0;
    }
  
    .chat-wrapper {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      padding: 1rem;
    }
  
    .chat-container {
      display: flex;
      flex-direction: column;
      width: 100%;
      max-width: 800px;
      height: 90vh;
      background-color: #1a1a1a;
      border-radius: 0.75rem;
      box-shadow: 0 0 20px rgba(0, 0, 0, 0.7);
      padding: 1rem;
      box-sizing: border-box;
    }
  
    .header {
      font-size: 1.2rem;
      font-weight: bold;
      margin-bottom: 1rem;
      text-align: center;
      color: #cccccc;
    }
  
    .messages {
      flex: 1;
      overflow-y: auto;
      margin-bottom: 1rem;
      display: flex;
      flex-direction: column;
    }
  
    .message {
      margin: 0.5rem 0;
      padding: 0.75rem 1rem;
      border-radius: 0.75rem;
      max-width: 75%;
      white-space: pre-wrap;
      line-height: 1.4;
      word-wrap: break-word;
    }
  
    .user {
      align-self: flex-end;
      background-color: #2f855a;
      color: white;
      border-bottom-right-radius: 0;
    }
  
    .bot {
      align-self: flex-start;
      background-color: #2d2d2d;
      color: #f0f0f0;
      border-bottom-left-radius: 0;
    }
  
    .input-row {
      display: flex;
      gap: 0.5rem;
      align-items: center;
    }
  
    textarea {
      flex: 1;
      padding: 0.75rem 1rem;
      resize: none;
      border-radius: 0.5rem;
      border: none;
      background-color: #2a2a2a;
      color: white;
      font-size: 1rem;
      box-shadow: inset 0 0 5px rgba(0,0,0,0.3);
    }
  
    button {
      padding: 0.75rem 1.25rem;
      border: none;
      border-radius: 0.5rem;
      background-color: white;
      color: #1a1a1a;
      font-weight: bold;
      cursor: pointer;
    }
  </style>


  <div class="chat-wrapper">
    
    <div class="chat-container">
      <div class="header">Welcome to DataVue – Chat with your data</div>
  
      <div class="messages">
        {#each messages as msg}
          <div class="message {msg.sender}">{msg.text}</div>
        {/each}
        {#if loading}
          <div class="message bot">...</div>
        {/if}
        <div bind:this={messagesEnd}></div> <!-- Reference to the bottom -->
      </div>
  
      <div class="input-row">
        <textarea
          bind:value={input}
          rows="2"
          on:keydown={handleKey}
          placeholder="Type a message and press Enter..."
        ></textarea>
        <button on:click={sendMessage}>Send</button>
      </div>
    </div>
  </div>