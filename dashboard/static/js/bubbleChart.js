const urls = {
    flight_2019_url : "/bubbleData_v1",
    flight_2020_url : "/bubbleData_v2"
};


d3.json(urls.flight_2019_url, function(flightData) {

    var airportMarkers_2019 = []

    for (var i = 0; i < flightData.length; i++){
        coordinates = [flightData[i].latitude, flightData[i].longitude]

        airportMarkers_2019.push(
            L.circle(coordinates, {
                fillOpacity: 0.75,
                color: "black",
                weight: 0.3,
                fillColor: getColor(flightData[i].arrival_delay),
                radius: markerSize(flightData[i].arrival_delay)
            }).bindPopup("Airport: " + flightData[i].airport_name + "<hr>" + 
            "City: "+ flightData[i].city + "<br>" + 
            "State: " + flightData[i].state + "<br>" +
            "Average Arrival Delay: " + flightData[i].arrival_delay.toFixed(0) + " mins" + "<br>" +
            "Average Departure Delay: " + flightData[i].departure_delay.toFixed(0) + " mins")
        )
    }
    createMap(airportMarkers_2019);
})



function createMap(airportMarkers_2019){

    var streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "streets-v9",
        accessToken: API_KEY
    });
  
    var darkmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "dark-v10",
        accessToken: API_KEY
    });

    
  
    var airports_2019 = L.layerGroup(airportMarkers_2019);
  

    var baseMaps = {
        "Street Map": streetmap,
        "Dark Map": darkmap
    };

    var airports_2020 = new L.LayerGroup();
    
    var overlayMaps = {
      "Before Covid-19": airports_2019,
      "After Covid-19" : airports_2020
    };
  
  
    var myMap = L.map("map", {
        center: [38.79, -97.65],
        zoom: 4.5,
        layers: [darkmap, airports_2019]
    });
    
    d3.json(urls.flight_2020_url, function(flightData) {
    
        for (var i = 0; i < flightData.length; i++){
            coordinates = [flightData[i].latitude, flightData[i].longitude]
    
                L.circle(coordinates, {
                    fillOpacity: 0.75,
                    color: "black",
                    weight: 0.3,
                    fillColor: getColor(flightData[i].arrival_delay),
                    radius: markerSize(flightData[i].arrival_delay)
                }).bindPopup("Airport: " + flightData[i].airport_name + "<hr>" + 
                                "City: "+ flightData[i].city + "<br>" + 
                                "State: " + flightData[i].state + "<br>" +
                                "Average Arrival Delay: " + flightData[i].arrival_delay.toFixed(0) + " mins" + "<br>" +
                                "Average Departure Delay: " + flightData[i].departure_delay.toFixed(0) + " mins").addTo(airports_2020)
            
        }

    })
    

    L.control.layers(baseMaps, overlayMaps, {
      collapsed: false
    }).addTo(myMap);


      //Create a legend 
    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (myMap) {var div = L.DomUtil.create('div', 'info legend'); return div;}
    legend.addTo(myMap);
    var grades = [-100, 0, 5, 10, 30, 50];
    var labels = ["<strong>Flight Delay Density</strong>"];

    for (var i = 0; i < grades.length; i++){
        var from = grades [i];
        var to = grades [i + 1] - 1;
        labels.push('<i style="background:' + getColor(from + 1) + '"></i> ' + from  + " " + (to ? '&ndash; ' + to : '+') + " mins");
    }

    var legendText = labels.join("<br>")
    d3.select(".legend.leaflet-control").html(legendText);
 
}
  
  
function getColor(delay){
    return delay > 50 ? "#cc0000":
        delay > 30 ? "#ff3333":
        delay > 10 ? "#ff8000":
        delay > 5 ? "#ffcc99":
        delay > 0 ? "#ffff33":
                    "#00ff80";
}

function markerSize(delay){
    return  delay < 0? 5000:
            delay * 6000;
}

