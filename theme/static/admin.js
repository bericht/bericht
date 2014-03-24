// @TODO Set djangos anti-cross-site-request-forgery-token.
//var token = $('meta[name="csrf-token"]').attr('content');
//xhr.setRequestHeader('X-CSRFToken', token);

$(document).ready(function() {
    var articles, keys;

    window.bericht = window.bericht || {};
    window.bericht.articles = articles = new ArticleList();
    new ArticleListView({collection: articles});
});

var render_template = function (name, context) {
    return Mustache.render(Mustache.TEMPLATES[name], context);
};

var Article = Backbone.Model.extend({
    defaults: {
        selected: false,
    },
});

var ArticleList = Backbone.Collection.extend({
    url: '/api/articles',
    model: Article,
    page: 1,

    initialize: function() {
        _.bindAll(this, 'select', 'next', 'prev', 'next_page', 'prev_page');
    },

    select: function(article) {
        if (typeof(this.selected) !== 'undefined') {
            this.selected.set({selected:false});
        }
        article.set({selected:true});
        this.selected = article;
    },

    next: function () {
        var next = this.at(this.indexOf(this.selected) + 1);
        if (typeof(next) !== 'undefined') {
            this.select(next);
        } else if (this.next_url) { this.next_page(); }
        return this;
    },

    next_page: function() {
        this.url = this.next_url;
        this.fetch().done(_.bind(function() {
            this.select(this.first());
        }, this));
    },

    prev: function() {
        var prev = this.at(this.indexOf(this.selected) - 1);
        if (typeof(prev) !== 'undefined') {
            this.select(prev);
        } else if (this.prev_url) { this.prev_page(); }
        return this;
    },

    prev_page: function() {
        this.url = this.prev_url;
        this.fetch().done(_.bind(function() {
            this.select(this.last());
        }, this));
    },

    parse: function(response) {
        this.prev_url = response.previous;
        this.next_url = response.next;
        return response.results;
    },
});

var ArticleSidebarView = Backbone.View.extend({
    tagName: 'li',
    events: { click: 'select' },

    initialize: function() {
        this.model.collection.on('change:selected', this.render, this);
        this.model.on('remove', _.bind(function(model, collection, options) {
            this.remove();
        }, this));
    },

    render: function() {
        this.$el.attr('id', 'sidebar-' + this.model.get('slug'))
            .toggleClass('selected', this.model.get('selected'))
            .html(this.model.get('title'));
        return this;
    },

    select: function() {
        this.model.collection.select(this.model);
    },
});

var ArticleView = Backbone.View.extend({
    initialize: function() {
        this.render();
        this.model.on('change:selected', this.render, this);
        this.model.on('remove', _.bind(function(model, collection, options) {
            this.remove();
        }, this));
    },

    render: function() {
        $('#content').html(render_template(
            'article-single', {article: this.model.attributes}));
        return this;
    },
});

var ArticleListView = Backbone.View.extend({
    el: "#sidebar-list",

    initialize: function() {
        this.collection.on('reset', this.addAll, this);
        this.collection.on('add', this.addOne, this);
        this.collection.fetch({reset: true});

        keys = {
            'k': this.collection.prev,
            'j': this.collection.next,
        };
        $.each(keys, function(key, fn) {
            $(document).bind('keypress.'+key, fn);
        });

        $('#sidebar .pager .previous a').click(this.collection.prev_page);
        $('#sidebar .pager .next a').click(this.collection.next_page);
    },

    addAll: function() {
        this.collection.each(this.addOne, this);
        this.collection.select(this.collection.at(0));
    },

    addOne: function(article) {
        new ArticleView({model: article});
        var sidebar_view = new ArticleSidebarView({model: article});
        this.$el.append(sidebar_view.render().el);
    },
});


