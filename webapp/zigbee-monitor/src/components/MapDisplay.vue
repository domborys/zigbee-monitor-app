<template>
    <l-map
      ref="map"
      :min-zoom="minZoom"
      :crs="crs"
      style="height: 100%"
      v-if="layer"
    >
    <l-image-overlay
        :url="layer.imgurl"
        :bounds="layerBounds"
    />
    <l-marker
        v-for="node in layer.nodes"
        :key="node.name"
        :lat-lng="{lng: node.x, lat: node.y}"
    >
        <l-popup :content="node.name" />
    </l-marker>
    <!--
        <l-image-overlay
            :url="url"
            :bounds="bounds"
        />
        <l-marker
            v-for="star in stars"
            :key="star.name"
            :lat-lng="star"
        >
        <l-popup :content="star.name" />
        </l-marker>
        <l-polyline :lat-lngs="travel" />
    -->
    </l-map>
</template>

<script>
import { CRS, Icon } from "leaflet";
import { LMap, LImageOverlay, LMarker, LPopup, LPolyline } from "vue2-leaflet";
import 'leaflet/dist/leaflet.css';

delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});


export default {
    components: {
        LMap,
        LImageOverlay,
        LMarker,
        LPopup,
        LPolyline
    },
    props:{
        layer: Object
    },
    data() {
        return {
            url: require("@/assets/plan1.jpg"),
            bounds: [[0, 0], [10, 10]],
            minZoom: -2,
            crs: CRS.Simple,
            stars: [
            { name: "Sol", lng: 1, lat: 1},
            { name: "Mizar", lng: 2, lat: 1 },
            { name: "Krueger-Z", lng: 7, lat: 1 },
            { name: "Deneb", lng: 5, lat: 9 }
            ],
            travel: [[1, 1], [9, 5]]
        };
    },
    computed:{
        /*
        isActiveLayer(){
            return this.layers && (typeof this.activeLayer !== 'undefined');
        },
        activeLayer(){
            return this.layers.find(l => l.active);
        },*/
        layerBounds(){
            return [[0, 0], [this.layer.height, this.layer.width]]
        }
    },
    mounted() {
        if(this.$refs.map)
            this.$refs.map.mapObject.fitBounds(this.bounds);
        //this.$refs.map.mapObject.setView([5, 5], 0);
    }
};
</script>