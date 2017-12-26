/* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */

function showMenu() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
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
  if (x.className === "topnav responsive") {
    x.className = "topnav";
};
  if (y.className === "search-mobile responsive") {
    y.className = "search-mobile";
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


$(function() {
  $(".auto-search").autocomplete({
    source: "/search/",
    minLength: 3,
    select: function(event, ui) {
      location.href="/" + ui.item.id;
}
});
});



$(".auto-position").autocomplete({
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



/*

$(function() {
  $(".auto-position").autocomplete({
    source: function(request, response) {
        $.ajax({
            url:'',
            dataType: 'json',
            data:{
                'field': $(this).val(this.item.val),
                },
            success: function(data){
                response(data);
                }
            })},
    minLength: 4,
    select: function(event, ui) {
      location.href="/" + ui.item.id;
}
});
})
*/
