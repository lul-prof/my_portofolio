// Intersection Observer for scroll animations
const sections = document.querySelectorAll('section');
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, {
    threshold: 0.1
});

sections.forEach(section => {
    observer.observe(section);
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});



document.getElementById('contactForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const submitButton = this.querySelector('button[type="submit"]');
    const messageStatus = document.getElementById('messageStatus');
    
    // Disable submit button while processing
    submitButton.disabled = true;
    submitButton.textContent = 'Sending...';
    
    try {
        const formData = new FormData(this);
        const response = await fetch('/send-message', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        messageStatus.textContent = result.message;
        messageStatus.className = `message-status ${result.status}`;
        
        if (result.status === 'success') {
            this.reset();
        }
    } catch (error) {
        messageStatus.textContent = 'An error occurred. Please try again later.';
        messageStatus.className = 'message-status error';
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = 'Send Message';
    }
});