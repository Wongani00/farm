// // Select all sidebar links
// const sidebarLinks = document.querySelectorAll('.sidebar a');

// // Default active link (set to the home page)
// const defaultActiveLink = '{{ url_for("index") }}'; // Adjust this for your routing

// // Function to set the active link on page load
// function setActiveLink() {
//     // Check if there's an active link stored in localStorage
//     let activeLink = localStorage.getItem('activeLink');

//     // If no active link is stored, set it to Home and store it
//     if (!activeLink) {
//         activeLink = defaultActiveLink; // Set to Home by default
//         localStorage.setItem('activeLink', activeLink); // Store the home link as the active link
//     } 

//     // Highlight the correct active link
//     sidebarLinks.forEach(link => link.classList.remove('active'));
//     const currentActiveLink = document.querySelector(`a[href="${activeLink}"]`);
//     if (currentActiveLink) {
//         currentActiveLink.classList.add('active');
//     }
// }

// // Call the function to set the active link on page load
// setActiveLink();

// // Loop through the links and add a click event listener
// sidebarLinks.forEach(link => {
//     link.addEventListener('click', function(event) {
//         // Remove the 'active' class from all links
//         sidebarLinks.forEach(link => link.classList.remove('active'));

//         // Add the 'active' class to the clicked link
//         this.classList.add('active');

//         // Store the clicked link's href in localStorage
//         localStorage.setItem('activeLink', this.getAttribute('href'));

//         // Trigger navigation to the new page
//         window.location.href = this.getAttribute('href');
//     });
// });

const activePage = window.location.pathname.replace(/\/$/, ""); // Remove trailing slash
const links = document.querySelectorAll(".sidebar a");

links.forEach(link => {
    const linkPath = new URL(link.href).pathname.replace(/\/$/, ""); // Remove trailing slash from href
    if (linkPath === activePage) {
        link.classList.add("active");
    }
});

//form handling
document.querySelector(".form").addEventListener("submit", function(event){
    event.preventDefault(); //preventing ormal form submission
    const formData = new FormData(this); //collecting form input data

    console.log(document.getElementById("market"));
    const data = {};//an object of form data
    formData.forEach((value, key)=>{
        data[key] = value;
    });
    console.log(data);
    //defining an api for ansynchronous communication
    fetch("/prediction", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(data)
    }).then(response => response.json()).then(result => {
        document.getElementById("result").innerHTML = "Predicted Price(MWK)/KG: "+result.price;
    }).catch(error => {
        console.log("Error: ",error); //printing the error in the console
    })
    document.querySelector("#date").value = "";
});