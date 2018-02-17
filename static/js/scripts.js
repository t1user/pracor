/* Toggle between adding and removing the "responsive" class to .menu-items when the user clicks on the icon */
function showMenu() {
    var x = document.getElementById("myTopnav");
    if (x.className === "menu-items") {
        x.className += " responsive";
    } else {
        x.className = "menu-items";
    }
}

/* show searchbar on mobile */
function showSearch() {
  var x = document.getElementById("mobile-searchbar");
    if (x.className === "search-mobile") {
        x.className += " responsive";
    } else {
        x.className = "search-mobile";
    }
}


/* switch off menu and searchbar on click outside */
var m = document.querySelector('main')
m.addEventListener("click", function() {
  var x = document.getElementById("myTopnav");
  var y = document.getElementById("mobile-searchbar");
  if (x.className === "menu-items responsive") {
    x.className = "menu-items";
};
  if (y.className === "search-mobile responsive") {
    y.className = "search-mobile";
};
}
)

/* on mobile - expand and collapse menu with add buttons*/
function listItems() {
    var x = document.getElementById("actionButton");
    if (x.className === "action-button") {
        x.className += " responsive";
        } else {
            x.className = "action-button";
}
}

/* autocomplete for search form */
$(function() {
  $(".auto-search").autocomplete({
    delay: 75,
    source: "/search/",
    minLength: 3,
    select: function(event, ui) {
      location.href="/" + ui.item.id + "/" + ui.item.slug;
}
});
});



$(".auto-position").autocomplete({
  delay: 75,
  source: function(request, response) {
    $.ajax({
      url:'',
      dataType: 'json',
      data:{
        'term': request.term,
        'field': this.element['0']['id']
      },
      success: function(data) {
        response(data);
      }
    })
  },
  minLength: 3,
});
