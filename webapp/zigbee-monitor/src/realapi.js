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
    changePassword,
    sendAtCommand,

    getUsers,
    addUser,
    modifyUser,
    deleteUser
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

async function changePassword(passwords){
    const request = preparePasswordChangeRequest(passwords);
    console.log(request);
    const response = await axios.post(apiurl('/password-change'), request);
    console.log(response);
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
    console.log('layer sent', layerToSend);
    //Ewentualnie dodać przetwarzanie
    if(typeof layer.id === 'number'){
        const response = await axios.put(apiurl('/floors/' + layer.id), layerToSend);
        returnedLayer = response.data;
    }
    else{
        const response = await axios.post(apiurl('/floors'), layerToSend);
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
    console.log('layer returned', returnedLayer);
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

async function getUsers(){
    const response = await axios.get(apiurl('/users'));
    console.log(response);
    return response.data;
}

async function addUser(user){
    const response = await axios.post(apiurl('/users'), user);
    const returnedUser = response.data;
    return returnedUser;
}

async function modifyUser(user){
    const response = await axios.put(apiurl('/users/' + user.id), user);
    const returnedUser = response.data;
    return returnedUser;
}

async function deleteUser(user){
    await axios.delete(apiurl('/users/' + user.id));
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
            const convertedRcs = node.reading_configs.map(processReadingConfig);
            node.readingConfigs = convertedRcs;
        }
    }
}

function prepareLayerToSend(layer){
    const nodes = layer.nodes.map(prepareNodeToSend);
    const layerToSend = {
        name: layer.name,
        number: layer.number,
        width:layer.width,
        height:layer.height,
        nodes:nodes
    };
    return layerToSend;
}

function prepareNodeToSend(node){
    return {
        id:node.id,
        name:node.name,
        address64:node.address64,
        x:node.x,
        y:node.y,
        reading_configs:node.readingConfigs.map(prepareReadingConfigToSend)
    };
}

function prepareReadingConfigToSend(rc){
    return {
        id: rc.id,
        name: rc.name,
        mode: rc.mode,
        refresh_period: rc.refreshPeriod,
        message_prefix: rc.messagePrefix,
        message_to_send: rc.messageToSend,
        at_command: rc.atCommand,
        at_command_data: rc.atCommandData,
        at_command_result_format: rc.atCommandResultFormat,
    };
}

function processReadingConfig(rc){
    return {
        id: rc.id,
        tempId:null,
        name: rc.name,
        mode: rc.mode,
        refreshPeriod: rc.refresh_period,
        messagePrefix: rc.message_prefix,
        messageToSend: rc.message_to_send,
        atCommand: rc.at_command,
        atCommandData: rc.at_command_data,
        atCommandResultFormat: rc.at_command_result_format
    };
}

function prepareAtCommandToSend(commandData){
    return{
        address64:commandData.address64,
        command_type:commandData.commandType,
        at_command:commandData.atCommand,
        value:commandData.value,
    };
}

function preparePasswordChangeRequest(passwords){
    return {
        old_password: passwords.oldPassword,
        new_password: passwords.newPassword
    };
}


function apiurl(path){
    return 'http://localhost:8000' + path;
}