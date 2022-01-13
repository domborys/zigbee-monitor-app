<template>
    <div class="main-container">
        <app-header />
        <div v-if="!isOneColumnMode" class="below-header">
            <section class="left-pane">
                <template v-if="mode === 'view'">
                    <layer-list :layers="layerNames" v-model="activeLayerName" />
                    <node-list :nodes="activeLayerNodes" />
                </template>
                <template v-if="mode === 'newLayer' || mode === 'editLayer'">
                    <layer-edit />
                </template>
                <template v-if="mode === 'newNode' || mode === 'editNode'">
                    <node-edit />
                </template>
                <template v-if="mode === 'selectNode'">
                    <node-select />
                </template>
                <template v-if="mode === 'newReadingConfig' || mode === 'editReadingConfig'">
                    <parameter-edit />
                </template>
            </section>
            <main class="main">
                <map-display v-if="mainDisplayMode === 'map'" :layer="activeLayer" />
                <message-display v-if="mainDisplayMode === 'messages'" :node="$store.state.displayedMessagesNode" />
            </main>
        </div>
        <div v-if="isOneColumnMode" class="below-header-one-column">
            <login-form v-if="mode === 'login'" />
            <password-change-form v-if="mode === 'changePassword'" />
            <user-management v-if="mode === 'manageUsers'" />
            <user-details v-if="mode === 'showUser'" />
            <user-edit v-if="mode === 'newUser' || mode === 'editUser'" />
        </div>
    </div>
</template>
<script>
import LayerList from './LayerList.vue';
import NodeList from './NodeList.vue';
import MapDisplay from './MapDisplay.vue';
import LayerEdit from './LayerEdit.vue';
import NodeEdit from './NodeEdit.vue';
import MessageDisplay from './MessageDisplay.vue'
import AppHeader from './AppHeader.vue';
import LoginForm from './LoginForm.vue';
import PasswordChangeForm from './PasswordChangeForm.vue';
import NodeSelect from './NodeSelect.vue';
import ParameterEdit from './ParameterEdit.vue';
import UserManagement from './UserManagement.vue';
import UserDetails from './UserDetails.vue';
import UserEdit from './UserEdit.vue'

/**
 * The component providing the main layout of the application.
 * 
 * The layout consists of a header (AppHeader) and the main part.
 * The main part may be either single-column or two-column, depending on the currently displayed part of the application.
 * Single-column parts are centered horizontally.
 * Two-column parts consist of two parts: left pane and right pane.
 * Left pane is used for configuration and navigation, the right pane is used for displaying maps or messages.
 */
export default {
    name:"MainLayout",
    components:{
        LayerList,
        NodeList,
        MapDisplay,
        LayerEdit,
        NodeEdit,
        MessageDisplay,
        AppHeader,
        LoginForm,
        NodeSelect,
        ParameterEdit,
        PasswordChangeForm,
        UserManagement,
        UserDetails,
        UserEdit
    },
    data(){
        return{}
    },
    computed:{
        mode(){
            return this.$store.getters.mode;
        },
        isOneColumnMode(){
            return this.$store.getters.isOneColumnMode;
        },
        mainDisplayMode(){
            return this.$store.state.mainDisplayMode;
        },
        layers(){
            return this.$store.state.layers;
        },
        activeLayer(){
            return this.$store.getters.activeLayer;
        },
        activeLayerNodes(){
            if (this.activeLayer === null)
                return [];
            else
                return this.activeLayer.nodes;

        },
        activeLayerName:{
            get(){
                return this.$store.state.activeLayerName;
            },
            set(value){
                this.$store.commit('setActiveLayer', value);
            }
        },
        layerNames(){
            return this.$store.getters.layerNames;
        }
    },
    methods:{
    },
    async mounted(){
        try{
            await this.$store.dispatch('loadDataAfterLogin');
        }
        catch(e){

        }
    }
}
</script>

<style scoped>
.main-container{
    height:100%;
    display:flex;
    flex-direction: column;
}

.below-header{
    display:flex;
    flex:auto;
    min-height:0;
}

.below-header-one-column{
    display:flex;
    justify-content: center;
    flex:auto;
    min-height:0;
}


.left-pane{
    flex:0 300px;
    border-right:1px solid #E6E6FA;
    overflow:auto;
    padding: 10px;
}

.main{
    flex:auto;
}
</style>