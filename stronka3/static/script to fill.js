// Function to handle the form submission
async function handleFormSubmit(event) {
    event.preventDefault();
  
    // Get the form data
    const formData = new FormData(event.target);
  
    // Validate the password length
    const password = formData.get('password');
    const passwordLengthMessageElement = document.getElementById('password-length-message');
    if (password.length < 6) {
      passwordLengthMessageElement.style.display = 'block';
      // Hide the error message after 5 seconds
      setTimeout(() => {
        passwordLengthMessageElement.style.display = 'none';
      }, 5000);
      return;
    }
  
    // Send a POST request to the server with the form data
    try {
      const response = await fetch('/api/signup', {
        method: 'POST',
        body: formData,
      });
  
      // Parse the response as JSON
      const data = await response.json();
  
      // Check if there's an error message in the response
      if (data.error) {
        // Display the error message below the form
        const errorMessageElement = document.getElementById('error-message');
        errorMessageElement.textContent = data.error;
  
        // Hide the error message after 5 seconds
        setTimeout(() => {
          errorMessageElement.textContent = '';
        }, 5000);
        return;
      }
  
      // Hide the form and password length message
      const signupForm = document.getElementById('signup-form');
      signupForm.style.display = 'none';
      passwordLengthMessageElement.style.display = 'none';
  
      // Display the confirmation message
      const confirmationMessageElement = document.getElementById('confirmation-message');
      confirmationMessageElement.style.display = 'block';
      confirmationMessageElement.innerHTML = data.message;
  
      // Hide the confirmation message after 10 seconds and show the signup form again
      setTimeout(() => {
        confirmationMessageElement.style.display = 'none';
        signupForm.style.display = 'block';
      }, 10000);
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  }
  
  // Function to handle going back to the signup form
  function handleBackToSignup() {
    const signupForm = document.getElementById('signup-form');
    signupForm.style.display = 'block';
  
    const confirmationMessageElement = document.getElementById('confirmation-message');
    confirmationMessageElement.style.display = 'none';
  }
  
  // Add event listener to the form for form submission
  const signupForm = document.getElementById('signup-form');
  signupForm.addEventListener('submit', handleFormSubmit);
  
  // Add event listener to the "Back to Sign Up" button
  const backToSignupBtn = document.getElementById('back-to-signup-btn');
  backToSignupBtn.addEventListener('click', handleBackToSignup);
  
  // Function to restrict input to numbers only for PIN and Character Deletion Number fields
  function restrictToNumbers(event) {
    const inputValue = event.target.value;
    event.target.value = inputValue.replace(/\D/g, ''); // Remove any non-digit characters
  }
  
  // Add event listeners to the PIN and Character Deletion Number fields
  const pinNumberField = document.getElementById('pin_number');
  const characterDeletionNumberField = document.getElementById('character_deletion_number');
  
  pinNumberField.addEventListener('input', restrictToNumbers);
  characterDeletionNumberField.addEventListener('input', restrictToNumbers);