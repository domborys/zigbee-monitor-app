<template>
    <div class="zigbee-message" :class="boundClasses">
        <div class="zigbee-message-top-row">
            <div class="message-field-time">
                {{messageTimeFormatted}}
            </div>
            <div class="message-field-status" :class="statusFieldClasses">
                {{messageStatus}}
            </div>
        </div>
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
        <div v-if="isError && message.error !== null" class="zigbee-message-error-row">
            {{ message.error }}
        </div>
    </div>
</template>

<script>
import utils from '../utils';

/**
 * Component used for displaying one ZigBee message.
 */
export default {
    name:"ZigbeeMessage",
    props:{
        /**
         * The message to display.
         */
        message: Object,

        /**
         * The mode in which the message will be displayed.
         * @values text, hex
         */
        mode: {
            type: String,
            default: 'text',
            validator(value){
                return ['text', 'hex'].indexOf(value) !== -1;
            }
        },

        /**
         * If true, the name and 64-bit address of the node will be shown.
         */
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
                'zigbee-message-right':this.message.type === 'sent' || this.message.type === 'at',
                'zigbee-message-success': this.message.status === 'acknowledged',
                'zigbee-message-error': this.isError,
                'zigbee-message-neutral': this.message.type === 'received',
            };
        },
        statusFieldClasses(){
            return {
                'status-success': this.message.status === 'acknowledged',
                'status-error': this.isError,
                'status-neutral': this.message.type === 'received',
            };
        },
        messageAsText(){
            return this.decodeTextMessage(this.message.message);
        },
        messageAsHex(){
            return this.decodeHexMessage(this.message.message);
        },
        isError(){
            return this.message.status === 'serverError' || this.message.status === 'sendingError';
        },
        messageError(){
            return this.message.error;
        },
        messageTimeFormatted(){
            const date = new Date(this.message.timestamp);
            return utils.formatDate(date);
        },
        messageStatus(){
            const message = this.message;
            if(message.type === 'received'){
                return 'Odebrano';
            }
            if(message.type === 'sent' || message.type === 'at'){
                if(message.status === 'sending')
                    return 'Wysyłam...';
                else if(message.status === 'serverError' || message.status === 'sendingError')
                    return 'Błąd';
                else if(message.status === 'acknowledged')
                    return 'Potwierdzono';
            }
            return '';
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
    },
    watch:{
        atCommandResult(){
            /**
             * Emitted when the size of the message container may have changed.
             */
            this.$emit('size-change');
        },
        messageError(){
            this.$emit('size-change');
        }
    }
}
</script>

<style scoped>

.zigbee-message{
    margin: 8px 0;
    padding:4px;
    border: 1px solid #888;
    border-radius: 5px;
}

.zigbee-message-left{
    text-align:left;
}

.zigbee-message-right{
    align-self: flex-end;
}

.message-field-time{
    color:#666666;
    margin-right:20px;
}

.message-field-status{
    color:#666666;
}

.status-success{
    color: rgb(90, 146, 0);
}

.status-error{
    color: rgb(190, 39, 2);
}

.status-neutral{
    color: rgb(130,68,190);
}

.zigbee-message-success{
    border-color: rgb(90, 146, 0);
}

.zigbee-message-error{
    border-color: rgb(190, 39, 2);
}

.zigbee-message-neutral{
    border-color: rgb(130,68,190);
}

.zigbee-message-top-row{
    border-bottom:1px solid #E6E6FA;
    padding-bottom:2px;
    display: flex;
    justify-content: space-between;
}

.zigbee-message-header{
    border-bottom: 1px solid #E6E6FA;
    padding:5px;
}

.zigbee-message-content{
    margin-top:2px;
}

.zigbee-message-error-row{
    margin-top:2px;
    border-top:1px solid #E6E6FA;
    padding-top:2px;
    color: rgb(190, 39, 2);
}

</style>