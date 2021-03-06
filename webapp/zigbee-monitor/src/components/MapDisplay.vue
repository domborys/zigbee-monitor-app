<template>
    <div class="map-display-container">
        <div v-if="mapVisible" class="map-header">
            <label>
                <input type="checkbox" v-model="showTooltips">
                Pokaż opisy czujników
            </label>
        </div>
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
                :icon="getIcon(node)"
            >
                <node-tooltip :node="node" :visible="showTooltips" />
            </l-marker>
            <l-marker
                v-if="editedNodeWasPlaced"
                :lat-lng="{lng: editedNode.x, lat: editedNode.y}"
                :icon="editedNodeIcon"
            >
                <node-tooltip :node="editedNode" :visible="showTooltips" />
            </l-marker>
            </l-map>
            <div class="place-node-message" v-if="!!editedNode">
                Kliknij na mapie, aby umieścić węzeł.
            </div>
        </div>
    </div>
</template>

<script>
import { CRS, icon,Icon } from "leaflet";
import { LMap, LImageOverlay, LMarker, LPopup, LPolyline, LTooltip } from "vue2-leaflet";
import 'leaflet/dist/leaflet.css';
import NodeTooltip from './NodeTooltip.vue';

delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const defaultIconSize = [25, 41];
const defaultIconAnchor = [12, 41];

const icons = {
    red: icon({
        iconUrl:require("@/assets/leaflet-icons/marker-icon-red.png"),
        iconSize:defaultIconSize,
        iconAnchor:defaultIconAnchor
    }),
    green: icon({
        iconUrl:require("@/assets/leaflet-icons/marker-icon-green.png"),
        iconSize:defaultIconSize,
        iconAnchor:defaultIconAnchor
    }),
    purple: icon({
        iconUrl:require("@/assets/leaflet-icons/marker-icon-purple.png"),
        iconSize:defaultIconSize,
        iconAnchor:defaultIconAnchor
    }),
    gray: icon({
        iconUrl:require("@/assets/leaflet-icons/marker-icon-gray.png"),
        iconSize:defaultIconSize,
        iconAnchor:defaultIconAnchor
    }),
}

/**
 * The component used for displaying maps. It should be used inside the right pane of MainLayout.
 */
export default {
    components: {
        LMap,
        LImageOverlay,
        LMarker,
        LPopup,
        LPolyline,
        LTooltip,
        NodeTooltip,
    },
    props:{
        /**
         * The currently displayed map.
         */
        layer: Object
    },
    data() {
        return {
            showTooltips:true,
            minZoom: -50,
            crs: CRS.Simple,
        };
    },
    computed:{
        mode(){
            return this.$store.getters.mode;
        },
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
        },
        editedNodeIcon(){
            return icons.purple;
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
        getIcon(node){
            if(this.mode === 'view'){
                if(node.discovered === true)
                    return icons.green;
                else if(node.discovered === false)
                    return icons.red;
                else
                    return icons.gray;
            }
            else{
                if(this.isNodeEdited(node))
                    return icons.purple;
                else
                    return icons.gray;
            }
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

.map-display-container{
    height:100%;
    display: flex;
    flex-direction: column;
}

.map-header{
    flex:none;
    box-sizing:border-box;
    padding:8px;
    border-bottom:1px solid #E6E6FA;
}

.map-container{
    flex:auto;
    overflow:auto;
    min-height:0;
}

.map-container{
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
    background-color: rgb(130,68,190);
    color:white;
}

.edited-node-mode .vue2leaflet-map{
    cursor:crosshair;
}

</style>