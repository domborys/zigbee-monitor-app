<template>
    <div class="main-container">
        <header class="header">
            <h1 class="page-title">Monitor sieci ZigBee</h1>
        </header>
        <div class="below-header">
            <section class="left-pane">
                <layer-list :layers="layerNames" v-model="activeLayerName" />
                <layer-details :layer="activeLayer" />
                <node-list :nodes="activeLayerNodes" />
            </section>
            <main class="main">
                <map-display :layer="activeLayer" />
            </main>
        </div>
    </div>
</template>
<script>
import LayerList from './LayerList.vue';
import LayerDetails from './LayerDetails.vue';
import NodeList from './NodeList.vue';
import MapDisplay from './MapDisplay.vue';

export default {
    name:"MainLayout",
    components:{
        LayerList,
        LayerDetails,
        NodeList,
        MapDisplay
    },
    data(){
        return{
            nodes:[
                {name:'Lodówka', deviceId:'lodowka', address16:'ABCD', address64:'DEADBEEF12345678', nodeType:'router', discovered:true},
                {name:'Żarówka nr 8 w żyrandolu', deviceId:'zar8', address16:'BACA', address64:'0000111122223333', nodeType:'router', discovered:false},
                {name:'Czujnik dymu', deviceId:'czujnik dymu', address16:'ABCD', address64:'DEADBEEF12345678', nodeType:'end', discovered:false},
                {name:'Termometr', deviceId:'termo', address16:'ABCD', address64:'DEADBEEF12345678', nodeType:'end', discovered:true},
            ],
            /*
            layers:[
                {name:'Parter', imgurl: require("@/assets/plan1.jpg"), width:10, height:10, active:false, nodes:[
                    {name:'Lodówka', deviceId:'lodowka', address16:'ABCD', address64:'DEADBEEF12345678', nodeType:'router', discovered:true, x:1, y:1},
                    {name:'Żarówka nr 8 w żyrandolu', deviceId:'zar8', address16:'BACA', address64:'0000111122223333', nodeType:'router', discovered:false, x:8, y:4},
                ]},
                {name:'Parter',  imgurl:require("@/assets/plan2.png"), width:7.8, height:5, active:true, nodes:[
                    {name:'Czujnik dymu', deviceId:'czujnik dymu', address16:'ABCD', address64:'DEADBEEF12345678', nodeType:'end', discovered:false, x:1, y:4},
                    {name:'Termometr', deviceId:'termo', address16:'ABCD', address64:'DEADBEEF12345678', nodeType:'end', discovered:true, x:5, y:2},
                ]},
            ]*/
        }
    },
    computed:{
        layers(){
            return this.$store.state.layers;
        },
        activeLayer(){
            return this.$store.getters.activeLayer;
        },
        activeLayerNodes(){
            if (this.activeLayer === null)
                return [];
            else
                return this.activeLayer.nodes;

        },
        activeLayerName:{
            get(){
                return this.$store.state.activeLayerName;
            },
            set(value){
                this.$store.commit('setActiveLayer', value);
            }
        },
        layerNames(){
            return this.$store.getters.layerNames;
        }
    },
    mounted(){
        this.$store.dispatch('downloadLayers')
            .then(() => this.$store.dispatch('downloadDiscoveryResults'))
    }
}
</script>

<style scoped>
.main-container{
    height:100%;
    display:flex;
    flex-direction: column;
}

.header{
    flex:none;
    border-bottom:1px solid #E6E6FA;
    box-sizing:border-box;
}

.page-title{
    font-size:25px;
    font-weight:normal;
    margin: 10px;
}

.below-header{
    display:flex;
    flex:auto;
    min-height:0;
}

.left-pane{
    flex:0 300px;
    border-right:1px solid #E6E6FA;
    overflow:auto;
    padding: 10px;
    
}

.main{
    flex:auto;
}
</style>