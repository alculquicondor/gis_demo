var viewer = new Cesium.Viewer('cesiumContainer', {
    imageryProvider: new Cesium.UrlTemplateImageryProvider({
        url: '/api/base_layer/{z}/{x}/{y}.png'
    }),
    baseLayerPicker : false
});

viewer.dataSources.add(Cesium.GeoJsonDataSource.load('/api/areas', {
    stroke: Cesium.Color.HOTPINK,
    fill: Cesium.Color.PINK,
    strokeWidth: 3,
    markerSymbol: '?'
}));
