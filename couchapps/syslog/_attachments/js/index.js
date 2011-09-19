var infoVis = {
    calcColor: function(percentage) {
        if(percentage < 2) {
            var color = '#00bfbf';
        } else if(percentage > 1 && percentage < 5) {
            var color = '#00bf5f';
        } else if(percentage > 4 && percentage < 15) {
            var color = '#00bf00';
        } else if(percentage > 14 && percentage < 25) {
            var color = '#5fbf00';
        } else if(percentage > 24 && percentage < 50) {
            var color = '#bfbf00';
        } else if(percentage > 49 && percentage < 75) {
            var color = '#bf5f00';
        } else if(percentage > 74) {
            var color = '#bf0000';
        }
        
        return color;
    },

    build: function(hostnames, daemons) {
        var labelType, useGradients, nativeTextSupport, animate;

        var json = new Object();
        json.id = "root";
        json.name = "Hostnames";
        json.data = {};
        json.children = new Array()
    
        for(var i in hostnames.rows) {
            var hostname = hostnames.rows[i].key;
            var total = hostnames.rows[i].value;

            json.children[i] = new Object();
            json.children[i].id = "hostname_" + hostname;
            json.children[i].name = hostname;
            json.children[i].data = new Object();
            json.children[i].data.total = total;
            json.children[i].data.$area = total;
            json.children[i].children = new Array();

            var cnt = 0;
            
            for(var ii in daemons.rows) {
                var dhostname = daemons.rows[ii].key[0];
                var daemon = daemons.rows[ii].key[1];
                var dtotal = daemons.rows[ii].value;
                
                if(dhostname == hostname) {
                    json.children[i].children[cnt] = new Object();
                    json.children[i].children[cnt].id = "daemon_" + daemon;
                    json.children[i].children[cnt].name = daemon;
                    json.children[i].children[cnt].data = new Object();
                    json.children[i].children[cnt].data.total = dtotal;
                    json.children[i].children[cnt].data.$area = dtotal;
                    json.children[i].children[cnt].data.$color = infoVis.calcColor(Math.round(dtotal / total * 100));
                    cnt++;   
                }
            }
        }
      
        //console.log(json);exit;

        /*var json = {
            "id": "root", 
            "name": "Hosts",
            "data": {},      
            "children": [
                {
                "id": "artist_A Perfect Circle", 
                "name": "A Perfect Circle",
                "data": {
                    "playcount": 547, 
                    "$area": 547
                },
                "children": [
                {
                    "id": "album-Thirteenth Step", 
                    "name": "Thirteenth Step",
                    "data": {
                        "playcount": "276", 
                        "$color": "#8E7032", 
                        "image": "http://userserve-ak.last.fm/serve/300x300/11403219.jpg", 
                        "$area": 276
                    }
                }, 
                {
                    "id": "album-Mer De Noms", 
                    "name": "Mer De Noms",
                    "data": {
                        "playcount": "271", 
                        "$color": "#906E32", 
                        "image": "http://userserve-ak.last.fm/serve/300x300/11393921.jpg", 
                        "$area": 271
                    }
                }]
            }]
        }*/

      //init TreeMap
      var tm = new $jit.TM.Squarified({
        //where to inject the visualization
        injectInto: 'infovis',
        //parent box title heights
        titleHeight: 15,
        //enable animations
        animate: animate,
        //box offsets
        offset: 1,
        //Attach left and right click events
        Events: {
          enable: true,
          onClick: function(node) {
            if(node) tm.enter(node);
          },
          onRightClick: function() {
            tm.out();
          }
        },
        duration: 1000,
        //Enable tips
        Tips: {
          enable: true,
          //add positioning offsets
          offsetX: 20,
          offsetY: 20,
          //implement the onShow method to
          //add content to the tooltip when a node
          //is hovered
          onShow: function(tip, node, isLeaf, domElement) {
            var html = "<div class=\"tip-title\">" + node.name 
              + "</div><div class=\"tip-text\">";
            var data = node.data;
            if(data.total) {
              html += "total: " + data.total;
            }
            tip.innerHTML =  html; 
          }  
        },
        //Add the name of the node in the correponding label
        //This method is called once, on label creation.
        onCreateLabel: function(domElement, node){
            domElement.innerHTML = node.name;
            var style = domElement.style;
            style.display = '';
            style.border = '1px solid transparent';
            domElement.onmouseover = function() {
              style.border = '1px solid #9FD4FF';
            };
            domElement.onmouseout = function() {
              style.border = '1px solid transparent';
            };
        }
      });
      tm.loadJSON(json);
      tm.refresh();
      //end
      //add events to radio buttons
      var sq = $jit.id('r-sq'),
          st = $jit.id('r-st'),
          sd = $jit.id('r-sd');
      var util = $jit.util;
      util.addEvent(sq, 'change', function() {
        if(!sq.checked) return;
        util.extend(tm, new $jit.Layouts.TM.Squarified);
        tm.refresh();
      });
      util.addEvent(st, 'change', function() {
        if(!st.checked) return;
        util.extend(tm, new $jit.Layouts.TM.Strip);
        tm.layout.orientation = "v";
        tm.refresh();
      });
      util.addEvent(sd, 'change', function() {
        if(!sd.checked) return;
        util.extend(tm, new $jit.Layouts.TM.SliceAndDice);
        tm.layout.orientation = "v";
        tm.refresh();
      });
      //add event to the back button
      var back = $jit.id('back');
      $jit.util.addEvent(back, 'click', function() {
        tm.out();
      });
    }
}

$.couch.db('syslog').view('all/distinct_hostnames?group=true', {
    success: function(hostnames) {
        $.couch.db('syslog').view('all/distinct_hostnames_and_daemons?group=true', {
            success: function(daemons) {
                infoVis.build(hostnames, daemons);
            }        
        });
    }
});
