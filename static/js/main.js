/* ===================================================================
   VISA SLOT BOOKING — MAIN JAVASCRIPT
   =================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    // ─── Mobile Menu Toggle ────────────────────────────────
    const mobileToggle = document.getElementById('mobileToggle');
    const mobileMenu = document.getElementById('mobileMenu');

    if (mobileToggle && mobileMenu) {
        mobileToggle.addEventListener('click', function () {
            mobileMenu.classList.toggle('active');
            const icon = mobileToggle.querySelector('i');
            if (mobileMenu.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });

        // Close menu when clicking a link
        mobileMenu.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                mobileMenu.classList.remove('active');
                const icon = mobileToggle.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            });
        });
    }

    // ─── Hero Background Slider ─────────────────────────────
    const bgSlides = document.querySelectorAll('.hero-slider-bg .slide-bg');
    if (bgSlides.length > 1) {
        let bgIndex = 0;
        setInterval(function () {
            bgSlides[bgIndex].classList.remove('active');
            bgIndex = (bgIndex + 1) % bgSlides.length;
            bgSlides[bgIndex].classList.add('active');
        }, 5000);
    }

    // ─── Hero Content Slider ────────────────────────────────
    const slides = document.querySelectorAll('.slider-wrapper .slide');
    const dots = document.querySelectorAll('.slider-dots .dot');
    if (slides.length > 1) {
        let slideIndex = 0;

        function goToSlide(index) {
            slides[slideIndex].classList.remove('active');
            if (dots[slideIndex]) dots[slideIndex].classList.remove('active');
            slideIndex = index;
            slides[slideIndex].classList.add('active');
            if (dots[slideIndex]) dots[slideIndex].classList.add('active');
        }

        // Auto-rotate
        setInterval(function () {
            goToSlide((slideIndex + 1) % slides.length);
        }, 4000);

        // Click dots
        dots.forEach(function (dot, i) {
            dot.addEventListener('click', function () {
                goToSlide(i);
            });
        });
    }

    // ─── Smooth Scroll for Anchor Links ─────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                const headerHeight = document.querySelector('.header')?.offsetHeight || 0;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ─── Header Shadow on Scroll ────────────────────────────
    const header = document.getElementById('header');
    if (header) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                header.style.boxShadow = '0 4px 30px rgba(13, 79, 79, 0.35)';
            } else {
                header.style.boxShadow = '0 4px 30px rgba(13, 79, 79, 0.25)';
            }
        });
    }

    // ─── Scroll Animations (Intersection Observer) ──────────
    const animateElements = document.querySelectorAll('.service-card, .why-card, .booking-form-card, .contact-info-block, .section-header');
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        animateElements.forEach(function (el) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            observer.observe(el);
        });
    }

    // ─── Service Card Click → Set Visa Type in Form ─────────
    document.querySelectorAll('.btn-service-book').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            const serviceId = this.getAttribute('data-service-id');
            const visaSelect = document.getElementById('visa_type');
            if (visaSelect && serviceId) {
                // Wait for smooth scroll to complete then set value
                setTimeout(function () {
                    visaSelect.value = serviceId;
                    // Highlight the select briefly
                    visaSelect.style.borderColor = '#0d4f4f';
                    visaSelect.style.boxShadow = '0 0 0 4px rgba(13, 79, 79, 0.12)';
                    setTimeout(function () {
                        visaSelect.style.borderColor = '';
                        visaSelect.style.boxShadow = '';
                    }, 1500);
                }, 600);
            }
        });
    });

    // ─── Booking Form AJAX Submission ───────────────────────
    const bookingForm = document.getElementById('bookingForm');
    const submitBtn = document.getElementById('submitBtn');
    const formMessage = document.getElementById('formMessage');

    if (bookingForm) {
        bookingForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // Disable button
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';

            // Get form data
            const formData = new FormData(bookingForm);

            fetch(bookingForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                formMessage.style.display = 'block';
                if (data.success) {
                    formMessage.className = 'form-message success';
                    formMessage.innerHTML = '<i class="fas fa-check-circle"></i> ' + data.message;
                    bookingForm.reset();
                } else {
                    formMessage.className = 'form-message error';
                    if (data.errors) {
                        let errorHtml = '<i class="fas fa-exclamation-circle"></i> Please fix the following:<ul>';
                        for (const key in data.errors) {
                            errorHtml += '<li>' + data.errors[key] + '</li>';
                        }
                        errorHtml += '</ul>';
                        formMessage.innerHTML = errorHtml;
                    } else {
                        formMessage.innerHTML = '<i class="fas fa-exclamation-circle"></i> ' + (data.message || 'Something went wrong.');
                    }
                }
            })
            .catch(function () {
                formMessage.style.display = 'block';
                formMessage.className = 'form-message error';
                formMessage.innerHTML = '<i class="fas fa-exclamation-circle"></i> Network error. Please try again.';
            })
            .finally(function () {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Booking Request';

                // Auto-hide message after 8 seconds
                setTimeout(function () {
                    formMessage.style.display = 'none';
                }, 8000);
            });
        });
    }

});
