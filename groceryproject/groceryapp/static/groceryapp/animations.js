// Create an Intersection Observer
const observer = new IntersectionObserver(handleIntersection, { threshold: 0 });

// Target elements with the .fade-up, .fade-left, and .fade-right classes
const fadeUpElements = document.querySelectorAll('.fade-up');
fadeUpElements.forEach(element => {
    observer.observe(element);
});

const fadeLeftElements = document.querySelectorAll('.fade-left');
fadeLeftElements.forEach(element => {
    observer.observe(element);
});

const fadeRightElements = document.querySelectorAll('.fade-right');
fadeRightElements.forEach(element => {
    observer.observe(element);
});

const slideUpElements = document.querySelectorAll('.slide-up');
slideUpElements.forEach(element => {
    observer.observe(element); // Create an Intersection Observer
    const observer = new IntersectionObserver(handleIntersection, { threshold: 0.0 });

    // Target elements with the .fade-up, .fade-left, and .fade-right classes
    const fadeUpElements = document.querySelectorAll('.fade-up');
    fadeUpElements.forEach(element => {
        observer.observe(element);
    });

    const fadeLeftElements = document.querySelectorAll('.fade-left');
    fadeLeftElements.forEach(element => {
        observer.observe(element);
    });

    const fadeRightElements = document.querySelectorAll('.fade-right');
    fadeRightElements.forEach(element => {
        observer.observe(element);
    });

    const slideUpElements = document.querySelectorAll('.slide-up');
    slideUpElements.forEach(element => {
        observer.observe(element);
    });

    const slideLeftElements = document.querySelectorAll('.slide-left');
    slideLeftElements.forEach(element => {
        observer.observe(element);
    });

    const slideRightElements = document.querySelectorAll('.slide-right');
    slideRightElements.forEach(element => {
        observer.observe(element);
    });

    // Function to handle the Intersection Observer callback
    function handleIntersection(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate'); // Add the animate class
                // If you want to remove the class after the animation completes, you can use setTimeout
                // setTimeout(() => { entry.target.classList.remove('animate'); }, 1000); // Adjust the delay as needed
                observer.unobserve(entry.target);
            }
        });
    }

});

const slideLeftElements = document.querySelectorAll('.slide-left');
slideLeftElements.forEach(element => {
    observer.observe(element);
});

const slideRightElements = document.querySelectorAll('.slide-right');
slideRightElements.forEach(element => {
    observer.observe(element);
});

// Function to handle the Intersection Observer callback
function handleIntersection(entries, observer) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
            observer.unobserve(entry.target);
        }
    });
}