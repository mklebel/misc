var couchmap = {
    map: '',
    init: function init() {
	    couchmap.map = new google.maps.Map(document.getElementById('map'),{
		    zoom: 6,
		    center: new google.maps.LatLng(46.000000, -93.662319),
		    mapTypeId: google.maps.MapTypeId.ROADMAP
	    });

        couchmap.query();
	},
    query: function() {
        $.couch.db('mn_hunter_walking_trails').allDocs({
            include_docs: true,
            success: function(data) {
                couchmap.buildStruct(data);
            }
        });
    },
    buildStruct: function(data) {
        var paths = new Object();
        paths.type = 'FeatureCollection';
        paths.features = new Array();
        var count = 0;

        for(x in data.rows) {
            // this check filters out the design docs
            if(data.rows[x].doc.geometry) {
                if(data.rows[x].doc.geometry.type == "MultiLineString") {
                    var coordinates = data.rows[x].doc.geometry.coordinates;
                    var mls_geometry = new Array();
                    data.rows[x].doc.geometry.coordinates = new Array();
                    for(i in coordinates) {
                        for(ii in coordinates) {
                            data.rows[x].doc.geometry.coordinates = coordinates[ii];
                        }
                    }
                    paths.features[count] = new Object();
                    paths.features[count] = data.rows[x].doc.geometry;                    
                    count++;
                } else {
                    paths.features[count] = new Object();
                    paths.features[count] = data.rows[x].doc.geometry;                    
                    count++;
                }            
            }
        }
        console.log(paths);exit();
        couchmap.showFeature(paths);
    },
    showFeature: function(geojson, style) {
	    currentFeature_or_Features = new GeoJSON(geojson, style || null);   
        if (currentFeature_or_Features.type && currentFeature_or_Features.type == "Error"){
		    document.getElementById("put_geojson_string_here").value = currentFeature_or_Features.message;
		    return;
	    }
	    if (currentFeature_or_Features.length){
		    for (var i = 0; i < currentFeature_or_Features.length; i++){
                if(typeof(currentFeature_or_Features[i].setMap) == 'undefined') {
                    console.log(currentFeature_or_Features[i]);
                    break;
                } else {
                    //console.log(currentFeature_or_Features[i]);
                    //break;
                }
                currentFeature_or_Features[i].setMap(couchmap.map);
		    }
	    }else{
		    currentFeature_or_Features.setMap(couchmap.map)
	    }      
    }
};
