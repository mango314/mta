nv.addGraph(function() {
  var chart = nv.models.multiBarChart()
                .x(function(d) { return d["hour"] })
                .y(function(d) { return d["in"] })
                .color(d3.scale.category10().range());

d3.json(  "bedford_park.json" , function(data) {
  d3.select('#chart svg')
      .datum(data)
    .transition().duration(500)
      .call(chart);
})
  nv.utils.windowResize(chart.update);

  return chart;
});
