document.addEventListener('DOMContentLoaded', () => {
    const turnOnBtn = document.getElementById('turnOnBtn');
    const turnOffBtn = document.getElementById('turnOffBtn');
    const pcStatusSpan = document.getElementById('pc-status');
    const messageDiv = document.getElementById('message');

    // Function to display messages
    function showMessage(text, type = 'info') {
        messageDiv.textContent = text;
        messageDiv.className = `message ${type}`; // Add type for different styling if needed
        setTimeout(() => {
            messageDiv.textContent = '';
            messageDiv.className = 'message';
        }, 5000); // Clear message after 5 seconds
    }

    // Function to update PC status
    async function updatePcStatus() {
        pcStatusSpan.textContent = 'Checking...';
        try {
            const response = await fetch('/status');
            const data = await response.json();
            if (data.status === 'success') {
                pcStatusSpan.textContent = data.is_online ? 'ON' : 'OFF';
                pcStatusSpan.style.color = data.is_online ? 'green' : 'red';
                turnOffBtn.disabled = !data.is_online; // Enable/disable turn off if PC is online
            } else {
                pcStatusSpan.textContent = 'Unknown';
                pcStatusSpan.style.color = '#6c757d';
                showMessage(`Error checking status: ${data.message}`, 'error');
                turnOffBtn.disabled = true; // Disable turn off on error
            }
        } catch (error) {
            pcStatusSpan.textContent = 'Error';
            pcStatusSpan.style.color = 'red';
            showMessage('Could not connect to server for status check.', 'error');
            turnOffBtn.disabled = true; // Disable turn off on error
            console.error('Error fetching PC status:', error);
        }
    }

    // Event listener for Turn On button
    turnOnBtn.addEventListener('click', async () => {
        turnOnBtn.disabled = true;
        showMessage('Sending magic packet...', 'info');
        try {
            // Using POST request
            const response = await fetch('/wake', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            if (data.status === 'success') {
                showMessage(`Success: ${data.message}`, 'success');
                // Give PC some time to boot, then recheck status
                setTimeout(updatePcStatus, 15000); // Check status after 15 seconds
            } else {
                showMessage(`Error: ${data.message}`, 'error');
            }
        } catch (error) {
            showMessage('Network error while sending wake packet.', 'error');
            console.error('Error sending wake packet:', error);
        } finally {
            turnOnBtn.disabled = false;
        }
    });

    // Event listener for Turn Off button
    turnOffBtn.addEventListener('click', async () => {
        turnOffBtn.disabled = true;
        showMessage('Sending shutdown command...', 'info');
        try {
            // Using POST request
            const response = await fetch('/shutdown', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            if (data.status === 'success') {
                showMessage(`Success: ${data.message}`, 'success');
                // Give PC some time to shut down, then recheck status
                setTimeout(updatePcStatus, 10000); // Check status after 10 seconds
            } else {
                showMessage(`Error: ${data.message}`, 'error');
            }
        } catch (error) {
            showMessage('Network error while sending shutdown command.', 'error');
            console.error('Error sending shutdown command:', error);
        } finally {
            turnOffBtn.disabled = false;
        }
    });

    // Initial status check when the page loads
    updatePcStatus();
    // Refresh status every 30 seconds
    setInterval(updatePcStatus, 30000);
});