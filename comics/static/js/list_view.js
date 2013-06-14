var module = angular.module('whampow', []);

module.directive('comicsList', function() {
  return {
    templateUrl: 'comic-search.html',
    link: function($scope) {
      $scope.selectedComics = window.selectedSeries || [];

      $scope.addSeries = function() {
        var title = $scope.formComic,
            series;

        $scope.allSeries.forEach(function(item) {
          if (item.title.toLowerCase() === title.toLowerCase()) series = item;
        });
        if (!series) {
          $.createAlert($("#search-alert-container"), "Series not found in our database.");
          return;
        }

        var exists = $scope.selectedComics.filter(function (comic) {
          return comic.id === series.id;
        }).length > 0;
        if (exists) {
          $.createAlert($("#search-alert-container"), "That series is already on your list.");
          return;
        }

        $scope.selectedComics.push(series);
        $scope.$emit("resetTypeahead");
      }
      $scope.removeSeries = function(idx) {
        $scope.selectedComics.splice(idx,1);
      }
    }
  }
});

module.directive('typeahead', function() {
  return function (scope, element, attrs) {
    element.typeahead({
      name: 'comics',
      prefetch: {
        url: '/comics',
        ttl: 0,
        filter: function(items) {
         scope.allSeries = items.map(function(item) {
           item.value = item.title;
           item.tokens = item.title.split(" ");
           return item;
         });
         return scope.allSeries;
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

    element.on("typeahead:selected", function(e, item) {
      scope.formComic = item.value;
    });
    element.on("typeahead:autocompleted", function(e, item) {
      scope.formComic = item.value;
    });

    scope.$on("resetTypeahead", function() {
      scope.formComic = "";
      element.typeahead('setQuery', '');
    })
  }
});

$.createAlert = function(container, message, type) {
  if (!type) type = 'error';
  var alertBox = $("<div class='alert alert-" + type + "'>").html(message)
    .append('<a class="close" data-dismiss="alert" href="#"><i class="icon-remove"></i></a>');
  container.append(alertBox);
};
