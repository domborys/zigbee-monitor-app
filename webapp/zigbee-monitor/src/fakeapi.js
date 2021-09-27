export default {
    getToken,
    setToken,
    getCurrentUser,
    logout,
    getLayers,
    getDiscoveryResults,
    sendLayer,
    deleteLayer,
    makeMessageSocket
};

import cloneDeep from 'lodash/cloneDeep';

function idGenerator(){
    let id = 1;
    function next(){
        return id++;
    }
    return {next:next};
}

function randomAddress16(){
    return Math.floor(Math.random()*(1<<16)).toString(16);
}

function randomRole(){
    const roles = ['Router', 'End device'];
    const roleIndex = Math.floor(Math.random()*roles.length);
    return roles[roleIndex];
}

function messageGenerator(layers){
    let l = 0;
    let n = -1;
    let messageNo = 1;
    function next(){
        
        n++;
        if(n === layers[l].nodes.length){
            n = 0;
            do{
                l++;
                if(l === layers.length){
                    l = 0;
                }
            } while(layers[l].nodes.length === 0);
        }
        const address64 = layers[l].nodes[n].address64;
        const message = btoa('Message number ' + messageNo++);
        return {type:'received', address64, message};
    }
    function reset(){
        l = 0;
        n = -1;
    }
    return {next, reset};
}

const layerIdGen = idGenerator();
const nodeIdGen = idGenerator();

const layers = [
    {id:layerIdGen.next(),name:'1 Piętro', imgurl: require("@/assets/plan1.jpg"), number:1, width:10, height:10, nodes:[
        {id:nodeIdGen.next(),name:'Lodówka', address64:'DEADBEEF12345678', x:1, y:1},
        {id:nodeIdGen.next(),name:'Żarówka nr 8 w żyrandolu', address64:'0000111122223333', x:8, y:4},
    ]},
    {id:layerIdGen.next(),name:'Parter',  imgurl:require("@/assets/plan2.png"), number:0, width:7.8, height:5, nodes:[
        {id:nodeIdGen.next(),name:'Czujnik dymu', address64:'9999000099990000', x:1, y:4},
        {id:nodeIdGen.next(),name:'Termometr', address64:'BACABECE87654321', x:5, y:2},
    ]},
];

const users = [
    {id:1, username:'jan', password:'jan', role:'user', disabled:false},
    {id:2, username:'anna', password:'anna', role:'admin', disabled:false},
];

let currentToken = null;

const receivedMessagesGenerator = messageGenerator(layers);

async function sleep(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function getToken(credentials){
    await sleep(100);
    const user = users.find(u => u.username === credentials.username && u.password === credentials.password);
    if(typeof user === 'undefined' || user.disabled){
        throw new Error("Incorrect username or password");
    }
    return user.id;
}

function setToken(token){
    currentToken = token;
}

async function getCurrentUser(){
    await sleep(100);
    const user = users.find(u => u.id === currentToken);
    if(typeof user === 'undefined'){
        throw new Error("User not logged in.");
    }
    return user;
}

async function logout(){
    currentToken = null;
}

async function getLayers(){
    await sleep(200);
    let newLayers = cloneDeep(layers);
    processLayersResponse(newLayers);
    return newLayers;
}

async function getDiscoveryResults(){
    await sleep(1000);
    const results = {devices:[]};
    let deviceCounter = 1;
    for(let layer of layers){
        for(let node of layer.nodes){
            if(Math.random() >= 0.5){
                results.devices.push({
                    address64:node.address64,
                    deviceId:`device ${deviceCounter++}`,
                    address16:randomAddress16(),
                    role:randomRole()
                });
            }
        }
    }
    return results;
}

async function sendLayer(layer, imageFile){
    await sleep(300);
    if(typeof layer.id === 'undefined'){
        addNewLayer(layer);
    }
    else{
        modifyLayer(layer);
    }
    layers.sort((a, b) => b.number - a.number);
    receivedMessagesGenerator.reset();
    if(imageFile)
        layer.imgurl = URL.createObjectURL(imageFile);
    return layer;
}

function addNewLayer(layer){
    layer.id = layerIdGen.next();
    layers.push(layer);
}

function modifyLayer(layer){
    const index = layers.findIndex(l => l.id === layer.id);
    layers.splice(index, 1, layer);
}

async function deleteLayer(layer){
    await sleep(300);
    const index = layers.findIndex(l => l.id === layer.id);
    layers.splice(index, 1);
    receivedMessagesGenerator.reset();
}

function makeMessageSocket(){
    const fakeSocket =  {
        send(){

        },

    };
    setInterval(() =>{
        if(typeof fakeSocket.onmessage === 'function'){
            const message = JSON.stringify(receivedMessagesGenerator.next());
            fakeSocket.onmessage({data:message});
        }
    },5000)
    return fakeSocket;
}

function processLayersResponse(layers){
    for(let layer of layers){
        for(let node of layer.nodes){
            node.address16 = null;
            node.deviceId = null;
            node.role = null;
            node.discovered = null;
            node.tempId = null;
        }
    }
}