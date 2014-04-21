
$(document).ready(function() {
    register_handlebar_helpers();

    var articles, keys;
    window.bericht = window.bericht || {};
    window.bericht.articles = articles = new ArticleList();
    new ArticleListView({collection: articles});
});

var render_template = function (name, context) {
    return Handlebars.templates[name](context);
};

var Article = Backbone.Model.extend({
    defaults: {
        selected: false,
    },
});

var ArticleList = Backbone.Collection.extend({
    url: function() { return window.bericht.api_endpoint; },
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

        if (response.count === 0) {
            $(ArticleView.prototype.el).html(
                '<div class="alert alert-info">' +
                    'Found no articles which matched the criteria.' +
                    '</div>');
            return;
        }
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
            .html('<a href="#">' + this.model.get('title') + '</a>');
        return this;
    },

    select: function() {
        this.model.collection.select(this.model);
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

        var first = this.collection.at(0);
        if (first !== undefined) {
            this.collection.select(first);
        }
    },

    addOne: function(article) {
        new ArticleView({model: article});
        var sidebar_view = new ArticleSidebarView({model: article});
        this.$el.append(sidebar_view.render().el);
    },
});

var ArticleView = Backbone.View.extend({
    el: "#content",

    initialize: function() {
        this.voting_bar = new VoteView({model: this.model});
        this.model.on('change:selected', this.render, this);

    },

    render: function() {
        this.$el.html(render_template(
            'article-single', {article: this.model.attributes}));
        this.$el.find('article .meta').prepend(this.voting_bar.render().el);
        this.voting_bar.delegateEvents();
        return this;
    },
});

var VoteView = Backbone.View.extend({
    className: "voting",
    events: { 'click button': 'vote' },

    render: function() {
        this.$el.html(render_template(
            'voting-bar', {article: this.model.attributes}));
        return this;
    },

    vote: function(event) {
        var self = this;
        var vote = $(event.target).children('.name').text().toLowerCase();
        $.post('/api/votes/' + this.model.attributes.id + '/' + vote + '/',
               function(data) {
                   self.model.set(data);
                   self.render();
               });
    },
});

var register_handlebar_helpers = function() {
    Handlebars.registerHelper('vote-icon', function(vote) {
        return new Handlebars.SafeString({
            'YES':  'glyphicon-thumbs-up',
            'NO':   'glyphicon-thumbs-down',
            'VETO': 'glyphicon-remove',
        }[vote]);
    });

    Handlebars.registerHelper('user-vote', function(vote, user_vote) {
        if (vote === user_vote) {
            return new Handlebars.SafeString({
                'YES':  'btn-success',
                'NO':   'btn-warning',
                'VETO': 'btn-danger',
            }[vote]);
        }
    });

    Handlebars.registerHelper('capitalize', function(vote) {
        return new Handlebars.SafeString(
            vote.charAt(0).toUpperCase() + vote.slice(1).toLowerCase());
    });
};
