window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature) {
                return {
                    color: '#3182bd',
                    weight: 2,
                    opacity: 0.8,
                    fillColor: '#6baed6',
                    fillOpacity: 0.4
                };
            }

            ,
        function1: function(feature, layer) {
            // Tooltip with state name
            layer.bindTooltip(`<strong>${feature.properties['NAME']}</strong>`, {
                sticky: true
            });

            // Mouseover event to highlight the state
            layer.on('mouseover', function() {
                layer.setStyle({
                    color: '#ff7800',
                    weight: 5,
                    fillOpacity: 0.9
                });
            });

            // Mouseout event to reset style
            layer.on('mouseout', function() {
                layer.setStyle({
                    color: '#3182bd',
                    weight: 2,
                    opacity: 0.8,
                    fillColor: '#6baed6',
                    fillOpacity: 0.4
                });
            });

            // Click event to log the state name and update style
            layer.on('click', function() {
                layer.setStyle({
                    color: '#ff7800', // Highlight clicked state
                    weight: 5,
                    fillOpacity: 0.9
                });
                console.log('Clicked state: ' + feature.properties['NAME']);

                // You can add additional actions like updating a Dash component or showing a message
                alert('You clicked on ' + feature.properties['NAME']);
            });
        }

    }
});