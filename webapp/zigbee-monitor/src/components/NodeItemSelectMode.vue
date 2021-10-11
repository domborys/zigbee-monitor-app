<template>
    <article class="node-item-select"  @click="nodeSelectClick">
        <div>
            <b>Id urządzenia: </b>{{ node.deviceId}}
        </div>
        <div>
            <b>Adres 16-bit: </b> {{ node.address16 }}
        </div>
        <div>
            <b>Adres 64-bit: </b> {{ node.address64 }}
        </div>
        <div>
            <b>Typ węzła: </b>{{ node.role }}
        </div>
    </article>
</template>
<script>


export default {
    name:"NodeItemSelectMode",
    props:{
        node: Object,
    },
    data(){
        return{
        }
    },
    computed:{
        
    },
    methods:{
        nodeSelectClick(){
            this.$emit('select-node');
        }
    }
    
}
</script>


<style scoped>

.node-item-select{
    font-size:12px;
    margin: 8px 0;
    padding:6px;
    border-width: 2px;
    border-style:solid;
    border-radius: 5px;
    border-color:rgb(130,68,190);
    cursor:pointer;
}

</style>