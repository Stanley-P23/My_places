function initAutocomplete() {
  var map = new google.maps.Map(document.getElementById('map'), {
    center: { lat: 52.2286, lng: 21.0092 },
    zoom: 13,
    mapTypeId: 'roadmap',
    disableDefaultUI: true // Disable all default UI controls
  });

  var geocoder = new google.maps.Geocoder();

  // Create the search box and link it to the UI element.
  var input = document.getElementById('pac-input');
  var searchBox = new google.maps.places.SearchBox(input);
  input.focus();
  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function () {
    searchBox.setBounds(map.getBounds());
  });

  var markers = [];

  // Function to clear all markers from the map
  function clearMarkers() {
    markers.forEach(function (marker) {
      marker.setMap(null);
    });
    markers = [];
  }

  searchBox.addListener('places_changed', function () {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

    // Show the map
    document.getElementById('map').style.display = 'block';

    // Clear out the old markers.
    clearMarkers();

    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function (place) {
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }

      // Create a marker for each place.
      var marker = new google.maps.Marker({
        map: map,
        title: place.name,
        position: place.geometry.location
      });
      markers.push(marker);

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }

      // Display place details
      displayPlaceDetails(place);
    });
    map.fitBounds(bounds);
  });

  map.addListener('click', function (event) {
    geocodeLatLng(geocoder, map, event.latLng);
  });

  function geocodeLatLng(geocoder, map, latLng) {
    geocoder.geocode({ 'location': latLng }, function (results, status) {
      if (status === 'OK') {
        if (results[0]) {
          var placeId = results[0].place_id;
          var service = new google.maps.places.PlacesService(map);
          service.getDetails({ placeId: placeId }, function (place, status) {
            if (status === google.maps.places.PlacesServiceStatus.OK) {
              // Clear out the old markers.
              clearMarkers();

              // Create a marker for the selected place.
              var marker = new google.maps.Marker({
                map: map,
                title: place.name,
                position: place.geometry.location
              });
              markers.push(marker);

              // Display place details
              displayPlaceDetails(place);

              map.panTo(latLng);
            } else {
              window.alert('Place details request failed: ' + status);
            }
          });
        } else {
          window.alert('No results found');
        }
      } else {
        window.alert('Geocoder failed due to: ' + status);
      }
    });
  }

  // Function to display place details
  function displayPlaceDetails(place) {
    var detailsDiv = document.getElementById('details');

    // Check if place and place.geometry exist
    if (place && place.geometry && place.geometry.location) {
      var latitude = parseFloat(place.geometry.location.lat());
      var longitude = parseFloat(place.geometry.location.lng());

      detailsDiv.innerHTML = '<br><h3>' + place.name + '</h3>' +
        'Address: ' + place.formatted_address + '<br>' +
        'Coordinates: ' + latitude.toFixed(6) + ', ' + longitude.toFixed(6);

      // Send the data via AJAX
      $.ajax({
        url: '/get_url',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
          latitude: latitude.toFixed(6),
          altitude: longitude.toFixed(6)
        }),
        success: function (response) {
          // Update the href attribute of the confirm button
          var confirmBtn = document.getElementById('confirm-btn');
          confirmBtn.href = response.url;
          confirmBtn.classList.add('visible');
        },
        error: function (error) {
          console.error(error);
          alert('An error occurred while sending coordinates.');
        }
      });

    } else {
      detailsDiv.innerHTML = '<br><p>Error: Place details not found.</p>';
    }
  }
}

// Load the Google Maps API script dynamically
function loadScript() {
  var script = document.createElement('script');
  script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyBaJYuwXHTR2kwFWFkIY8eTfhRjf7S8SS0&libraries=places&callback=initAutocomplete';
  script.defer = true;
  script.async = true;
  document.head.appendChild(script);
}

window.onload = loadScript;
