<template>
    <li class="node-item" :class="{'node-item-good': isGood, 'node-item-bad': isBad}">
        <h3 class="node-item-header">{{ node.name }}</h3>
        <div>
            {{ node.address64 }}
        </div>
        <div :class="{'status-text-recognized': isGood, 'status-text-unrecognized': isBad}">
            {{ status }}
        </div>
    </li>
</template>

<script>

/**
 * Component used for displaying one node in the NodeList.
 * 
 * As the root element of this component is HTML li element, this component must be used inside a list.
 */
export default {
    name:"NodeItem",
    props:{
        /**
         * The node to display.
         */
        node: Object,
    },
    data(){
        return {}
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
    padding:10px;
    border-bottom: 1px solid #E6E6FA;
    border-right: 1px solid #E6E6FA;
    border-left: 4px solid gray;
}

.node-item:first-child{
    border-top: 1px solid #E6E6FA;
}

.node-item:hover{
    background-color: #E6E6FA;
    cursor: pointer;
}

.node-item-good{
    border-left-color: rgb(90, 146, 0);
}

.node-item-bad{
    border-left-color: rgb(190, 39, 2);
}

.status-text-recognized{
    color: rgb(90, 146, 0);
}

.status-text-unrecognized{
    color: rgb(190, 39, 2);
}

.node-item-header{
    margin:0 0 6px 0;
    font-size: 15px;
    font-weight:600;
}

</style>