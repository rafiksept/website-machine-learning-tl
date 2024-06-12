var dropdownUser = document.getElementById("dropdown-user");
var profile = document.getElementById("profile");

dropdownUser.addEventListener("click",function() {

    if(profile.classList.contains("visible")){
        profile.classList.remove("visible");
        profile.classList.add("hidden");
    } else {
        profile.classList.add("visible");
        profile.classList.remove("hidden");
    }
    
    
})