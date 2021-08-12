import Vue from 'vue'
import Vuex from 'vuex'
import api from '../fakeapi';

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        layers:[],
        activeLayerName:null,
        discoveryResults:null,
    },
    getters:{
        activeLayer(state){
            const found = state.layers.find(l => l.name === state.activeLayerName);
            return found ? found : null;
        },
        layerNames(state){
            return state.layers.map(l => l.name);
        }
    },
    mutations: {
        setLayers(state, newLayers){
            state.layers = newLayers;
        },
        setDiscoveryResults(state, discoveryResults){
            state.discoveryResults = discoveryResults;
        },
        setActiveLayer(state, layerName){
            state.activeLayerName = layerName;
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
        async downloadLayers(context){
            const layers = await api.getLayers();
            context.commit('setLayers', layers);
        },
        async downloadDiscoveryResults(context){
            const results = await api.getDiscoveryResults();
            context.commit('setDiscoveryResults', results);
            context.commit('writeDiscoveryStatusToNodes');
        }
    },
    modules: {
    }
})
