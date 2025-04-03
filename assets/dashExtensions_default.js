window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature) {
                const selectedColor = feature.properties.selectedColor || '#6baed6'; // Default color (blue)
                const selectedOpacity = feature.properties.selectedOpacity || 0.4; // Default color (blue)
                return {
                    color: '#3182bd',
                    weight: 0.5,
                    opacity: 0.8,
                    fillColor: selectedColor,
                    fillOpacity: selectedOpacity
                };
            }

            ,
        function1: function(feature, layer) {
            // Mouseover event
            layer.on('mouseover', function() {
                if (!layer.options._originalStyle) {
                    // Save the original style if not already saved
                    layer.options._originalStyle = {
                        color: layer.options.color,
                        weight: layer.options.weight,
                        opacity: layer.options.opacity,
                        fillColor: layer.options.fillColor,
                        fillOpacity: layer.options.fillOpacity,
                    };
                }
                // Apply highlight style only to the hovered feature
                layer.setStyle({
                    color: '#2b5775',
                    weight: 3,
                    opacity: 1,
                    fillOpacity: 0.7
                });
            });

            // Mouseout event
            layer.on('mouseout', function() {
                if (layer.options._originalStyle) {
                    // Reset the style of the hovered feature
                    layer.setStyle(layer.options._originalStyle);
                }
            });
        }

    }
});