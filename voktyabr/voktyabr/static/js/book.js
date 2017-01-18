(function () {
    'use strict';

    App.book_context_views = function (url) {
        //$('#search_result .gif').show();
        $.ajax({
            method: 'GET',
            type: "POST",
            url: url
            //url: window.location.pathname.replace('stats/keyword/', 'stats/keyword/search/'),
            //data: {
            //    'search_text': search_text,
            //    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            //}
        }).done(function (resp) {
            $('#book_context').html(resp);
        });
    };

    //$('#btn_book_context').on('click', App.book_context_views);


})();