<template>
    <header class="header">
        <h1 class="page-title">Monitor sieci ZigBee</h1>
        <nav>
            <template v-if="isViewMode">
                <button type="button" class="button" @click="refresh">Odśwież</button>
                <button type="button" class="button" @click="editNewLayer">Dodaj piętro</button>
                <button type="button" class="button" @click="editActiveLayer">Edytuj piętro</button>
                <button type="button" class="button" @click="deleteActiveLayer">Usuń piętro</button>
            </template>
            <template v-if="isLoggedIn">
                <span>{{ user.username }}</span>
                <button type="button" class="button" @click="logout">Wyloguj</button>
            </template>
        </nav>
    </header>
</template>

<script>


export default {
    name:"AppHeader",
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
</style>