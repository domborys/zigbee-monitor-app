export default {
    getToken,
    setToken,
    getCurrentUser,
    logout,
    changePassword,
    getLayers,
    getDiscoveryResults,
    sendLayer,
    deleteLayer,
    makeMessageSocket,
    sendAtCommand,

    getUsers,
    addUser,
    modifyUser,
    deleteUser
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
const userIdGen = idGenerator();

const layers = [
    {id:layerIdGen.next(),name:'1 Piętro', imgurl: require("@/assets/plan1.jpg"), number:1, width:10, height:10, nodes:[
        {id:nodeIdGen.next(),name:'Lodówka', address64:'DEADBEEF12345678', x:1, y:1, readingConfigs:[]},
        {id:nodeIdGen.next(),name:'Żarówka nr 8 w żyrandolu', address64:'0000111122223333', x:8, y:4, readingConfigs:[]},
    ]},
    {id:layerIdGen.next(),name:'Parter',  imgurl:require("@/assets/plan2.png"), number:0, width:7.8, height:5, nodes:[
        {id:nodeIdGen.next(),name:'Czujnik dymu', address64:'9999000099990000', x:1, y:4, readingConfigs:[]},
        {id:nodeIdGen.next(),name:'Termometr', address64:'BACABECE87654321', x:5, y:2, readingConfigs:[
            {name:'Temperatura', mode:'listen', messagePrefix:btoa('temp'), messageToSend:null, refreshPeriod:null, atCommand:null, atCommandData:null},
            {name:'Ciśnienie', mode:'send', messagePrefix:btoa('press'), messageToSend:btoa('getpress'), refreshPeriod:10, atCommand:null, atCommandData:null},
            {name:'Wilgotność', mode:'at', messagePrefix:null, messageToSend:null, refreshPeriod:5, atCommand:'HU', atCommandData:null}
        ]},
    ]},
];

const users = [
    {id:userIdGen.next(), username:'jan', password:'jan', role:'user', disabled:false},
    {id:userIdGen.next(), username:'anna', password:'anna', role:'admin', disabled:false},
    {id:userIdGen.next(), username:'łobuz', password:'aaa', role:'user', disabled:true},
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

async function changePassword(passwords){
    const user = await getCurrentUser();
    if(user.password !== passwords.oldPassword){
        throw new Error("Bad password");
    }
    user.password = passwords.newPassword;
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

async function sendAtCommand(commandData){
    await sleep(150);
    const responseData = {result:null};
    if(commandData.atCommand === 'NI' && commandData.commandType === 'get_parameter'){
        responseData.result = btoa('fajne urzadzenie');
    }
    else if(commandData.atCommand === 'ER'){
        responseData.error = 'Wystąpił poważny błąd';
    }
    else if(commandData.commandType === 'get_parameter'){
        responseData.result = btoa('ABCD');
    }

    return responseData;

}

async function getUsers(){
    await sleep(200);
    const returnedUsers = cloneDeep(users);
    delete returnedUsers.password;
    console.log(returnedUsers);
    return returnedUsers;
}

async function addUser(user){
    await sleep(150);
    const apiUser = {...user};
    apiUser.id = userIdGen.next();
    users.push(apiUser);
    const returnedUser = {...apiUser};
    delete returnedUser.password;
    return returnedUser;
}

async function modifyUser(user){
    await sleep(250);
    const apiUser = {...user};
    const index = users.findIndex(u => u.id === apiUser.id);
    if(apiUser.password === null){
        apiUser.password = users[index].password;
    }
    users.splice(index, 1, apiUser);
    const returnedUser = {...apiUser};
    delete returnedUser.password;
    return returnedUser;
}

async function deleteUser(user){
    await sleep(250);
    const index = users.findIndex(u => u.id === user.id);
    users.splice(index, 1);
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