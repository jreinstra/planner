(function() {
  'use strict';

  angular.module('cardinalPlanner', ['ui.router', 'as.sortable', 'ngCookies'])
  
  .constant('BASE_URL', '.')
  
  .factory('AuthenticationService', ['$rootScope', '$http', '$cookies', 'BASE_URL', function($rootScope, $http, $cookies, BASE_URL) {
    var factory = {};
      
    factory.login = function() {
      FB.login(function(response) {
        console.log(response);
        if (response.status == "connected") {
          factory.getAuthToken(response);
        } else {
          alert('Could not login with Facebook, please try again.');
        }
      }, {scope: 'email'});
    }
    
    factory.getLoginStatus = function() {
      if (typeof($cookies.get('auth_token')) != "undefined") {
        $http.defaults.headers.common['Authorization'] = 'Token ' + $cookies.get('auth_token');
        $rootScope.loggedIn = true;
        $rootScope.$emit('loggedIn');
      }
    };
    
    factory.getAuthToken = function(response) {
      $http.post(BASE_URL + '/api/login/', {fb_access_token: response.authResponse.accessToken})
        .then(function(response) {
          console.log(response);
          $http.defaults.headers.common['Authorization'] = 'Token ' + response.data;
          $rootScope.loggedIn = true;
          $rootScope.$emit('loggedIn'); // Controller cannot detect this emission.
          $cookies.put('auth_token', response.data, {'expires': (new Date((new Date()).getFullYear(), (new Date()).getMonth(), (new Date()).getDate() + 7))});
        }, function(response) {
          console.log(response);
          alert('Could not get auth token from server.');
        });
    };
    
    factory.logout = function() {
      delete $http.defaults.headers.common['Authorization']
      $cookies.remove('auth_token');
      $rootScope.loggedIn = false;
      $rootScope.$emit('loggedOut');
    }
    
    return factory;
  }])
  
  .controller('LoginCtrl', function($rootScope, $scope, $state, $http, BASE_URL, AuthenticationService) {
    $scope.login = function() {
      AuthenticationService.login();
    };
    
    $scope.logout = function() {
      AuthenticationService.logout();
    }
    
    $scope.init = function() {
      AuthenticationService.getLoginStatus()
    }
    
    $scope.$on('$stateChangeSuccess', function () {
      // do something
      console.log('state changed success');
    });
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
          alert('Could not connect to server.');
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
          alert('Could not connect to server.');
        });
      } else {
        $http.post(BASE_URL + '/api/comments/', {content_object: 'course:' + $state.params.id, text: $scope.newReply})
          .then(function(response) {
            $scope.result.comments.push(response.data);
            $scope.newReply = '';
        }, function(response) {
          alert('Could not connect to server.');
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
        alert('Could not connect to server.');
      });
    };
    
    return $scope;
  })
  
  .controller('InstructorCtrl', function($rootScope, $scope, $state, $http, BASE_URL) {
    
    $scope.loading = true;
    $http.get(BASE_URL + '/api/instructors/' + $state.params.sunet)
      .then(function(response) {
        $scope.loading = false;
        $scope.result = response.data;
      }, function(response) {
        $scope.loading = false;
        alert('Could not connect to server.')
      });
  })
  
  .controller('PlannerCtrl', function($rootScope, $scope, $state, $http, $window, BASE_URL, AuthenticationService) {
    
    $rootScope.$on("$stateChangeSuccess", function(event, toState, toParams, fromState, fromParams) {
      if (!$rootScope.loggedIn) {
        $state.go('home');
      }
    });
    
    $rootScope.$on('loggedOut', function() {
      $state.go('home');
    });
    
    $scope.loading = true;
    // Create A Default Plan With Major ID
    $http.get(BASE_URL + '/api/plans/')
      .then(function(response) {
        console.log(response.data);
        if (response.data.count == 0) {
          $http.post(BASE_URL + '/api/plans/', {degrees: [1], years:[]})
            .then(function(response) {
              console.log(response.data);
              $scope.plans.push(response.data);
              alert('Created a new plan.');
          }, function(response) {
            alert('Could not connect to server.');
          });
        } else {
          $scope.plans = response.data.results;
        }
      }, function(response) {
        console.log(response);
        alert('Could not connect to server.');
      });
    
    $scope.terms = ['autumn', 'winter', 'spring'];
    
    $scope.courses = {
      'autumn':[],
      'winter':[],
      'spring':[]
    };
    
    $scope.courses_ids = {
      'autumn':[],
      'winter':[],
      'spring':[]
    };
    
    $scope.courses_units = {
      'autumn':{
        'min_units': 0,
        'max_units': 0,
      },
      'winter':{
        'min_units': 0,
        'max_units': 0,
      },
      'spring':{
        'min_units': 0,
        'max_units': 0,
      }
    }
    
    // Get Plan Years
    $http.get(BASE_URL + '/api/plan_years/')
      .then(function(response) {
        console.log(response.data);
        $scope.plan_years = response.data.results;

        if ($scope.plan_years.length == 0) {
          $http.post(BASE_URL + '/api/plan_years/', {plan: $scope.plans[0].id, year: '2016-2017', summer: [], autumn: [], winter: [], spring: []})
            .then(function(response) {
              console.log(response.data);
              $scope.plan_years.push(response.data);
              alert('Created a new plan year.');
          }, function(response) {
            alert('Could not connect to server.');
          });
        }
        
        $scope.years = _.uniq($scope.plan_years.map(function(pq) {
          return pq.year;
        }));
        
        $scope.selected_plan_year = $scope.plan_years[0];
        $scope.selected_year = $scope.years[0];
        
        $scope.finishedInitialLoad = false;
        $scope.initialLoadTotalCount = ($scope.selected_plan_year.summer.length + $scope.selected_plan_year.autumn.length + $scope.selected_plan_year.winter.length + $scope.selected_plan_year.spring.length)
        $scope.initialLoadCurrentCount = 0;
        
        $scope.terms.forEach(function(term, index) {
          $scope.selected_plan_year[term].forEach(function(course_id, index2) {
            $http.get(BASE_URL + '/api/courses/' + course_id + '/')
              .then(function(response) {
                $scope.courses[term].push(response.data);
                $scope.initialLoadCurrentCount++;
              }, function(response) {
                console.log(response);
                alert('Could not connect to server.');
              });
          });
        });
        
        $scope.$watch('initialLoadCurrentCount', function(count) {
          console.log('current count:');
          console.log(count);
          console.log($scope.initialLoadTotalCount);
          if (count == $scope.initialLoadTotalCount) {
            $scope.finishedInitialLoad = true;
          }
        });
        
        // For depth = 1
        /*$scope.courses = {
          'autumn': $scope.selected_plan_year.autumn,
          'winter': $scope.selected_plan_year.winter,
          'spring': $scope.selected_plan_year.spring
        };*/
        
        console.log($scope.years);
        $scope.loading = false;
      }, function(response) {
        console.log(response);
        alert('Could not connect to server.');
      });
    
    $scope.$watch('courses', function(courses) {
      console.log(courses);
      for (var key in courses) {
        $scope.courses_ids[key] = $scope.courses[key].map(function(course) {
          return course.id;
        });
        $scope.courses_units[key]['min_units'] = $scope.courses[key].map(function(course) {
          return course.min_units;
        }).reduce(function(a, b) { return a + b; }, 0);
        $scope.courses_units[key]['max_units'] = $scope.courses[key].map(function(course) {
          return course.max_units;
        }).reduce(function(a, b) { return a + b; }, 0);
      }
      
      if (typeof($scope.selected_plan_year) != "undefined" && $scope.finishedInitialLoad == true) {
        $scope.saving = true;
        $http.put(BASE_URL + '/api/plan_years/' + $scope.selected_plan_year.id + '/', {plan: $scope.selected_plan_year.plan, year: $scope.selected_plan_year.year, autumn: $scope.courses_ids.autumn, winter: $scope.courses_ids.winter, spring: $scope.courses_ids.spring})
          .then(function(response) {
            console.log(response.data);
            console.log('Updated plan year.');
            $scope.saving = false;
        }, function(response) {
          alert('Could not connect to server.');
        });
      }
      
      console.log($scope.courses_ids);
      console.log($scope.courses_units);
    }, true)
    
    $scope.deleteCourse = function(term, index) {
      $scope.courses[term].splice(index, 1);
    }
    
    $scope.update = function() {
      if ($scope.search == "") {
        $scope.result = [];
        return;
      }
      $scope.loading_search = true;
      $http.get(BASE_URL + '/api/search/?q=' + $scope.search)
        .then(function(response) {
          $scope.result = response.data
          $scope.loading_search = false;
        }, function(response) {
          alert('Could not connect to server.');
          $scope.loading_search = false;
        });
    };
    
    $window.onbeforeunload = function (event) {
      if ($scope.saving) {
        var message = 'Changes you made may not be saved.';
        if (typeof event == 'undefined') {
          event = window.event;
        }
        if (event) {
          event.returnValue = message;
        }
        return message;
      }
    }
    
    $scope.cloneCoursesOptions = {
      accept: function (sourceItemHandleScope, destSortableScope) {
        return true;
      },//override to determine drag is allowed or not. default is true.
      itemMoved: function (event) {},
      orderChanged: function(event) {},
      containment: '#planner',//optional param.
      clone: true, //optional param for clone feature.
      allowDuplicates: false //optional param allows duplicates to be dropped.
    };
    
    $scope.coursesOptions = {
      accept: function (sourceItemHandleScope, destSortableScope) {
        return true;
      },//override to determine drag is allowed or not. default is true.
      itemMoved: function (event) {},
      orderChanged: function(event) {},
      containment: '#planner',//optional param.
      clone: false, //optional param for clone feature.
      allowDuplicates: false //optional param allows duplicates to be dropped.
    };
  })
  
  .filter('capitalize', function() {
      return function(input) {
        return (!!input) ? input.charAt(0).toUpperCase() + input.substr(1).toLowerCase() : '';
      }
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
      })
      .state('planner', {
        url: '/planner/',
        templateUrl: 'static/frontend/partials/planner.html',
        controller: 'PlannerCtrl'
      });
      
    $locationProvider.hashPrefix('!');
  })
  
  .run(function() {
    FastClick.attach(document.body);
  });

})();