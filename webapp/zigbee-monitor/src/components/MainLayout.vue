<template>
    <div class="main-container">
        <header class="header">
            <h1 class="page-title">Monitor sieci ZigBee</h1>
            <button type="button" @click="editNewLayer">Dodaj piętro</button>
            <button type="button" @click="editActiveLayer">Edytuj piętro</button>
        </header>
        <div class="below-header">
            <section class="left-pane">
                <template v-if="mode === 'view'">
                    <layer-list :layers="layerNames" v-model="activeLayerName" />
                    <layer-details :layer="activeLayer" />
                    <node-list :nodes="activeLayerNodes" />
                </template>
                <template v-if="mode === 'editLayer'">
                    <layer-edit />
                </template>
                <template v-if="mode === 'editNode'">
                    <node-edit />
                </template>
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
import LayerEdit from './LayerEdit.vue';
import NodeEdit from './NodeEdit.vue';

export default {
    name:"MainLayout",
    components:{
        LayerList,
        LayerDetails,
        NodeList,
        MapDisplay,
        LayerEdit,
        NodeEdit
    },
    data(){
        return{
            nodes:[
                {name:'Lodówka', deviceId:'lodowka', address16:'ABCD', address64:'DEADBEEF12345678', nodeType:'router', discovered:true},
                {name:'Żarówka nr 8 w żyrandolu', deviceId:'zar8', address16:'BACA', address64:'0000111122223333', nodeType:'router', discovered:false},
                {name:'Czujnik dymu', deviceId:'czujnik dymu', address16:'ABCD', address64:'DEADBEEF12345678', nodeType:'end', discovered:false},
                {name:'Termometr', deviceId:'termo', address16:'ABCD', address64:'DEADBEEF12345678', nodeType:'end', discovered:true},
            ],
        }
    },
    computed:{
        mode(){
            return this.$store.state.mode;
        },
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
    methods:{
        editNewLayer(){
            this.$store.commit('prepareNewLayer');
            this.$store.commit('setMode', 'editLayer');
        },
        editActiveLayer(){
            this.$store.commit('prepareLayerForEdit', this.$store.getters.activeLayer);
            this.$store.commit('setMode', 'editLayer');
        },
        setMode(mode){
            this.$store.commit('setMode', mode);
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