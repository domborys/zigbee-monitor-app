<template>
    <section>
        <h2 class="layer-list-header">Mapy</h2>
        <ul v-if="layers.length > 0" class="layer-list">
            <li v-for="layer in layers" :key="layer" @click="layerClick(layer)" :class="{'layer-list-item-selected':layer === selectedLayer}">
                {{ layer }}
            </li>
        </ul>
        <div v-else>
            W systemie nie znajdują się żadne mapy.
        </div>
    </section>
</template>

<script>

/**
 * A component which displays a list of maps which are present in the system.
 */
export default {
    name:"LayerList",
    props:{
        /**
         * The maps to display.
         */
        layers: {type:Array, default:[]},

        /**
         * Currently selected map.
         * @model
         */
        value: { type:String, default: ''}
    },
    data(){
        return{
            selectedLayer: this.value
        }
    },
    methods:{
        layerClick(layer){
            this.selectedLayer = layer;
            /**
             * Event emitted when a layer is clicked.
             */
            this.$emit('input', this.selectedLayer);
        }
    }
}
</script>


<style scoped>
.layer-list-header{
    margin:5px 0 15px 0;
    font-size:22px;
    font-weight:600;
}

.layer-list{
    list-style-type: none;
    padding:0;
    margin:0;
    font-size:18px;
}

.layer-list > li{
    padding:10px;
    border-bottom: 1px solid #E6E6FA;
    border-left: 1px solid #E6E6FA;
    border-right: 1px solid #E6E6FA;
}

.layer-list > li:first-child{
    border-top: 1px solid #E6E6FA;
}

.layer-list > li:hover{
    background-color: #E6E6FA;
    cursor: pointer;
}

.layer-list > li.layer-list-item-selected{
    background-color: rgb(130,68,190);
    border-color:rgb(130,68,190);
    color:white;
}

</style>