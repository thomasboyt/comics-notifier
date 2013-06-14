// series to subscribe to
// global so that submit code can access it
// (implicit TODO there of course being to refactor, this is pretty gnarly)
if (!window.selectedSeries)
  window.selectedSeries = {};

$.createAlert = function(container, message, type) {
  if (!type) type = 'error';
  var alertBox = $("<div class='alert alert-" + type + "'>").html(message)
    .append('<a class="close" data-dismiss="alert" href="#"><i class="icon-remove"></i></a>');
  container.append(alertBox);
};

$(function() {
  var allSeries; // populated in prefetch

  var addRow = function(data) {
    var table = $("#series-table");
    var row = $("<tr>");
    row.append($("<td>").text(data.title));

    var delLink = $("<a href='#' class='delete-link'><i class='icon-remove'></i></a>");
    row.append($("<td>").append(delLink));

    delLink.click(function(e) {
      e.preventDefault();
      delete selectedSeries[data.id];
      row.remove();
    })

    table.append(row);

    if (table.css("display") == "none") table.toggle();
  }

  for (var prop in selectedSeries) {
    if (selectedSeries.hasOwnProperty(prop)) {
      addRow(selectedSeries[prop]);
    }
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
        if (!(a.indexOf(prefix) == 0 && b.indexOf(prefix) == 0)) {
          if (a.indexOf(prefix) == 0) return -1;
          if (b.indexOf(prefix) == 0) return 1;
        }
        return a > b ? 1 : -1;
      });
    }
  });

  $("#search-form").submit(function(e) {
    e.preventDefault();

    var title = $("#search").val();
    var series;
    allSeries.forEach(function(item) {
      if (item.title.toLowerCase() === title.toLowerCase()) series = item;
    });

    if (!series) {
      $.createAlert($("#search-alert-container"), "Series not found in our database.");
    }
    else if (selectedSeries[series.id]) {
      $.createAlert($("#search-alert-container"), "That series is already on your list.");
    }
    else {
      selectedSeries[series.id] = series;
      addRow(series);
      $("#search").typeahead('setQuery', '');
    }
  });

});
