import Vue from 'vue'
import Vuex from 'vuex'
import api from '../api';
import idGenerator from '../idGenerator';
import cloneDeep from 'lodash/cloneDeep';
import escapeRegExp from 'lodash/escapeRegExp';
import utils from '../utils';
import usersModule from './users';

Vue.use(Vuex)

const tempIdGenerator = idGenerator();
const tempMessageIdGenerator = idGenerator();
const modes = ['view', 'newLayer', 'editLayer', 'newNode', 'editNode', 'selectNode', 'newReadingConfig', 'editReadingConfig', 'login', 'changePassword', 'manageUsers', 'showUser', 'newUser', 'editUser'];
function isValidMode(mode){
    return modes.indexOf(mode) !== -1;
}
function isOneColumnMode(mode){
    const oneColumnModes = ['login', 'changePassword'];
    return oneColumnModes.indexOf(mode) !== -1;
}

const store = new Vuex.Store({
    state: {
        user:null,
        modeStack:['login'],
        mainDisplayMode:'map',
        layers:[],
        editedLayer:null,
        editedLayerImageFile:null,
        editedNode:null,
        editedReadingConfig:null,
        activeLayerName:null,
        discoveryResults:null,
        displayedMessagesNode:null,
        readingTimers:[],
        messages:[
            {type:'sent', address64:'DEADBEEF12345678', message:btoa('ledon'), tempId:tempMessageIdGenerator.next()},
            {type:'received', address64:'DEADBEEF12345678', message:btoa('temp 31'), tempId:tempMessageIdGenerator.next()},
            {type:'received', address64:'DEADBEEF12345678', message:btoa('result 234'), tempId:tempMessageIdGenerator.next()},
            {type:'sent', address64:'DEADBEEF12345678', message:btoa('freeze'), tempId:tempMessageIdGenerator.next()},
        ],
        messageSocket:null,
    },
    getters:{
        mode(state){
            return state.modeStack[state.modeStack.length-1];
        },
        isOneColumnMode(state, getters){
            return isOneColumnMode(getters.mode);
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
        },
        nodeAddressesInSystem(state){
            const addr2node = {};
            for(let layer of state.layers){
                for(let node of layer.nodes){
                    addr2node[node.address64] = true;
                }
            }
            return addr2node;
        },
        discoveredNodesNotInSystem(state, getters){
            if(state.discoveryResults === null)
                return [];
            const addressLookup = getters.nodeAddressesInSystem;
            return state.discoveryResults.devices.filter(node => !addressLookup[node.address64]);
        },
        discoveredNodesInSystem(state, getters){
            if(state.discoveryResults === null)
                return [];
            const addressLookup = getters.nodeAddressesInSystem;
            return state.discoveryResults.devices.filter(node => addressLookup[node.address64]);
        }
    },
    mutations: {
        /*
        setMode(state, mode){
            
            if(modes.indexOf(mode) === -1)
                throw new Error("Invalid mode");
            state.mode = mode;
        },*/
        setUser(state, user){
            state.user = user;
        },
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
            state.editedLayer = {name:null, imgurl:null, number:null, width:null, height:null, nodes:[], isNewImage:false};
        },
        prepareLayerForEdit(state, layer){
            state.editedLayer = cloneDeep(layer);
            state.editedLayer.isNewImage = false;
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
            state.editedNode = {id:null, tempId:null, name:null, address64:null,  x:null, y:null, readingConfigs:[]};
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
        prepareNewReadingConfig(state){
            state.editedReadingConfig = {id:null, tempId:null, name:null, mode:null, messagePrefix:null, messageToSend:null, refreshPeriod:null, atCommand:null, atCommandData:null, atCommandResultFormat:null, lastReading:null};
        },
        prepareReadingConfigForEdit(state, readingConfig){
            state.editedReadingConfig = cloneDeep(readingConfig);
        },
        setEditedReadingConfigParam(state, description){
            state.editedReadingConfig[description.name] = description.value;
        },
        saveEditedReadingConfig(state){
            if(state.editedReadingConfig.id !== null){
                const index = state.editedNode.readingConfigs.findIndex(rc => rc.id === state.editedReadingConfig.id);
                if(index !== -1){
                    state.editedNode.readingConfigs.splice(index, 1, state.editedReadingConfig);
                }
            }
            else if(state.editedReadingConfig.tempId !== null){
                const index = state.editedNode.readingConfigs.findIndex(rc => rc.tempId === state.editedReadingConfig.tempId);
                if(index !== -1){
                    state.editedNode.readingConfigs.splice(index, 1, state.editedReadingConfig);
                }
            }
            else{
                state.editedReadingConfig.tempId = tempIdGenerator.next();
                state.editedNode.readingConfigs.push(state.editedReadingConfig);
            }
            state.editedReadingConfig = null;
        },
        discardEditedReadingConfig(state){
            state.editedReadingConfig = null;
        },
        deleteReadingConfig(state, readingConfig){
            if(readingConfig.id !== null){
                const index = state.editedNode.readingConfigs.findIndex(rc => rc.id === readingConfig.id);
                if(index !== -1){
                    state.editedNode.readingConfigs.splice(index, 1);
                }
            }
            else if(readingConfig.tempId !== null){
                const index = state.editedNode.readingConfigs.findIndex(rc => rc.tempId === readingConfig.tempId);
                if(index !== -1){
                    state.editedNode.readingConfigs.splice(index, 1);
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
        },
        updateLastReadings(state, message){
            let messageText = utils.decodeMessageToText(message.message);
            for(let layer of state.layers){
                for(let node of layer.nodes){
                    if(node.address64 === message.address64){
                        for(let rc of node.readingConfigs){
                            if(rc.mode === 'listen' || rc.mode === 'send'){
                                const prefix = utils.decodeMessageToText(rc.messagePrefix);
                                const regExp = new RegExp('^' + escapeRegExp(prefix) + '\\s*(.*)');
                                const matchResults = messageText.match(regExp);
                                if(matchResults !== null){
                                    const reading = matchResults[1];
                                    rc.lastReading = reading;
                                }
                            }
                        }
                    }
                }
            }
        },
        setLastReading(state, data){
            data.readingConfig.lastReading = data.lastReading;
        },
        addReadingTimer(state, timerId){
            state.readingTimers.push(timerId);
        },
        clearReadingTimers(state){
            state.readingTimers.forEach(clearInterval);
        },
        setMessageSocket(state, socket){
            state.messageSocket = socket;
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
        async loadDataAfterLogin(context, credentials){
            await context.dispatch('getCurrentUser', credentials);
            context.commit('replaceMode', 'view');
            context.dispatch('openMessageSocket');
            await context.dispatch('downloadLayers');
            await context.dispatch('downloadDiscoveryResults');
        },
        async login(context, credentials){
            await api.login(credentials);
        },
        async getCurrentUser(context){
            const user = await api.getCurrentUser();
            context.commit('setUser', user);
        },
        async logout(context){
            context.commit('clearReadingTimers');
            context.commit('setUser', null);
            context.dispatch('closeMessageSocket');
            await api.logout();
        },
        async changePassword(context, passwords){
            await api.changePassword(passwords);
        },
        async downloadLayers(context){
            const layers = await api.getLayers();
            context.commit('setLayers', layers);
            context.commit('clearReadingTimers');
            context.dispatch('setReadingTimers');
        },
        async downloadDiscoveryResults(context){
            const results = await api.getDiscoveryResults();
            context.commit('setDiscoveryResults', results);
            context.commit('writeDiscoveryStatusToNodes');
        },
        async saveEditedLayer(context){
            const layer = context.getters.activeLayer;
            if(layer.isNewImage){
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
            await api.sendMessage(message);
            context.commit('addMessage', message);
        },
        addReceivedMessage(context, message){
            store.commit('addMessage', message);
            store.commit('updateLastReadings', message);
        },
        setReadingTimers(context){
            for(let layer of context.state.layers){
                for(let node of layer.nodes){
                    for(let rc of node.readingConfigs){
                        if(rc.mode === 'send'){
                            const actionData = {node:node, readingConfig:rc};
                            const timerId = setInterval(context.dispatch, rc.refreshPeriod*1000, 'sendMessageForReading', actionData);
                            context.commit('addReadingTimer', timerId);
                            context.dispatch('sendMessageForReading', actionData);
                        }
                        else if(rc.mode === 'at'){
                            const actionData = {node:node, readingConfig:rc};
                            const timerId = setInterval(context.dispatch, rc.refreshPeriod*1000, 'sendAtCommandForReading', actionData);
                            context.commit('addReadingTimer', timerId);
                            context.dispatch('sendAtCommandForReading', actionData);
                        }
                    }
                }
            }
        },
        async sendMessageForReading(context, data){
            const message = {type:'sent', address64:data.node.address64, message:data.readingConfig.messageToSend};
            await context.dispatch('sendMessage', message);

        },
        async sendAtCommandForReading(context, data){
            const commandData = {
                commandType:'get_parameter',
                address64:data.node.address64,
                atCommand:data.readingConfig.atCommand,
                value:data.readingConfig.atCommandData,
                //format:???,
            };
            const message = await context.dispatch('sendAtCommand', commandData);
            let lastReading;
            if(data.readingConfig.atCommandResultFormat === 'hex')
                lastReading = utils.decodeMessageToHex(message.result);
            else if(data.readingConfig.atCommandResultFormat === 'dec')
                lastReading = utils.decodeToDecBigEndian(message.result);
            else
                lastReading = utils.decodeMessageToText(message.result);

            context.commit('setLastReading', {readingConfig:data.readingConfig, lastReading:lastReading});

        },
        async sendAtCommand(context, commandData){
            const message = {
                type:'at',
                result:null,
                ...commandData
            };
            context.commit('addMessage', message);
            const responseData = await api.sendAtCommand(commandData);
            message.result = responseData.result;
            return message;
        },
        openMessageSocket(context){
            const socket = api.makeMessageSocket();
            socket.onmessage = e => store.dispatch('addReceivedMessage', JSON.parse(e.data));
            context.commit('setMessageSocket', socket);
        },
        closeMessageSocket(context){
            if(context.state.messageSocket)
                context.state.messageSocket.close(1000);
            context.commit('setMessageSocket', null);
        }
    },
    modules: {
        users:usersModule,
    }
});

//let socket = api.makeMessageSocket();
//socket.onmessage = e => store.dispatch('addReceivedMessage', JSON.parse(e.data));

export default store;