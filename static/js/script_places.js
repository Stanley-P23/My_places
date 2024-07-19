$(document).ready(function() {

  var map;
  var markers = [];

  // Function to toggle column visibility based on window width
  function toggleColumns() {
    if ($(window).width() > 768) {
      $(".side-column, .main-column").show();
      $(".btn-toggle").hide();
    } else {
      $(".side-column, .main-column").hide();
      $("#mainColumn").show(); // Show the main column by default in thin view
      $(".btn-toggle").show();
    }
  }

  // Initialize Google Map
  function initMap() {
    // Map options
    var mapOptions = {
      center: { lat: 52.2298, lng: 21.0118 }, // Warsaw coordinates
      zoom: 13, // Adjust zoom level as needed
      disableDefaultUI: true // Disable all default UI controls
    };

    // Create map
    map = new google.maps.Map(document.getElementById('map'), mapOptions);

    // Apply filters immediately after loading the page
    applyFilters();
  }

  // Load map after document is ready
  initMap();

  function addMarker(lat, lng, title) {
    var marker = new google.maps.Marker({
      position: { lat: lat, lng: lng },
      map: map,
      title: title
    });
    markers.push(marker);
    return marker;
  }

  function clearMarkers() {
    for (var i = 0; i < markers.length; i++) {
      markers[i].setMap(null);
    }
    markers = [];
  }

  function highlightListItem($item) {
    $("#myList li").removeClass('active');
    $item.addClass('active');
  }

  function resetHighlight() {
  $("#myList li").removeClass('active');
}

  function enlargeMarker(marker) {
    markers.forEach(m => m.setIcon(null));
    marker.setIcon({
      path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
      scale: 10, // Enlarge the marker
      fillColor: '#DC143C',
      fillOpacity: 0.7,
      strokeColor: '#EF9C66',
      strokeWeight: 4
    });
  }


  // Toggle left column
  $("#toggleLeftColumn").on("click", function() {
    $(".side-column, .main-column").hide();
    $("#leftColumn").show();
  });

  // Toggle right column
  $("#toggleRightColumn").on("click", function() {
    $(".side-column, .main-column").hide();
    $("#rightColumn").show();
  });

  // Toggle main column
  $("#toggleMainColumn").on("click", function() {
    $(".side-column, .main-column").hide();
    $("#mainColumn").show();
  });

  // Toggle columns on window resize
  $(window).resize(function() {
    toggleColumns();
  });

  // Initial call to toggleColumns to set initial state
  toggleColumns();

  // Filter button click event
  $('#filterButton').click(function() {
    applyFilters();
  });

  // Clear filters button click event
  $('#clearFiltersButton').click(function() {
    clearFilters();
    applyFilters();
  });

  function applyFilters() {
    var value = $("#myInput").val().toLowerCase();
    var bounds = new google.maps.LatLngBounds();

    clearMarkers();

    $("#myList li").each(function() {
      var $place = $(this);
      var textMatch = $place.text().toLowerCase().indexOf(value) > -1;

      if (textMatch) {
        var foodChecked = $('#foodCheckbox').prop('checked');
        var myFoodChecked = $('#myFoodCheckbox').prop('checked');
        var tableChecked = $('#tableCheckbox').prop('checked');
        var socketChecked = $('#socketCheckbox').prop('checked');
        var culturalChecked = $('#culturalCheckbox').prop('checked');
        var outdoorChecked = $('#outdoorCheckbox').prop('checked');
        var studyChecked = $('#studyCheckbox').prop('checked');

        var hasFood = $place.find('.fa-utensils').length > 0;
        var hasMyFood = $place.find('.fa-suitcase').length > 0;
        var hasTable = $place.find('.fa-couch').length > 0;
        var hasSocket = $place.find('.fa-plug').length > 0;
        var hasCultural = $place.find('.fa-masks-theater').length > 0;
        var hasOutdoor = $place.find('.fa-bicycle').length > 0;
        var hasStudy = $place.find('.fa-computer').length > 0;

        if ((foodChecked && !hasFood) ||
            (myFoodChecked && !hasMyFood) ||
            (tableChecked && !hasTable) ||
            (socketChecked && !hasSocket) ||
            (culturalChecked && !hasCultural) ||
            (outdoorChecked && !hasOutdoor) ||
            (studyChecked && !hasStudy)) {
          $place.hide();
        } else {
          $place.show();

          // Add marker to map
          var lat = parseFloat($place.find('.latitude').text());
          var lng = parseFloat($place.find('.longitude').text());
          var title = $place.find('.fs-4').text();
          var marker = addMarker(lat, lng, title);
          bounds.extend({ lat: lat, lng: lng });

          // Click event for list item
          $place.click(function() {
            highlightListItem($place);
            enlargeMarker(marker);
          });
        }
      } else {
        $place.hide();
      }
    });

    if (!bounds.isEmpty()) {
      map.fitBounds(bounds);
      var listener = google.maps.event.addListener(map, "idle", function() {
        if (map.getZoom() > 15) map.setZoom(15); // Set the desired maximum zoom level
        if (map.getZoom() < 10) map.setZoom(10); // Set the desired minimum zoom level
        google.maps.event.removeListener(listener);
      });
      resetHighlight()
    }
  }

  function clearFilters() {
    $('#foodCheckbox').prop('checked', false);
    $('#myFoodCheckbox').prop('checked', false);
    $('#tableCheckbox').prop('checked', false);
    $('#socketCheckbox').prop('checked', false);
    $('#culturalCheckbox').prop('checked', false);
    $('#outdoorCheckbox').prop('checked', false);
    $('#studyCheckbox').prop('checked', false);
    document.getElementById('myInput').value = '';

    resetHighlight();
    $('#myList li').show();
  }

  // Apply filters after the page is loaded
  applyFilters();
});
