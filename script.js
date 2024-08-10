let currentIndex = 0;

    function showNextSlide() {
        const slides = document.querySelector('.slides');
        const totalSlides = document.querySelectorAll('.slide').length;
        currentIndex = (currentIndex + 1) % totalSlides;
        slides.style.transform = `translateX(-${currentIndex * 100 / totalSlides}%)`;
    }

    setInterval(showNextSlide, 3000); // Change slide every 3 seconds