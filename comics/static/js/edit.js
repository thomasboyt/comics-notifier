var module = angular.module('whampow');

module.controller('editCtrl', function($scope, $http) {
  function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
  }

  $scope.submit = function() {
    var ids = $scope.selectedComics.map(function(comic) {
      return comic.id;
    });

    $http.post("/edit", {
      email: getParameterByName("email"),
      key: getParameterByName("key"),
      ids: ids
    }).success(function(data) {
      if (data.error) {
        $.createAlert($("#edit-alert-container"), "Mysterious error!")
      }
      else {
        $.createAlert($("#edit-alert-container"), "Your subscriptions have been updated.", "success")
      }
    })
  }
})
