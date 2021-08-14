import Vue from 'vue'
import Vuex from 'vuex'
import api from '../fakeapi';

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        mode:'view',
        layers:[],
        editedLayer:null,
        editedLayerImageFile:null,
        activeLayerName:null,
        discoveryResults:null,
    },
    getters:{
        activeLayer(state){
            if(state.editedLayer === null){
                const found = state.layers.find(l => l.name === state.activeLayerName);
                return found ? found : null;
            }
            else{
                return state.editedLayer;
            }
        },
        layerNames(state){
            return state.layers.map(l => l.name);
        }
    },
    mutations: {
        setMode(state, mode){
            state.mode = mode;
        },
        setLayers(state, newLayers){
            state.layers = newLayers;
        },
        setDiscoveryResults(state, discoveryResults){
            state.discoveryResults = discoveryResults;
        },
        setActiveLayer(state, layerName){
            state.activeLayerName = layerName;
        },
        setEditedLayer(state, editedLayer){
            state.editedLayer = editedLayer;
        },
        setEditedLayerParam(state, description){
            state.editedLayer[description.name] = description.value;
        },
        setEditedLayerImage(state, imageData){
            state.editedLayerImageFile = imageData.file;
            state.editedLayer.imgurl = imageData.imgurl;
            state.editedLayer.width = imageData.width;
            state.editedLayer.height = imageData.height;
        },
        prepareNewLayer(state){
            state.editedLayer = {name:null, imgurl:null, floorNo:null, width:null, height:null, nodes:[]};
        },
        writeDiscoveryStatusToNodes(state){
            if(state.discoveryResults === null)
                return;
            for(let layer of state.layers){
                for(let node of layer.nodes){
                    node.discovered = state.discoveryResults.devices.some(dev => dev.address64 === node.address64);
                }
            }
        }
    },
    actions: {
        loadLayerImage(context, imageFile){
            const imgurl = URL.createObjectURL(imageFile);
            const image = new Image();
            image.src = imgurl;
            image.onload = () => {
                if(context.state.editedLayer.imgurl)
                    URL.revokeObjectURL(context.state.editedLayer.imgurl);
                const imageData = {file:imageFile, imgurl:imgurl, width:image.width, height:image.height};
                context.commit('setEditedLayerImage', imageData);
            }
            image.onerror = (error) => console.log(error);
            
        },
        async downloadLayers(context){
            const layers = await api.getLayers();
            context.commit('setLayers', layers);
        },
        async downloadDiscoveryResults(context){
            const results = await api.getDiscoveryResults();
            context.commit('setDiscoveryResults', results);
            context.commit('writeDiscoveryStatusToNodes');
        },
        async saveEditedLayer(context){
            const layer = context.getters.activeLayer;
            await api.sendLayer(layer, context.state.editedLayerImageFile);
            await context.dispatch('downloadLayers');
        }
    },
    modules: {
    }
})
