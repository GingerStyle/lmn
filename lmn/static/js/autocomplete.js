// Code at https://medium.com/@ninajlu/django-ajax-jquery-search-autocomplete-d4b4bf6494dd

let queryType = $('.query-type').attr('id');

$(document).ready(function() {
    $("#txtSearch").autocomplete({
        source: `/ajax_calls/search/${queryType}`,
        minLength: 1,
        open: function() {
            setTimeout(function() {
                $('.ui-autocomplete').css('z-index', 99);
            }, 0);
        }
    });
});
