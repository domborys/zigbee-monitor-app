<template>
    <section>
        <h2 class="node-list-header">Węzły</h2>
        <ul v-if="nodes.length > 0" class="node-list">
            <node-item v-for="node in nodes" :key="node.id" :node="node" @click.native="showMessages(node)" />
        </ul>
        <div v-else>
            Na wybranej mapie nie znajdują się żadne węzły.
        </div>
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
    margin:15px 0 15px 0;
    font-size:22px;
    font-weight:600;
}

.node-list{
    list-style-type: none;
    padding:0;
    margin:0;
}

</style>