function scrollToNewsletter() {
    const newsletterSection = document.getElementById('newsletter');
    newsletterSection.scrollIntoView({ behavior: 'smooth' });
}

function toggleFeatures() {
    const featureGrid = document.querySelector('.feature-grid');
    const viewMoreButton = document.querySelector('#features .secondary-button');
    
    if (featureGrid.style.maxHeight) {
        featureGrid.style.maxHeight = null;
        viewMoreButton.textContent = 'View More';
    } else {
        featureGrid.style.maxHeight = featureGrid.scrollHeight + "px";
        viewMoreButton.textContent = 'View Less';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('newsletter-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = form.querySelector('input[type="email"]').value;
        
        // Here you would typically send the email to your server
        // For this example, we'll just show a thank you message
        const thankYouMessage = document.createElement('p');
        thankYouMessage.textContent = 'Thank you for subscribing!';
        thankYouMessage.classList.add('thank-you-message');
        form.appendChild(thankYouMessage);
        
        form.reset();
    });

    // Intersection Observer for fade-in effect
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('section').forEach(section => {
        observer.observe(section);
    });
});

// Dark mode toggle
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Check for saved dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// Add smooth scrolling to all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
