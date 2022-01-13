<template>
    <li class="node-item"  @click="nodeSelectClick">
        <div>
            <b>Id urządzenia: </b>{{ node.id}}
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
    </li>
</template>
<script>

/**
 * Component used for displaying one node on the list of discovered nodes in the NodeSelect component.
 * 
 * As the root element of this component is HTML li element, this component must be used inside a list.
 */
export default {
    name:"NodeItemSelectMode",
    props:{
        /**
         * The node to display.
         */
        node: Object,
    },
    data(){
        return {}
    },
    computed:{
        
    },
    methods:{
        nodeSelectClick(){
            /**
             * Emitted when the user clicks on the item.
             */
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

.node-item{
    padding:10px;
    border-bottom: 1px solid #E6E6FA;
    border-right: 1px solid #E6E6FA;
    border-left: 1px solid #E6E6FA;
}

.node-item:first-child{
    border-top: 1px solid #E6E6FA;
}

.node-item:hover{
    background-color: #E6E6FA;
    cursor: pointer;
}

</style>