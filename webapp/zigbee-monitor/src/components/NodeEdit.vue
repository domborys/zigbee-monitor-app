<template>
    <form class="node-edit-container" @submit.prevent="saveNode">
        <div class="node-edit-main">
            <h2 class="side-panel-h2">{{headerText}}</h2>
            <div class="input-label-group">
                <label for="nodeNameInput" class="text-label">Nazwa węzła</label>
                <input type="text" class="text-input" v-model="nodeName" id="nodeNameInput" placeholder="np. czujnik dymu">
            </div>
            <div class="input-label-group">
                <label for="nodeAddressInput" class="text-label">64-bitowy adres węzła</label>
                <input type="text" class="text-input" v-model="nodeAddress" id="nodeAddressInput" placeholder="np. 0123456789ABCDEF">
                <button type="button" class="button" @click="searchDevice">Szukaj urządzenia</button>
            </div>
            <div>
                <h3 class="side-panel-h3">Pozycja węzła na planie</h3>
                Kliknij na planie aby wskazać pozycję węzła.
            </div>
            <div>
                <h3 class="side-panel-h3">Wyświetlane wartości</h3>
                <button type="button" class="button" @click="addReadingConfig">Dodaj wartość</button>
                <ul class="parameter-list-edit">
                    <node-parameter v-for="config in node.readingConfigs" :key="makeParameterKey(config)" :readingConfig="config" @edit-config="editConfig(config)" @delete-config="deleteConfig(config)" />
                </ul>
            </div>
        </div>
        <div class="node-edit-footer">
            <button type="button" class="button footer-button" @click="discardNode">Anuluj</button>
            <button type="submit" class="button footer-button">{{submitButtonText}}</button>
        </div>
    </form>
</template>

<script>

import NodeItemEditMode from './NodeItemEditMode.vue';
import NodeParameter from './NodeParameter.vue';

export default {
    name:"NodeEdit",
    components:{
        NodeItemEditMode,
        NodeParameter
    },
    props:{
        
    },
    data(){
        return{
        }
    },
    computed:{
        newNodeMode(){
            return this.$store.getters.mode === 'newNode';
        },
        headerText(){
            return this.newNodeMode ? 'Dodawanie węzła' : 'Edycja węzła';
        },
        submitButtonText(){
            return this.newNodeMode ? 'Dodaj' : 'Zapisz';
        },
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
        makeParameterKey(config){
            const idStr = typeof config.id === 'number' ? config.id.toString() : '';
            const tempIdStr = typeof config.tempId === 'number' ? config.tempId.toString() : '';
            return idStr + '_' + tempIdStr;
        },
        searchDevice(){
            this.$store.commit('pushMode', 'selectNode');
        },
        addReadingConfig(){
            this.$store.commit('prepareNewReadingConfig');
            this.$store.commit('pushMode', 'newReadingConfig');
        },
        editConfig(config){
            this.$store.commit('prepareReadingConfigForEdit', config);
            this.$store.commit('pushMode', 'editReadingConfig');
        },
        deleteConfig(config){
            this.$store.commit('deleteReadingConfig', config);
        },
        saveNode(){
            this.$store.commit('saveEditedNode');
            this.$store.commit('previousMode');
        },
        discardNode(){
            this.$store.commit('discardEditedNode');
            this.$store.commit('previousMode', 'editLayer');
        }
    },
    mounted(){
        this.isNewImage = false;
    }
    
}
</script>


<style scoped>

.node-edit-container{
    height:100%;
    display: flex;
    flex-direction: column;
}

.node-edit-main{
    flex:auto;
    overflow:auto;
    min-height:0;
    border-bottom:1px solid #E6E6FA;
}

.node-edit-footer{
    flex:none;
    box-sizing:border-box;
    display:flex;
    justify-content: flex-end;
    padding-top:8px;
}

.footer-button{
    flex:1;
}

.parameter-list-edit{
    list-style-type: none;
    padding:0;
    margin:5px 0 0 0;
}
</style>