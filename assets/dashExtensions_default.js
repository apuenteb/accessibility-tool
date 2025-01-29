window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature) {
                const selectedColor = feature.properties.selectedColor || '#6baed6'; // Default color (blue)
                const selectedOpacity = feature.properties.selectedOpacity || 0.4; // Default color (blue)
                return {
                    color: '#3182bd',
                    weight: 0,
                    opacity: 0.8,
                    fillColor: selectedColor,
                    fillOpacity: selectedOpacity
                };
            }

            ,
        function1: function(feature, layer) {
            // Mouseover event
            layer.on('mouseover', function() {
                const CUSEC = feature.properties['CUSEC'];

                // Highlight all polygons with the same CUSEC
                this._map.eachLayer((otherLayer) => {
                    if (otherLayer.feature && otherLayer.feature.properties['CUSEC'] === CUSEC) {
                        if (!otherLayer.options._originalStyle) {
                            // Save the original style if not already saved
                            otherLayer.options._originalStyle = {
                                color: otherLayer.options.color,
                                weight: otherLayer.options.weight,
                                opacity: otherLayer.options.opacity,
                                fillColor: otherLayer.options.fillColor,
                                fillOpacity: otherLayer.options.fillOpacity,
                            };
                        }
                        otherLayer.setStyle({
                            color: '#2b5775',
                            weight: 3,
                            opacity: 1,
                            fillOpacity: 0.7
                        });
                    }
                });
            });

            // Mouseout event
            layer.on('mouseout', function() {
                const CUSEC = feature.properties['CUSEC'];

                // Reset the style of all polygons with the same CUSEC
                this._map.eachLayer((otherLayer) => {
                    if (otherLayer.feature && otherLayer.feature.properties['CUSEC'] === CUSEC) {
                        const originalStyle = otherLayer.options._originalStyle;
                        if (originalStyle) {
                            otherLayer.setStyle(originalStyle);
                        }
                    }
                });
            });
        }

    }
});