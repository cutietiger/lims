require([
  'jquery',
  'pat-base',
  'highcharts'
], function($, Base) {
  'use strict';

  Base.extend({
    name: 'chart',
    trigger: '.pat-chart',
    parser: 'mockup',
    defaults: {
      chart: {
        type: 'bar'
      },
      title: {
        text: 'Fruit Consumption'
      }
    },
    init: function() {
      var self = this;
      Highcharts.chart(self.$el[0], self.options);
    }
  });
});

require([
  'jquery',
  'pat-base',
  'datatables.net',
  'datatables.net-buttons',
  'datatables.net-select',
  'datatables.net-colvis'
], function($, Base) {
  'use strict';

  Base.extend({
    name: 'datatable',
    trigger: '.pat-datatable',
    parser: 'mockup',
    defaults: {
      dom: '<"table-toolbar">Bfrtip',
      ajax: {
        data: function(d) {
          d.inactive_state = $('input[name=list_review_state]').val();
        }
      },
      buttons: [{
        extend: 'colvis',
        className: 'btn btn-default',
        columns: '.toggle'
        }
      ],
      columnDefs: [{
        targets: 0,
        searchable: false,
        orderable: false,
        width: '1%',
        className: 'dt-body-center',
        render: function ( data, type, full, meta ) {
          return '<input type="checkbox" data-transitions="'+full.valid_transitions+'">';      
          }
        },{
        targets: "_all",
        render: function ( data, type, full, meta ) {
          if (typeof data === 'string' || data instanceof String)
            return data;
          if ($.isArray(data)) {
            var res = ''
            for (var i = 0; i < data.length; i++) {
              var d = data[i];
              if (i > 0)
                res += '<br/>';
              if ("href" in d)
                res += '<a href="'+d.href+'">'+d.title+'</a>';
              else
                res += d.title;
            }
            return res;
          }
          if ("url" in data)
            return '<a href="'+data.url+'">'+data.title+'</a>';
          if ("image" in data)
            return '<img class="center-image" src="'+data.image+'" />';
          return "";
          }
      }]
    },
    init: function() {
      var self = this;
      var rows_selected = [];

      var opts = $.extend(self.options, {
        rowCallback: function(row, data, dataIndex){
          // Get row ID
          var rowId = data.uuid;

          // If row ID is in the list of selected row IDs
          if($.inArray(rowId, rows_selected) !== -1){
            $(row).find('input[type="checkbox"]').prop('checked', true);
            $(row).addClass('selected');
          }
         },
         initComplete: function(settings, json) {
           initColVis();
           initStates();
         }
        });

      var table = self.$el.DataTable(opts);

      // Handle form submission event 
      $('form#list').on('submit', function(e){
        var form = this;
      
        // Iterate over all selected checkboxes
        $.each(rows_selected, function(index, rowId){
          // Create a hidden element 
          $(form).append(
            $('<input>')
              .attr('type', 'hidden')
              .attr('name', 'uids[]')
              .val(rowId)
          );
        });
      });

      // Styling the column visible button
      function initColVis() {
        var title = table.i18n('buttons.colvis', 'Column Visibility');
        $('.buttons-colvis').html('<span class="glyphicon glyphicon-th" ' +
                                  'data-toggle="tooltip" title="'+title+'" />');
      }

      // State buttons
      function initStates() {
        var states = self.options.review_states;
        var current_state = self.options.state_id;
        for (var i = 0; i < states.length; i++) {
          var state = states[i];
          var btn = $('<a/>').addClass('btn btn-default')
            .attr('name', 'states')
            .attr('value', state.id)
            .attr('href',state.url)
            .html(state.title);
          if(current_state.id === state.id)
            btn.addClass('selected');
          $("div.table-toolbar").append(btn);
        }
        $("div.table-toolbar").addClass('btn-group');
      }

      // Workflow actions
      $('a[name="workflow_action_button"]').on('click', function(e) {
        e.preventDefault();
        $('form#list').append(
          $('<input>')
            .attr('type', 'hidden')
            .attr('name', 'workflow_action_id')
            .val($(this).attr('transition'))
        );
        $('form#list').submit();
      });
      
      // Updates "Select all" control in a data table
      //
      function updateDataTableSelectAllCtrl(table){
        var $table             = table.table().node();
        var $chkbox_all        = $('tbody input[type="checkbox"]', $table);
        var $chkbox_checked    = $('tbody input[type="checkbox"]:checked', $table);
        var chkbox_select_all  = $('thead input[name="select_all"]', $table).get(0);
        var all_valid_transitions = [];

        // If none of the checkboxes are checked
        if($chkbox_checked.length === 0){
          chkbox_select_all.checked = false;
          if('indeterminate' in chkbox_select_all){
            chkbox_select_all.indeterminate = false;
          }
          // Hide all workflow action buttons
          $("a[name='workflow_action_button']").hide();
          return;
        }

        // If all of the checkboxes are checked
        if ($chkbox_checked.length === $chkbox_all.length){
          chkbox_select_all.checked = true;
          if('indeterminate' in chkbox_select_all){
            chkbox_select_all.indeterminate = false;
          }

          // If some of the checkboxes are checked
        } else {
          chkbox_select_all.checked = true;
          if('indeterminate' in chkbox_select_all){
            chkbox_select_all.indeterminate = true;
          }
        }

        // Get intersection of all valid transactions
        for(var i = 0; i < $chkbox_checked.length; i++){
          all_valid_transitions.push($($chkbox_checked[i]).attr("data-transitions").split(","));
        }

        // intersect values from all arrays in all_valid_transitions
        var valid_transitions = all_valid_transitions.shift().filter(function (v) {
           return all_valid_transitions.every(function (a) {
		        return a.indexOf(v) !== -1;
          })
        })

        // Hide all buttons except the ones listed as valid
        $.each($("a[name='workflow_action_button']"), function(i, e){
          if ($.inArray($(e).attr('transition'), valid_transitions) == -1) {
            $(e).hide();
          }
          else {
            $(e).show();
          }
        });
      }

      // Handle click on checkbox
      $('tbody').on('click', 'input[type="checkbox"]', function(e){
        var $row = $(this).closest('tr');

        // Get row data
        var data = table.row($row).data();

        // Get row ID
        var rowId = data.uuid;

        // Determine whether row ID is in the list of selected row IDs 
        var index = $.inArray(rowId, rows_selected);

        // If checkbox is checked and row ID is not in list of selected row IDs
        if(this.checked && index === -1){
          rows_selected.push(rowId);

        // Otherwise, if checkbox is not checked and row ID is in list of selected row IDs
        } else if (!this.checked && index !== -1){
          rows_selected.splice(index, 1);
        }

        if(this.checked){
          $row.addClass('selected');
        } else {
          $row.removeClass('selected');
        }

        // Update state of "Select all" control
        updateDataTableSelectAllCtrl(table);

        // Prevent click event from propagating to parent
        e.stopPropagation();
      });

      // Handle click on table cells with checkboxes
      $('table').on('click', 'tbody td:not(:has(> a)), thead th:first-child', function(e){
        $(this).parent().find('input[type="checkbox"]').trigger('click');
      });

      // Handle click on "Select all" control
      $('thead input[name="select_all"]', table.table().container()).on('click', function(e){
        if(this.checked){
           $('tbody input[type="checkbox"]:not(:checked)').trigger('click');
        } else {
           $('tbody input[type="checkbox"]:checked').trigger('click');
        }

        // Prevent click event from propagating to parent
        e.stopPropagation();
      });

      // Handle table draw event
      table.on('draw', function(){
        // Update state of "Select all" control
        updateDataTableSelectAllCtrl(table);
      });
    }
  });
});
