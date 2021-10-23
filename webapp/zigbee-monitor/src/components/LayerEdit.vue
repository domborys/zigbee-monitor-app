<template>
    <form class="layer-edit-container" @submit.prevent="saveLayer"> 
        <div class="layer-edit-main">
            <h2 class="side-panel-h2">{{ headerText }}</h2>
            <div class="input-label-group">
                <label for="layerNameInput" class="text-label">Nazwa mapy</label>
                <input type="text" class="text-input" v-model="layerName" id="layerNameInput" placeholder="Parter">
            </div>
            <div class="input-label-group">
                <label for="floorNoInput" class="text-label">Poziom</label>
                <input type="text" class="text-input" v-model="floorNo" id="floorNoInput" placeholder="0">
            </div>
            <div>
                <h3 class="side-panel-h3">Plan</h3>
                <label for="floorPlanInput" class="file-input-button">{{ imageInputText }}</label>
                <input type="file" ref="floorPlanFile" class="file-input-hidden" @change="loadFloorPlan" accept="image/*" id="floorPlanInput">
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
            <button type="button" class="button footer-button" @click="discardLayer">Anuluj</button>
            <button type="submit" class="button footer-button">Zapisz</button>
        </div>
    </form>
</template>

<script>

import NodeItemEditMode from './NodeItemEditMode.vue';

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
        layerName:{
            get(){
                return this.layer.name;
            },
            set(value){
                this.$store.commit('setEditedLayerParam', {name:'name', value:value});
            }
        },
        floorNo:{
            get(){
                return this.layer.number;
            },
            set(value){
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
                const imgurl = URL.createObjectURL(file);
                this.$store.dispatch('loadLayerImage', file);
            }
            this.$store.commit('setEditedLayerParam', {name:'isNewImage', value:true});
        },
        async saveLayer(){
            try{
                await this.$store.dispatch('saveEditedLayer');
                this.$store.commit('setActiveLayer', this.layer.name);
                this.$store.commit('previousMode');
                //URL.revokeObjectURL(this.layer.imgurl);
                this.$store.commit('setEditedLayer', null);
                this.$store.dispatch('downloadDiscoveryResults');
            }
            catch(e){
                console.error(e);
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
    display:flex;
    justify-content: flex-end;
    padding-top:8px;
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