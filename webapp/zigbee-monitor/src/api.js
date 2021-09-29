export default {
    getLayers,
    getDiscoveryResults,
    sendLayer,
    deleteLayer,
    makeMessageSocket,
    getToken,
    setToken,
    getCurrentUser,
    logout,
    sendAtCommand,
};

import axios from 'axios';

let currentToken = null;

async function getToken(credentials){
    let formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    const response = await axios.post(apiurl('/token'), formData, {
        headers: {'Content-Type': 'multipart/form-data'},
    });
    const token = response.data.access_token;
    console.log(token);
    if(typeof token !== 'string'){
        throw new Error("Invalid token.");
    }
    return token;
}

function setToken(token){
    currentToken = token;
    axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;
}

async function getCurrentUser(){
    const response = await axios.get(apiurl('/users/me'));
    console.log(response.data);
    return response.data;
}

async function logout(){
    currentToken = null;
    delete axios.defaults.headers.common['Authorization'];
}

async function getLayers(){
    const response = await axios.get(apiurl('/floors'));
    let layers = response.data;
    processLayersResponse(layers);
    console.log(layers);
    return layers;
}

async function getDiscoveryResults(){
    const response = await axios.get(apiurl('/network-discovery'));
    console.log(response.data);
    return response.data;
}

async function sendLayer(layer, imageFile){
    const layerToSend = prepareLayerToSend(layer);
    let returnedLayer;
    console.log(layerToSend);
    //Ewentualnie dodać przetwarzanie
    if(typeof layer.id === 'number'){
        const response = await axios.put(apiurl('/floors/' + layer.id), layer);
        returnedLayer = response.data;
    }
    else{
        const response = await axios.post(apiurl('/floors'), layer);
        returnedLayer = response.data;
    }
    if(imageFile){
        let formData = new FormData();
        formData.append('file', imageFile);
        console.log('sending image file');
        await axios.put(apiurl('/floors/' + returnedLayer.id + '/image'), formData, {
            headers: {'Content-Type': 'multipart/form-data'},
        })
    }
    return returnedLayer;
}

async function deleteLayer(layer){
    await axios.delete(apiurl('/floors/' + layer.id));

}

function makeMessageSocket(){
    const socket = new WebSocket('ws://localhost:8000/message-socket');
    return socket;
}

async function sendAtCommand(commandData){
    const commandToSend = prepareAtCommandToSend(commandData);
    const response = await axios.post(apiurl('/xbee-at-command'), commandToSend);
    console.log(response);
    return response.data;
}

function processLayersResponse(layers){
    for(let layer of layers){
        layer.imgurl = apiurl('/floors/'+layer.id+'/image');
        for(let node of layer.nodes){
            node.address16 = null;
            node.deviceId = null;
            node.role = null;
            node.discovered = null;
            node.tempId = null;
        }
    }
}

function prepareLayerToSend(layer){
    const nodes = layer.nodes.map(node => ({
        id:node.id, name:node.name, address64:node.address64, x:node.x, y:node.y
    }));
    const layerToSend = {
        name: layer.name,
        number: layer.number,
        width:layer.width,
        height:layer.height,
        nodes:nodes
    };
    return layerToSend;
}

function prepareAtCommandToSend(commandData){
    return{
        address64:commandData.address64,
        command_type:commandData.commandType,
        at_command:commandData.atCommand,
        value:commandData.value,
    }
}

function apiurl(path){
    return 'http://localhost:8000' + path;
}