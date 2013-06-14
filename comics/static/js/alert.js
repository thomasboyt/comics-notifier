var module = angular.module("whampow", []);

module.directive("alert", function() {
  return {
    templateUrl: "alert.html",
    restrict: "E",
    scope: {
      "alertObject": "=alertObject"
    },
  }
});