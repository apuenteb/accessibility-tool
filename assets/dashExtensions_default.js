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
            // Reference to highlighted layers
            let highlightedLayers = [];

            // Mouseover event
            layer.on('mouseover', function() {
                const CUSEC = feature.properties['CUSEC'];

                // Highlight all polygons with the same CUSEC
                this._map.eachLayer((otherLayer) => {
                    if (otherLayer.feature && otherLayer.feature.properties['CUSEC'] === CUSEC) {
                        otherLayer.setStyle({
                            color: '#2b5775',
                            weight: 3,
                            opacity: 1,
                            fillOpacity: 0.7
                        });
                        highlightedLayers.push(otherLayer);
                    }
                });
            });

            // Mouseout event
            layer.on('mouseout', function() {
                // Reset the style of all highlighted layers
                highlightedLayers.forEach((hlLayer) => {
                    hlLayer.setStyle({
                        color: '#3182bd',
                        weight: 2,
                        opacity: 0.8,
                        fillColor: '#6baed6',
                        fillOpacity: 0.4
                    });
                });
                highlightedLayers = [];
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