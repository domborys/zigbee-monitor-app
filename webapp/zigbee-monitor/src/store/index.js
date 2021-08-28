import Vue from 'vue'
import Vuex from 'vuex'
import api from '../fakeapi';
import idGenerator from '../idGenerator';
import cloneDeep from 'lodash/cloneDeep';

Vue.use(Vuex)

const tempIdGenerator = idGenerator();
const tempMessageIdGenerator = idGenerator();
const modes = ['view', 'newLayer', 'editLayer', 'newNode', 'editNode'];
function isValidMode(mode){
    return modes.indexOf(mode) !== -1;
}

const store = new Vuex.Store({
    state: {
        //mode:'view',
        modeStack:['view'],
        mainDisplayMode:'map',
        layers:[],
        editedLayer:null,
        editedLayerImageFile:null,
        editedNode:null,
        //editedNodeCopy:null,
        activeLayerName:null,
        discoveryResults:null,
        displayedMessagesNode:null,
        messages:[
            {type:'sent', address64:'DEADBEEF12345678', message:btoa('ledon'), tempId:tempMessageIdGenerator.next()},
            {type:'received', address64:'DEADBEEF12345678', message:btoa('temp 31'), tempId:tempMessageIdGenerator.next()},
            {type:'received', address64:'DEADBEEF12345678', message:btoa('result 234'), tempId:tempMessageIdGenerator.next()},
            {type:'sent', address64:'DEADBEEF12345678', message:btoa('freeze'), tempId:tempMessageIdGenerator.next()},
        ],
    },
    getters:{
        mode(state){
            return state.modeStack[state.modeStack.length-1];
        },
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
        /*
        setMode(state, mode){
            
            if(modes.indexOf(mode) === -1)
                throw new Error("Invalid mode");
            state.mode = mode;
        },*/
        pushMode(state, mode){
            if(!isValidMode(mode))
                throw new Error("Invalid mode");
            state.modeStack.push(mode);
        },
        replaceMode(state, mode){
            if(!isValidMode(mode))
                throw new Error("Invalid mode");
            if(state.modeStack.length > 0)
                state.modeStack.pop();
            state.modeStack.push(mode);
        },
        previousMode(state){
            if(state.modeStack.length > 1)
                state.modeStack.pop();
        },

        setMainDisplayMode(state, mode){
            state.mainDisplayMode = mode;
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
                    const result = state.discoveryResults.devices.find(dev => dev.address64 === node.address64);
                    if(typeof result === 'undefined'){
                        node.discovered = false;
                        node.address16 = null;
                        node.role = null;
                        node.deviceId = null;
                    }
                    else{
                        node.discovered = true;
                        node.address16 = result.address16;
                        node.role = result.role;
                        node.deviceId = result.deviceId;
                    }
                    
                }
            }
        },
        addMessage(state, message){
            message.tempId = tempMessageIdGenerator.next();
            state.messages.push(message);
        },
        setDisplayedMessagesNode(state, node){
            state.displayedMessagesNode = node;
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
        },
        async deleteLayer(context, layer){
            await api.deleteLayer(layer);
            await context.dispatch('downloadLayers');
        },
        async sendMessage(context, message){
            context.commit('addMessage', message)
        }
    },
    modules: {
    }
});

const socket = api.makeMessageSocket();
socket.onmessage = message => store.commit('addMessage', message);

export default store;