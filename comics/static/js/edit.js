var module = angular.module('whampow');

module.controller('editCtrl', ['$scope', '$http', function($scope, $http) {
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
        $scope.alert = {type: "error", message: "Mysterious error!" }
      }
      else {
        $scope.alert = { type: "success", message:  "Your subscriptions have been updated."}
      }
    });
  }
}]);