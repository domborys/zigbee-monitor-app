export default {
    encodeTextMessage,
    encodeHexMessage,
    decodeMessageToText,
    decodeMessageToHex,
    decodeToDecBigEndian
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