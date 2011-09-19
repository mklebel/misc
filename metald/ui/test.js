var db = new CouchDB("warehouse");
var request = CouchDB.request('GET', 'http://localhost:5984/warehouse/_design/non_beam/_view/all?limit=1');
print(request);
