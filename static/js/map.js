
// Wait for the DOM to be ready
document.addEventListener('DOMContentLoaded', function () {
    // Initialize the map
    var map = L.map('map').setView([51.505, -0.09], 13);

    // Add the tile layer from OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Initialize the marker
    var marker;

    // Add a click event listener to the map
    map.on('click', function (e) {
        // If a marker already exists, remove it
        if (marker) {
            map.removeLayer(marker);
        }

        // Add a marker at the clicked location
        marker = L.marker(e.latlng).addTo(map);

        // Set the coordinates in the format expected by GeoDjango PointField
        var coordinates = 'POINT (' + e.latlng.lng + ' ' + e.latlng.lat + ')';

        // Set the value of the hidden input
        document.getElementById('GPS_locatie').value = coordinates;
    });
});
