'use strict';

/* Controllers */

var commentControllers = angular.module('kpcomments.controllers', []);

commentControllers.controller('MainCtrl', ['$scope', '$window', function($scope, $window) {
    $window.init= function() {
      $scope.$apply($scope.load_guestbook_lib);
    };
    $scope.load_guestbook_lib = function() {
        gapi.client.load('guestbook', 'v1', function() {
        $scope.is_backend_ready = true;
        $scope.list();
      }, '/_ah/api');
    };
    $scope.list = function() {
        gapi.client.guestbook.messages.list().execute(function(resp) {
            $scope.messages = resp.items;
            $scope.$apply();
        });
    }
}]);

commentControllers.controller('CommentListCtrl', ['$scope',
  function($scope) {
    $scope.messages = [{'content':'A message', 'date':'20041212'}];
 }]);
