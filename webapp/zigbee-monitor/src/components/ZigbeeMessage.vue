<template>
    <article class="zigbee-message" :class="boundClasses">
        <div v-if="showNodeInfo" class="zigbee-message-header">
            <b>{{ message.nodeName }}</b>
            {{ message.address64 }}
        </div>
        <div class="zigbee-message-content">
            <template v-if="mode === 'text'">
                {{ messageAsText }}
            </template>
            <template v-if="mode === 'hex'">
                {{ messageAsHex }}
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
                'zigbee-message-received':this.message.type === 'received',
                'zigbee-message-sent':this.message.type === 'sent'
            };
        },
        messageAsText(){
            return atob(this.message.message);
        },
        messageAsHex(){
            const messageBinary = atob(this.message.message);
            return [...messageBinary].map(char => char.charCodeAt(0).toString(16).padStart(2, '0')).join(' ');
        }
        
    },
    methods:{
    }
}
</script>


<style scoped>

.zigbee-message{
    margin: 8px 0;
    border: 2px solid #630094;
    border-radius: 5px;
}

.zigbee-message-received{
    margin-right:20%;
    text-align:left;
}

.zigbee-message-sent{
    margin-left:20%;
    text-align:right;
}

.zigbee-message-header{
    border-bottom: 1px solid #E6E6FA;
    padding:5px;
}

.zigbee-message-content{
    padding:5px;
}



</style>