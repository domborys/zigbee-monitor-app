<template>
    <li class="node-item" @click="editClick">
        <div class="node-item-content">
            <h3 class="node-item-header">{{ readingConfig.name }}</h3>
        </div>
        <button type="button" class="close-button" @click.stop="deleteClick">
            <img :src="require('@/assets/icons/x.svg')" width="35" height="35">
        </button>
    </li>
</template>

<script>

export default {
    name:"NodeParameter",
    props:{
        readingConfig: Object,
    },
    data(){
        return{
            
        }
    },
    methods:{
        editClick(){
            this.$emit('edit-config');
        },
        deleteClick(){
            this.$emit('delete-config');
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