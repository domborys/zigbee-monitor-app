export default {
    getLayers,
    getDiscoveryResults,
    sendLayer,
    deleteLayer,
    makeMessageSocket
};

function idGenerator(){
    let id = 1;
    function next(){
        return id++;
    }
    return {next:next};
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
    {id:layerIdGen.next(),name:'1 Piętro', imgurl: require("@/assets/plan1.jpg"), floorNo:1, width:10, height:10, nodes:[
        {id:nodeIdGen.next(),name:'Lodówka', deviceId:'lodowka', address16:'ABCD', address64:'DEADBEEF12345678', nodeType:'router', discovered:null, x:1, y:1, tempId:null},
        {id:nodeIdGen.next(),name:'Żarówka nr 8 w żyrandolu', deviceId:'zar8', address16:'BACA', address64:'0000111122223333', nodeType:'router', discovered:null, x:8, y:4, tempId:null},
    ]},
    {id:layerIdGen.next(),name:'Parter',  imgurl:require("@/assets/plan2.png"), floorNo:0, width:7.8, height:5, nodes:[
        {id:nodeIdGen.next(),name:'Czujnik dymu', deviceId:'czujnik dymu', address16:'ABCD', address64:'9999000099990000', nodeType:'end', discovered:null, x:1, y:4, tempId:null},
        {id:nodeIdGen.next(),name:'Termometr', deviceId:'termo', address16:'ABCD', address64:'BACABECE87654321', nodeType:'end', discovered:null, x:5, y:2, tempId:null},
    ]},
];

const receivedMessagesGenerator = messageGenerator(layers);

const discoveryResults = {
    devices:[
        {address64:'DEADBEEF12345678', deviceId:'lodowka'},
        {address64:'BACABECE87654321', deviceId:'termo'}
    ]
};

async function sleep(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function getLayers(){
    await sleep(200);
    return layers;
}

async function getDiscoveryResults(){
    await sleep(1000);
    const results = {devices:[]};
    for(let layer of layers){
        for(let node of layer.nodes){
            if(Math.random() >= 0.5){
                results.devices.push({address64:node.address64});
            }
        }
    }
    //return discoveryResults;
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
    layers.sort((a, b) => b.floorNo - a.floorNo);
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
            const message = receivedMessagesGenerator.next();
            fakeSocket.onmessage(message);
        }
    },5000)
    return fakeSocket;
}