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
        $scope.alert = { type: "error",
          message: "You've already subscribed. To update your subscriptions, use the update link in your last email."}
      }
      else if (data.error) {
        $scope.alert = { type: "error",
          message: "Mysterious error."}
      }
      else {
        $scope.alert = { type: "success",
          message: "Success! You should receive a confirmation email shortly."}
      }
    }).error(function(data) {
      $scope.alert = { type: "error",
        message: "Mysterious error."}
    })
  }

  $scope.validate = function() {
    return $scope.selectedComics
      && $scope.selectedComics.length > 0
      && $scope.email !== undefined
      && $scope.email !== "";
  }
}]);
