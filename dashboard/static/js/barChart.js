var gurls = {
    delay_data_url : "/barData",
    delay_day_url : "/calendarData",
    airport_url : "/barChartAirport"
};


function init(){
    d3.json(gurls.airport_url).then((data) => {
        var airport = data.map(item => item.airport_name);

        d3.select("#selDeparture").selectAll("option")
            .data(airport)
            .enter()
            .append("option")
            .attr("value", d=>d)
            .text(d => d);


        d3.select("#selArrival").selectAll("option")
            .data(airport)
            .enter()
            .append("option")
            .attr("value", d=>d)
            .text(d => d);

        
        var departureName = " St Louis Lambert International";
        document.getElementById("selDeparture").value = departureName;
        var arrivalName = " Chicago O'Hare International";
        document.getElementById("selArrival").value = arrivalName;

        var depData = data.filter(row => row.airport_name == departureName);
        var departureID = depData[0].airport_id;


        var arrData = data.filter(row => row.airport_name == arrivalName);
        var arrivalID = arrData[0].airport_id;

        var delayYear = d3.select("#d3-dropdown").property("value")


        buildCharts(departureID, arrivalID, delayYear);
        buildLine(departureID, arrivalID, delayYear);

    });
}

function buildCharts(departureID, arrivalID, delayYear){

    d3.json(gurls.delay_data_url).then((data) =>{

        var filteredData = data.filter(row => row.arrival_airport == arrivalID && row.departure_airport == departureID && row.year == delayYear);
        var flightQuantity = filteredData.map(item => item.airline).length
        var avgDeparture = (filteredData.map(item => item.departure_delay).reduce((a, b) => a + b, 0) / filteredData.map(item => item.departure_delay).length).toFixed(0);
        var avgArrival = (filteredData.map(item => item.arrival_delay).reduce((a, b) => a + b, 0) / filteredData.map(item => item.arrival_delay).length).toFixed(0);
        var cancel = ((filteredData.map(item => item.cancelled).reduce((a, b) => a + b, 0) / filteredData.map(item => item.cancelled).length)* 100 ).toFixed(2); 
        

        var panelValue1 = d3.select("#di_text");
        var panelValue2 = d3.select("#aad_text");
        var panelValue3 = d3.select("#pd_text");
        var panelValue4 = d3.select("#cr_text");



        panelValue1.html("")
        panelValue2.html("");
        panelValue3.html("");
        panelValue4.html("");


        panelValue1.append("h3").text(flightQuantity + " Airlines");
        panelValue2.append("h3").text(avgDeparture + " mins");
        panelValue3.append("h3").text(avgArrival + " mins");
        panelValue4.append("h3").text(cancel + "%");

        var flightAirline = filteredData.map(item => item.airline_name);
        // console.log(flightAirline);

        var trace1 = {
            x: flightAirline,
            y: filteredData.map(item => item.departure_delay),
            type: 'bar',
            name: 'Departure Delay',
            marker: {
              color: 'rgb(49,130,189)',
              opacity: 0.7,
            }
          };
          
        var trace2 = {
            x: flightAirline,
            y: filteredData.map(item => item.arrival_delay),
            type: 'bar',
            name: 'Arrival Delay',
            marker: {
              color: 'rgb(250,86,86)',
              opacity: 0.5
            }
          };
          
        var data = [trace1, trace2];
          
        var layout = {
            title: 'Flight Delay by Airlines',
            margin: {"t": 50, "b": 120, "l": 50, "r": 50},
            xaxis: {
              tickangle: -45
            },
            barmode: 'group',
          };
          
        Plotly.newPlot('bar', data, layout)


        var carrierDelay = filteredData.map(item => item.carrier_delay).reduce((a, b) => a + b, 0) / filteredData.map(item => item.carrier_delay).length
        var weatherDelay = filteredData.map(item => item.weather_delay).reduce((a, b) => a + b, 0) / filteredData.map(item => item.weather_delay).length
        var nasDelay = filteredData.map(item => item.nas_delay).reduce((a, b) => a + b, 0) / filteredData.map(item => item.nas_delay).length
        var securityDelay = filteredData.map(item => item.security_delay).reduce((a, b) => a + b, 0) / filteredData.map(item => item.security_delay).length
        var LADelay = filteredData.map(item => item.late_aircraft_delay).reduce((a, b) => a + b, 0) / filteredData.map(item => item.late_aircraft_delay).length


        var data2 = [{
            values: [carrierDelay, weatherDelay, nasDelay, securityDelay, LADelay],
            labels: ['Carrier Delay', 'Weather Delay', 'NAS Delay', 'Security delay', 'Late Aircraft Delay' ],
            textinfo: "label+percent",
            hoverinfo: "label+percent",
            hole: .4,
            type: 'pie'
          }];
          
        var layout2 = {
            title: 'Reasons of Delay',
            margin: {"t": 50, "b": 50, "l": 50, "r": 50},
            showlegend: false
          };
          
        Plotly.newPlot('pie', data2, layout2)
    
    
    
    })
}

function buildLine(departureID, arrivalID, delayYear){
    d3.json(gurls.delay_day_url).then((data) =>{
        var filteredData = data.filter(row => row.arrival_airport == arrivalID && row.departure_airport == departureID && row.year == delayYear);

        var dayData = []

        for (var i = 1; i <= 31; i++) {
            dayData.push(i);
        }

        var depArray = []
        for (var [key, value] of Object.entries(filteredData)) {
            depArray.push(value.departure_delay.toFixed(2));
        }

        var arrArray = []
        for (var [key, value] of Object.entries(filteredData)) {
            arrArray.push(value.arrival_delay.toFixed(2));
        }


        var trace3 = {
            x: dayData,
            y: depArray,
            type: 'scatter',
            mode: 'lines',
            name: "Avg Departure Delay",
            marker: {
                color: 'rgb(49,130,189)',
                opacity: 0.7,
              }
          };
          
          var trace4 = {
            x: dayData,
            y: arrArray,
            type: 'scatter',
            mode: 'lines',
            name: "Avg Arrival Delay",
            marker: {
                color: 'rgb(250,86,86)',
                opacity: 0.5
              }
          };

          var layout3 = {
            title: 'Flight Delay by Day of March',
            xaxis: {
              title: 'Day',
              showgrid: false,
              zeroline: false
            },
            yaxis: {
              title: 'Delay(mins)',
              showline: false
            }
          };
          
          var data3 = [trace3, trace4];
          
          Plotly.newPlot('line', data3, layout3);

        
    })
}



function optionDeChanged(depName){
    d3.json(gurls.airport_url).then((data) => {
        depData = data.filter(row => row.airport_name == depName);
        departureID = depData[0].airport_id;
        document.getElementById("selDeparture").value = depName

        var newArrivalName = document.getElementById("selArrival").value 
        arrData = data.filter(row => row.airport_name == newArrivalName)
        arrivalID = arrData[0].airport_id;

        delayYear = d3.select("#d3-dropdown").property("value")
        

        buildCharts(departureID, arrivalID, delayYear);
        buildLine(departureID, arrivalID, delayYear);
    })

}

function optionArChanged(arrName){
    d3.json(gurls.airport_url).then((data) => {
        arrData = data.filter(row => row.airport_name == arrName);
        arrivalID = arrData[0].airport_id;
        document.getElementById("selArrival").value = arrName;

        var newDepartureID = document.getElementById("selDeparture").value;
        depData = data.filter(row => row.airport_name == newDepartureID);
        departureID = depData[0].airport_id;

        delayYear = d3.select("#d3-dropdown").property("value");

        buildCharts(departureID, arrivalID, delayYear);
        buildLine(departureID, arrivalID, delayYear);
    })

}

function optionCovChanged(menu){
    d3.json(gurls.airport_url).then((data) => {
        
        delayYear = menu;

        var newDepartureID = document.getElementById("selDeparture").value;
        depData = data.filter(row => row.airport_name == newDepartureID);
        departureID = depData[0].airport_id;

        var newArrivalName = document.getElementById("selArrival").value ;
        arrData = data.filter(row => row.airport_name == newArrivalName);
        arrivalID = arrData[0].airport_id;

        buildCharts(departureID, arrivalID, delayYear);
        buildLine(departureID, arrivalID, delayYear);

    })
}



init();
