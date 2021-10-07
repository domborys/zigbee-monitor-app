<template>
    <article class="node-item">
        <div class="node-item-content" @click="editClick">
            <h3 class="node-item-header">{{ readingConfig.name }}</h3>
        </div>
        <div class="node-item-close">
            <button type="button" class="close-button" @click="deleteClick"></button>
        </div>
    </article>
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
    font-size:12px;
    margin: 8px 0;
    padding:6px;
    border-width: 2px;
    border-style:solid;
    border-radius: 5px;
    border-color:#630094;
    display:flex;
    align-items:center;
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
	cursor: pointer;
    font-family: inherit;
    font-size: 35px;
    width:30px;
    height:30px;
    overflow:hidden;
    
}

.close-button::after{
    content:"×";
}

.node-item:hover{
    background-color: #E6E6FA;
    cursor: pointer;
}


.node-item-header{
    margin:0 0 4px 0;
    font-size: 15px;
}


</style>