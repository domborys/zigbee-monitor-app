<template>
    <section>
        <h2 class="layer-list-header">Piętra</h2>
        <ul class="layer-list">
            <li v-for="layer in layers" :key="layer" @click="layerClick(layer)" :class="{'layer-list-item-selected':layer === selectedLayer}">
                {{ layer }}
            </li>
        </ul>
    </section>
</template>

<script>

export default {
    name:"LayerList",
    props:{
        layers: Array,
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
            this.$emit('input', this.selectedLayer);
        }
    }
}
</script>


<style scoped>
.layer-list-header{
    margin:0;
    font-size:22px;
    font-weight:bold;
}

.layer-list{
    list-style-type: none;
    padding:0;
    margin:0;
    font-size:20px;
}

.layer-list > li{
    padding:5px;
    border-bottom: 1px solid #E6E6FA;
}

.layer-list > li:hover{
    background-color: #E6E6FA;
    cursor: pointer;
}

.layer-list > li.layer-list-item-selected{
    background-color: #630094;
    color:white;
}

</style>