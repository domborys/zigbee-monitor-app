<template>
    <div class="map-container" :class="{'edited-node-mode':!!editedNode}">
        <l-map
        ref="map"
        :min-zoom="minZoom"
        :crs="crs"
        style="height: 100%; z-index:10"
        v-if="mapVisible"
        @click="mapClick"
        >
        <l-image-overlay
            :url="layer.imgurl"
            :bounds="layerBounds"
        />
        <l-marker
            v-for="node in nodesToDisplay"
            :key="node.name"
            :lat-lng="{lng: node.x, lat: node.y}"
        >
            <l-popup :content="node.name" />
        </l-marker>
        <l-marker
            v-if="editedNodeWasPlaced"
            :lat-lng="{lng: editedNode.x, lat: editedNode.y}"
        >
            <l-popup :content="editedNode.name" />
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
        <div class="place-node-message" v-if="!!editedNode">
            Kliknij na mapie, aby umieścić węzeł.
        </div>
    </div>
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
            minZoom: -10,
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
        },
        layerUrl(){
            return this.layer ? this.layer.imgurl : null;
        },
        mapVisible(){
            return this.layer && this.layer.imgurl;
        },
        nodesToDisplay(){
            if(this.editedNode){
                return this.layer.nodes.filter(l => !this.isNodeEdited(l));
            }
            else{
                return this.layer.nodes;
            }
        },
        editedNode(){
            return this.$store.state.editedNode;
        },
        editedNodeWasPlaced(){
            return this.editedNode && (typeof this.editedNode.x === 'number') && (typeof this.editedNode.y === 'number');
        }
    },
    methods:{
        isNodeEdited(node){
            if(!this.editedNode)
                return false;
            else if(this.editedNode.id !== null && node.id === this.editedNode.id)
                return true;
            else if(this.editedNode.tempId !== null && node.tempId === this.editedNode.tempId)
                return true;
            else
                return false;
        },
        mapClick(e){
            if(this.editedNode){
                const coordinates = {x:e.latlng.lng, y:e.latlng.lat};
                this.$store.commit('setCoordinatesOfEditedNode', coordinates);
            }
        },
        fitBounds(){
            this.$nextTick(function () {
                if(this.layerUrl && this.$refs.map){
                    this.$refs.map.mapObject.fitBounds(this.layerBounds, {animate:false});
                }
            })
        }
    },
    watch:{
        layerUrl(newUrl, oldUrl){
            this.fitBounds();
        },
    },
    mounted(){
        this.fitBounds();
    }
};
</script>

<style scoped>
.map-container{
    height: 100%;
    position:relative;
}

.place-node-message{
    position:absolute;
    left: 50%;
    transform: translate(-50%, 0);
    top:0;
    text-align:center;
    padding:10px;
    z-index:100;
    font-size:20px;
    background-color: #630094;
    color:white;
}
.edited-node-mode .vue2leaflet-map{
    cursor:crosshair;
}
</style>