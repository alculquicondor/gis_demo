var viewer = new Cesium.Viewer('cesiumContainer', {
    imageryProvider: new Cesium.UrlTemplateImageryProvider({
        url: '/api/base_layer/{z}/{x}/{y}.png'
    }),
    baseLayerPicker : false
});


