// Declare global variables for the map, the Places service, and the info window
let map;
let service;
let infowindow;

// Initialize the map
function initMap() {
  // Create a new info window
  infowindow = new google.maps.InfoWindow();

  // Set the initial center of the map to Caguas, PR
  const caguasPR = { lat: 18.2341, lng: -66.0485 };

  // Create a new map and set its center and zoom level
  map = new google.maps.Map(document.getElementById("map"), {
    center: caguasPR,
    zoom: 9,
  });

  // Get the search button and the specialty input field
  const searchButton = document.getElementById('search-button');
  const specialtyInput = document.getElementById('specialty-input');

  // Add a click event listener to the search button
  searchButton.addEventListener('click', () => {
    // Get the value of the specialty input field
    const specialty = specialtyInput.value;

    // Perform a search with the entered specialty
    performSearch(specialty, map);
  });
}

// Perform a search with the entered specialty
function performSearch(specialty, map) {
  // Create a request with the map's current center, a radius, and the query
  const request = {
    location: map.getCenter(),
    radius: '56000',
    query: specialty
  };

  // Create a new Places service
  service = new google.maps.places.PlacesService(map);

  // Perform a text search with the request
  service.textSearch(request, (results, status) => {
    // If the search was successful and there are results
    if (status === google.maps.places.PlacesServiceStatus.OK && results) {
      // Clear any existing markers
      clearMarkers();

      // For each place in the results, create a new marker
      results.forEach((place) => {
        createMarker(place, map);
      });

      // Create a new LatLngBounds object
      const bounds = new google.maps.LatLngBounds();

      // For each place in the results, extend the bounds to include the place
      results.forEach((place) => {
        if (place.geometry.viewport) {
          bounds.union(place.geometry.viewport);
        } else {
          bounds.extend(place.geometry.location);
        }
      });

      // Adjust the map's viewport to fit the bounds
      map.fitBounds(bounds);
    }
  });
}

// Declare a global array to hold all markers
let markers = [];

// Create a new marker for a place
function createMarker(place, map) {
  // If the place does not have a location, return
  if (!place.geometry || !place.geometry.location) return;

  // Create a new marker at the place's location
  const marker = new google.maps.Marker({
    map,
    position: place.geometry.location,
  });

  // Add a click event listener to the marker
  google.maps.event.addListener(marker, "click", () => {
    // Get the place's name or use "Unknown Place" if it does not have a name
    const placeName = place.name || "Unknown Place";

    // Create the content for the info window
    const infoContent = `
      <div>
        <h3>${placeName}</h3>
        <p><a href="https://www.google.com/search?q=${encodeURIComponent(placeName)}" target="_blank" style="color: blue;"">More Info</a></p>
      </div>
    `;

    // Set the content of the info window and open it on the marker
    infowindow.setContent(infoContent);
    infowindow.open(map, marker);
  });

  // Add the marker to the array of markers
  markers.push(marker);
}

// Clear all markers
function clearMarkers() {
  // For each marker in the array, remove it from the map
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }

  // Clear the array of markers
  markers = [];
}
