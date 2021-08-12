<template>
    <article class="node-item" :class="{'node-item-good': isGood, 'node-item-bad': isBad}">
        <h3 class="node-item-header">{{ node.name }}</h3>
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
            <b>Typ węzła: </b>{{ node.nodeType}}
        </div>
        <div>
            <b>Status: </b> {{ status }}
        </div>
    </article>
</template>

<script>

export default {
    name:"NodeItem",
    props:{
        node: Object,
    },
    data(){
        return{
            
        }
    },
    computed:{
        status(){
            return this.node.discovered ? 'Rozpoznane' : 'Nierozpoznane';
        },
        isGood(){
            return this.node.discovered;
        },
        isBad(){
            return !this.node.discovered;
        }
    },
    methods:{
    }
}
</script>


<style scoped>

.node-item{
    font-size:12px;
    margin: 8px 0;
    padding:8px;
    border-width: 2px 6px 2px 2px;
    border-style:solid;
    border-radius: 5px;
}

.node-item:hover{
    background-color: #E6E6FA;
    cursor: pointer;
}

.node-item-good{
    border-color: green;
}

.node-item-bad{
    border-color: red;
}

.node-item-header{
    margin:0 0 6px 0;
    font-size: 15px;
}


</style>