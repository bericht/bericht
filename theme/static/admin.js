// @TODO Set djangos anti-cross-site-request-forgery-token.
//var token = $('meta[name="csrf-token"]').attr('content');
//xhr.setRequestHeader('X-CSRFToken', token);

$(document).ready(function() {
    var articles, keys;

    window.bericht = window.bericht || {};
    window.bericht.articles = articles = new ArticleList();
    new ArticleListView({collection: articles});

    keys = {
        'j': articles.next,
        'k': articles.prev,
    };
    
    $.each(keys, function(key, fn) {
        $(document).bind('keypress.'+key, fn);
    });
});

var Article = Backbone.Model.extend({
    defaults: {
        selected: false,
    },
});

var ArticleList = Backbone.Collection.extend({
    url: '/api/articles',
    model: Article,

    initialize: function() {
        _.bindAll(this, 'select', 'next', 'prev');
    },

    select: function(article) {
        if (typeof(this.selected) !== 'undefined') {
            this.selected.set({selected:false});
        } else {
            // @TODO: For the first change - from the default value to a new
            // one - there's no event triggered. For now: Workaround and
            // trigger it manually.
        }
        article.set({selected:true});
        this.selected = article;
    },

    next: function () {
        var next = this.at(this.indexOf(this.selected) + 1);
        if (typeof(next) !== 'undefined') this.select(next);
        return this;
    },

    prev: function() {
        var prev = this.at(this.indexOf(this.selected) - 1);
        if (typeof(prev) !== 'undefined') this.select(prev);
        return this;
    },

    parse: function(response) {
        return response.results;
    },
});

var ArticleSidebarView = Backbone.View.extend({
    tagName: 'li',
    events: { click: 'select' },

    initialize: function() {
        this.model.collection.on('change:selected', this.render, this);
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
    tagName: 'article',

    initialize: function() {
        this.render();
        this.model.on('change:selected', this.selected, this);
    },

    selected: function() {
        $('#content').html(this.$el);
    },
    
    render: function() {
        this.$el.attr('id', this.model.get('slug'))
            .append($('<h2>').html(this.model.get('title')))
            .append($('<div>').html(this.model.get('content')));
        return this;
    },
});

var ArticleListView = Backbone.View.extend({
    el: "#sidebar-list",

    initialize: function() {
        this.collection.on('reset', this.addAll, this);
        this.collection.on('add', this.addOne, this);
        this.collection.fetch({reset: true});
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


