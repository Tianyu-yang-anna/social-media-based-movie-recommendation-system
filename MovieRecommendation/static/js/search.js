var states = [
    "Alabama AL",
    "Alaska AK",
    "Arizona AZ",
    "Arkansas AR",
    "California CA",
    "Colorado CO",
    "Connecticut CT",
    "Delaware DE",
    "Florida FL",
    "Georgia GA",
    "Hawaii HI",
    "Idaho ID",
    "Illinois IL",
    "Indiana IN",
    "Iowa IA",
    "Kansas KS",
    "Kentucky KY",
    "Louisiana LA",
    "Maine ME",
    "Maryland MD",
    "Massachusetts MA",
    "Michigan MI",
    "Minnesota MN",
    "Mississippi MS",
    "Missouri MO",
    "Montana MT",
    "Nebraska NE",
    "Nevada NV",
    "New Hampshire NH",
    "New Jersey NJ",
    "New Mexico NM",
    "New York NY",
    "North Carolina NC",
    "North Dakota ND",
    "Ohio OH",
    "Oklahoma OK",
    "Oregon OR",
    "Pennsylvania PA",
    "Rhode Island RI",
    "South Carolina SC",
    "South Dakota SD",
    "Tennessee TN",
    "Texas TX",
    "Utah UT",
    "Vermont VT",
    "Virginia VA",
    "Washington WA",
    "West Virginia WV",
    "Wisconsin WI",
    "Wyoming WY"
]

// function initMap() {
//     map = new google.maps.Map(document.getElementById("map"), {
//         center: { lat: -34.397, lng: 150.644 },
//         zoom: 8,
//     });
//     console.log("initial test")
// }
//
// window.initMap = initMap;

var time_period = [
    "1 week",
    "2 weeks",
    "30 days",
    "60 days"
]

var period_to_num = {
    "1 week": 7,
    "2 weeks": 14,
    "30 days": 30,
    "60 days": 60
}

var days = []

function generate_location_zone(){
    let comment = $("<span>").text("Location: ")
    $(".location_zone").append(comment)
    let loc = $("<input>").attr("id", "location_input")
    loc.attr("type", "text")
    loc.attr("list", "loc_list")
    $(".location_zone").append(loc)
    let loc_list = $("<datalist>").attr("id", "loc_list")
    for(i=0; i<states.length; i++){
        let new_option = $("<option>")
        new_option.val(states[i])
        loc_list.append(new_option)
    }
    $(".location_zone").append(loc_list)
}

function generate_time_zone(){
    let comment = $("<span>").text("Time: ")
    $(".time_zone").append(comment)
    let time_input = $("<input>").attr("id", "time_input")
    time_input.attr("type", "text")
    time_input.attr("list", "time_list")
    $(".time_zone").append(time_input)
    let time_list = $("<datalist>").attr("id", "time_list")
    for(i=0; i<time_period.length; i++){
        let new_option = $("<option>")
        new_option.val(time_period[i])
        time_list.append(new_option)
    }
    $(".time_zone").append(time_list)
}

function get_days(period){
    let time = new Date()
    let num = period_to_num[period]
    for (i=0; i<num; i++){
        let dd = time.getDate().toString()
        let mm = time.getMonth()+1
        mm = mm.toString()
        let yy = time.getFullYear().toString()
        if (dd.length < 2){
            dd = "0"+ dd
        }
        if (mm.length < 2){
            mm = "0"+ mm
        }
        days.push(yy+"-"+mm+"-"+dd)
        time.setDate(time.getDate()-1)
    }
}

// function get_geoinfo(location){
//     let loc = location.substring(0, location.length-2)
//     loc = loc+"State"
//     console.log(loc)
//     var geocoder = new google.maps.Geocoder()
//     geocoder.geocode({ 'address': loc}, function(results, status) {
//         if (status == 'OK') {
//             console.log("status ok")
//             let center = {
//                 "lat":results[0].geometry.location.lat(),
//                 "lng":results[0].geometry.location.lng()
//             }
//             console.log("center ",center)
//             // console.log(results[0].geometry.location)
//             let north = results[0].geometry.bounds.Ab.j
//             let east = results[0].geometry.bounds.Va.j
//             // console.log(results[0].geometry.bounds)
//             let ne =  {
//                 "lat": north,
//                 "lng": east
//             }
//             console.log("ne", ne)
//             let radius = google.maps.geometry.spherical.computeDistanceBetween(center, ne)
//             console.log("radius", radius)
//             geocodes.push({
//                 "latitude": center.lat,
//                 "longitude": center.lng,
//                 'radius': radius
//             })
//         } else {
//             console.log("status not ok")
//             alert('Geocode was not successful for the following reason: ' + status);
//             geocodes.push({
//                 "latitude": 0.0,
//                 "longitude": 0.0,
//                 'radius': 0.0
//             })
//         }
//     })
// }

function clear_page(){
    $("#title_input").val("")
    $("#title_input").focus()
    $("#location_input").val("")
    $("#time_input").val("")
    $(".result_comment_zone").empty()
    $(".result_topic_zone").empty()
    $(".score_zone").empty()
    $(".clear_button_zone").empty()
    $(".submit_search").removeAttr("disabled")
}

function show_result(info) {
    $(".result_topic_zone").text("Search Result:")
    let comment = "Title: "+info.title+", time period: from "
    let first_day = days[days.length-1]
    let last_day = days[0]
    comment = comment + first_day+ " to "+ last_day
    comment = comment + ", location: "+ info.location
    $(".result_comment_zone").text(comment)
    if (info.score >= 0){
        $(".score_zone").text("Score: "+info.score)
    } else {
        $(".score_zone").text("Sorry, there isn't tweets and youtube commends base on your location and time period choice. Please try longer time period or other location.")
    }
    let clear_button = $("<button>").addClass("clear_button")
    clear_button.text("clear")
    $(".clear_button_zone").append(clear_button)
    $(".clear_button").click(function (){
        clear_page()
    })
}


$(document).ready(function (){
    generate_location_zone()
    generate_time_zone()
    $(".submit_search").click(function (){
        let period = $("#time_input").val()
        let location = $("#location_input").val()
        let title = $("#title_input").val()
        if (period.length>0){
            get_days(period)
            if (location.length>0){
                let info = {
                    'title': title,
                    'geo_info': location,
                    'dates': days,
                    'csrfmiddlewaretoken': token
                }
                // console.log("info" ,info)
                $.ajax({
                    type: "POST",
                    url: "/search",
                    // dataType : "json",
                    // contentType: "application/json; charset=utf-8",
                    // contentType: "application/json",
                    // data : JSON.stringify(info),
                    data : info,
                    success: function (result){
                        console.log(result)
                        $(".submit_search").attr("disabled", "true")
                        let result_for_show = {
                            "title": title,
                            "location": location,
                            "score": result["scores"].score
                        }
                        show_result(result_for_show)
                        days = []
                    },
                    error: function(request, status, error){
                        console.log("Error");
                        console.log(request)
                        console.log(status)
                        console.log(error)
                    }
                })
            }
        }
    })
})