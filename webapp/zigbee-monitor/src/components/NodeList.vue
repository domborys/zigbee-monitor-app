<template>
    <section>
        <h2 class="node-list-header">Węzły</h2>
        <node-item v-for="node in nodes" :key="node.id" :node="node" />
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
        
    }
}
</script>


<style scoped>
.node-list-header{
    margin:0;
    font-size:22px;
    font-weight:bold;
}

</style>