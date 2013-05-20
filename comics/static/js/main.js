$(function() {

  // series to subscribe to
  var series = {};

  var addRow = function(data) {
    var table = $("#series-table");
    var row = $("<tr>");
    row.append($("<td>").text(data.title));

    var delLink = $("<a href='#' class='delete-link'>[ X ]</a>");
    row.append($("<td>").append(delLink));

    delLink.click(function(e) {
      e.preventDefault();
      delete series[data.id];
      row.remove();
    })

    table.append(row);

    if (table.css("display") == "none") table.toggle();
  }

  var autocompleter = function(query, process) {
    $.getJSON("/search", {query: query}, function(data, status) {
      process(data.map(function(item) {return item.title}));
    });
  };

   var typeahead = $("#search").typeahead({
    source: autocompleter,
    items: 20,
    minLength: 1,
    highlighter: function(item) {
      var query = this.query.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/, '\\$&');

      // one char change: made matcher not global, since this is just prefix search
      return item.replace(new RegExp('(' + query + ')', 'i'), function ($1, match) {
        return '<strong>' + match + '</strong>'
      });
    }
  });

  var createAlert = function(container, message, type) {
    if (!type) type = 'error';
    var alertBox = $("<div class='alert alert-" + type + "'>").html(message)
      .append('<a class="close" data-dismiss="alert" href="#">&times;</a>');
    container.append(alertBox);
  }

  $("#search-form").submit(function(e) {
    e.preventDefault();
    
    var title = $("#search").val();
    $.getJSON("/title/" + encodeURIComponent(title), function(data, status) {
      if (!series[data.id]) {
        series[data.id] = data;
        addRow(data);
        $("#search").val("");
      }
      else {
        createAlert($("#search-alert-container"), "That series is already on your list.");
      }
    }).fail(function(e) {
      if (e.status == 404) {
        createAlert($("#search-alert-container"), "Series not found.");
      }
    });
  });

  $("#email-form").submit(function(e) {
    e.preventDefault();

    var ids = [];
    for (prop in series) {
      ids.push(prop);
    }
    if (ids.length == 0) {
      // do some error
      createAlert($("#subscribe-alert-container"), "You need to add some series to subscribe to!");
      return;
    }
    ids = ids.join(",");

    var email = $("#email").val();
    if (!email) {
      return;
    }

    $.getJSON("/subscribe", {email: email, ids: ids}, function(data) {
      if (data.error) {
        createAlert($("#subscribe-alert-container"), "Mysterious error!");
      }
      else {
        createAlert($("#subscribe-alert-container"), "Success! You should receive a confirmation email shortly.", "success");
      }
    });
  });
    
});
