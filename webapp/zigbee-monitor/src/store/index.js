import Vue from 'vue'
import Vuex from 'vuex'
import api from '../fakeapi';
import idGenerator from '../idGenerator';
import cloneDeep from 'lodash/cloneDeep';

Vue.use(Vuex)

const tempIdGenerator = idGenerator();

export default new Vuex.Store({
    state: {
        mode:'view',
        layers:[],
        editedLayer:null,
        editedLayerImageFile:null,
        editedNode:null,
        //editedNodeCopy:null,
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
        prepareLayerForEdit(state, layer){
            state.editedLayer = cloneDeep(layer);
        },
        /*
        prepareNewNode(state){
            state.editedNodeCopy = null;
            const newNode = {id:null, name:null, address64:null,  x:null, y:null, edited:true};
            state.editedLayer.nodes.push(newNode);
        },
        prepareNodeForEdit(state, node){
            state.editedNodeCopy = cloneDeep(node);
            node.edited = true;
            state.editedLayer.nodes.push(newNode);
        },*/
        
        prepareNewNode(state){
            state.editedNode = {id:null, tempId:null, name:null, address64:null,  x:null, y:null};
        },
        prepareNodeForEdit(state, node){
            state.editedNode = cloneDeep(node);
        },
        setEditedNodeParam(state, description){
            state.editedNode[description.name] = description.value;
        },
        setCoordinatesOfEditedNode(state, coordinates){
            state.editedNode.x = coordinates.x;
            state.editedNode.y = coordinates.y;
        },
        saveEditedNode(state){
            if(state.editedNode.id !== null){
                const index = state.editedLayer.nodes.findIndex(n => n.id === state.editedNode.id);
                if(index !== -1){
                    state.editedLayer.nodes.splice(index, 1, state.editedNode);
                }
            }
            else if(state.editedNode.tempId !== null){
                const index = state.editedLayer.nodes.findIndex(n => n.tempId === state.editedNode.tempId);
                if(index !== -1){
                    state.editedLayer.nodes.splice(index, 1, state.editedNode);
                }
            }
            else{
                state.editedNode.tempId = tempIdGenerator.next();
                state.editedLayer.nodes.push(state.editedNode);
            }
            state.editedNode = null;
        },
        discardEditedNode(state){
            state.editedNode = null;
        },
        deleteNode(state, node){
            if(node.id !== null){
                const index = state.editedLayer.nodes.findIndex(n => n.id === node.id);
                if(index !== -1){
                    state.editedLayer.nodes.splice(index, 1);
                }
            }
            else if(node.tempId !== null){
                const index = state.editedLayer.nodes.findIndex(n => n.tempId === node.tempId);
                if(index !== -1){
                    state.editedLayer.nodes.splice(index, 1);
                }
            }
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
        async saveEditedLayer(context, config){
            const layer = context.getters.activeLayer;
            if(config.isNewImage){
                await api.sendLayer(layer, context.state.editedLayerImageFile);
            }
            else{
                await api.sendLayer(layer);
            }
            await context.dispatch('downloadLayers');
        }
    },
    modules: {
    }
})
