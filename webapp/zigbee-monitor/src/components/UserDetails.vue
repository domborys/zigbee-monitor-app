<template>
    <div class="one-column-container">
        <div class="heading-back-group">
            <button type="button" class="heading-back-button" @click="back"></button>
            <h2 class="heading-back-heading">Użytkownik {{ user.username }}</h2>
        </div>
        <div class="user-details-main">
            <dl class="dl-inline">
                <dt>Nazwa użytkownika: </dt>
                <dd>{{ user.username }}</dd>
                <dt>Rola: </dt>
                <dd>{{ role }}</dd>
                <dt>Zablokowany: </dt>
                <dd>{{ disabledText }}</dd>
            </dl>
            <button type="button" class="button" @click="deleteUser">Usuń użytkownika</button>
            <button type="button" class="button" @click="editUser">Edytuj użytkownika</button>
        </div>
    </div> 
</template>

<script>
import UserItem from './UserItem.vue'

export default {
    name:"UserManagement",
    components:{
        UserItem
    },
    props:{
    },
    computed:{
        user(){
            return this.$store.state.users.selectedUser;
        },
        role(){
            return this.user.role === 'admin' ? 'Administrator' : 'Użytkownik';
        },
        disabledText(){
            return this.user.disabled ? 'Tak' : 'Nie';
        }
    },
    methods:{
        back(){
            this.$store.commit('previousMode');
        },
        editUser(){
            this.$store.commit('pushMode', 'editUser');
        },
        async deleteUser(){
            await this.$store.dispatch('deleteUser', this.user);
            this.$store.commit('deleteUser', this.user);
            this.$store.commit('previousMode');
        },
    },
}
</script>


<style scoped>

.user-list-header{
    margin:15px 0 15px 0;
    font-size:22px;
    font-weight:600;
}

.user-list{
    list-style-type: none;
    padding:0;
    margin:0;
}

.user-details-main{
    padding:0 8px;
}

</style>