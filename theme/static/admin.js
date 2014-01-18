$(document).ready(function() {
    window.bericht = window.bericht || {};
    window.bericht.admin = admin = {

        init: function() {
            admin.container = $('#article-list');
            $.getJSON('/articles.json')
                .success(admin.render_articles)
                .error(function(error) {
                    // @TODO: Handle errors
                });

            var keys = {
                'j': admin.select_prev_article,
                'k': admin.select_next_article
            };

            $.each(keys, function(k, f) {
                $(document).bind('keypress.'+k, f);
            });

        },
        render_articles: function(data) {
            $.each(data, admin.render_article);

            admin.articles = $(admin.container.children());
            admin.select_article(admin.articles.first());
        },
        render_article: function(index, item) {
            $('<article id="' + item.slug + '">' + 
              '<h2>' + item.title + '</h2>' + 
              '<div class="description">' + item.description + '</div>' +
              '</article>')
                .appendTo(admin.container); 
        },
        select_article: function(el) {
            if (typeof el === 'undefined' || el.length === 0) { return; }
            if (typeof admin.selected !== 'undefined') {
                admin.selected.removeClass('selected');
            }
            admin.selected = $(el);
            admin.selected.addClass('selected');
            // @TODO: scroll to element.
        },
        select_prev_article: function() {
            admin.select_article(admin.selected.prev());
        },
        select_next_article: function() {
            admin.select_article(admin.selected.next());
        },
    };
    admin.init();
});
