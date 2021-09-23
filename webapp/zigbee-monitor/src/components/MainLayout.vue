<template>
    <div class="main-container">
        <app-header />
        <div v-if="!isOneColumnMode" class="below-header">
            <section class="left-pane">
                <template v-if="mode === 'view'">
                    <layer-list :layers="layerNames" v-model="activeLayerName" />
                    <node-list :nodes="activeLayerNodes" />
                </template>
                <template v-if="mode === 'newLayer' || mode === 'editLayer'">
                    <layer-edit />
                </template>
                <template v-if="mode === 'newNode' || mode === 'editNode'">
                    <node-edit />
                </template>
            </section>
            <main class="main">
                <map-display v-if="mainDisplayMode === 'map'" :layer="activeLayer" />
                <message-display v-if="mainDisplayMode === 'messages'" :node="$store.state.displayedMessagesNode" />
            </main>
        </div>
        <div v-if="isOneColumnMode" class="below-header-one-column">
            <login-form v-if="mode === 'login'" />
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
import MessageDisplay from './MessageDisplay.vue'
import AppHeader from './AppHeader.vue';
import LoginForm from './LoginForm.vue';

export default {
    name:"MainLayout",
    components:{
        LayerList,
        LayerDetails,
        NodeList,
        MapDisplay,
        LayerEdit,
        NodeEdit,
        MessageDisplay,
        AppHeader,
        LoginForm
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
            return this.$store.getters.mode;
        },
        isOneColumnMode(){
            return this.$store.getters.isOneColumnMode;
        },
        mainDisplayMode(){
            return this.$store.state.mainDisplayMode;
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



.below-header{
    display:flex;
    flex:auto;
    min-height:0;
}

.below-header-one-column{
    display:flex;
    justify-content: center;
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