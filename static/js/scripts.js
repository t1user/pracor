/* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */
function showMenu() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}

var m = document.querySelector('main')

m.addEventListener("click", function() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav responsive") {
    x.className = "topnav";
};
}
)


function listItems() {
    var x = document.getElementById("actionButton");
    if (x.className === "action-button") {
        x.className += " responsive";
        } else {
            x.className = "action-button";
}
}

