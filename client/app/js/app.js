'use strict';
/* init gapi */

function init(){
    window.init();
}
// Declare app level module which depends on filters, and services
angular.module('kpcomments', [
  'ngRoute',
  // 'kpcomments.filters',
  // 'kpcomments.services',
  // 'kpcomments.directives',
  'kpcomments.controllers'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/list', {templateUrl: 'partials/list.html', controller: 'CommentListCtrl'});
  $routeProvider.otherwise({redirectTo: '/list'});
}]);
