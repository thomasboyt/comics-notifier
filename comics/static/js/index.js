/* global createAlert, selectedSeries */

var module = angular.module('whampow');

module.controller('indexCtrl', ['$scope', '$http', function($scope, $http) {
  $scope.submit = function() {
    if (!$scope.validate()) {
      return;
    }

    var ids = $scope.selectedComics.map(function(comic) {
      return comic.id;
    });

    $http.post("/subscribe", {
      email: $scope.email,
      ids: ids
    }).success(function(data) {
      if (data.error === "user exists") {
        $.createAlert($("#subscribe-alert-container"), "You've already subscribed. To update your subscriptions, use the update link in your last email.")
      }
      else if (data.error) {
        $.createAlert($("#subscribe-alert-container"), "Mysterious error.")
      }
      else {
        $.createAlert($("#subscribe-alert-container"), "Success! You should receive a confirmation email shortly.", "success");
      }
    })
  }

  $scope.validate = function() {
    return $scope.selectedComics
      && $scope.selectedComics.length > 0
      && $scope.email !== undefined
      && $scope.email !== "";
  }
}]);
