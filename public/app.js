let passwordSequence = [];

function updatePasswordDisplay() {
    document.getElementById('passwordDisplay').textContent = 'Password Sequence: ' + passwordSequence.join(' ');
}



// Add event listeners for the 4 buttons
document.getElementById('button0').addEventListener('click', function() {
    if (passwordSequence.length >= 4) {
        alert("You have reached the maximum amount of combinations for your password!")
    }
    else {
        passwordSequence.push(0);
        updatePasswordDisplay()
    }

    console.log('Password sequence:', passwordSequence);
});


document.getElementById('button1').addEventListener('click', function() {
    if (passwordSequence.length >= 4) {
        alert("You have reached the maximum amount of combinations for your password!")
    }
    else {
        passwordSequence.push(1);
        updatePasswordDisplay()
    }

    console.log('Password sequence:', passwordSequence);
});

document.getElementById('button2').addEventListener('click', function() {
    if (passwordSequence.length >= 4) {
        alert("You have reached the maximum amount of combinations for your password!")
    }
    else {
        passwordSequence.push(2);
        updatePasswordDisplay()

    }
    console.log('Password sequence:', passwordSequence);
});

document.getElementById('button3').addEventListener('click', function() {
    if (passwordSequence.length >= 4) {
        alert("You have reached the maximum amount of combinations for your password!")
    }
    else {
        passwordSequence.push(3);
        updatePasswordDisplay()

    }    console.log('Password sequence:', passwordSequence);
    
});

document.getElementById('button4').addEventListener('click', function() {
    if (passwordSequence.length >= 4) {
        alert("You have reached the maximum amount of combinations for your password!")
    }
    else {
        passwordSequence.push(4);
        updatePasswordDisplay()

    }
    console.log('Password sequence:', passwordSequence);
});

document.getElementById('button5').addEventListener('click', function() {
    if (passwordSequence.length >= 4) {
        alert("You have reached the maximum amount of combinations for your password!")
    }
    else {
        passwordSequence.push(5);
        updatePasswordDisplay()
    }

    console.log('Password sequence:', passwordSequence);
});

// Handle the submit button click
document.getElementById('submitButton').addEventListener('click', function() {
    var name = document.getElementById("name").value;

    if (passwordSequence.length === 4) {
        // Send the password to the server to store in the database
        fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({name, passwordSequence})
        })
        .then(response => response.json())
        .then(data => {
            console.log('Password saved:', data);
            alert("User and password submitted successfully!")
            // Clear the sequence after submitting
            passwordSequence = [];
            updatePasswordDisplay()

        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert('Please select all 4 values before submitting.');
    }
});