let map;
let service;
let infowindow;
let userMarker; // A marker for the user's location

function initMap() {
  infowindow = new google.maps.InfoWindow();
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15, // A default zoom
  });

  if (navigator.geolocation) {
    navigator.geolocation.watchPosition(
      (position) => {
        const userLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

        // If there's already a marker for the user's location, remove it
        if (userMarker) {
          userMarker.setMap(null);
        }

        // Place a new marker at the new location
        userMarker = new google.maps.Marker({
          position: userLocation,
          map: map,
          title: "Your Location",
          icon: {
              url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png" // URL to a blue marker icon
          }
      });

        // Update the map's center to the new location
        map.setCenter(userLocation);
      },
      () => {
        console.error("Error: The Geolocation service failed or permission was denied.");
      },
      {
        maximumAge: 60000, // Accept a cached position within 60 seconds
        timeout: 10000, // Stop trying after 5 seconds
        enableHighAccuracy: true, // Request the best accuracy possible
      }
    );
  } else {
    console.error("Error: Your browser doesn't support geolocation.");
  }

  const searchButton = document.getElementById('search-button');
  const specialtyInput = document.getElementById('specialty-input');

  searchButton.addEventListener('click', () => {
    const specialty = specialtyInput.value;
    performSearch(specialty, map);
  });
}

function performSearch(specialty, map) {
  const request = {
      location: map.getCenter(), // Use the map's current center as the search location
      radius: '5000', // Search within a 5000-meter radius
      query: specialty
  };

  service = new google.maps.places.PlacesService(map);
  service.textSearch(request, (results, status) => {
      if (status === google.maps.places.PlacesServiceStatus.OK && results) {
          clearMarkers(); // Clear existing markers before adding new ones
          results.forEach((place) => {
              createMarker(place, map);
          });

          // Optionally, adjust the map's bounds to include all search results
          const bounds = new google.maps.LatLngBounds();
          results.forEach((place) => {
              if (place.geometry.viewport) {
                  // Only geocodes have viewport.
                  bounds.union(place.geometry.viewport);
              } else {
                  bounds.extend(place.geometry.location);
              }
          });
          map.fitBounds(bounds);
      }
  });
}


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


let markers = []; // Array to hold all markers
function clearMarkers() {
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
  markers = [];
}
