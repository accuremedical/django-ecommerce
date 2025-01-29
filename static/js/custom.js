
  (function ($) {
  
  "use strict";

    // PRE LOADER
    $(window).load(function(){
      $('.preloader').delay(500).slideUp('slow'); // set duration in brackets    
    });

    $('.slick-slideshow').slick({
      autoplay: true,
      infinite: true,
      arrows: false,
      fade: true,
      dots: true,
    });

    $('.slick-testimonial').slick({
      arrows: false,
      dots: true,
    });
    
  })(window.jQuery);

//navbar
  // set active in nav
  document.addEventListener("DOMContentLoaded", function () {
    const currentPage = window.location.pathname;

    // Check if the current path matches specific pages
    if (currentPage === '/' || currentPage.includes('index')) {
        setActive('home');  // Home page
    } else if (currentPage.includes('about')) {
        setActive('about'); // About page
    } else if (currentPage.includes('categories')) {
        setActive('categories');
    } else if (currentPage.includes('contact')) {
        setActive('contact');
    } else if (currentPage.includes('wishlist')) {
        setActive('wishlist');
    } else if (currentPage.includes('cart')) {
        setActive('cart');
    } else if (currentPage.includes('order-list')) {
      setActive('order-list');
  } 
});

function setActive(page) {
    // Remove the 'active' class from all nav links
    const links = document.querySelectorAll('.nav-link');
    links.forEach(link => {
        link.classList.remove('active');
    });

    // Add the 'active' class to the correct link
    const activeLink = document.getElementById(page);
    if (activeLink) {
        activeLink.classList.add('active');
    }
}

/* header scrolling*/

const topmenu = document.getElementById('topmenu');
    const navigation = document.getElementById('navigation');

    // Check if the user is on a mobile device
    const isMobile = window.matchMedia("(max-width: 991px)");

    let hasScrolled = false;

    window.addEventListener('scroll', () => {
      if (!isMobile.matches) {
        // Desktop view behavior
        if (!hasScrolled && window.scrollY > 10) {
          // Hide topmenu when scrolling down
          topmenu.style.display = 'none';
          navigation.style.marginTop = '0'; // Shift navigation up
          hasScrolled = true;
        } else if (hasScrolled && window.scrollY === 0) {
          // Show topmenu when scrolled back to the top
          topmenu.style.display = 'block';
          hasScrolled = false;
        }
      } else {
        // Mobile view: Always show both topmenu and navigation
        topmenu.style.display = 'block';
      }
    });

/* header scrolling*/



// error message timeout
document.addEventListener("DOMContentLoaded", function () {
  // Select all messages
  const messages = document.querySelectorAll('.message-container');

  // Loop through each message and set a timeout to hide it after a delay
  messages.forEach(function (message) {
      setTimeout(function () {
          message.style.display = 'none';
      }, 3000);
  });
});





//  Redirect to WhatsApp-start

    document.addEventListener('DOMContentLoaded', function () {
        document.getElementById('whatsappButton').addEventListener('click', function () {
            
            var phoneNumber = '8448983842';  //WhatsApp number
            var message = 'Hi, I would like to request a quote.'; // Customize the message
            var url = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;

            // Redirect to WhatsApp
            window.open(url, '_blank');
        });
    });



// request call 
  $('#request-call-btn').on('click', function () {
    $('#requestCallModal').modal('show');
});

// Handle the form submission via AJAX
$('#request-call-form').on('submit', function (e) {
    e.preventDefault();  // Prevent form from submitting the default way

    var formData = $(this).serialize();  // Serialize the form data

    // AJAX request to submit form data
    $.ajax({
        url: '/request-call/',  // The URL for handling the form submission
        method: 'POST',
        data: formData,
        success: function (response) {
            // Display success message
            $('#form-response').html('<div class="alert alert-success">Your request has been sent successfully!</div>');
            $('#request-call-form')[0].reset();  // Reset the form fields
            $('#requestCallModal').modal('hide');  // Close the modal
        },
        error: function (xhr, errmsg, err) {
            // Display error message
            $('#form-response').html('<div class="alert alert-danger">Something went wrong. Please try again.</div>');
        }
    });
});
 


//whatsapp icon fixed
const whatsappWrapper = document.createElement('div');
whatsappWrapper.classList.add('whatsapp-wrapper','pulse');

const whatsappLink = document.createElement('a');
whatsappLink.href = 'tel:84489 83842';
whatsappLink.target = '_blank';
whatsappLink.classList.add('whatsapp-icon');

whatsappWrapper.appendChild(whatsappLink);
document.body.appendChild(whatsappWrapper);
//whatsapp icon fixed

// side-social-icon

// Create the main wrapper div
const wrapper = document.createElement('div');
wrapper.classList.add('social-wrapper');

// Create the social block div
const socialBlock = document.createElement('div');
socialBlock.classList.add('social-block');

// Define an array of social media links and details
const socialMediaLinks = [
  {href: 'https://www.instagram.com/accuremedical/', class: 'facebook'},
  { href: 'https://www.linkedin.com/in/prashant-sharma-14604028b', class: 'linkedin' },
  { href: 'https://www.youtube.com/@AccureMedical', class: 'youtube' },
  { href: 'https://www.instagram.com/accuremedical/', class: 'instagram' },
  { href: 'https://x.com/AccuMart123', class: 'twitter' },
];

// Dynamically create social media icons
socialMediaLinks.forEach((social) => {
  const link = document.createElement('a');
  link.href = social.href;
  link.target = '_blank'; // Open in a new tab
  link.classList.add('side-social', social.class);
  socialBlock.appendChild(link);
});

// Append the social block to the wrapper
wrapper.appendChild(socialBlock);

// Append the wrapper to the body
document.body.appendChild(wrapper);
// side-social-icon



$.ajax({
  url: "/add-to-wishlist/" + productId + "/",
  method: "POST",
  headers: {
      'X-CSRFToken': csrfToken
  },
  success: function (response) {
      alert(response.message);

      // Update wishlist count dynamically
      if (response.wishlist_item_count) {
          $("#wishlist-item-count").text(response.wishlist_item_count);
      } else {
          console.error("wishlist_item_count not found in response");
      }
  },
  error: function (xhr, status, error) {
      alert("Error: " + error);
  }
});





