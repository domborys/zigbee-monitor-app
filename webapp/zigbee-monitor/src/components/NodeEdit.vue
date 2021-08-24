<template>
    <section>
        <h2 class="layer-details-header">Dodawanie węzła</h2>
        <form @submit.prevent="saveNode"> 
            <div>
                <label for="nodeNameInput">Nazwa węzła</label>
                <input type="text" v-model="nodeName" id="nodeNameInput" placeholder="np. czujnik dymu">
            </div>
            <div>
                <label for="nodeAddressInput">64-bitowy adres węzła</label>
                <input type="text" v-model="nodeAddress" id="nodeAddressInput" placeholder="np. 0123456789ABCDEF">
                <button type="button" @click="searchDevice">Szukaj urządzenia</button>
            </div>
            <div>
                Kliknij na mapie aby wskazać pozycję węzła.
            </div>
            
            <div>
                <button type="button" @click="discardNode">Anuluj</button>
                <button type="submit">Dodaj</button>
            </div>
        </form>
    </section>
</template>

<script>

import NodeItemEditMode from './NodeItemEditMode.vue';

export default {
    name:"NodeEdit",
    components:{
        NodeItemEditMode
    },
    props:{
        
    },
    data(){
        return{
        }
    },
    computed:{
        node(){
            return this.$store.state.editedNode;
        },
        nodeName:{
            get(){
                return this.node.name;
            },
            set(value){
                this.$store.commit('setEditedNodeParam', {name:'name', value:value});
            }
        },
        nodeAddress:{
            get(){
                return this.node.address64;
            },
            set(value){
                this.$store.commit('setEditedNodeParam', {name:'address64', value:value});
            }
        }
    },
    methods:{
        searchDevice(){

        },
        saveNode(){
            this.$store.commit('saveEditedNode');
            this.$store.commit('setMode', 'editLayer');
        },
        discardNode(){
            this.$store.commit('discardEditedNode');
            this.$store.commit('setMode', 'editLayer');
        }
    },
    mounted(){
        this.isNewImage = false;
    }
    
}
</script>


<style scoped>
.layer-details-header{
    font-size:22px;
    font-weight:bold;
}


</style>