<template>
    <div class="node-select-container">
        <div class="heading-back-group">
            <button type="button" class="heading-back-button" @click="back"></button>
            <h2 class="heading-back-heading">Wykryte węzły</h2>
        </div>
        <section>
            <h3>Nowe węzły</h3>
            <ul v-if="nodesNotInSystem.length > 0" class="node-list-select">
                <node-item-select-mode v-for="node in nodesNotInSystem" :key="node.address64" :node="node" @select-node="selectNode(node)" />
            </ul>
            <div v-else>
                Nie znaleziono nowych węzłów.
            </div>
        </section>
        <section>
            <h3>Węzły obecne w systemie</h3>
            <ul v-if="nodesInSystem.length > 0" class="node-list-select">
                <node-item-select-mode v-for="node in nodesInSystem" :key="node.address64" :node="node" @select-node="selectNode(node)" />
            </ul>
            <div v-else>
                Nie wykryto węzłów obecnych w systemie.
            </div>
        </section>
    </div>
</template>

<script>
import NodeItemSelectMode from './NodeItemSelectMode.vue';

export default {
    name:"NodeSelect",
    components:{
        NodeItemSelectMode
    },
    props:{
        
    },
    data(){
        return{
        }
    },
    computed:{
        nodesNotInSystem(){
            return this.$store.getters.discoveredNodesNotInSystem;
        },
        nodesInSystem(){
            return this.$store.getters.discoveredNodesInSystem;
        }
    },
    methods:{
        selectNode(node){
            this.$store.commit('setEditedNodeParam', {name:'address64', value:node.address64});
            this.$store.commit('previousMode');
        },
        back(){
            this.$store.commit('previousMode');
        }
    },
    
}
</script>


<style scoped>
.node-list-select{
    list-style-type: none;
    padding:0;
    margin:5px 0 0 0;
}
</style>