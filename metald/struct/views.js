Non Beam
==============
function(doc) {
  if(doc.profile && doc.grade && doc.thickness && doc.width && doc.length) {
    var key = {
		profile:doc.profile,
		grade:doc.grade,
		thickness:doc.thickness,
		width:doc.width,
		length:doc.length
    };
    var value = {company:doc.company};
    emit(key, value);
  }
}
