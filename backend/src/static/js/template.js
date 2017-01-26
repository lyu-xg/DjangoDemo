$(document).ready(function($) {

	$(".headroom").headroom({
		"tolerance": 20,
		"offset": 50,
		"classes": {
			"initial": "animated",
			"pinned": "slideDown",
			"unpinned": "slideUp"
		}
	});

});

// a static method which is uesd in html to make UI cleaner
String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}


// Our one page APP
var app = angular.module("myApp",['ngResource'])

// configure basic settings
.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{$').endSymbol('$}');
})
.config(function($httpProvider) {
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
})

// the C in MCV
// the main controller which has methods which will be invoked by html(view)
.controller('mainCtrl',function($scope, $http, $resource){
	$scope.locations = ["Los Angeles", "Orange County", "San Diego"];
	$scope.themes = ["comedy", "musical"];
	$scope.roles = ["V","S"];

	$scope.hoverIn = function(){this.hoverShow = true;};
	$scope.hoverOut = function(){this.hoverShow = false;};
	// hide the signin form at first
	$scope.showSignin = false;
	$scope.showRegister = false;
	$scope.showPost = false;
	$scope.registerErrorMessage = 'Some fields are not acceptable.';
	$scope.registerErrorMessage = 'Some fields are not acceptable.';
	var UserProfile = $resource('/api/v1/auth/me/');
	var VenueSuggestion = $resource('/api/v1/me/recommand_venues/?format=json');
  var ShowSuggestion = $resource('/api/v1/me/recommand_shows/?format=json');
	var ShowList = $resource('/api/v1/shows/');
	var VenueList = $resource('/api/v1/venues/');
	$scope.goHome = function(){$scope.home = true;
	$scope.removeHeader=false;$scope.browseShows=false;$scope.browseVenues=false;};
	$scope.goHome();//initial setting.
	$scope.toggleshowSigninSignup = function(){$scope.showSignin=!$scope.showSignin;};
	$scope.toggleRegister = function(){$scope.showRegister=!$scope.showRegister;$scope.showSignin=false;};
	$scope.togglebrowseShows = function(){
		$scope.home = false;$scope.removeHeader=true;
		$scope.browseShows=true;$scope.browseVenues=false;
		$scope.shows = ShowList.query(function(){console.log("got my shows",$scope.shows);});
	};
	$scope.togglebrowseVenues = function(){
		$scope.home = false;$scope.removeHeader=true;
		$scope.browseShows=false;$scope.browseVenues=true;
		$scope.venues = VenueList.query(function(){console.log("got VenueList: ",$scope.venues)})
	};
	$scope.togglePost = function(){
		$scope.showPost = true;
	}
	/*
	var getUserInfo = function(token){
		BackEndService.sendInfoRequest(token,function(response){
			console.log(response.data);
			$scope.user=response.data;
			if ($scope.user.role == "S"){
				getVenueList($scope.mytoken);
			}
		})
	};
  */
	var getVenueList = function(token){
		BackEndService.sendVenueRequest(token, function(response){
			console.log('got venue list from API: ',response.data);
			$scope.venues = response.data;
		})
	};

	$scope.register = function(registerInformation){
		console.log('posting data to API: ',registerInformation);
		$http.post("api/v1/auth/register/",registerInformation,[{headers: {'Content-Type': "application/json"}}]
		).then(function(response){
			//on success
			console.log('got response from API: ',response.data);
			$scope.login({username:registerInformation.username,password:registerInformation.password});

		},function(response){
			// on failing
			console.log('failed to register, got this back: ',response);
			$scope.postFailed=true;
			$scope.registerErrorMessage=reponse.data.toString();
		});
	}

	$scope.login = function(loginInformation){

		$http({
			method: "POST",
			url: "api/v1/auth/login/",
			headers: {'Content-Type': "application/json"},
			data: loginInformation
		})
		.then(function(response){
			// when login success
			console.log('got auth_token from API: '+response.data.auth_token);
			// called when request complete
			// store user-token into scope
			$scope.loginFailed=false;
			$scope.postFailed=false;
			$scope.mytoken = response.data.auth_token;
			$scope.showSignin=false;
			$scope.removeHeader=true;
			// get the user profile and store in scope
			var theUser = UserProfile.get(function(){
				$scope.user=theUser;
				// get recommendations based on user's role
				if (theUser.role == "S") {
					$scope.suggestions = VenueSuggestion.query(function(){console.log('venue suggestions fetched: '+$scope.suggestions);});
					$scope.myposts = ShowList.query(function(){console.log("got my shows",$scope.myposts);});
					//TODO now returning all the shows, should be user specific.
				}
				if (theUser.role == "V") {
					$scope.suggestions = ShowSuggestion.query(function(){console.log('show suggestions fetched: '+$scope.suggestions);});
					$scope.myposts = VenueList.query(function(){console.log("got my shows",$scope.myposts);});
					//TODO now returning all the venues, should be user specific.
				}
			});

		},function(){
			// when login failed.
			$scope.loginFailed=true;
		});
	};
});

//this directive modal is for pop-up windows
app.directive('modal', function () {
    return {
      template: '<div class="modal fade">' +
          '<div class="modal-dialog">' +
            '<div class="modal-content">' +
              '<div class="modal-header">' +
                '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>' +
                '<h4 class="modal-title">{{ title }}</h4>' +
              '</div>' +
              '<div class="modal-body" ng-transclude></div>' +
            '</div>' +
          '</div>' +
        '</div>',
      restrict: 'E',
      transclude: true,
      replace:true,
      scope:true,
      link: function postLink(scope, element, attrs) {
        scope.title = attrs.title;

        scope.$watch(attrs.visible, function(value){
          if(value == true)
            $(element).modal('show');
          else
            $(element).modal('hide');
        });

        $(element).on('shown.bs.modal', function(){
          scope.$apply(function(){
            scope.$parent[attrs.visible] = true;
          });
        });

        $(element).on('hidden.bs.modal', function(){
          scope.$apply(function(){
            scope.$parent[attrs.visible] = false;
          });
        });
      }
    };
  });
