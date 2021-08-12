export default {
    getLayers,
    getDiscoveryResults
};

const layers = [
    {name:'1 Piętro', imgurl: require("@/assets/plan1.jpg"), width:10, height:10, nodes:[
        {name:'Lodówka', deviceId:'lodowka', address16:'ABCD', address64:'DEADBEEF12345678', nodeType:'router', discovered:null, x:1, y:1},
        {name:'Żarówka nr 8 w żyrandolu', deviceId:'zar8', address16:'BACA', address64:'0000111122223333', nodeType:'router', discovered:null, x:8, y:4},
    ]},
    {name:'Parter',  imgurl:require("@/assets/plan2.png"), width:7.8, height:5, nodes:[
        {name:'Czujnik dymu', deviceId:'czujnik dymu', address16:'ABCD', address64:'9999000099990000', nodeType:'end', discovered:null, x:1, y:4},
        {name:'Termometr', deviceId:'termo', address16:'ABCD', address64:'BACABECE87654321', nodeType:'end', discovered:null, x:5, y:2},
    ]},
];

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
    return discoveryResults;
}