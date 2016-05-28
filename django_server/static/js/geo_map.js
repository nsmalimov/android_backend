function getCoordinates() {
    var coordArray = [];

    var newURL = window.location.pathname;
    newURL = newURL.split("|")[1];
    var split_url = newURL.split("+");

    for (var i = 0; i < split_url.length; i++) {
        coordArray.push(split_url[i]);
    }
    return coordArray;
}

$(document).ready(
    function () {

        var map, mapRoute;

        var coordArray = getCoordinates();

        ymaps.ready(function () {
            map = new ymaps.Map('map', {
                center: [59.9244, 30.3474],
                zoom: 9
            });
            createRoute();
        });

        function createRoute() {
            // Удаление старого маршрута
            if (mapRoute) {
                map.geoObjects.remove(mapRoute);
            }

            var s = [];
            for (var i = 0; i < coordArray.length; i++) {
                var coordSplit = coordArray[i].split(",");
                var latitude = coordSplit[0];
                var longitude = coordSplit[1];

                s.push({type: 'wayPoint', point: [latitude, longitude]});

            }
            ymaps.route(s, {mapStateAutoApply: true}).then(
                function (route) {
                    map.geoObjects.add(route);
                    mapRoute = route;
                },
                function (error) {
                    alert('Невозможно построить маршрут');
                }
            );
        }
    }
);
