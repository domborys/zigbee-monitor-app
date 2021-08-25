<template>
    <div class="message-display-container">
        <div class="message-display-header">
            <label class="mode-radio-item">
                Text
                <input type="radio" v-model="displayMode" value="text" name="radioMessageDisplayMode" id="radioModeText">
            </label>
            <label class="mode-radio-item">
                Hex
                <input type="radio" v-model="displayMode" value="hex" name="radioMessageDisplayMode" id="radioModeHex">
            </label>
            <div>
                <button type="button" class="button" @click="showMap">Pokaż mapę</button>
            </div>
        </div>
        <div class="message-display-messages">
            <zigbee-message v-for="message in messagesToDisplay" :key="message.tempId" :message="message" :mode="displayMode" />
        </div>
        <div class="message-display-inputs">
            <div class="message-input-container">
                <input type="text" class="text-input full-width-input" v-model="messageToSend">
            </div>
            <div>
                <button type="button" class="button" @click="sendMessage">Wyślij</button>
            </div>
        </div>
    </div>
</template>

<script>

import ZigbeeMessage from './ZigbeeMessage.vue';

export default {
    name:"MessageDisplay",
    components: {
        ZigbeeMessage
    },
    props:{
        node:Object
    },
    data() {
        return {
            displayMode:'text',
            messageToSend:'',
        };
    },
    computed:{
        messagesToDisplay(){
            return this.$store.state.messages.filter(message => message.address64 === this.node.address64);
        }
    },
    methods:{
        sendMessage(){
            try{
                const encodedMessage = this.getEncodedMessage();
                const message = {
                    type:'sent',
                    address64:this.node.address64,
                    message:encodedMessage
                };
                this.$store.dispatch('sendMessage', message);
                this.messageToSend = '';
            }
            catch(error){
                console.log(error);
            }
        },
        getEncodedMessage(){
            if(this.displayMode === 'text')
                return this.encodeTextMessage();
            else if(this.displayMode === 'hex')
                return this.encodeHexMessage();
        },
        encodeTextMessage(){
            return btoa(this.messageToSend);
        },
        encodeHexMessage(){
            const numArray = this.messageToSend.split(/\s+/).map(str => parseInt(str, 16));
            const isValid = numArray.every(n => !isNaN(n) && n >= 0 && n <= 255);
            if(!isValid){
                throw new Error("Invalid hex string");
            }
            const binaryString = numArray.map(n => String.fromCharCode(n)).join('');
            return btoa(binaryString);
        },
        showMap(){
            this.$store.commit('setMainDisplayMode', 'map');
        }
    },
};
</script>

<style scoped>

.message-display-container{
    height:100%;
    display: flex;
    flex-direction: column;
}

.message-display-header{
    flex:none;
    box-sizing:border-box;
    display:flex;
    justify-content: flex-end;
    padding:8px;
}

.message-display-messages{
    flex:auto;
    overflow:auto;
    min-height:0;
    padding:15px;
    border-bottom:1px solid #E6E6FA;
}

.message-display-inputs{
    flex:none;
    box-sizing:border-box;
    display:flex;
    padding:8px;
}

.message-input-container{
    flex:auto;
}

.mode-radio-item{
    display: block;
    padding:8px;
    margin:0 2px;
    border-radius:2px;
    font-weight: 600;
}

.mode-radio-item:hover{
    background-color: #E6E6FA;
    cursor: pointer;
}
</style>