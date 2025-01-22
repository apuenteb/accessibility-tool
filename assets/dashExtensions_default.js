window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature) {
                const isClicked = feature.properties.clicked || false;
                const selectedColor = feature.properties.selectedColor || '#6baed6'; // Default color
                return {
                    color: '#3182bd',
                    weight: 2,
                    opacity: 0.8,
                    fillColor: isClicked ? '#ff0000' : selectedColor,
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
                    fillColor: feature.properties.selectedColor || '#6baed6', // Default fill color
                    fillOpacity: 0.4
                });
            });

            // Click event to change fillColor to red and log the state name
            layer.on('click', function() {
                feature.properties.clicked = !feature.properties.clicked; // Toggle clicked state
                layer.setStyle({
                    fillColor: feature.properties.clicked ? '#ff0000' : feature.properties.selectedColor, // Toggle color
                    weight: 5,
                    fillOpacity: 0.9
                });
                console.log('Clicked state: ' + feature.properties['NAME']);
            });
        }

    }
});