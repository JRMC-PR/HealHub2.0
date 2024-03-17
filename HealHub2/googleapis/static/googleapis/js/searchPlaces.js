let map;
let service;
let infowindow;

function initMap() {
  infowindow = new google.maps.InfoWindow();
  // Set initial center to Caguas, PR
  const caguasPR = { lat: 18.2341, lng: -66.0485 };
  map = new google.maps.Map(document.getElementById("map"), {
    center: caguasPR, // Use Caguas, PR as the center
    zoom: 9, // Adjust zoom to show more of the island
  });

  const searchButton = document.getElementById('search-button');
  const specialtyInput = document.getElementById('specialty-input');

  searchButton.addEventListener('click', () => {
    const specialty = specialtyInput.value;
    performSearch(specialty, map);
  });
}

function performSearch(specialty, map) {
  const request = {
    location: map.getCenter(), // Continue to use the map's current center
    radius: '56000', // Adjusted radius to cover Puerto Rico
    query: specialty
  };

  service = new google.maps.places.PlacesService(map);
  service.textSearch(request, (results, status) => {
    if (status === google.maps.places.PlacesServiceStatus.OK && results) {
      clearMarkers(); // Clear existing markers before adding new ones
      results.forEach((place) => {
        createMarker(place, map);
      });

      // Adjust the map's bounds to include all search results
      const bounds = new google.maps.LatLngBounds();
      results.forEach((place) => {
        if (place.geometry.viewport) {
          bounds.union(place.geometry.viewport);
        } else {
          bounds.extend(place.geometry.location);
        }
      });
      map.fitBounds(bounds);
    }
  });
}

let markers = []; // Array to hold all markers

function createMarker(place, map) {
  if (!place.geometry || !place.geometry.location) return;

  const marker = new google.maps.Marker({
    map,
    position: place.geometry.location,
  });

  google.maps.event.addListener(marker, "click", () => {
    const placeName = place.name || "Unknown Place";
    const infoContent = `
      <div>
        <h3>${placeName}</h3>
        <p><a href="https://www.google.com/search?q=${encodeURIComponent(placeName)}" target="_blank">More Info</a></p>
      </div>
    `;
    infowindow.setContent(infoContent);
    infowindow.open(map, marker);
  });

  markers.push(marker); // Add the marker to the array of markers
}

function clearMarkers() {
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
  markers = [];
}
