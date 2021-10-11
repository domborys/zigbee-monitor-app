<template>
    <article class="zigbee-message" :class="boundClasses">
        <div v-if="showNodeInfo" class="zigbee-message-header">
            <b>{{ message.nodeName }}</b>
            {{ message.address64 }}
        </div>
        <div v-if="message.type === 'sent' || message.type === 'received'" class="zigbee-message-content">
            <template v-if="mode === 'text'">
                {{ messageAsText }}
            </template>
            <template v-if="mode === 'hex'">
                {{ messageAsHex }}
            </template>
        </div>
        <div v-if="message.type === 'at'" class="zigbee-message-content">
            <b>Komenda AT</b>: {{ message.atCommand }}<br>
            <template v-if="message.value !== null">
                <b>Dane:</b> {{ atCommandData }}<br>
            </template>
            <template v-if="message.result !== null">
                <b>Wynik:</b> {{ atCommandResult }}
            </template>
        </div>
    </article>
</template>

<script>

export default {
    name:"ZigbeeMessage",
    props:{
        message: Object,
        mode: {
            type: String,
            default: 'text',
            validator(value){
                return ['text', 'hex'].indexOf(value) !== -1;
            }
        },
        showNodeInfo:{
            type: Boolean,
            default: false
        }
    },
    data(){
        return{
            
        }
    },
    computed:{
        boundClasses(){
            return {
                'zigbee-message-left':this.message.type === 'received',
                'zigbee-message-right':this.message.type === 'sent' || this.message.type === 'at'
            };
        },
        messageAsText(){
            return this.decodeTextMessage(this.message.message);
        },
        messageAsHex(){
            return this.decodeHexMessage(this.message.message);
        },
        atCommandData(){
            if(this.message.format === 'text'){
                return this.decodeTextMessage(this.message.value);
            }
            else if(this.message.format === 'hex'){
                return this.decodeHexMessage(this.message.value);
            }
            else{
                return '';
            }
        },
        atCommandResult(){
            if(!this.message.result)
                return '';
            const messageHex = this.decodeHexMessage(this.message.result);
            const messageText = this.decodeTextMessage(this.message.result);
            return `${messageHex} (${messageText})`;
        }
        
    },
    methods:{
        decodeTextMessage(message){
            return atob(message);
        },
        decodeHexMessage(message){
            const messageBinary = atob(message);
            return [...messageBinary].map(char => char.charCodeAt(0).toString(16).padStart(2, '0')).join(' ');
        }
    }
}
</script>


<style scoped>

.zigbee-message{
    margin: 8px 0;
    border: 2px solid rgb(130,68,190);
    border-radius: 5px;
}

.zigbee-message-left{
    /*margin-right:20%;*/
    
    text-align:left;
}

.zigbee-message-right{
    /*margin-left:20%;*/
    align-self: flex-end;
    /*text-align:right;*/
}

.zigbee-message-header{
    border-bottom: 1px solid #E6E6FA;
    padding:5px;
}

.zigbee-message-content{
    padding:5px;
}



</style>