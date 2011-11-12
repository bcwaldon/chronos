# -*- coding: utf-8 -*- 
<%inherit file='layout.mako'/>

<div class='graph_container'>

    <div class='control'>
        <select id='graph_window'>
            <option value='6400'>2 Hours</option>
            <option value='3600'>1 Hour</option>
            <option value='1800'>30 Min.</option>
        </select>
        <input class='submit' type='button' value='Refresh' id='refresh_graph'/>
    </div>

    <div class='graph' id='graph_image_container'>
        <img id='index_graph' src='/static/loading.gif' />
    </div>

</div>

<script type='text/javascript'>
    function get_window() {
        return $('#graph_window option:selected').val();
    }

    load_graph(get_window());
    $('#refresh_graph').click(function() { load_graph(get_window()); });

</script>
