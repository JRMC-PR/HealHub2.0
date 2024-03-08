document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.getElementById('toggle1'); // Get the checkbox
  const menu = document.querySelector('.menu1'); // Get the menu

  toggle.addEventListener('change', function () {
    // Listen for the checkbox state change
    if (this.checked) {
      menu.style.transform = 'translateX(0)'; // Show the menu
    } else {
      menu.style.transform = 'translateX(-100%)'; // Hide the menu
    }
  });
});
