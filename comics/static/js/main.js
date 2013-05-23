$(function() {

  // series to subscribe to
  var selectedSeries = {};
  var allSeries; // populated in prefetch

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

  var typeahead = $("#search").typeahead({
    name: 'comics',
    prefetch: {
      url: '/comics',
      ttl: 0,
      filter: function(items) {
       allSeries = items.map(function(item) {
         item.value = item.title;
         item.tokens = item.title.split(" ");
         return item;
       });
       return allSeries;
      }
    },
    limit: 10,
    transformSuggestions: function(terms, suggestions) {
      var prefix = terms.join(" ").toLowerCase();
      return suggestions.sort(function(a,b) {
        a = a.value.toLowerCase(), b = b.value.toLowerCase();
        if(!(a.indexOf(prefix) == 0 && b.indexOf(prefix) == 0)) {
          if(a.indexOf(prefix) == 0) return -1;
          if(b.indexOf(prefix) == 0) return 1;
        }
        return a > b ? 1 : -1;
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
    var series;
    allSeries.forEach(function(item) {
      if (item.title.toLowerCase() === title.toLowerCase()) series = item;
    });

    if (!series) {
      createAlert($("#search-alert-container"), "Series not found in our database.");
    }
    else if (selectedSeries[series.id]) {
      createAlert($("#search-alert-container"), "That series is already on your list.");
    }
    else {
      selectedSeries[series.id] = series;
      addRow(series);
      $(".tt-query").val("");
      $(".tt-hint").val("");
      $(".tt-dropdown-menu").hide();
    }
  });

  $("#email-form").submit(function(e) {
    e.preventDefault();

    var ids = [];
    for (prop in selectedSeries) {
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
        if (data.desc === "USER_EXISTS") {
          createAlert($("#subscribe-alert-container"), "You've already subscribed. To update your subscriptions, use the update link in your last email.")
        }
        else {
          createAlert($("#subscribe-alert-container"), "Mysterious error!");
        }
      }
      else {
        createAlert($("#subscribe-alert-container"), "Success! You should receive a confirmation email shortly.", "success");
      }
    });
  });
    
});
