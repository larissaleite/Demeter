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

    $scope.init = function(recipe_id, user_id, isFavorite, rating) {
        $scope.recipe_id = recipe_id;
        $scope.user_id = user_id;

        if (isFavorite == 'False')
            $scope.isFavoriteRecipe = false;
        else
            $scope.isFavoriteRecipe = true;

        $scope.rating = rating;

        $http.get('/recipe/reviews', { params : { recipe_id: recipe_id } })
        .success(function(response) {
            console.log(response.reviews)
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
            recipe_id : $scope.recipe_id
        }

        $http.post('/favorite/new', data)
        .success(function(response) {
            console.log(response)
            $scope.isFavoriteRecipe = true;
        });
    }

    $scope.unfavorite = function() {
        var data = {
            recipe_id : $scope.recipe_id
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
            recipe_id: $scope.recipe_id,
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
            recipe_id: $scope.recipe_id,
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

.controller('AnalysisCtrl', ['$scope', '$http', '$filter', function($scope, $http, $filter) {

    //$scope.categories = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


    $scope.showWeek = false; $scope.showMonth = false; $scope.showYear = false;

    $scope.countries = ["All", "Belgium", "Spain", "France", "Germany"]

    $scope.country = $scope.countries[0];

    $scope.month = {
      value: new Date(2016, 0, 1)
    };

    $scope.week = {
      value: new Date(2016, 0, 3)
    };

    $scope.selectWeek = function() {
        $scope.showWeek = true;
        $scope.showMonth = false;
        $scope.showYear = false;
    }

    $scope.selectMonth = function() {
        $scope.showWeek = false;
        $scope.showMonth = true;
        $scope.showYear = false;
    }

    $scope.selectYear = function() {
        $scope.showWeek = false;
        $scope.showMonth = false;
        $scope.showYear = true;
    }

    $scope.getData = function() {
        if ($scope.showWeek) {
            var week = $scope.week.value;
            /*week = week.split("-")[1]
            if (week.charAt(0) == '0') {
                week = week.charAt(1)
            }*/
            console.log(week)
            var week_no = $filter('date')(week, 'w');
            console.log(week_no);

            /*$http.get('/comments_favorites_week', { params : { week: week, country : country } })
            .success(function(response) {
                console.log(response)
            });*/
        } else if ($scope.showMonth) {
            var month = $scope.month.value + '';
            month = month.split(" ")[1]
            console.log(month)
            console.log($scope.country)

            $http.get('/comments_favorites_month', { params : { month: month, country : country } })
            .success(function(response) {
                console.log(response)
            });
        } else  {
            $http.get('/comments_favorites_year', { params : { country : $scope.country } })
            .success(function(response) {
                $scope.categories = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug",  "Sep", "Oct", "Nov", "Dec"]

                var favorite_months_data = new Array(12+1).join('0').split('').map(parseFloat)

                for (var r in response) {
                    console.log(response[r])
                    if (response[r]._id == "Jan") {
                        favorite_months_data[0] = response[r].count;
                    }  else if (response[r]._id == "Feb") {
                        favorite_months_data[1] = response[r].count;
                    } else if (response[r]._id == "Mar") {
                        favorite_months_data[2] = response[r].count;
                    } else if (response[r]._id == "Apr") {
                        favorite_months_data[3] = response[r].count;
                    } else if (response[r]._id == "May") {
                        favorite_months_data[4] = response[r].count;
                    } else if (response[r]._id == "June") {
                        favorite_months_data[5] = response[r].count;
                    } else if (response[r]._id == "July") {
                        favorite_months_data[6] = response[r].count;
                    } else if (response[r]._id == "Aug") {
                        favorite_months_data[7] = response[r].count;
                    } else if (response[r]._id == "Sep") {
                        favorite_months_data[8] = response[r].count;
                    } else if (response[r]._id == "Oct") {
                        favorite_months_data[9] = response[r].count;
                    } else if (response[r]._id == "Nov") {
                        favorite_months_data[10] = response[r].count;
                    } else if (response[r]._id == "Dec") {
                        favorite_months_data[11] = response[r].count;
                    }
                }

                $scope.favorite_months_data = favorite_months_data;

                $(function () {
                    Highcharts.chart('chart_nb_interaction', {
                        chart: {
                            type: 'line'
                        },
                        title: {
                            text: 'Number of Interaction (Global)'
                        },
                        xAxis: {
                              categories: $scope.categories
                        },
                    series: [
                          {
                            name: 'Favourite',
                            data: $scope.favorite_months_data
                          },
                          {
                            name: 'Comment',
                            data: [18, 21, 25, 26, 23, 6, 9]
                        }
                       ]
                    });
                });
            });
        }
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
