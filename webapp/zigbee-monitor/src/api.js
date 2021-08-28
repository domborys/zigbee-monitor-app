export default {
    getLayers,
    getDiscoveryResults,
    sendLayer,
    deleteLayer,
    makeMessageSocket
};

import axios from 'axios';

async function getLayers(){
    const response = await axios.get('/floors');
    return response.data;
}

async function getDiscoveryResults(){
    const response = await axios.get('/network-discovery');
    return response.data;
}

async function sendLayer(layer, imageFile){
    let returnedLayer;
    if(typeof layer.id === 'number'){
        returnedLayer = await axios.put('/floors/' + layer.id, layer);
    }
    else{
        returnedLayer = await axios.post('/floors', layer);
    }
    if(imageFile){
        let formData = new FormData();
        formData.append('file', imageFile);
        await axios.put('/floors/' + layer.id + '/image', formData, {
            headers: {'Content-Type': 'multipart/form-data'},
        })
    }

}

async function deleteLayer(layer){
    await axios.delete('/floors/' + layer.id);

}

function makeMessageSocket(){
    const socket = new WebSocket('ws://localhost:8000/message-socket');
    return socket;
}

function processLayersResponse(layers){
    for(let layer of layers){
        layer.imgurl = '/floors/'+layer.id+'/image';
        for(let node of layer.nodes){
            node.address16 = null;
            node.deviceId = null;
            node.role = null;
            node.discovered = null;
            node.tempId = null;
        }
    }
}