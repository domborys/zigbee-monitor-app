<template>
    <section>
        <h2 class="layer-details-header">Dodawanie piętra</h2>
        <form @submit.prevent="saveLayer"> 
            <div>
                <label for="layerNameInput">Nazwa piętra</label>
                <input type="text" v-model="layerName" id="layerNameInput" placeholder="Parter">
            </div>
            <div>
                <label for="floorNoInput">Poziom</label>
                <input type="text" v-model="floorNo" id="floorNoInput" placeholder="0">
            </div>
            <div>
                <label for="floorPlanInput">Plan piętra</label>
                <input type="file" ref="floorPlanFile" @change="loadFloorPlan" accept="image/*" id="floorPlanInput">
            </div>
            <!--
            <fieldset>
                <legend>Rzeczywiste rozmiary planu</legend>
                <div>
                    <label for="imageWidthInput">Poziomo</label>
                    <input type="text" :value="layer.width" @input="widthChange" id="floorWidthInput" placeholder="9.5">m
                </div>
                <div>
                    <label for="imageHeightInput">Pionowo</label>
                    <input type="text" :value="layer.height" @input="heightChange" id="floorHeightInput" placeholder="7">m
                </div>
                <div>
                    <input type="checkbox" v-model="keepRatio" id="keepRatioInput">
                    <label for="keepRatioInput">Zachowaj proporcje</label>
                </div>
            </fieldset>-->
            <div>
                <h3>Węzły sieci</h3>
                <button type="button" @click="addNode">Dodaj węzeł</button>
                <node-item-edit-mode v-for="node in layer.nodes" :key="makeNodeKey(node)" :node="node" @edit-node="editNode(node)" @delete-node="deleteNode(node)" />
            </div>
            <div>
                <button type="button" @click="discardLayer">Anuluj</button>
                <button type="submit">Zapisz</button>
            </div>
        </form>
    </section>
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
            isNewImage:false,
        }
    },
    computed:{
        layer(){
            return this.$store.state.editedLayer;
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
                return this.layer.floorNo;
            },
            set(value){
                this.$store.commit('setEditedLayerParam', {name:'floorNo', value:value});
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
            this.$store.commit('setMode', 'editNode');
        },
        editNode(node){
            this.$store.commit('prepareNodeForEdit', node);
            this.$store.commit('setMode', 'editNode');
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
            this.isNewImage = true;
        },
        async saveLayer(){
            await this.$store.dispatch('saveEditedLayer', {isNewImage:this.isNewImage});
            this.$store.commit('setActiveLayer', this.layer.name);
            this.$store.commit('setMode', 'view');
            //URL.revokeObjectURL(this.layer.imgurl);
            this.$store.commit('setEditedLayer', null);
            
        },
        discardLayer(){
            this.$store.commit('setEditedLayer', null);
            this.$store.commit('setMode', 'view');
        },
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