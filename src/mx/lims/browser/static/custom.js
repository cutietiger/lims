require([
  'jquery',
  'pat-base'
], function($, Base) {
  'use strict';

  Base.extend({
    name: 'lims-table',
    trigger: '.pat-lims-table',
    parser: 'mockup',
    defaults: {
    },
    init: function() {
      var self = this;
      $('.workflow_action-button').on('click', function(event) {
        var form = $(this).parents("form");
        var form_id = $(form).attr("id");
        $(form).append("<input type='hidden' name='workflow_action_id' value='" 
          + $(this).attr("transition") + "'>");
      }
    }
  });
});

require([
  'jquery',
  'pat-base',
  'datatables.net',
  'datatables.net-bs',
  'datatables.net-select'
], function($, Base) {
  'use strict';

  Base.extend({
    name: 'datatable',
    trigger: '.pat-datatable',
    parser: 'mockup',
    defaults: {
      dom: '<"table-toolbar">frtBip',
      ajax: {
        data: function(d) {
          d.inactive_state = $('input[name=states]:checked').val();
        }
      },
      buttons: [{
        text: 'Activate',
        action: function(e, dt, node, config) {
          var rows = JSON.stringify(dt.rows('.selected').data().toArray());
          var table = dt;
          console.log(rows);
          $.ajax({
            type : "POST",
            url : 'http://123.57.20.123:8080/Lims/methods/@@activate_objects',
            data : { 'data' : rows },
            success : function (result) {
              table.ajax.reload();
              alert(result)
            },
          });
        }
      }],
      columnDefs: [{
        targets: 0,
        className: 'select-checkbox'
        },{
        targets: 1,
        render: function ( data, type, full, meta ) {
          return '<a href="'+data.url+'">'+data.title+'</a>';
        }
      }],
      select: {
        style: 'multi'
      }
    },
    init: function() {
      var self = this;
      var table = self.$el.DataTable(self.options);

      var buttons = '<label>' +
                    '<input type="radio" name="states" value="" checked="checked">All</label>' +
                    '<label>' +
                    '<input type="radio" name="states" value="active">Active</label>' +
                    '<label>' +
                    '<input type="radio" name="states" value="inactive">Inactive</label>';

      $("div.table-toolbar").html(buttons);

      $('input[name=states]').on('change', function() {
        table.ajax.reload();
      });
    }
  });
});
