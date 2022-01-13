<template>
    <form class="node-edit-container" @submit.prevent="saveNode">
        <div class="node-edit-main">
            <h2 class="side-panel-h2">{{headerText}}</h2>
            <div class="input-label-group">
                <label for="nodeNameInput" class="text-label">Nazwa węzła</label>
                <input type="text" class="text-input" :class="{'text-input-invalid':nodeNameError !== null}" v-model="nodeName" id="nodeNameInput" placeholder="np. czujnik dymu">
                <div v-if="nodeNameError !== null" class="input-error-message">{{ nodeNameError }}</div>
            </div>
            <div class="input-label-group">
                <label for="nodeAddressInput" class="text-label">64-bitowy adres węzła</label>
                <input type="text" class="text-input" :class="{'text-input-invalid':nodeAddressError !== null}" v-model="nodeAddress" id="nodeAddressInput" placeholder="np. 0123456789ABCDEF">
                <div v-if="nodeAddressError !== null" class="input-error-message">{{ nodeAddressError }}</div>
                <button type="button" class="button" @click="searchDevice">Szukaj urządzenia</button>
            </div>
            <div>
                <h3 class="side-panel-h3">Pozycja węzła na planie</h3>
                Kliknij na planie, aby wskazać pozycję węzła.
                <div v-if="nodePositionError !== null" class="input-error-message">{{ nodePositionError }}</div>
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
            <div class="node-edit-footer-buttons">
                <button type="button" class="button footer-button" @click="discardNode">Anuluj</button>
                <button type="submit" class="button footer-button">{{submitButtonText}}</button>
            </div>
            <div>
                <div v-if="formSubmitAttempted && !isFormValid" class="input-error-message">{{ generalError }}</div>
            </div>
        </div>
    </form>
</template>

<script>

import NodeItemEditMode from './NodeItemEditMode.vue';
import NodeParameter from './NodeParameter.vue';

function isValid64Address(address){
    if(typeof address !== 'string')
        return false;
    const regex = /^[0-9a-fA-F]{16}$/;
    return regex.test(address);
}

/**
 * Component used for creating new nodes or editing the existing ones.
 * It should be used inside the left pane.
 */
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
            nodeNameError: null,
            nodeAddressError: null,
            nodePositionError: null,
            generalError: null,
            formSubmitAttempted: false,
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
        nodeX(){
            return this.node.x;
        },
        nodeName:{
            get(){
                return this.node.name;
            },
            set(value){
                this.validateNodeName(value);
                this.$store.commit('setEditedNodeParam', {name:'name', value:value});
            }
        },
        nodeAddress:{
            get(){
                return this.node.address64;
            },
            set(value){
                this.validateNodeAddress(value);
                this.$store.commit('setEditedNodeParam', {name:'address64', value:value});
            }
        },
        isFormValid(){
            return this.nodeNameError === null && this.nodeAddressError === null && this.nodePositionError === null;
        },
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
        validateNodeName(nodeName){
            if(typeof nodeName === 'undefined')
                nodeName = this.nodeName;
            if(typeof nodeName === 'string' && nodeName.trim().length > 0){
                this.nodeNameError = null;
                return true;
            }
            else{
                this.nodeNameError = 'Nazwa węzła nie może być pusta.';
                return false;
            }  
        },
        validateNodeAddress(nodeAddress){
            if(typeof nodeAddress === 'undefined')
                nodeAddress = this.nodeAddress;
            if(isValid64Address(nodeAddress)){
                this.nodeAddressError = null;
                return true;
            }
            else{
                this.nodeAddressError = 'Adres powinien być liczbą szesnastkową składającą się z 16 cyfr.';
                return false;
            }  
        },
        validateNodePosition(){
            const isValid = typeof this.node.x === 'number' && typeof this.node.y === 'number';
            if(isValid){
                this.nodePositionError = null;
                return true;
            }
            else{
                this.nodePositionError = 'Proszę zaznaczyć pozycję węzła na mapie';
                return false;
            }
        },
        checkIfValid(){
            this.formSubmitAttempted = true;
            this.validateNodeName();
            this.validateNodeAddress();
            this.validateNodePosition();
            const isValid = this.isFormValid;
            if(isValid){
                this.generalError = null;
            }
            else{
                this.generalError = 'Proszę poprawić błędy.';
            }
            return isValid;
        },

        saveNode(){
            if(this.checkIfValid()){
                this.$store.commit('saveEditedNode');
                this.$store.commit('previousMode');
            }
        },
        discardNode(){
            this.$store.commit('discardEditedNode');
            this.$store.commit('previousMode', 'editLayer');
        }
    },
    watch:{
        nodeX(newX){
            this.validateNodePosition();
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
    padding-top:8px;
}

.node-edit-footer-buttons{
    display:flex;
    justify-content: flex-end;
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