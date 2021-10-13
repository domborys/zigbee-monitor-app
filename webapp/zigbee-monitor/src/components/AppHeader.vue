<template>
    <header class="header">
        <h1 class="page-title">Monitor sieci ZigBee</h1>
        <nav>
            <template v-if="isViewMode">
                <button type="button" class="header-button" @click="refresh">Odśwież</button>
                <button type="button" class="header-button" @click="editNewLayer">Dodaj mapę</button>
                <button type="button" class="header-button" @click="editActiveLayer">Edytuj mapę</button>
                <button type="button" class="header-button" @click="deleteActiveLayer">Usuń mapę</button>
            </template>
            <template v-if="isLoggedIn">
                <!--
                <span>{{ user.username }}</span>
                <button type="button" class="header-button" @click="logout">Wyloguj</button>
                -->
                <!--
                <div class="dropdown-menu">
                    <button type="button" class="header-button dropdown-toggle button-username">
                        {{ user.username }}
                    </button>
                    <div class="dropdown-content">
                        
                        <button type="button" class="dropdown-list-button">Zmień hasło</button>
                        <button type="button" class="dropdown-list-button">Wyloguj</button>
                    </div>
                </div>-->
                <dropdown-menu>
                    <template v-slot:toggle-button>
                        <img src="~@/assets/icons/person.svg" class="user-icon" />
                        <span class="button-username">{{ user.username }}</span>
                    </template>
                    <template v-slot:content>
                        <button type="button" class="dropdown-list-button">Zmień hasło</button>
                        <button type="button" class="dropdown-list-button" @click="logout">Wyloguj</button>
                    </template>
                </dropdown-menu>
            </template>
        </nav>
    </header>
</template>

<script>

import DropdownMenu from './DropdownMenu.vue';

export default {
    name:"AppHeader",
    components:{
        DropdownMenu
    },
    data(){
        return{
        }
    },
    computed:{
        isViewMode(){
            return this.$store.getters.mode === 'view';
        },
        isLoggedIn(){
            return this.$store.state.user !== null;
        },
        user(){
            return this.$store.state.user;
        }
    },
    methods:{
        editNewLayer(){
            this.$store.commit('prepareNewLayer');
            this.$store.commit('pushMode', 'newLayer');
        },
        editActiveLayer(){
            this.$store.commit('prepareLayerForEdit', this.$store.getters.activeLayer);
            this.$store.commit('pushMode', 'editLayer');
        },
        async deleteActiveLayer(){
            await this.$store.dispatch('deleteLayer', this.$store.getters.activeLayer);
        },
        async refresh(e){
            try{
                e.target.disabled = true;
                await this.$store.dispatch('downloadDiscoveryResults');
            }
            finally{
                e.target.disabled = false;
            }
        },
        async logout(){
            try{
                await this.$store.dispatch('logout');
                this.$store.commit('replaceMode', 'login');
            }
            catch(e){
                console.log(e);
            }
        }
    },
}
</script>

<style scoped>

.header{
    flex:none;
    border-bottom:1px solid #E6E6FA;
    box-sizing:border-box;
    display:flex;
    align-items: center;
    justify-content: space-between;
}

.page-title{
    font-size:20px;
    font-weight:normal;
    margin: 10px;
}

.user-icon{
    width: 1.3em;
    height: 1.3em;
    vertical-align: -0.4em;
    display:inline-block;
    margin-right:5px;
}

.button-username{
    font-weight:600;
}


</style>