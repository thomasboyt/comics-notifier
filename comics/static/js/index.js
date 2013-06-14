/* global createAlert, selectedSeries */

$(function() {
  $("#email-form").submit(function(e) {
    e.preventDefault();

    var ids = [];
    for (prop in selectedSeries) {
      ids.push(prop);
    }
    if (ids.length == 0) {
      // do some error
      $.createAlert($("#subscribe-alert-container"), "You need to add some series to subscribe to!");
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
          $.createAlert($("#subscribe-alert-container"), "You've already subscribed. To update your subscriptions, use the update link in your last email.")
        }
        else {
          $.createAlert($("#subscribe-alert-container"), "Mysterious error!");
        }
      }
      else {
        $.createAlert($("#subscribe-alert-container"), "Success! You should receive a confirmation email shortly.", "success");
      }
    });
  });
});
