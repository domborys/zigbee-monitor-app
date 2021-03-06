<template>
    <header class="header">
        <h1 class="page-title" tabindex="0" @click="showMainMode">Monitor sieci ZigBee</h1>
        <nav>
            <template v-if="isViewMode && isMapView">
                <button type="button" class="header-button" @click="refresh">
                    <img src="~@/assets/icons/arrow-repeat.svg" class="manage-users-icon" />
                    Odśwież
                </button>
                <dropdown-menu>
                    <template v-slot:toggle-button>
                        <img src="~@/assets/icons/gear.svg" class="manage-users-icon" />
                        Konfiguracja
                    </template>
                    <template v-slot:content>
                        <button type="button" class="dropdown-list-button" @click="editNewLayer">Dodaj mapę</button>
                        <button type="button" class="dropdown-list-button" @click="editActiveLayer" :disabled="!isActiveLayer">Edytuj mapę</button>
                        <button type="button" class="dropdown-list-button" @click="deleteActiveLayer" :disabled="!isActiveLayer">Usuń mapę</button>
                    </template>
                </dropdown-menu>
            </template>
            <button v-if="isUsersManagement || !isMapView" type="button" class="header-button" @click="showMainMode">
                <img src="~@/assets/icons/map.svg" class="manage-users-icon" />
                Mapa
            </button>
            <button v-if="isAdmin && !isUsersManagement" type="button" class="header-button" @click="manageUsers">
                <img src="~@/assets/icons/people.svg" class="manage-users-icon" />
                Użytkownicy
            </button>
            <template v-if="isLoggedIn">
                <dropdown-menu>
                    <template v-slot:toggle-button>
                        <img src="~@/assets/icons/person-circle.svg" class="user-icon" />
                        <span class="button-username">{{ user ? user.username : '' }}</span>
                    </template>
                    <template v-slot:content>
                        <button type="button" class="dropdown-list-button" @click="changePassword">Zmień hasło</button>
                        <button type="button" class="dropdown-list-button" @click="logout">Wyloguj</button>
                    </template>
                </dropdown-menu>
            </template>
        </nav>
    </header>
</template>

<script>

import DropdownMenu from './DropdownMenu.vue';

/**
 * Application header and horizontal menu. The buttons available in the menu depend on application state.
 */
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
        isUsersManagement(){
            const userManagementModes = ['changePassword', 'manageUsers', 'showUser', 'newUser', 'editUser']
            return userManagementModes.includes(this.$store.getters.mode);
        },
        isMapView(){
            return this.$store.state.mainDisplayMode === 'map';
        },
        isLoggedIn(){
            return this.$store.state.user !== null;
        },
        isAdmin(){
            return this.user &&  this.user.role === 'admin';
        },
        user(){
            return this.$store.state.user;
        },
        isActiveLayer(){
            return !!this.$store.getters.activeLayer;
        }
    },
    methods:{
        showMainMode(){
            this.$store.commit('pushMode', 'view');
            this.$store.commit('setMainDisplayMode', 'map');
        },
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
        },
        changePassword(){
            this.$store.commit('pushMode', 'changePassword');
        },
        manageUsers(){
            this.$store.commit('pushMode', 'manageUsers');
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
    cursor: pointer;
}

.user-icon{
    width: 1.3em;
    height: 1.3em;
    vertical-align: -0.4em;
    display:inline-block;
    margin-right:8px;
}

.manage-users-icon{
    width: 1.3em;
    height: 1.3em;
    vertical-align: -0.4em;
    display:inline-block;
    margin-right:2px;
}

.button-username{
    font-weight:600;
}

</style>

