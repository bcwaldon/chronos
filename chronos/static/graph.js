
function load_graph(graph_window)
{
    $('#index_graph').remove();
    var img = $("<img id='index_graph' />").attr('src', '/graph?window='+graph_window)
                .load(function() { $('#graph_image_container').append(img); });
}
