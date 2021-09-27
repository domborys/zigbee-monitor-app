<template>
    <div class="node-select-container">
        <h2>Wybierz węzeł</h2>
        <section>
            <h3>Nowe węzły</h3>
            <node-item-select-mode v-for="node in nodesNotInSystem" :key="node.address64" :node="node" @select-node="selectNode(node)" />
        </section>
        <section>
            <h3>Węzły obecne w systemie</h3>
            <node-item-select-mode v-for="node in nodesInSystem" :key="node.address64" :node="node" @select-node="selectNode(node)" />
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
        }
    },
    
}
</script>


<style scoped>

</style>