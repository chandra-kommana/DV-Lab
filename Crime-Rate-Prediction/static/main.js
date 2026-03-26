// Mode Switching
function switchMode(mode) {
    // Hide all mode contents
    document.querySelectorAll('.mode-content').forEach(el => {
        el.classList.remove('active');
    });

    // Remove active state from all buttons
    document.querySelectorAll('.mode-button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected mode
    const modeContent = document.getElementById(mode + '-mode');
    if (modeContent) {
        modeContent.classList.add('active');
    }

    // Activate clicked button
    event.target.closest('.mode-button').classList.add('active');

    // Initialize year dropdown for the new mode
    if (mode === 'compare') {
        initYearDropdown('year-dropdown-compare');
    } else {
        initYearDropdown('year-dropdown');
    }
}

// Initialize year dropdown
function initYearDropdown(dropdownId) {
    const yearDropdown = document.getElementById(dropdownId);
    if (!yearDropdown || yearDropdown.options.length > 1) return; // Already initialized
    
    // Generate years from 2000 to 2050
    for (let i = 2000; i <= 2050; i++) {
        const option = document.createElement("option");
        option.value = i;
        option.textContent = i;
        yearDropdown.appendChild(option);
    }

    // Set current year as default
    const currentYear = new Date().getFullYear();
    if (currentYear <= 2050 && currentYear >= 2000) {
        yearDropdown.value = currentYear;
    }
}

// Initialize year dropdown
window.addEventListener('load', function () {
    initYearDropdown('year-dropdown');
    initYearDropdown('year-dropdown-compare');

    // Smooth scroll navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const target = this.getAttribute('href');
            
            // Update active state
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Scroll to section
            if (target !== '#') {
                const section = document.querySelector(target);
                if (section) {
                    section.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });

    // Form validation and submission feedback
    const predictionForm = document.querySelector('.prediction-form');
    if (predictionForm) {
        predictionForm.addEventListener('submit', function (e) {
            const city = document.getElementById('city-select').value;
            const crime = document.getElementById('crime-select').value;
            const year = document.getElementById('year-dropdown').value;

            if (!city || !crime || !year) {
                e.preventDefault();
                alert('Please fill in all fields before predicting!');
                return;
            }
        });
    }

    // Add animation to feature cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'slideUp 0.6s ease-out forwards';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card').forEach(card => {
        observer.observe(card);
    });

    // Add slideUp animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);
});

// Smooth scroll navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();
        const target = this.getAttribute('href');
        
        // Update active state
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        this.classList.add('active');
        
        // Scroll to section
        if (target !== '#') {
            const section = document.querySelector(target);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
});

// Form validation and submission feedback
const predictionForm = document.querySelector('.prediction-form');
if (predictionForm) {
    predictionForm.addEventListener('submit', function (e) {
        const city = document.getElementById('city-select').value;
        const crime = document.getElementById('crime-select').value;
        const year = document.getElementById('year-dropdown').value;

        if (!city || !crime || !year) {
            e.preventDefault();
            alert('Please fill in all fields before predicting!');
            return;
        }
    });
}

// Add animation to feature cards on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function (entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'slideUp 0.6s ease-out forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.feature-card').forEach(card => {
    observer.observe(card);
});

// Add slideUp animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);