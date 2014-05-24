'use strict';

/* Services */

var commentServices = angular.module('kpcomments.services', ['ngResource']);

commentServices.factory('Comment', ['$resource',
  function($resource){
    return $resource('comments/:commentId.json', {}, {
      query: {method:'GET', isArray:true}
    });
  }]);
