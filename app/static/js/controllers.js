angular.module('demeter', ['oi.select', 'ngSanitize', 'jkAngularRatingStars'])

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

    $scope.labels = []

    /* get all labels in the database, so that they can be displayed in the lists */
    $http.get('/api/labels')
    .success(function(response) {
        var all_labels = response.all_labels;

        for (var i=0; i<all_labels.length; i++) {
            $scope.labels.push(all_labels[i]);
        }
    });

    $scope.cuisines = []

    /* get all cuisines in the database, so that they can be displayed in the lists */
    $http.get('/api/cuisines')
    .success(function(response) {
        var all_cuisines = response.all_cuisines;

        for (var i=0; i<all_cuisines.length; i++) {
            $scope.cuisines.push(all_cuisines[i]);
        }
    });

    $scope.ingredientsSelected;
    $scope.restrictionsSelected;
    $scope.labelsSelected;
    $scope.cuisinesSelected;

    $scope.age = $scope.ages[0];

    $scope.gender = $scope.genders[0];

    $scope.latitude, $scope.longitude;

    /* function to initialize user information when the user already exists */
    $scope.init = function(user_id) {
        if (user_id != undefined) {
            $scope.user_id = user_id

            console.log(user_id)

            $http.get('/user')
            .success(function(response) {
                var user = response.user;
                console.log(user)

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

                if (user.preferred_ingredients != undefined) {
                    $scope.ingredientsSelected = [];
                    for (var i=0; i< user.preferred_ingredients.length; i++) {
                        $scope.ingredientsSelected.push(user.preferred_ingredients[i].name);
                    }
                }

                if (user.restricted_ingredients != undefined) {
                    $scope.restrictionsSelected = [];
                    for (var i=0; i< user.restricted_ingredients.length; i++) {
                        $scope.restrictionsSelected.push(user.restricted_ingredients[i].name);
                    }
                }

                if (user.diet_labels != undefined) {
                    $scope.labelsSelected = [];
                    for (var i=0; i< user.diet_labels.length; i++) {
                        $scope.labelsSelected.push(user.diet_labels[i]);
                    }
                }

                if (user.favorite_cuisines != undefined) {
                    $scope.cuisinesSelected = [];
                    for (var i=0; i< user.favorite_cuisines.length; i++) {
                        $scope.cuisinesSelected.push(user.favorite_cuisines[i]);
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
        } else {
            location = $scope.userLocation;
            coordinates = $scope.coordinates;
        }

        var ingredients = $scope.ingredientsSelected;
        var restrictions = $scope.restrictionsSelected;
        var diet_labels = $scope.labelsSelected;
        var favorite_cuisines = $scope.cuisinesSelected;

        var user_profile = {
            location: location,
            coordinates: coordinates,
            age: age,
            gender: gender,
            preferred_ingredients: ingredients,
            restricted_ingredients: restrictions,
            diet_labels: diet_labels,
            favorite_cuisines: favorite_cuisines
        }

        $http.post('/profile', user_profile)
        .success(function(response) {
            window.location = '/home';
        });

    }

}])

.controller('RecipeCtrl', ['$scope', '$http', function($scope, $http) {

    $scope.rating = 0;

    $scope.reviews = [];

    $scope.isFavoriteRecipe;

    $scope.init = function(recipe_oid, recipe_id, user_id, isFavorite, rating) {
        $scope.recipe_oid = recipe_oid;
        $scope.recipe_id = recipe_id;
        $scope.user_id = user_id;

        if (isFavorite == 'False')
            $scope.isFavoriteRecipe = false;
        else
            $scope.isFavoriteRecipe = true;

        $scope.rating = rating;
        console.log($scope.rating)

        $http.get('/recipe/reviews', { params : { recipe_id: recipe_oid } })
        .success(function(response) {
            $scope.reviews = response.reviews;
        });
    }

    $scope.onRating = function(rating) {
        console.log(rating)

        var data = {
            recipe_id : $scope.recipe_id,
            rating : rating
        }

        $http.post('/rating/new', data)
        .success(function(response) {
            console.log(response)
        });
    }

    $scope.favorite = function() {
        var data = {
            recipe_id : $scope.recipe_oid
        }

        $http.post('/favorite/new', data)
        .success(function(response) {
            console.log(response)
            $scope.isFavoriteRecipe = true;
        });
    }

    $scope.unfavorite = function() {
        var data = {
            recipe_id : $scope.recipe_oid
        }

        $http.post('/favorite/delete', data)
        .success(function(response) {
            console.log(response)
            $scope.isFavoriteRecipe = false;
        });

    }

    $scope.comment = function() {
        var review = $scope.review;

        var data = {
            recipe_id: $scope.recipe_oid,
            review: review
        }

        $http.post('/recipe/review/new', data)
        .success(function(response) {
            $scope.review = "";
            console.log(response.reviews[0]);
            $scope.reviews.push(response.reviews[0])
        });
    }

    $scope.delete_comment = function(review) {

        var data = {
            recipe_id: $scope.recipe_oid,
            date: review.date,
            review_id: review.id
        }

        $http.post('/recipe/review/delete', data)
        .success(function(response) {
            var index = $scope.reviews.indexOf(review);
            $scope.reviews.splice(index, 1);
        });
    }
}])

.controller('SearchCtrl', ['$scope', '$http', '$filter', function($scope, $http, $filter) {
    $scope.recipes = [];

    $scope.ingredients = [];

    $http.get('/api/ingredients')
    .success(function(response) {
        var all_ingredients = response.all_ingredients;

        for (var i=0; i<all_ingredients.length; i++) {
            $scope.ingredients.push(all_ingredients[i]);
        }
    });

    $scope.labels = []

    $http.get('/api/labels')
    .success(function(response) {
        var all_labels = response.all_labels;

        for (var i=0; i<all_labels.length; i++) {
            $scope.labels.push(all_labels[i]);
        }
    });

    $scope.cuisines = []

    $http.get('/api/cuisines')
    .success(function(response) {
        var all_cuisines = response.all_cuisines;

        for (var i=0; i<all_cuisines.length; i++) {
            $scope.cuisines.push(all_cuisines[i]);
        }
    });

    $scope.title;
    $scope.ingredientsSelected;
    $scope.labelsSelected;
    $scope.cuisinesSelected;

    $scope.showResults = false;

    $scope.search = function() {
        var search = {
            'title' : $scope.title,
            'ingredients' : $scope.ingredientsSelected,
            'labels' : $scope.labelsSelected,
            'cuisines' : $scope.cuisinesSelected
        }

        $http.post('/search', search)
        .success(function(response) {
            console.log(response)
            $scope.recipes = response
            $scope.showResults = true;
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
