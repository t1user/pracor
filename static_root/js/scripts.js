/* Toggle between adding and removing the "responsive" class to .menu-items when the user clicks on the icon */

function showCollapsibleMenu() {
    var x = document.getElementById("collapsibleMenu");
    if (x.className === "collapsible-menu") {
        x.className += " responsive";
    } else {
        x.className = "collapsible-menu";
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
  var z = document.getElementById("collapsibleMenu");
  if (x.className === "menu-items responsive") {
    x.className = "menu-items";
};
  if (y.className === "search-mobile responsive") {
    y.className = "search-mobile";
};
  if (z.className === "collapsible-menu responsive") {
    z.className = "collapsible-menu";
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


/* autocomplete for Position forms */
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
