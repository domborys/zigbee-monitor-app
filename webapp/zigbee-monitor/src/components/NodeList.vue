<template>
    <section>
        <h2 class="node-list-header">Węzły</h2>
        <node-item v-for="node in nodes" :key="node.id" :node="node" @click.native="showMessages(node)" />
    </section>
</template>

<script>
import NodeItem from './NodeItem.vue'

export default {
    name:"NodeList",
    components:{
        NodeItem
    },
    props:{
        nodes: Array,
    },
    methods:{
        showMessages(node){
            console.log("node clicked");
            this.$store.commit('setDisplayedMessagesNode', node);
            this.$store.commit('setMainDisplayMode', 'messages');
        }
    }
}
</script>


<style scoped>
.node-list-header{
    margin:0;
    font-size:22px;
    font-weight:600;
}

</style>