<template>
    <li class="node-item" @click="editClick">
        <div class="node-item-content" >
            <h3 class="node-item-header">{{ node.name }}</h3>
            <div>
                {{ node.address64 }}
            </div>
        </div>
        <button type="button" class="close-button" @click.stop="deleteClick">
            <img :src="require('@/assets/icons/trash.svg')" width="25" height="25">
        </button>
    </li>
</template>

<script>

/**
 * Component used for displaying one node on the list of nodes in the LayerEdit component.
 * 
 * As the root element of this component is HTML li element, this component must be used inside a list.
 */
export default {
    name:"NodeItemEditMode",
    props:{
        /**
         * The node to display.
         */
        node: Object,
    },
    data(){
        return{}
    },
    computed:{
        
    },
    methods:{
        editClick(){
            /**
             * Emitted when the user clicks on the item outside the garbage can icon.
             */
            this.$emit('edit-node');
        },
        deleteClick(){
            /**
             * Emitted when the user clicks on the garbage can icon.
             */
            this.$emit('delete-node');
        }
    }
}
</script>


<style scoped>

.node-item{
    padding:10px;
    border-bottom: 1px solid #E6E6FA;
    border-right: 1px solid #E6E6FA;
    border-left: 1px solid #E6E6FA;
    display:flex;
    align-items:center;
}

.node-item:first-child{
    border-top: 1px solid #E6E6FA;
}

.node-item-content{
    flex:auto;
    cursor: pointer;
}

.close-button{
    
    background: none;
	color: inherit;
	border: none;
	padding: 0;
    font-family: inherit;
    cursor:pointer;
}

.close-button > *{
    display:block;
}

.node-item:hover{
    background-color: #E6E6FA;
    cursor: pointer;
}

.node-item-header{
    margin:0 0 4px 0;
    font-size: 15px;
    font-weight:600;
}

</style>