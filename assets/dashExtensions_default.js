window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature) {
                const choice = "{choice}";
                return {
                    color: '#3182bd',
                    weight: 2,
                    opacity: 0.8,
                    fillColor: feature.properties["color"] || '#6baed6',
                    fillOpacity: 0.4
                };
            }

            ,
        function1: function() {
                return {
                    color: '#2b5775',
                    weight: 3,
                    opacity: 1,
                    fillOpacity: 0.7
                };
            }

            ,
        function2: function(feature, layer) {
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

            // Tooltip
            layer.bindTooltip(
                `<strong>${feature.properties['CUSEC']}</strong><br>Municipio: ${feature.properties['Municipio']}`, {
                    permanent: false,
                    direction: 'top'
                }
            );
        }

    }
});