###

ownCloud - News

@author Bernhard Posselt
@copyright 2012 Bernhard Posselt dev@bernhard-posselt.com

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
License as published by the Free Software Foundation; either
version 3 of the License, or any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU AFFERO GENERAL PUBLIC LICENSE for more details.

You should have received a copy of the GNU Affero General Public
License along with this library.  If not, see <http://www.gnu.org/licenses/>.

###

angular.module('News').directive 'newsPullToRefresh', ['$rootScope',
($rootScope) ->

	allowed = true
	$rootScope.$on 'loadingNewItems', ->
		allowed = false
	$rootScope.$on 'loadedNewItems', ->
		allowed = true

	directive =
		restrict: 'A'
		link: (scope, elm, attrs) ->
			scrollTop = 0
			elm.scroll ->
				if @scrollTop == 0 && allowed
					scope.$apply attrs.newsPullToRefresh
]