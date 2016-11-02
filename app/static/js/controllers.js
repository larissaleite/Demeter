angular.module('demeter', ['oi.select', 'ngSanitize', 'ngMap'])

.config(['$interpolateProvider', function($interpolateProvider) {
          $interpolateProvider.startSymbol('{[');
          $interpolateProvider.endSymbol(']}');
   }])

  .controller('ProfileCtrl', ['$scope', '$http', '$q', function($scope, $http, $q) {

      $scope.ingredients = [];

      $http.get('/api/ingredients')
            .success(function(response) {
                var all_ingredients = response.all_ingredients;

                for (var i=0; i<all_ingredients.length; i++) {
                    $scope.ingredients.push(all_ingredients[i]);
                }
            });

      $scope.ages = [];

      for (var i=13; i<=90; i++) {
          $scope.ages.push(i);
      }

      $scope.genders = ['F', 'M'];

      $scope.ingredientsSelected;
      $scope.restrictionsSelected;

      $scope.age = $scope.ages[0];

      $scope.gender = $scope.genders[0];

      $scope.init = function(user_id) {
        if (user_id != undefined) {
            $scope.user_id = user_id

            $http.get('/api/user')
              .success(function(response) {
                  var user = response.user;

                  if (user.age != undefined) {
                      $scope.age = user.age;
                  }
                  if (user.gender != undefined) {
                      $scope.gender = user.gender;
                  }

                  if (user.location != undefined) {
                      $scope.location = user.location;
                  }

                  if (user.coordinates != undefined) {
                      $scope.coordinates = "["+user.coordinates+"]";
                  }

                  if (user.ingredients != undefined) {
                      $scope.ingredientsSelected = [];
                for (var i=0; i< user.ingredients.length; i++) {
                    $scope.ingredientsSelected.push(user.ingredients[i].name);
                }
            }

            if (user.restrictions != undefined) {
                $scope.restrictionsSelected = [];
                for (var i=0; i< user.restrictions.length; i++) {
                    $scope.restrictionsSelected.push(user.restrictions[i].name);
                }
            }
              });
          }
        }

      $scope.register = function() {

          var age = $scope.age;
          var gender = $scope.gender;

          var place = $scope.location;

          var location;

          if (place != undefined) {
              location = place.formatted_address;
              coordinates = place.geometry.location.lat() + ',' + place.geometry.location.lng()
          }

          var ingredients = $scope.ingredientsSelected;
          var restrictions = $scope.restrictionsSelected;

          var user_profile = {
              location: location,
              coordinates: coordinates,
              age: age,
              gender: gender,
              ingredients: ingredients,
              restrictions: restrictions
          }

          $http.post('/register', user_profile)
            .success(function(response) {
                window.location = '/home';
            });

    }

}])

    .directive('googlePlaces', function(){
        return {
            restrict:'E',
            replace:true,
            scope: {location: '='},
            template: '<div><div class="form-group"><label>Location</label><input id="google_places_ac" ng-model="placeModel" name="google_places_ac" type="text" class="form-control" placeholder="Location" /></div></div>',
            link: function($scope, elm, attrs){
                var autocomplete = new google.maps.places.Autocomplete($("#google_places_ac")[0], {});
                google.maps.event.addListener(autocomplete, 'place_changed', function() {
                    var place = autocomplete.getPlace();
                    //$scope.location = place.name + ',' + place.geometry.location.lat() + ',' + place.geometry.location.lng() + "," + place.formatted_address;
                    $scope.location = place;
                    $scope.$apply();
                });

            }
        }
    })
    .directive('ngEnter', function () {
        return function (scope, element, attrs) {
            element.bind("keydown keypress", function (event) {
                if(event.which === 13) {
                    scope.$apply(function (){
                        scope.$eval(attrs.ngEnter);
                    });

                    event.preventDefault();
                }
            });
        };
    });
