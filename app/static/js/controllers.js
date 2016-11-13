angular.module('demeter', ['oi.select', 'ngSanitize'])

.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
}])

.controller('ProfileCtrl', ['$scope', '$http', '$q', function($scope, $http, $q) {

    $scope.ingredients = [];

    /* get all ingredients in the database, so that they can be displayed in the lists */
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

    $scope.labels = ['Vegetarian', 'Gluten Free', 'Lactose Free']

    $scope.ingredientsSelected;
    $scope.restrictionsSelected;
    $scope.labelsSelected;

    $scope.age = $scope.ages[0];

    $scope.gender = $scope.genders[0];

    $scope.latitude, $scope.longitude;

    /* function to initialize user information when the user already exists */
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
                    $scope.userLocation = user.location;
                }

                if (user.coordinates != undefined) {
                    $scope.coordinates = "["+user.coordinates+"]";
                    var coordinates = user.coordinates.split(",");
                    $scope.latitude = coordinates[0];
                    $scope.longitude = coordinates[1];
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

                if (user.diet_labels != undefined) {
                    $scope.labelsSelected = [];
                    for (var i=0; i< user.diet_labels.length; i++) {
                        $scope.labelsSelected.push(user.diet_labels[i]);
                    }
                }
            });
        }
    }

    $scope.changeLocation = function() {
        $scope.userLocation = null;
    }

    /* function called when the save button is clicked */
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
        var diet_labels = $scope.labelsSelected;

        var user_profile = {
            location: location,
            coordinates: coordinates,
            age: age,
            gender: gender,
            ingredients: ingredients,
            restrictions: restrictions,
            diet_labels: diet_labels
        }

        $http.post('/register', user_profile)
        .success(function(response) {
            window.location = '/home';
        });

    }

}])

.controller('RecipeCtrl', ['$scope', '$http', function($scope, $http) {

    $scope.favorite = function(recipe_id) {
        //console.log(recipe_id)
        var data = {
            recipe_id : recipe_id
        }

        $http.post('/favorite', data)
        .success(function(response) {
            console.log(response)
            console.log("favorited!")
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
