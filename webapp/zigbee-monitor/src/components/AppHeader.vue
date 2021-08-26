<template>
    <header class="header">
        <h1 class="page-title">Monitor sieci ZigBee</h1>
        <nav v-if="isViewMode">
            <button type="button" class="button" @click="editNewLayer">Dodaj piętro</button>
            <button type="button" class="button" @click="editActiveLayer">Edytuj piętro</button>
            <button type="button" class="button" @click="deleteActiveLayer">Usuń piętro</button>
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
    font-size:25px;
    font-weight:normal;
    margin: 10px;
}
</style>