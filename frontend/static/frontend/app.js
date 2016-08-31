(function() {
  'use strict';

  angular.module('cardinalPlanner', ['ui.router'])
  
  .constant('BASE_URL', '.')
  
  .controller('LoginCtrl', function($scope, $state, $http, BASE_URL) {
    $scope.login = function() {
      FB.login(function(response) {
        console.log(response);
        $scope.response = response;
      }, {scope: 'email'});
      
      if ($scope.response.status == "connected") {
        $http.post(BASE_URL + '/api/login/', {fb_access_token: $scope.response.authResponse.accessToken})
          .then(function(response) {
            console.log(response);
          }, function(response) {
            console.log(response);
          });
      } else {
        alert('Could not login with Facebook, please try again.');
      }
    };
  })
  
  .controller('HomeCtrl', function($scope, $state, $http, BASE_URL){
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
  
  .controller('CourseCtrl', function($scope, $state, $http, BASE_URL){
    
    $http.get(BASE_URL + '/api/courses/' + $state.params.id)
      .then(function(response) {
        console.log(response);
        $scope.result = response.data;
      }, function(response) {
        alert('Could not connect to server.')
      });
    
    $scope.submitNewComment = function() {
      $http.post(BASE_URL + '/api/comments/', {content_object: 'course:' + $state.params.id, text: $scope.new_comment_text})
        .then(function(response) {
          $scope.new_comment_text = "";
          $scope.result.comments.push(response.data);
      }, function(response) {
        alert('Could not connect to server.')
      });
    }
    
    return $scope;
  })
  
  .controller('InstructorCtrl', function($scope, $state, $http, BASE_URL) {
    
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
      enabled:true,
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