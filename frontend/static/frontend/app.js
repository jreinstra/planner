(function() {
  'use strict';

  angular.module('cardinalPlanner', ['ui.router'])
  
  .constant('BASE_URL', '.')
  
  .controller('LoginCtrl', function($rootScope, $scope, $state, $http, BASE_URL) {
    $scope.login = function() {
      FB.login(function(response) {
        console.log(response);
        if (response.status == "connected") {
          $scope.getAuthToken(response);
        } else {
          alert('Could not login with Facebook, please try again.');
        }
      }, {scope: 'email'});
    };
    
    $scope.getAuthToken = function(response) {
      $http.post(BASE_URL + '/api/login/', {fb_access_token: response.authResponse.accessToken})
        .then(function(response) {
          console.log(response);
          $http.defaults.headers.common['Authorization'] = 'Token ' + response.data;
          $rootScope.loggedIn = true;
        }, function(response) {
          console.log(response);
        });
    };
  })
  
  .controller('HomeCtrl', function($rootScope, $scope, $state, $http, BASE_URL){
    $scope.update = function() {
      if ($scope.search == "") {
        $scope.result = [];
        return;
      }
      $scope.loading = true;
      $http.get(BASE_URL + '/api/search/?q=' + $scope.search)
        .then(function(response) {
          $scope.result = response.data
          $scope.loading = false;
        }, function(response) {
          alert('Could not connect to server.')
          $scope.loading = false;
        });
    };
    return $scope;
  })
  
  .controller('CourseCtrl', function($rootScope, $scope, $state, $http, BASE_URL){
    
    // Comments
    $scope.reply = true;
    $scope.minimal = false;
    $scope.collapsible = false;
    $scope.replyingTo = null;
    $scope.newReply = '';
    
    // Reviews
    $scope.canPostReview = true;
    $scope.loading = true;
    $http.get(BASE_URL + '/api/courses/' + $state.params.id)
      .then(function(response) {
        console.log(response);
        $scope.result = response.data;
        $scope.loading = false;
      }, function(response) {
        alert('Could not connect to server.');
        $scope.loading = false;
      });
    
    // Add Logic Here To Check If User canPostReview
    
    $scope.replyTo = function(comment) {
      $scope.replyingTo = comment;
    };
    
    $scope.cancelReply = function() {
      $scope.replyingTo = null;
    };
    
    $scope.addReply = function() {
      if (!$scope.newReply) {
        return alert("Please fill out a comment.");
      }

      if ($scope.replyingTo) {
        $http.post(BASE_URL + '/api/comments/', {content_object: 'comment:' + $scope.replyingTo.id, text: $scope.newReply})
          .then(function(response) {
            $scope.replyingTo.comments.push(response.data);
            $scope.replyingTo = null;
            $scope.newReply = '';
        }, function(response) {
          alert('Could not connect to server.')
        });
      } else {
        $http.post(BASE_URL + '/api/comments/', {content_object: 'course:' + $state.params.id, text: $scope.newReply})
          .then(function(response) {
            $scope.result.comments.push(response.data);
            $scope.newReply = '';
        }, function(response) {
          alert('Could not connect to server.')
        });
      }
    };
    
    $scope.addReview = function() {
      if (!$scope.newReview) {
        return alert("Please fill out the review." + $scope.rating + $scope.grade);
      }
      
      if (typeof $scope.rating == "undefined" || typeof $scope.grade == "undefined" || $scope.grade == "") {
        return alert("Please fill out your grade and rating.");
      }

      $http.post(BASE_URL + '/api/reviews/', {course: $state.params.id, rating: $scope.rating, grade:$scope.grade, text: $scope.newReview})
        .then(function(response) {
          $scope.result.reviews.push(response.data);
          $scope.newReview = '';
          $scope.canPostReview= false;
      }, function(response) {
        alert('Could not connect to server.')
      });
    };
    
    return $scope;
  })
  
  .controller('InstructorCtrl', function($rootScope, $scope, $state, $http, BASE_URL) {
    
    $http.get(BASE_URL + '/api/instructors/' + $state.params.sunet)
      .then(function(response) {
        $scope.result = response.data;
      }, function(response) {
        alert('Could not connect to server.')
      });
  })
  
  
  .config(function($stateProvider, $urlRouterProvider, $locationProvider) {
  
    $urlRouterProvider.otherwise('/');
  
    $locationProvider.html5Mode({
      enabled: false,
      requireBase: false
    });
  
    $stateProvider
      .state('home', {
        url: '/',
        templateUrl: 'static/frontend/partials/home.html',
        controller: 'HomeCtrl'
      })
      .state('course', {
        url: '/course/:id',
        templateUrl: 'static/frontend/partials/course.html',
        controller: 'CourseCtrl'
      })
      .state('instructor', {
        url: '/instructor/:sunet',
        templateUrl: 'static/frontend/partials/instructor.html',
        controller: 'InstructorCtrl'
      });
      
    $locationProvider.hashPrefix('!');
  })
  
  .run(function() {
    FastClick.attach(document.body);
  });

})();