// This script is responsible for the dropdown menu in the navbar
// We need to wait until the DOM is loaded before we can interact with it
document.addEventListener('DOMContentLoaded', function() {
    // Store the current state of the dropdown menu, intially closed
    let isDropdownOpen = false;
    // Find the menu div
    const menu = document.querySelector('#menu');
    // Define the function to handle the dropdown button being clicked
    const handleDropdownClick = () => {
        // Toggle the state of the dropdown
        isDropdownOpen = !isDropdownOpen;
        // If the dropdown is open, add the open class to the menu, otherwise remove it
        if (isDropdownOpen) {
            menu.classList.add('open');
        } else {
            menu.classList.remove('open');
        }
    };
    // Define the function to handle the dropdown losing focus
    const handleDropdownFocusLoss = (event) => {
        // If the dropdown is open and the related target is not inside the menu, close the dropdown
        if (!event.relatedTarget || !menu.contains(event.relatedTarget)) {
            isDropdownOpen = false;
            menu.classList.remove('open');
        }
    };
    // Add event listeners to the dropdown button and the menu to handle clicks and focus loss
    document.querySelector('#accButton').addEventListener('click', handleDropdownClick);
    document.querySelector('#dropdown').addEventListener('focusout', handleDropdownFocusLoss);
});