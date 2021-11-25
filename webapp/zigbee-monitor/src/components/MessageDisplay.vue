<template>
    <div class="message-display-container">
        <div class="message-display-header">
            <h2 class="node-name-header">
                {{node.name}}
            </h2>
            <label class="mode-radio-item">
                Text
                <input type="radio" v-model="displayMode" value="text" name="radioMessageDisplayMode" id="radioModeText">
            </label>
            <label class="mode-radio-item">
                Hex
                <input type="radio" v-model="displayMode" value="hex" name="radioMessageDisplayMode" id="radioModeHex">
            </label>
            <!--
            <div>
                <button type="button" class="button" @click="showMap">Pokaż mapę</button>
            </div>
            -->
        </div>
        <div class="message-display-messages" ref="messagesContainer">
            <zigbee-message v-for="message in messagesToDisplay" :key="message.tempId" :message="message" :mode="displayMode" />
        </div>
        <div class="message-display-footer">
            <div class="writing-mode-container">
                <label class="mode-radio-item">
                    Wyślij wiadomość
                    <input type="radio" v-model="writingMode" value="message" name="radioWritingMode">
                </label>
                <label class="mode-radio-item">
                    Odczytaj parametr
                    <input type="radio" v-model="writingMode" value="getParameter" name="radioWritingMode">
                </label>
                <label class="mode-radio-item">
                    Zapisz parametr
                    <input type="radio" v-model="writingMode" value="setParameter" name="radioWritingMode">
                </label>
                <label class="mode-radio-item">
                    Wykonaj rozkaz
                    <input type="radio" v-model="writingMode" value="executeCommand" name="radioWritingMode">
                </label>
            </div>
            <div v-if="writingMode === 'message'" class="message-display-inputs">
                <label class="mode-radio-item">
                    Text
                    <input type="radio" v-model="messageWriteFormat" value="text" name="radioMessageWriteFormat" id="radioMessageWriteFormatText">
                </label>
                <label class="mode-radio-item">
                    Hex
                    <input type="radio" v-model="messageWriteFormat" value="hex" name="radioMessageWriteFormat" id="radioMessageWriteFormatHex">
                </label>
                <div class="message-input-container">
                    <input type="text" class="text-input message-input" v-model="messageToSend">
                </div>
                <div class="button-send-container">
                    <button type="button" class="button" @click="sendMessage">Wyślij</button>
                </div>
            </div>
            <div v-if="writingMode === 'getParameter' || writingMode === 'setParameter' || writingMode === 'executeCommand'" class="at-command-container">
                <div class="at-command-item">
                    <label for="atCommandName" class="at-data-label">Komenda AT</label>
                    <input type="text" class="text-input at-command-input" v-model="atCommandName" id="atCommandName">
                </div>
                <div class="at-command-item">
                    <div>
                        Typ danych
                    </div>
                    <div class="at-data-mode-container">
                        
                        <label class="mode-radio-item">
                            Brak
                            <input type="radio" v-model="atDataMode" value="none" name="atDataMode">
                        </label>
                        <label class="mode-radio-item">
                            Text
                            <input type="radio" v-model="atDataMode" value="text" name="atDataMode">
                        </label>
                        <label class="mode-radio-item">
                            Hex
                            <input type="radio" v-model="atDataMode" value="hex" name="atDataMode">
                        </label>
                    </div>
                </div>
                <div  class="at-command-item">
                    <label for="atCommandData" class="at-data-label">Dane</label>
                    <input type="text" class="text-input at-data-input" :disabled="atDataMode === 'none'" v-model="atCommandData" id="atCommandData">
                </div>
                <div  class="at-command-item">
                    <button type="button" class="button" @click="sendAtCommand">Wyślij</button>
                </div>
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
            writingMode:'message',
            messageWriteFormat: 'text',
            atDataMode:'none',
            displayMode:'text',
            atCommandName:'',
            atCommandData:'',
            messageToSend:'',
        };
    },
    computed:{
        messagesToDisplay(){
            return this.$store.state.messages.filter(message => message.address64 === this.node.address64);
        },
        messagesToDisplayLength(){
            return this.messagesToDisplay.length;
        }
    },
    methods:{
        async sendMessage(){
            try{
                const encodedMessage = this.getEncodedMessage();
                const message = {
                    type:'sent',
                    address64:this.node.address64,
                    status:'sending',
                    message:encodedMessage
                };
                this.messageToSend = '';
                await this.$store.dispatch('sendMessage', message);
                
            }
            catch(error){
                console.log(error);
            }
        },
        getEncodedMessage(){
            if(this.messageWriteFormat === 'text')
                return this.encodeTextMessage(this.messageToSend);
            else if(this.messageWriteFormat === 'hex')
                return this.encodeHexMessage(this.messageToSend);
        },
        encodeTextMessage(message){
            return btoa(message);
        },
        encodeHexMessage(message){
            const numArray = message.split(/\s+/).map(str => parseInt(str, 16));
            const isValid = numArray.every(n => !isNaN(n) && n >= 0 && n <= 255);
            if(!isValid){
                throw new Error("Invalid hex string");
            }
            const binaryString = numArray.map(n => String.fromCharCode(n)).join('');
            return btoa(binaryString);
        },
        getEncodedCommandValue(){
            if(this.atDataMode === 'text')
                return this.encodeTextMessage(this.atCommandData);
            else if(this.atDataMode === 'hex')
                return this.encodeHexMessage(this.atCommandData);
            else
                return null;
            
        },
        getAtCommandType(){
            if(this.writingMode === 'getParameter')
                return 'get_parameter';
            else if(this.writingMode === 'setParameter')
                return 'set_parameter';
            else if(this.writingMode === 'executeCommand')
                return 'execute_command';
            else
                return '';
        },
        async sendAtCommand(){
            try{
                const commandData = {
                    commandType:this.getAtCommandType(),
                    address64:this.node.address64,
                    atCommand:this.atCommandName,
                    value:this.getEncodedCommandValue(),
                    format:this.atDataMode,
                };
                await this.$store.dispatch('sendAtCommand', commandData);
            }
            catch(error){
                console.error(error);
            }

        },
        showMap(){
            this.$store.commit('setMainDisplayMode', 'map');
        },
        scrollToBottom(){
            const messagesContainer = this.$refs.messagesContainer;
            messagesContainer.scrollTop = messagesContainer.scrollHeight - messagesContainer.clientHeight;
        },
    },
    watch:{
        atDataMode(newMode){
            if(newMode === 'none'){
                this.atCommandData = '';
            }
        },
        messagesToDisplayLength(newLength){
            this.$nextTick(function(){
                this.scrollToBottom();
            });
        },
    },
    mounted(){
        this.scrollToBottom();
    }
};
</script>

<style scoped>

.node-name-header{
    font-size:16px;
    font-weight:600;
    margin:0 auto 0 0;
}

.message-display-container{
    height:100%;
    display: flex;
    flex-direction: column;
}

.message-display-header{
    flex:none;
    box-sizing:border-box;
    display:flex;
    align-items:center;
    justify-content: flex-end;
    padding:4px 12px;
    border-bottom:1px solid #E6E6FA;
}

.message-display-messages{
    flex:auto;
    overflow:auto;
    min-height:0;
    padding:15px;
    border-bottom:1px solid #E6E6FA;
    display:flex;
    flex-direction: column;
    align-items: flex-start;
}

.message-display-footer{
    flex:none;
    box-sizing:border-box;
    padding:8px;
}

.message-display-inputs{
    display:flex;
}

.message-input-container{
    flex:auto;
    display:flex;
    padding-right:5px;
}

.writing-mode-container{
    display:flex;
}

.message-input{
    flex:1;
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

.at-command-container{
    display:flex;
    flex-wrap: wrap;
    margin-top:16px;
}

.at-command-input{
    width:30px;
}

.at-data-label{
    display:block;
}

.at-data-mode-container{
    
    display:flex;
    
}

.at-command-item{
    margin-left:8px;
    margin-right:16px;
}

.at-data-input{
    width:300px;
}
</style>