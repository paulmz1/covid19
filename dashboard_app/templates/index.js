{% macro js() -%}
$.fn.dataTable.ext.order['dom-checkbox'] = function  ( settings, col ){
      return this.api().column( col, {order:'index'} ).nodes().map( function ( td, i ) {
        return $(td).closest('tr').hasClass('selected') ? '1' : '0';
      } );
    }


$(document).ready(function() {
    var table = $('#countries').DataTable({
       "stateSave": true,
       "stateDuration": 0,
       "lengthMenu": [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],

       columnDefs: [{
          orderable: true,
          className: 'select-checkbox',
          targets: 0,
                orderDataType: 'dom-checkbox'
        }],
        select: {
          style: 'multi',
          selector: 'td:first-child'
        },
        order: [
          [0, 'desc'],[2, 'desc']
        ]
    });


    $(  '<div class="per_mil">'+
        '<label><input type="checkbox" id="per_million" name="per_million" value="per_million"/>'+
        'Show cases per million</label>'+
        '</div>'
    ).insertAfter( "#countries_length" );

    $('#per_million').change(function() {
        showPopulation(this.checked)
    });

    table
        .on( 'select', saveSelections)
        .on( 'deselect', saveSelections);

    showPopulation(false);
    loadSelections();
    loadCharts(table);
    // loadFooter();

    function showPopulation(show){
        table.columns([2,3,4,5,6]).visible(!show);
        table.columns([7,8,9,10,11]).visible(show);
    }

    $('#updateBtn').click(function(){
        table.draw();
        loadCharts(table);

    });

    function loadSelections(){
        var rks = localStorage.rowKeyStore;

        if(!rks){
            rks = default_countries
        }

        var rowKeys = JSON.parse(rks);
        for (var key in rowKeys){
            table.row(rowKeys[key]).select()
        }
        table.draw()

    }

    function saveSelections(){
        var sel = table.rows( { selected: true } );
        localStorage.rowKeyStore = JSON.stringify(sel[0]);
    }

});

function loadCharts(table){
    // $('#countries_page').load('/countries?countries='+q)
    var per_million = $('#per_million').is(":checked")
    loadCountriesLastDayCharts(table, per_million);
    loadCountriesCharts(table, per_million);
}

function loadCountriesLastDayCharts(table, per_million){
    var sel = table.rows( {  selected: true, order: 'applied' } );
    var q = JSON.stringify(sel[0]);
    $('#countries_last_day_page').load('/countries_last_day?countries='+q+'&per_million='+per_million);
}

function loadCountriesCharts(table, per_million){
    var sel = table.rows( {  selected: true } );
    var i = sel[0]
    i.sort();
    var q = JSON.stringify(i);

    loadCountriesChart(table, 'Confirmed', q, per_million);
    loadCountriesChart(table, 'Closed', q, per_million);
    loadCountriesChart(table, 'Recovered', q, per_million);
    loadCountriesChart(table, 'Deaths', q, per_million);
    loadCountriesChart(table, 'Active', q, per_million);
}

function loadCountriesChart(table, name, q, per_million){
    Plotly.d3.csv('/countries_csv?countries='+q+'&column='+name+'&per_million='+per_million, function(data){
        processData(data, name, per_million)
    } );
}

function processData(rows, name, per_million) {
    function unpack(rows, key) {
        return rows.map(function(row) {
             return row[key];
         });
    }

    var headers = Plotly.d3.keys(rows[0]);

    var traces = [];

    for (var i=1; i<headers.length; i++) {
        header = headers[i];
        traces.push({
            x: unpack(rows, 'Date'),
            y: unpack(rows, header),
            name: header
        });
    }
    
    var title = 'Incidents by country '+ (per_million ? 'per million population ' : '') +'('+name+')'
    Plotly.newPlot('countries_'+name+'_chart', traces, {title: title});

}

function loadFooter(){
    $('#footer').load('/static/footer.html');
}
{%- endmacro %}

