export default {
    getLayers,
    getDiscoveryResults,
    sendLayer,
    deleteLayer,
    makeMessageSocket
};

import axios from 'axios';

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
    let returnedLayer;
    console.log(layer);
    //Ewentualnie dodać przetwarzanie
    if(typeof layer.id === 'number'){
        returnedLayer = await axios.put(apiurl('/floors/' + layer.id), layer);
    }
    else{
        returnedLayer = await axios.post(apiurl('/floors'), layer);
    }
    if(imageFile){
        let formData = new FormData();
        formData.append('file', imageFile);
        await axios.put(apiurl('/floors/' + layer.id + '/image'), formData, {
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

function apiurl(path){
    return path;
}