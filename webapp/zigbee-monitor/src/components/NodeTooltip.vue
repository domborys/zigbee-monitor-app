<template>
    <l-tooltip ref="lTooltipComponent" :options="{direction:'top', permanent:true, offset:[0,-35], opacity:1}" @ready="tooltipReady">
        <b>{{node.name}}</b><br>
        <div v-for="config in node.readingConfigs" :key="config.name">
            {{config.name}}: {{config.lastReading === null ? '---' : config.lastReading}}
        </div>
    </l-tooltip>
</template>

<script>
import { LTooltip } from "vue2-leaflet";

export default {
    name:"NodeTooltip",
    components: {
        LTooltip,
    },
    data(){
        return {
            tooltipMapObject: null,
        }
    },
    props:{
        node: Object,
        visible:{
            type: Boolean,
            default:true,
        },
    },
    methods:{
        tooltipReady(mapObject){
            this.tooltipMapObject = mapObject;
        }
    },
    watch:{
        visible(newVisible, oldVisible){
            try{
                if(newVisible){
                    this.$refs.lTooltipComponent.parentContainer.mapObject.openTooltip();
                }
                else{
                    this.$refs.lTooltipComponent.parentContainer.mapObject.closeTooltip();
                }
            }
            catch(e){
                console.error(e);
            }
        }
    }
    
}
</script>