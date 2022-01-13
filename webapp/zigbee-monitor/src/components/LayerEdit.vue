<template>
    <form class="layer-edit-container" @submit.prevent="saveLayer"> 
        <div class="layer-edit-main">
            <h2 class="side-panel-h2">{{ headerText }}</h2>
            <div class="input-label-group">
                <label for="layerNameInput" class="text-label">Nazwa mapy</label>
                <input type="text" class="text-input" :class="{'text-input-invalid':layerNameError !== null}" v-model="layerName" id="layerNameInput" placeholder="np. Parter">
                <div v-if="layerNameError !== null" class="input-error-message">{{ layerNameError }}</div>
            </div>
            <div class="input-label-group">
                <label for="floorNoInput" class="text-label">Poziom</label>
                <input type="text" class="text-input" :class="{'text-input-invalid':floorNoError !== null}" v-model="floorNo" id="floorNoInput" placeholder="np. 0">
                <div v-if="floorNoError !== null" class="input-error-message">{{ floorNoError }}</div>
            </div>
            <div>
                <h3 class="side-panel-h3">Plan</h3>
                <label for="floorPlanInput" class="file-input-button">{{ imageInputText }}</label>
                <input type="file" ref="floorPlanFile" class="file-input-hidden" @change="loadFloorPlan" accept="image/*" id="floorPlanInput">
                <div v-if="layerImageError !== null" class="error-message">{{ layerImageError }}</div>
            </div>
            <div v-if="isMapVisible">
                <h3 class="side-panel-h3">Węzły sieci</h3>
                <button type="button" class="button" @click="addNode">Dodaj węzeł</button>
                <ul class="node-list-edit">
                    <node-item-edit-mode v-for="node in layer.nodes" :key="makeNodeKey(node)" :node="node" @edit-node="editNode(node)" @delete-node="deleteNode(node)" />
                </ul>
            </div>
        </div>
        <div class="layer-edit-footer">
            <div class="layer-edit-footer-buttons">
                <button type="button" class="button footer-button" @click="discardLayer">Anuluj</button>
                <button type="submit" class="button footer-button">Zapisz</button>
            </div>
            <div>
                <div v-if="formSubmitAttempted && !isFormValid" class="input-error-message">{{ generalError }}</div>
            </div>
        </div>
    </form>
</template>

<script>

import NodeItemEditMode from './NodeItemEditMode.vue';
import utils from '../utils';

/**
 * Component used for editing maps. It lets the user type the name of the map, the floor number, upload map image and add nodes.
 * 
 *  This component should be used in the left pane of MainLayout.
 */
export default {
    name:"LayerEdit",
    components:{
        NodeItemEditMode
    },
    props:{
        
    },
    data(){
        return{
            keepRatio:true,
            image:null,
            layerNameError:null,
            floorNoError:null,
            layerImageError:null,
            generalError:null,
            formSubmitAttempted:false,
        }
    },
    computed:{
        newLayerMode(){
            return this.$store.getters.mode === 'newLayer';
        },
        editLayerMode(){
            return this.$store.getters.mode === 'editLayer';
        },
        headerText(){
            return this.newLayerMode ? 'Nowa mapa' : 'Edytuj mapę';
        },
        imageInputText(){
            return this.newLayerMode ? 'Dodaj plik z planem' : 'Załaduj nowy plan';
        },
        layer(){
            return this.$store.state.editedLayer;
        },
        isMapVisible(){
            return this.layer && this.layer.imgurl;
        },
        isFormValid(){
            return this.layerNameError === null && this.floorNoError === null && this.layerImageError === null;
        },
        layerName:{
            get(){
                return this.layer.name;
            },
            set(value){
                this.validateLayerName(value);
                this.$store.commit('setEditedLayerParam', {name:'name', value:value});
            }
        },
        floorNo:{
            get(){
                return this.layer.number;
            },
            set(value){
                this.validateFloorNo(value);
                this.$store.commit('setEditedLayerParam', {name:'number', value:value});
            }
        },
    },
    methods:{
        makeNodeKey(node){
            const idStr = typeof node.id === 'number' ? node.id.toString() : '';
            const tempIdStr = typeof node.tempId === 'number' ? node.tempId.toString() : '';
            return idStr + '_' + tempIdStr;
        },
        addNode(){
            this.$store.commit('prepareNewNode');
            this.$store.commit('pushMode', 'newNode');
        },
        editNode(node){
            this.$store.commit('prepareNodeForEdit', node);
            this.$store.commit('pushMode', 'editNode');
        },
        deleteNode(node){
            this.$store.commit('deleteNode', node);
        },
        loadFloorPlan(e){
            const file = e.target.files[0];
            if(file){
                this.layerImageError = null;
                const imgurl = URL.createObjectURL(file);
                this.$store.dispatch('loadLayerImage', file);
            }
            this.$store.commit('setEditedLayerParam', {name:'isNewImage', value:true});
        },
        async saveLayer(){
            if(!this.checkIfValid()){
                return;
            }
            try{
                await this.$store.dispatch('saveEditedLayer');
                this.$store.commit('setActiveLayer', this.layer.name);
                this.$store.commit('previousMode');
                this.$store.commit('setEditedLayer', null);
            }
            catch(e){
                this.generalError = 'Wystąpił błąd podczas zapisywania mapy: ' + e.message;
                console.error(e);
            }
            
        },
        checkIfValid(){
            this.formSubmitAttempted = true;
            this.validateLayerName();
            this.validateFloorNo();
            this.validateLayerImage();
            const isValid = this.isFormValid;
            if(isValid){
                this.generalError = null;
            }
            else{
                this.generalError = 'Proszę poprawić błędy.';
            }
            return isValid;
        },
        validateLayerName(layerName){
            if(typeof layerName === 'undefined')
                layerName = this.layerName;
            if(typeof layerName === 'string' && layerName.trim().length > 0){
                this.layerNameError = null;
                return true;
            }
            else{
                this.layerNameError = 'Nazwa mapy nie może być pusta.';
                return false;
            }
        },
        validateFloorNo(floorNo){
            if(typeof floorNo === 'undefined')
                floorNo = this.floorNo;
            if(!utils.isNumeric(floorNo)){
                this.floorNoError = 'Poziom musi być liczbą.';
                return true;
            }
            else{
                this.floorNoError = null;
                return false;
            }
        },
        validateLayerImage(){
            if(this.isMapVisible){
                this.layerImageError = null;
                return true;
            }
            else{
                this.layerImageError = 'Proszę załadować plik z planem.';
                return false;
            }
        },
        discardLayer(){
            this.$store.commit('previousMode');
            this.$store.commit('setEditedLayer', null);
        },
    },
    mounted(){
        this.isNewImage = false;
    }
    
}
</script>


<style scoped>
.layer-edit-container{
    height:100%;
    display: flex;
    flex-direction: column;
}

.layer-edit-main{
    flex:auto;
    overflow:auto;
    min-height:0;
    border-bottom:1px solid #E6E6FA;
}

.layer-edit-footer{
    flex:none;
    box-sizing:border-box;
    padding-top:8px;
}

.layer-edit-footer-buttons{
    display:flex;
    justify-content: flex-end;
}

.footer-button{
    flex:1;
}

.node-list-edit{
    list-style-type: none;
    padding:0;
    margin:5px 0 0 0;
}

</style>