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
     limit: 10
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
