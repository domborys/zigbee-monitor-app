<template>
    <section>
        <h2 class="user-list-header">Użytkownicy</h2>
        <button type="button" class="button" @click="addUser">Dodaj użytkownika</button>
        <ul class="user-list">
            <user-item v-for="user in users" :key="user.id" :user="user" @click.native="showUser(user)" />
        </ul>
        
    </section>
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
        users(){
            return this.$store.state.users.users;
        }
    },
    methods:{
        showUser(user){
            this.$store.commit('selectUser', user);
            this.$store.commit('pushMode', 'showUser');
        },
        addUser(){
            this.$store.commit('selectNewUser');
            this.$store.commit('pushMode', 'newUser');
        },
    },
    mounted(){
        this.$store.dispatch('getUsers');
    }
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

</style>