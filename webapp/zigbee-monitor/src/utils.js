export default {
    encodeTextMessage,
    encodeHexMessage,
    decodeMessageToText,
    decodeMessageToHex,
    decodeToDecBigEndian,
    isNumeric,
    downloadTextFile,
    formatDate
};

function encodeTextMessage(message){
    return btoa(message);
}

function encodeHexMessage(message){
    const numArray = message.split(/\s+/).map(str => parseInt(str, 16));
    const isValid = numArray.every(n => !isNaN(n) && n >= 0 && n <= 255);
    if(!isValid){
        throw new Error("Invalid hex string");
    }
    const binaryString = numArray.map(n => String.fromCharCode(n)).join('');
    return btoa(binaryString);
}

function decodeMessageToText(base64Message){
    return atob(base64Message);
}

function decodeMessageToHex(base64Message){
    const messageBinary = atob(base64Message);
    return [...messageBinary].map(char => char.charCodeAt(0).toString(16).padStart(2, '0')).join(' ');
}

function decodeToDecBigEndian(base64Message){
    const messageBinary = atob(base64Message);
    return [...messageBinary]
        .map(char => char.charCodeAt(0))
        .reduce((previous, current) => current + (previous << 8));
}

function isNumeric(val){
    const goodType = typeof val === 'string' || typeof val === 'number';
    return goodType && !isNaN(val) && !isNaN(parseFloat(val));
}

function downloadTextFile(text, filename){
    const a = document.createElement('a');
    a.href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(text);
    a.download = filename;
    a.click();
}

function formatDate(date){
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth()+1).toString().padStart(2, '0');
    const year = date.getFullYear().toString();
    const hour = date.getHours().toString().padStart(2, '0');
    const minute = date.getMinutes().toString().padStart(2, '0');
    const second = date.getSeconds().toString().padStart(2, '0');
    return `${day}.${month}.${year} ${hour}:${minute}:${second}`;
}