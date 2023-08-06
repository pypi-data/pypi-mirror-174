ckan.module("flakes-rating-rate", function ($) {
  "use strict";

  return {
    options: {
      type: null,
      id: null,
      current: 0,
    },
    initialize: function () {
      $.proxyAll(this, /_on/);
      this.el.find(".star").on({
        click: this._onClick,
        mouseover: this._onOver,
        mouseout: this._onOut,
      });
      if (this.options.current) {
        this.setStars(this.options.current);
      }
    },
    setStars: function (n) {
      var el = this.$(".star").eq(n - 1);
      el.prevAll()
        .add(el)
        .removeClass("star-empty fa-star-o")
        .addClass("fa-star");
      el.nextAll().addClass("star-empty fa-star-o").removeClass("fa-star");
    },

    _onClick: function (e) {
      var rating = this.$(".star").index(e.target) + 1;
      this.setStars(rating);
      this.sandbox.client.call("POST", "flakes_rating_rate", {
        target_type: this.options.type,
        target_id: this.options.id,
        rating: rating,
      });
    },
    _onOver: function (e) {
      var el = $(e.target);
      el.prevAll().add(el).addClass("active");
    },
    _onOut: function (e) {
      var el = $(e.target);
      el.prevAll().add(el).removeClass("active");
    },
  };
});
