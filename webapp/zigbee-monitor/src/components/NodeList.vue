<template>
    <section>
        <h2 class="side-panel-h2">Węzły</h2>
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

</style>