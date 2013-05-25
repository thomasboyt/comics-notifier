$(function() {
  function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
  } 

  $("#edit-submit").click(function(e) {
    e.preventDefault();

    var ids = [];
    for (prop in selectedSeries) {
      ids.push(prop);
    }
    ids = ids.join(",");

    $.post("/edit", {
      email: getParameterByName("email"),
      key: getParameterByName("key"),
      ids: ids
    }, function(data) {
      if (data.error) {
        $.createAlert($("#edit-alert-container"), "Mysterious error!")
      }
      else {
        $.createAlert($("#edit-alert-container"), "Your subscriptions have been updated.", "success")
      }
    });
  });
});
