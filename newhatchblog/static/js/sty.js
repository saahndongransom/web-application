// Get the slideshow container
var slideshow = document.querySelector('.slideshow');

// Get the slides
var slides = slideshow.querySelectorAll('.slide');

// Set the current slide index to 0
var currentSlideIndex = 0;

// Show the next slide
function showNextSlide() {
	// Hide the current slide
	slides[currentSlideIndex].style.opacity = 0;
	// Increment the slide index
	currentSlideIndex++;
	// Reset the slide index if it goes beyond the last slide
	if (currentSlideIndex >= slides.length) {
		currentSlideIndex = 0;
	}
	// Show the next slide
	slides[currentSlideIndex].style.opacity = 1;
}


// Show the previous slide
function showPreviousSlide() {
	// Hide the current slide
	slides[currentSlideIndex].style.opacity = 0;
	// Decrement the slide index
	currentSlideIndex--;
	// Reset the slide index if it goes below the first slide
	if (currentSlideIndex < 0) {
      currentSlideIndex = slides.length - 1;
    }
    // Show the previous slide
    slides[currentSlideIndex].style.opacity = 1;
}

// Set an interval to show the next slide every 5 seconds
setInterval(showNextSlide, 5000);

// Add event listeners for the previous and next buttons
var previousButton = slideshow.querySelector('.previous-button');
previousButton.addEventListener('click', showPreviousSlide);

var nextButton = slideshow.querySelector('.next-button');
nextButton.addEventListener('click', showNextSlide);













