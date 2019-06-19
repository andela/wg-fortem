/*
 This file is part of wger Workout Manager.

 wger Workout Manager is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 wger Workout Manager is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 */

'use strict';

$(document).ready(function () {
  var url;
  var username;
  var nametext;
  var chartParams;
  var weightChart;
  var checkboxes;
  var data;
  $('#compare').hide();

  $('input[type=checkbox].checkbox').change(function () {
    checkboxes = $('input[type=checkbox].checkbox:checked');
    if (checkboxes.size() === 2) {
      $('#compare').show();
    } else {
      $('#compare').hide();
      $('#compare_weight_diagrams').empty();
    }
  });


  $('#compare').click(function () {
    var users = [];
    $(checkboxes).each(function (index) {
      username = $(this).attr('id');
      nametext = $(this).attr('value');
      url = '/weight/api/compare_weight_data/' + username;
      users.push(nametext + ' (' + username + ')');
      d3.json(url).then(function (json) {
        weightChart = {};
        chartParams = {
          animate_on_load: true,
          full_width: true,
          top: 10,
          left: 30,
          right: 10,
          show_secondary_x_label: true,
          xax_count: 10,
          target: '[data-id="weight_diagram_' + index + '"]',
          x_accessor: 'date',
          y_accessor: 'weight',
          min_y_from_data: true,
          colors: ['#3465a4'],
          title: users[index]
        };

        if (json.length) {
          $('#compare_weight_diagrams').append("<div data-id='weight_diagram_" + index + "'></div>");
          data = MG.convert.date(json, 'date');
          weightChart.data = data;
          // Plot the data
          chartParams.data = data;
          MG.data_graphic(chartParams);
        } else {
          $('#compare_weight_diagrams').append('<div class="alert alert-danger" role="alert">' + users[index] + '"has no weight data"</div>');
        }
      });
    });
  });
});
