// Create an Intersection Observer
const observer = new IntersectionObserver(handleIntersection, { threshold: 0.5 });

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
// Function to handle the Intersection Observer callback
function handleIntersection(entries, observer) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
            observer.unobserve(entry.target);
        }
    });
}