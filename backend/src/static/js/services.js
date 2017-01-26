// these stuff is useless for now. ignore this file.
angular.module('core.user')
.factory('UserInfo', ['$resource',
    function($resource) {
      return $resource('/api/v1/auth/me/?format=json', {}, {
        query: {
          method: 'GET',
          params: {userID: 'user'},
          isArray: true
        }
      });
    }
  ]);
